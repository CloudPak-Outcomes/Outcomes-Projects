#===============================================================================
# IBM Software Hub installation variables
#===============================================================================
# ------------------------------------------------------------------------------
# Client workstation
# ------------------------------------------------------------------------------
# Set the following variables if you want to override the default behavior of the IBM Software Hub CLI.
#
# To export these variables, you must uncomment each command in this section.
# export CPD_CLI_MANAGE_WORKSPACE=<enter a fully qualified directory>
# export OLM_UTILS_LAUNCH_ARGS=<enter launch arguments>
# ------------------------------------------------------------------------------
# Cluster
# ------------------------------------------------------------------------------
export OCP_URL=<Enter your own value>
export OPENSHIFT_TYPE=self-managed
export IMAGE_ARCH=amd64
export OCP_USERNAME=<Enter your own value>
export OCP_PASSWORD=<Enter your own value>
# export OCP_TOKEN=<enter your token>
export SERVER_ARGUMENTS="--server=${OCP_URL}"
export LOGIN_ARGUMENTS="--username=${OCP_USERNAME} --password=${OCP_PASSWORD}"
# export LOGIN_ARGUMENTS="--token=${OCP_TOKEN}"
export CPDM_OC_LOGIN="cpd-cli manage login-to-ocp ${SERVER_ARGUMENTS} ${LOGIN_ARGUMENTS}"
export OC_LOGIN="oc login ${SERVER_ARGUMENTS} ${LOGIN_ARGUMENTS}"
# ------------------------------------------------------------------------------
# Proxy server
# ------------------------------------------------------------------------------
# export PROXY_HOST=<enter your proxy server hostname>
# export PROXY_PORT=<enter your proxy server port number>
# export PROXY_USER=<enter your proxy server username>
# export PROXY_PASSWORD=<enter your proxy server password>
# ------------------------------------------------------------------------------
# Projects
# ------------------------------------------------------------------------------
export PROJECT_CERT_MANAGER=ibm-cert-manager
export PROJECT_LICENSE_SERVICE=ibm-licensing
export PROJECT_SCHEDULING_SERVICE=ibm-cpd-scheduler
# export PROJECT_IBM_EVENTS=<enter your IBM Events Operator project>
export PROJECT_PRIVILEGED_MONITORING_SERVICE=ibm-privileged-monitors
export PROJECT_CPD_INST_OPERATORS=ibm-common-services
export PROJECT_CPD_INST_OPERANDS=cpd-edu
# export PROJECT_CPD_INSTANCE_TETHERED=<enter your tethered project>
# export PROJECT_CPD_INSTANCE_TETHERED_LIST=<a comma-separated list of tethered projects>
# ------------------------------------------------------------------------------
# Storage
# ------------------------------------------------------------------------------
export STG_CLASS_BLOCK=ocs-storagecluster-ceph-rbd
export STG_CLASS_FILE=ocs-storagecluster-cephfs
# ------------------------------------------------------------------------------
# IBM Entitled Registry
# ------------------------------------------------------------------------------
export IBM_ENTITLEMENT_KEY=<enter your IBM entitlement API key>
# ------------------------------------------------------------------------------
# Private container registry
# ------------------------------------------------------------------------------
# Set the following variables if you mirror images to a private container registry.
#
# To export these variables, you must uncomment each command in this section.
# export PRIVATE_REGISTRY_LOCATION=<enter the location of your private container registry>
# export PRIVATE_REGISTRY_PUSH_USER=<enter the username of a user that can push to the registry>
# export PRIVATE_REGISTRY_PUSH_PASSWORD=<enter the password of the user that can push to the registry>
# export PRIVATE_REGISTRY_PULL_USER=<enter the username of a user that can pull from the registry>
# export PRIVATE_REGISTRY_PULL_PASSWORD=<enter the password of the user that can pull from the registry>
# ------------------------------------------------------------------------------
# IBM Software Hub version
# ------------------------------------------------------------------------------
export VERSION=5.1.3
# ------------------------------------------------------------------------------
# Components
# ------------------------------------------------------------------------------
export COMPONENTS=ibm-licensing,scheduler,cpfs,cpd_platform
# export COMPONENTS=ikc_premium,dmc,db2oltp,datastage_ent_plus,ws,dataproduct,datalineage,dashboard
# export COMPONENTS_TO_SKIP=<component-ID-1>,<component-ID-2>
# ------------------------------------------------------------------------------
# watsonx Orchestrate
# ------------------------------------------------------------------------------
# export PROJECT_IBM_APP_CONNECT=<enter your IBM App Connect in containers project>
# export AC_CASE_VERSION=<version>
# export AC_CHANNEL_VERSION=<version>