#!/bin/bash

################################################################################
# IBM Software Hub 5.4.x - Configure Embedded LDAP Integration
#
# Automates the procedure documented at:
# https://www.ibm.com/docs/en/software-hub/5.4.x?topic=service-configuring-software-hub-use-embedded-ldap-integration
#
# What this script does:
#   1. Validates prerequisites (oc, jq, cluster login, namespace)
#   2. Sets the CPD_ROUTE from the live cluster
#   3. Patches product-configmap to enable zen_native_auth
#   4. Restarts usermgmt and zen-core deployments and waits for rollout
#   5. Retrieves the initial admin password from the cluster secret
#   6. Obtains an admin Bearer token via the CPD preauth API
#   7. Prompts for (and sets) a new cpadmin password via the usermgmt API
#   8. Optionally patches db2u-product-cm and restarts Db2U engine pods
#      (required if any of: Data Virtualization, Db2, Db2 Big SQL, Db2 Warehouse,
#       or OpenPages are installed)
#   9. Scrubs all sensitive variables from the shell environment
#
# Prerequisites:
#   - oc CLI installed and logged in as cluster-admin
#   - jq installed  (brew install jq / dnf install jq / apt install jq)
#   - PROJECT_CPD_INST_OPERANDS  env var set  (namespace where CPD operands live)
#   - PROJECT_CPD_INST_OPERATORS env var set  (namespace where CPD operators live)
#     OR pass them as arguments: ./setup-embedded-ldap.sh <operands-ns> <operators-ns>
#
# Usage:
#   # Using environment variables already set:
#   export PROJECT_CPD_INST_OPERANDS=cpd
#   export PROJECT_CPD_INST_OPERATORS=cpd-operators
#   ./setup-embedded-ldap.sh
#
#   # Passing namespaces as positional arguments:
#   ./setup-embedded-ldap.sh cpd cpd-operators
#
# IBM Documentation:
#   https://www.ibm.com/docs/en/software-hub/5.4.x?topic=service-configuring-software-hub-use-embedded-ldap-integration
################################################################################

set -euo pipefail

