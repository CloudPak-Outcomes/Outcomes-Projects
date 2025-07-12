#===============================================================================
# IBM Software Hub administration variables
#===============================================================================
# ------------------------------------------------------------------------------
# Cluster
# ------------------------------------------------------------------------------
export OCP_URL=<Enter your own value>
export OPENSHIFT_TYPE=self-managed
export IMAGE_ARCH=amd64
export OCP_USERNAME=<Enter your own value>
export OCP_PASSWORD=<Enter youre own value>
# export OCP_TOKEN=<enter your token>
export SERVER_ARGUMENTS="--server=${OCP_URL}"
export LOGIN_ARGUMENTS="--username=${OCP_USERNAME} --password=${OCP_PASSWORD}"
# export LOGIN_ARGUMENTS="--token=${OCP_TOKEN}"
export CPDM_OC_LOGIN="cpd-cli manage login-to-ocp ${SERVER_ARGUMENTS} ${LOGIN_ARGUMENTS}"
export OC_LOGIN="oc login ${SERVER_ARGUMENTS} ${LOGIN_ARGUMENTS}"
# ------------------------------------------------------------------------------
# Projects
# ------------------------------------------------------------------------------
export PROJECT_CPD_INST_OPERATORS=cpd-operators
export PROJECT_CPD_INST_OPERANDS=cpd
# ------------------------------------------------------------------------------
# Storage
# ------------------------------------------------------------------------------
export STG_CLASS_BLOCK=ocs-storagecluster-ceph-rbd
export STG_CLASS_FILE=ocs-storagecluster-cephfs
# ------------------------------------------------------------------------------
# IBM Entitled Registry
# ------------------------------------------------------------------------------
# export IBM_ENTITLEMENT_KEY=<enter your IBM entitlement API key>
# ------------------------------------------------------------------------------
# IBM Software Hub version
# ------------------------------------------------------------------------------
export VERSION=5.1.3
# ------------------------------------------------------------------------------
# Components
# ------------------------------------------------------------------------------
export COMPONENTS=ibm-licensing,scheduler,cpfs,cpd_platform
# export COMPONENTS=ikc_premium,dmc,db2oltp,datastage_ent_plus,ws,dataproduct,datalineage,dashboard
# ------------------------------------------------------------------------------
# Management
# ------------------------------------------------------------------------------
export API_KEY=<Enter your own value>
export CPD_USERNAME=admin
export LOCAL_USER=admin
export CPD_PROFILE_NAME=admin_profile
export CPD_PROFILE_URL=https://<Enter your own value for cpd_url>