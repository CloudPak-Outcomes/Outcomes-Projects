from client import ImportClient

def easy_import():
    client = ImportClient()

    # Check Variables/Credentials
    client.verify_vars()

    # Check Bearer Token is valid
    bearer_token = client.get_bearer_token()
    if bearer_token:
        print("")
        print(f"Bearer token: {bearer_token}")
        print("")
        
    # Cloud Object Storage
    client.define_cos_connection(bearer_token)

    # DB2 Warehouse
    client.define_db2_connection(bearer_token)

    client.main_import_process("governance_artifacts.zip", process_id=None)