# ---------------------------------------------------------------------------
# Accept positional arguments as an alternative to env vars
# ---------------------------------------------------------------------------
if [[ $# -ge 1 ]]; then
  PROJECT_CPD_INST_OPERANDS="$1"
fi
if [[ $# -ge 2 ]]; then
  PROJECT_CPD_INST_OPERATORS="$2"
fi

# ---------------------------------------------------------------------------
# Colour codes
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error()   { echo -e "${RED}✗ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_info()    { echo -e "${BLUE}ℹ $1${NC}"; }

# Wait for a deployment rollout to complete, with a configurable timeout.
# Usage: wait_for_rollout <deployment-name> <namespace> [timeout-seconds]
wait_for_rollout() {
    local deploy="$1"
    local ns="$2"
    local timeout="${3:-300}"

    print_info "Waiting for rollout of deployment/$deploy in $ns (timeout ${timeout}s)..."
    if oc rollout status deployment/"$deploy" -n "$ns" --timeout="${timeout}s"; then
        print_success "deployment/$deploy is ready"
    else
        print_warning "Rollout of deployment/$deploy did not complete within ${timeout}s."
        print_info "Check manually:  oc rollout status deployment/$deploy -n $ns"
    fi
}

# ---------------------------------------------------------------------------
# Step 0 – Prerequisites
# ---------------------------------------------------------------------------
check_prerequisites() {
    print_header "Step 0 · Checking Prerequisites"

    # oc
    if ! command -v oc &>/dev/null; then
        print_error "oc CLI is not installed. Install it and log in, then re-run."
        exit 1
    fi
    print_success "oc CLI found: $(oc version --client --short 2>/dev/null || oc version --client)"

    # jq
    if ! command -v jq &>/dev/null; then
        print_error "jq is required but not installed."
        print_info "  macOS:          brew install jq"
        print_info "  RHEL/Fedora:    sudo dnf install jq"
        print_info "  Ubuntu/Debian:  sudo apt-get install jq"
        exit 1
    fi
    print_success "jq found: $(jq --version)"

    # curl
    if ! command -v curl &>/dev/null; then
        print_error "curl is required but not installed."
        exit 1
    fi
    print_success "curl found"

    # OpenShift login
    if ! oc whoami &>/dev/null; then
        print_error "Not logged in to OpenShift. Run: oc login"
        exit 1
    fi
    print_success "Logged in to OpenShift as: $(oc whoami)"

    # cluster-admin check
    if ! oc auth can-i '*' '*' --all-namespaces &>/dev/null; then
        print_warning "You may not have cluster-admin privileges. Some steps might fail."
    else
        print_success "Cluster-admin privileges confirmed"
    fi

    # Namespace variables
    if [[ -z "${PROJECT_CPD_INST_OPERANDS:-}" ]]; then
        print_error "PROJECT_CPD_INST_OPERANDS is not set."
        print_info "Set it: export PROJECT_CPD_INST_OPERANDS=<namespace>"
        print_info "Or pass as argument: $0 <operands-ns> <operators-ns>"
        exit 1
    fi
    if [[ -z "${PROJECT_CPD_INST_OPERATORS:-}" ]]; then
        print_warning "PROJECT_CPD_INST_OPERATORS is not set."
        print_warning "Db2U step will be skipped if you choose to run it."
    fi

    # Namespace existence
    if ! oc get namespace "$PROJECT_CPD_INST_OPERANDS" &>/dev/null; then
        print_error "Namespace '$PROJECT_CPD_INST_OPERANDS' does not exist on this cluster."
        exit 1
    fi
    print_success "Operands namespace: $PROJECT_CPD_INST_OPERANDS"

    if [[ -n "${PROJECT_CPD_INST_OPERATORS:-}" ]]; then
        if ! oc get namespace "$PROJECT_CPD_INST_OPERATORS" &>/dev/null; then
            print_warning "Operators namespace '$PROJECT_CPD_INST_OPERATORS' does not exist. Db2U step will be skipped."
            PROJECT_CPD_INST_OPERATORS=""
        else
            print_success "Operators namespace: $PROJECT_CPD_INST_OPERATORS"
        fi
    fi
}

# ---------------------------------------------------------------------------
# Step 1 – Resolve CPD route
# ---------------------------------------------------------------------------
get_cpd_route() {
    print_header "Step 1 · Resolving CPD Route"

    CPD_ROUTE=$(oc get route cpd \
        -n "$PROJECT_CPD_INST_OPERANDS" \
        -o jsonpath='{.spec.host}' 2>/dev/null || true)

    if [[ -z "$CPD_ROUTE" ]]; then
        print_error "Could not find route 'cpd' in namespace '$PROJECT_CPD_INST_OPERANDS'."
        print_info "Available routes:"
        oc get routes -n "$PROJECT_CPD_INST_OPERANDS" 2>/dev/null || true
        exit 1
    fi

    print_success "CPD_ROUTE = $CPD_ROUTE"
    export CPD_ROUTE
}

# ---------------------------------------------------------------------------
# Step 2 – Enable zen_native_auth in product-configmap
# ---------------------------------------------------------------------------
patch_product_configmap() {
    print_header "Step 2 · Enabling zen_native_auth in product-configmap"

    print_info "Patching ConfigMap product-configmap in $PROJECT_CPD_INST_OPERANDS..."
    oc patch cm product-configmap \
        --namespace="$PROJECT_CPD_INST_OPERANDS" \
        --type=merge \
        --patch '{"data": {"zen_native_auth": "enabled"}}'

    print_success "product-configmap patched → zen_native_auth: enabled"
}

# ---------------------------------------------------------------------------
# Step 3 – Restart usermgmt
# ---------------------------------------------------------------------------
restart_usermgmt() {
    print_header "Step 3 · Restarting usermgmt Deployment"

    oc rollout restart deployment usermgmt \
        --namespace="$PROJECT_CPD_INST_OPERANDS"
    wait_for_rollout usermgmt "$PROJECT_CPD_INST_OPERANDS" 300
}

# ---------------------------------------------------------------------------
# Step 4 – Restart zen-core
# ---------------------------------------------------------------------------
restart_zen_core() {
    print_header "Step 4 · Restarting zen-core Deployment"

    oc rollout restart deployment zen-core \
        --namespace="$PROJECT_CPD_INST_OPERANDS"
    wait_for_rollout zen-core "$PROJECT_CPD_INST_OPERANDS" 300
}

# ---------------------------------------------------------------------------
# Step 5 – Retrieve initial admin password
# ---------------------------------------------------------------------------
get_admin_password() {
    print_header "Step 5 · Retrieving Initial Admin Password"

    ADMIN_PASSWORD=$(oc get secret admin-user-details \
        -n "$PROJECT_CPD_INST_OPERANDS" \
        -o 'jsonpath={.data.initial_admin_password}' | base64 -d)

    if [[ -z "$ADMIN_PASSWORD" ]]; then
        print_error "Could not retrieve initial_admin_password from secret admin-user-details."
        print_info "Verify the secret exists:  oc get secret admin-user-details -n $PROJECT_CPD_INST_OPERANDS"
        exit 1
    fi

    print_success "Admin password retrieved from cluster secret"
}

# ---------------------------------------------------------------------------
# Step 6 – Obtain Bearer token for admin
# ---------------------------------------------------------------------------
get_auth_token() {
    print_header "Step 6 · Obtaining Admin Bearer Token"

    local response
    response=$(curl -k -s \
        -H "username: admin" \
        -H "password: ${ADMIN_PASSWORD}" \
        "https://${CPD_ROUTE}/v1/preauth/validateAuth" 2>/dev/null)

    AUTH_TOKEN=$(echo "$response" | jq -r '.accessToken // empty')

    if [[ -z "$AUTH_TOKEN" ]]; then
        print_error "Failed to obtain Bearer token. API response:"
        echo "$response"
        print_info "Ensure the CPD pods are fully ready and the route is reachable."
        exit 1
    fi

    print_success "Bearer token obtained for admin user"
}

# ---------------------------------------------------------------------------
# Step 7 – Set cpadmin password
# ---------------------------------------------------------------------------
set_cpadmin_password() {
    print_header "Step 7 · Setting cpadmin Password"

    print_warning "The cpadmin user is the primary embedded-LDAP administrator."
    print_info "Choose a strong password (min 16 characters recommended)."
    echo

    while true; do
        read -s -p "Enter new password for cpadmin: " CPADMIN_PASSWORD
        echo
        if [[ -z "$CPADMIN_PASSWORD" ]]; then
            print_error "Password cannot be empty."
            continue
        fi
        if [[ ${#CPADMIN_PASSWORD} -lt 8 ]]; then
            print_warning "Password is shorter than 8 characters. Consider using a stronger password."
            read -p "Continue anyway? (y/n): " confirm
            [[ "$confirm" == "y" ]] && break
            continue
        fi
        read -s -p "Confirm new password for cpadmin: " CPADMIN_PASSWORD_CONFIRM
        echo
        if [[ "$CPADMIN_PASSWORD" != "$CPADMIN_PASSWORD_CONFIRM" ]]; then
            print_error "Passwords do not match. Try again."
            continue
        fi
        break
    done

    print_info "Updating cpadmin password via usermgmt API..."

    local http_code
    http_code=$(curl -sk -o /dev/null -w "%{http_code}" \
        --location --request PUT \
        "https://${CPD_ROUTE}/api/v1/usermgmt/v1/user/cpadmin" \
        --header "Content-Type: application/json" \
        --header "Authorization: Bearer ${AUTH_TOKEN}" \
        --data "{
          \"username\": \"cpadmin\",
          \"authenticator\": \"default\",
          \"password\": \"${CPADMIN_PASSWORD}\"
        }")

    if [[ "$http_code" == "200" || "$http_code" == "204" ]]; then
        print_success "cpadmin password updated successfully (HTTP $http_code)"
    else
        print_error "Unexpected HTTP response: $http_code"
        print_info "The password may not have been updated. Check CPD logs."
        exit 1
    fi
}

# ---------------------------------------------------------------------------
# Step 8 – Verify cpadmin login
# ---------------------------------------------------------------------------
verify_cpadmin_login() {
    print_header "Step 8 · Verifying cpadmin Login"

    print_info "Testing login as cpadmin with the new password..."

    local response
    response=$(curl -k -s \
        -H "username: cpadmin" \
        -H "password: ${CPADMIN_PASSWORD}" \
        "https://${CPD_ROUTE}/v1/preauth/validateAuth" 2>/dev/null)

    local token
    token=$(echo "$response" | jq -r '.accessToken // empty')

    if [[ -n "$token" ]]; then
        print_success "cpadmin login verified successfully"
    else
        print_warning "Could not verify cpadmin login. Response:"
        echo "$response"
        print_info "Try logging in manually:  https://${CPD_ROUTE}"
    fi
}

# ---------------------------------------------------------------------------
# Step 9 – Unset sensitive environment variables
# ---------------------------------------------------------------------------
unset_sensitive_vars() {
    print_header "Step 9 · Unsetting Sensitive Environment Variables"

    unset ADMIN_PASSWORD
    unset AUTH_TOKEN
    unset CPADMIN_PASSWORD
    unset CPADMIN_PASSWORD_CONFIRM

    print_success "ADMIN_PASSWORD, AUTH_TOKEN, CPADMIN_PASSWORD unset from environment"
}

# ---------------------------------------------------------------------------
# Step 10 – Optional: Db2U ConfigMap + pod restart
# ---------------------------------------------------------------------------
configure_db2u() {
    print_header "Step 10 · Db2U Authentication Update (Optional)"

    echo -e "${YELLOW}This step is required only if you have ANY of the following services:${NC}"
    echo -e "  • Data Virtualization"
    echo -e "  • Db2"
    echo -e "  • Db2 Big SQL"
    echo -e "  • Db2 Warehouse"
    echo -e "  • OpenPages"
    echo

    read -p "Do you have any Db2U-dependent services installed? (y/n): " has_db2u
    if [[ "$has_db2u" != "y" && "$has_db2u" != "Y" ]]; then
        print_info "Skipping Db2U configuration"
        return
    fi

    if [[ -z "${PROJECT_CPD_INST_OPERATORS:-}" ]]; then
        print_error "PROJECT_CPD_INST_OPERATORS is not set — cannot apply db2u-product-cm."
        print_info "Set the variable and run the Db2U steps manually."
        return
    fi

    # Apply ZEN_NATIVE_AUTH to db2u-product-cm in the operators namespace
    print_info "Applying ZEN_NATIVE_AUTH: \"true\" to db2u-product-cm in $PROJECT_CPD_INST_OPERATORS..."
    cat <<EOF | oc apply -f -
apiVersion: v1
data:
  ZEN_NATIVE_AUTH: "true"
kind: ConfigMap
metadata:
  name: db2u-product-cm
  namespace: ${PROJECT_CPD_INST_OPERATORS}
EOF
    print_success "db2u-product-cm applied in $PROJECT_CPD_INST_OPERATORS"

    # Restart all Db2U engine pods in the operands namespace
    print_info "Deleting all Db2U engine pods in $PROJECT_CPD_INST_OPERANDS (they will self-restart)..."
    if oc get pods -n "$PROJECT_CPD_INST_OPERANDS" -l type=engine --no-headers 2>/dev/null | grep -q .; then
        oc delete pods \
            -n "$PROJECT_CPD_INST_OPERANDS" \
            -l type=engine
        print_success "Db2U engine pods deleted — Kubernetes will restart them"
        print_info "Monitor restart:  oc get pods -n $PROJECT_CPD_INST_OPERANDS -l type=engine -w"
    else
        print_warning "No Db2U engine pods found in $PROJECT_CPD_INST_OPERANDS with label type=engine"
    fi

    echo
    print_info "Once pods are running, validate ZEN_NATIVE_AUTH inside a Db2U engine pod:"
    echo -e "  ${GREEN}oc exec -it \$(oc get pods -n $PROJECT_CPD_INST_OPERANDS -l type=engine -o name | head -1) \\
      -n $PROJECT_CPD_INST_OPERANDS -- bash -c 'env | grep ZEN_NATIVE_AUTH'${NC}"
}

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print_summary() {
    print_header "Configuration Complete!"

    echo -e "${GREEN}IBM Software Hub is now configured to use the embedded LDAP integration.${NC}\n"

    echo -e "${BLUE}What was done:${NC}"
    echo -e "  ✓ product-configmap patched  →  zen_native_auth: enabled"
    echo -e "  ✓ usermgmt deployment restarted and rolled out"
    echo -e "  ✓ zen-core deployment restarted and rolled out"
    echo -e "  ✓ cpadmin password set via usermgmt API"
    echo -e "  ✓ Sensitive environment variables unset"
    echo

    echo -e "${BLUE}Next Steps:${NC}"
    echo -e "  1. Log in to IBM Software Hub as ${GREEN}cpadmin${NC}:"
    echo -e "     ${GREEN}https://${CPD_ROUTE}${NC}"
    echo -e "  2. Connect to your LDAP server:"
    echo -e "     Administration → Access control → Identity provider connection"
    echo -e "     Docs: https://www.ibm.com/docs/en/software-hub/5.4.x?topic=service-connecting-your-identity-provider"
    echo -e "  3. Add and manage additional users in the IBM Software Hub UI."
    echo

    echo -e "${YELLOW}Reminder:${NC}"
    echo -e "  The embedded LDAP integration is deprecated by IBM."
    echo -e "  Migrate to the Identity Management Service (LDAP integration) when you are ready."
    echo -e "  Docs: https://www.ibm.com/docs/en/software-hub/5.4.x?topic=service-integrating-identity-management-service"
    echo
}

################################################################################
# Main Execution
################################################################################

main() {
    clear
    print_header "IBM Software Hub 5.4.x — Enable Embedded LDAP Integration"
    echo -e "${BLUE}This script automates the IBM documentation procedure at:${NC}"
    echo -e "${GREEN}https://www.ibm.com/docs/en/software-hub/5.4.x?topic=service-configuring-software-hub-use-embedded-ldap-integration${NC}"
    echo

    if [[ -n "${PROJECT_CPD_INST_OPERANDS:-}" ]]; then
        echo -e "${YELLOW}Operands namespace:  ${GREEN}${PROJECT_CPD_INST_OPERANDS}${NC}"
    fi
    if [[ -n "${PROJECT_CPD_INST_OPERATORS:-}" ]]; then
        echo -e "${YELLOW}Operators namespace: ${GREEN}${PROJECT_CPD_INST_OPERATORS}${NC}"
    fi
    echo

    read -p "Press Enter to continue or Ctrl+C to cancel..."

    check_prerequisites
    get_cpd_route
    patch_product_configmap
    restart_usermgmt
    restart_zen_core
    get_admin_password
    get_auth_token
    set_cpadmin_password
    verify_cpadmin_login
    unset_sensitive_vars
    configure_db2u
    print_summary
}

main

# Made with Bob
