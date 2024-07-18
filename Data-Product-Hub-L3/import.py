import time
from client import ImportClient

client = ImportClient()


# Check Bearer Token is valid
bearer_token = client.get_bearer_token()
if bearer_token:
    print("")
    print(f"Bearer token Aquired")
    print("")
    
# Cloud Object Storage
client.define_cos_connection(bearer_token, catalog=False)

# DB2 Warehouse
client.define_db2_connection(bearer_token, catalog=False)

# PostgreSQL Database
client.define_psql_connection(bearer_token, catalog=False)

print("")
# Import Governance Artifacts
#client.main_import_process("governance_artifacts.zip", process_id=None)
print("")

# Create and run the metadata import DB2 Warehouse
print("Running Metadata Import for DB2 Warehouse")
path_db2=["/EMPLOYEE/EMPLOYEE_HISTORY","/EMPLOYEE/EMPLOYEE_RECORDS","/EMPLOYEE/EMPLOYEE_SUMMARY","/EMPLOYEE/EMPLOYEE"]
db2_mdid, db2_mdi_response = client.create_and_run_metadata_import(client.db2_id, path_db2, name="2 DB2 Metadata Import")

# Create and run the metadata import COS
print("Running Metadata Import for Cloud Object Storage")
path_cos = ["/cpd-outcomes/Warehouse/WAREHOUSE_ASSIGNED_SHIFTS.csv","/cpd-outcomes/Warehouse/WAREHOUSE_SHIFTS.csv","/cpd-outcomes/Warehouse/WAREHOUSE_STAFF.csv","/cpd-outcomes/Warehouse/WAREHOUSE_STAFFING.csv"]
cos_mdid, cos_mdi_response = client.create_and_run_metadata_import(client.cos_id, path_cos, name="2 Cloud Object Storage Metadata Import")

# Create and run the metadata import
print("Running Metadata Import for PostgreSQL")
path_psql = ["/CUSTOMER/CUSTOMER_LOYALTY"]
psql_mdid, psql_mdid_response = client.create_and_run_metadata_import(client.psql_id, path_psql, name="2 Postgresql Metadata Import")

# Metadata Enrichment
print("Running Metadata Enrichment for DB2 Warehouse")
db2_result = client.create_and_run_metadata_enrichment(
        name="Db2 Warehouse MDE",
        mdi_id=db2_mdid,
        job_name=client.db2_name+" Enrichment Job",
        publish_job_name=client.db2_name+" publish Job",
    )

print("🌩️ Running Metadata Enrichment for Cloud Object Storage 🌩️")
cos_result = client.create_and_run_metadata_enrichment(
        name="Cloud Object Storage Enrichment",
        mdi_id=cos_mdid,
        job_name=client.cos_name+" Enrichment Job",
        publish_job_name=client.cos_name+" publish Job",
    )

print("🐘 Running Metadata Enrichment for PostgreSQL 🐘")
psql_result = client.create_and_run_metadata_enrichment(
        name="Postgresql MDE",
        mdi_id=psql_mdid,
        job_name=client.psql_name+" Enrichment Job",
        publish_job_name=client.psql_name+" publish Job",
    )


print("Sleeping for 60 seconds to allow enrichment to complete")
time.sleep(60)
print("Sleeping for 60 seconds to allow enrichment to complete")
time.sleep(60)
print("Sleeping for 60 seconds to allow enrichment to complete")
time.sleep(60)
# Publish Assets
print("")
db2_mde_id = db2_result.get("metadata", {}).get("asset_id")
db2_publish_result = client.publish_metadata_enrichment_assets(db2_mde_id)
print("DB2 Warehouse Successfully Published")

cos_mde_id = cos_result.get("metadata", {}).get("asset_id")
cos_publish_result = client.publish_metadata_enrichment_assets(cos_mde_id)
print("Cloud Object Storage Successfully Published")

psql_mde_id = psql_result.get("metadata", {}).get("asset_id")
psql_publish_result = client.publish_metadata_enrichment_assets(psql_mde_id)
print("PostgreSQL Successfully Published")

print("Congratulations! You have successfully setup the Data Product Hub Environment.")
