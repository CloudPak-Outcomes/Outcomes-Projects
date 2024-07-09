import time
import requests
from dotenv import load_dotenv
import os
import json
import urllib3
import cowsay
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.urllib3.disable_warnings()

bold_blue_start = "\033[1;34m"
bold_green_start = "\033[1;32m"
bold_red_start = "\033[1;31m"
reset = "\033[0m"

class ImportClient:
    """
    A class to handle import operations for governance artifacts, 
    define connections to data sources, and manage catalog operations in IBM Cloud Pak for Data (CPD).
    """

    def __init__(self):
        """
        Initialize the ImportClient instance by loading environment variables
        and setting up necessary attributes.
        """
        # Load environment variables from .env file
        os.environ.clear()
        load_dotenv()

        # Access the CPD_CLUSTER_HOST variable and other environment variables
        self.cpd_cluster_host = os.getenv("CPD_CLUSTER_HOST")
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.catalog_name = os.getenv("CATALOG_NAME")
        self.project_id = os.getenv("PROJECT_ID")
        self.base_url = f"https://{self.cpd_cluster_host}"

        # Db2 Warehouse specific variables
        self.db_username = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")
        self.host = os.getenv("DB_HOST")
        self.db_port = "50001"
        self.db2_name = "Data Warehouse"
        self.db2_description = "Database that contains warehouse data needed by the business for analytics and AI."
        #self.owner_id = os.getenv("OWNER_ID")
        self.origin_country = os.getenv("ORIGIN_COUNTRY")
        self.db2_datasource_type = os.getenv("DB2_DATASOURCE_TYPE")
        
        # Db2 Warehouse specific variables
        self.psql_username = os.getenv("PSQL_DB_USERNAME")
        self.psql_password = os.getenv("PSQL_DB_PASSWORD")
        self.psql_database = os.getenv("PSQL_DB_DATABASE")
        self.psql_host = os.getenv("PSQL_DB_HOST")
        self.psql_db_port = os.getenv("PSQL_DB_PORT")
        self.psql_name = "3rd Party Data"
        self.psql_description = "Database that contains warehouse data needed by the business for analytics and AI."
        #self.owner_id = os.getenv("OWNER_ID")
        self.origin_country = os.getenv("ORIGIN_COUNTRY")
        self.psql_datasource_type = os.getenv("PSQL_DATASOURCE_TYPE")

        # Cloud Object Storage specific variables
        self.cos_bucket = os.getenv("COS_BUCKET")
        self.cos_secret_key = os.getenv("COS_SECRET_KEY")
        self.cos_api_key = os.getenv("COS_API_KEY")
        self.cos_access_key = os.getenv("COS_ACCESS_KEY")
        self.cos_resource_instance_id = os.getenv("COS_RESOURCE_INSTANCE_ID")
        self.cos_url = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
        self.cos_name = "Cloud Object Storage"
        self.cos_description = "IBM Cloud Object Storage bucket that contains data files used for analytics and AI."
        self.bearer_token = None
        
        # Get the catalog ID based on the catalog name
        self.catalog_id = self.get_catalog_id_by_name()
        
                # Initialize db2_id and cos_id attributes
        self.db2_id, self.cos_id, self.psql_id = self.fetch_resource_ids()

    def create_metadata_import(self, project_id, create_job, job_name, name, connection_id, target_catalog_id, import_type='METADATA'):
        url = f"{self.base_url}/v2/metadata_imports"
        
        # Request query parameters
        params = {
            'project_id': project_id,
            'create_job': create_job,
            'job_name': job_name
        }
        
        # Request body
        data = {
            'name': name,
            'connection_id': connection_id,
            'target_catalog_id': target_catalog_id,
            'import_type': import_type
        }

        # Headers (if authentication is required, e.g., Bearer token)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_bearer_token()}'
        }


        response = requests.post(url, headers=headers, params=params, json=data, verify=False)
        
        if response.status_code in [200, 201]:
            print('Metadata import created successfully:', response.json())
        else:
            print('Failed to create metadata import:', response.status_code, response.text)



    def fetch_resource_ids(self):
        """
        Fetch DB2 Warehouse and Cloud Object Storage asset IDs from the CPD catalog.

        Returns:
            tuple: (db2_id, cos_id, psql_id)
        """
        bearer_token = self.get_bearer_token()
        if bearer_token:
            data = self.get_connections(bearer_token)
            db2_id = None
            cos_id = None
            psql_id = None

            # Iterate through resources to find DB2 Warehouse and Cloud Object Storage
            for resource in data['resources']:
                if resource['entity']['name'] == 'Data Warehouse':
                    db2_id = resource['metadata']['asset_id']
                elif resource['entity']['name'] == 'Cloud Object Storage':
                    cos_id = resource['metadata']['asset_id']
                elif resource['entity']['name'] == '3rd Party Data':
                    psql_id = resource['metadata']['asset_id']

            return db2_id, cos_id, psql_id
        else:
            print("Failed to fetch resource IDs. Bearer token not obtained.")
            return None, None


    def verify_vars(self):
        """
        Verify and print the environment variables and instance attributes.
        """
        vars_dict = self.__dict__
        for key, value in vars_dict.items():
            if not key.startswith('__') and not callable(value):
                print(f"{bold_blue_start}{key}{reset}: {value}")

    def get_bearer_token(self):
        """
        Obtain a bearer token for authentication.
        
        Returns:
            str: The bearer token if the request is successful, otherwise None.
        """
        url = f"https://{self.cpd_cluster_host}/icp4d-api/v1/authorize"
        headers = {
            "cache-control": "no-cache",
            "content-type": "application/json"
        }
        payload = {
            "username": self.username,
            "password": self.password
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

        if response.status_code == 200:
            data = response.json()
            return data.get('token')  # Return the token
        else:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)
            return None

    def get_connections(self, bearer):
        """
        Returns the connections active in catalog.
        
        Returns:
            str: The catalogs if the request is successful, otherwise None.
        """
        url = f"https://{self.cpd_cluster_host}/v2/connections"  # Ensure this is the correct endpoint
        headers = {
            "Inject-Token": "false",  # Update to "true" if token injection is needed
            "Authorization": f"Bearer {bearer}",  # Insert the actual bearer token
            "cache-control": "no-cache",
            "content-type": "application/json"
        }

        # Query parameters
        params = {
            "catalog_id": self.catalog_id,  
            "sort": "-metadata.create_time",
            "limit": 50
        }

        response = requests.get(url, headers=headers, params=params, verify=False)
        
        if response.status_code == 200:
            #print("Authenticated request was successful")
            data = response.json()
            #print(json.dumps(data, indent=4)) 
            return data 
        else:
            print(f"Authenticated request failed with status code {response.status_code}")
            print(response.text)
        

    def define_cos_connection(self, bearer):
        """
        Define a connection to Cloud Object Storage (COS).

        Args:
            bearer (str): Bearer token for authentication.
        """
        url = f"{self.base_url}/v2/connections?catalog_id={self.catalog_id}"
        headers = {
            "Authorization": f"Bearer {bearer}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "Skip-Enforcement": "false"
        }

        # Request body
        payload = {
            "datasource_type": "193a97c1-4475-4a19-b90c-295c4fdc6517",
            "name": self.cos_name,
            "description": self.cos_description,
            "properties": {
                "bucket": self.cos_bucket,
                "secret_key": self.cos_secret_key,
                "trust_all_ssl_cert": "false",
                "auth_method": "instanceid_apikey_accesskey_secretkey",
                "iam_url": "https://iam.cloud.ibm.com/identity/token",
                "api_key": self.cos_api_key,
                "resource_instance_id": self.cos_resource_instance_id,
                "access_key": self.cos_access_key,
                "url": self.cos_url
            },
            "origin_country": self.origin_country,
            "data_source_definition_searchable": f"{self.cos_url}|{self.cos_bucket}"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

        if response.status_code == 200 or response.status_code == 201:
            print(f"Connection to {bold_blue_start}Cloud Object Storage{reset} defined successfully!")
            data = response.json()
        else:
            print(f"Failed to define connection with status code {response.status_code}")
            print(response.text)

    def define_db2_connection(self, bearer):
        """
        Define a connection to a DB2 Warehouse.

        Args:
            bearer (str): Bearer token for authentication.
        """
        url = f"{self.base_url}/v2/connections?catalog_id={self.catalog_id}"
        headers = {
            "Authorization": f"Bearer {bearer}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "Skip-Enforcement": "false"
        }

        # Request body
        payload = {
            "datasource_type": self.db2_datasource_type,
            "name": self.db2_name,
            "description": self.db2_description,
            "properties": {
                "database": self.database,
                "auth_method": "username_password",
                "password": self.db_password,
                "port": self.db_port,  # Use the correct port
                "host": self.host,
                "ssl": "true",
                "username": self.db_username
            },
            "origin_country": self.origin_country,
            "data_source_definition_searchable": f"{self.host}|50001|{self.database}"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

        if response.status_code == 200 or response.status_code == 201:
            print(f"Connection to {bold_blue_start}DB2 Warehouse{reset} defined successfully!")
            data = response.json()
        else:
            print(f"Failed to define connection with status code {response.status_code}")
            print(response.text)

    def define_psql_connection(self, bearer):
        """
        Define a connection to a DB2 Warehouse.

        Args:
            bearer (str): Bearer token for authentication.
        """
        url = f"{self.base_url}/v2/connections?catalog_id={self.catalog_id}"
        headers = {
            "Authorization": f"Bearer {bearer}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "Skip-Enforcement": "false"
        }

        # Request body
        payload = {
            "datasource_type": self.datasource_type,
            "name": self.psql_name,
            "description": self.psql_description,
            "properties": {
                "database": self.psql_database,
                "auth_method": "username_password",
                "password": self.psql_password,
                "port": self.psql_port,  # Use the correct port
                "host": self.psql_host,
                "ssl": "true",
                "username": self.psql_db_username
            },
            "origin_country": self.origin_country,
            "data_source_definition_searchable": f"{self.host}|{self.db_port,}|{self.database}"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

        if response.status_code == 200 or response.status_code == 201:
            print(f"Connection to {bold_blue_start}DB2 Warehouse{reset} defined successfully!")
            data = response.json()
        else:
            print(f"Failed to define connection with status code {response.status_code}")
            print(response.text)


    def import_governance_artifacts(self, zip_file_path):
        """
        Import governance artifacts from a ZIP file.

        Args:
            zip_file_path (str): Path to the ZIP file containing governance artifacts.

        Returns:
            str: Process ID if the import is in progress, otherwise None.
        """
        bearer = self.get_bearer_token()
        if not bearer:
            print("Failed to obtain bearer token.")
            return None

        url = f"{self.base_url}/v3/governance_artifact_types/import"
        headers = {
            "Authorization": f"Bearer {bearer}"
        }

        with open(zip_file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, headers=headers, files=files, params={'merge_option': 'specified'}, verify=False)

            if response.status_code in [200, 201]:
                print("Imported governance artifacts successfully.")
                return None
            elif response.status_code == 202:
                process_id = response.json().get("process_id")
                print(f"Process ID: {process_id}")
                return process_id
            else:
                print(f"Failed to import governance artifacts with status code {response.status_code}")
                print(response.text)
                return None

    def check_import_status(self, process_id):
        """
        Check the status of the import process.

        Args:
            process_id (str): Process ID of the import process.

        Returns:
            dict: Status data if the request is successful, otherwise None.
        """
        bearer = self.get_bearer_token()
        if not bearer:
            print("Failed to obtain bearer token.")
            return None

        url = f"{self.base_url}/v3/governance_artifact_types/import/status/{process_id}"
        headers = {
            "Authorization": f"Bearer {bearer}"
        }

        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200:
            status_data = response.json()
            return status_data
        else:
            print(f"Failed to check import status with status code {response.status_code}")
            print(response.text)
            return None

    def main_import_process(self, zip_file_path, process_id=None):
        """
        Main script for importing governance artifacts and checking status.

        Args:
            zip_file_path (str): Path to the ZIP file containing governance artifacts.
            process_id (str, optional): Process ID of the ongoing import process.
        """
        start_time = datetime.now()
        if not process_id:
            process_id = self.import_governance_artifacts(zip_file_path)
        
        if process_id:
            while True:
                status_data = self.check_import_status(process_id)
                if not status_data:
                    break
                
                status = status_data.get("status")
                step_number = status_data.get("step_number")
                total_steps = status_data.get("total_steps")
                
                elapsed_time = datetime.now() - start_time
                elapsed_time_str = str(timedelta(seconds=elapsed_time.seconds))
                
                percent_complete = (step_number / total_steps) * 100
                print(f"Import Progress: {percent_complete:.2f}%")
                print(f"Time elapsed: {elapsed_time_str}")
                
                if status == "SUCCEEDED" or step_number == total_steps:
                    success_message=f"✅✅✅ {bold_green_start}Import process completed successfully.{reset} ✅✅✅"
                    cowsay.stegosaurus(success_message)
                    break
                elif status == "FAILED":
                    fail_message=f"❌😢❌😢❌ {bold_red_start}Import process failed.{reset} ❌😢❌😢❌"
                    cowsay.beavis(fail_message)
                    break
                else:
                    wip_message = "Import process is still in progress. Checking again in 30 seconds..."
                    cowsay.tux(wip_message)
                    time.sleep(30)

    def get_catalogs(self, bearer):
        """
        Get the list of catalogs.

        Args:
            bearer (str): Bearer token for authentication.

        Returns:
            list: List of catalogs with their GUID and name.
        """
        url = f"{self.base_url}/v2/catalogs"
        headers = {
            "Authorization": f"Bearer {bearer}",
            "cache-control": "no-cache",
            "content-type": "application/json"
        }

        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200:
            catalogs_data = response.json()
            catalogs = catalogs_data.get("catalogs", [])
            catalog_info = [{"guid": catalog["metadata"]["guid"], "name": catalog["entity"]["name"]} for catalog in catalogs]
            return catalog_info
        else:
            print(f"Failed to get catalogs with status code {response.status_code}")
            print(response.text)
            return None

    def get_catalog_id_by_name(self):
        """
        Get the catalog ID based on the catalog name.

        Returns:
            str: Catalog ID if found, otherwise None.
        """
        bearer_token = self.get_bearer_token()
        if bearer_token:
            catalogs = self.get_catalogs(bearer_token)
            if catalogs:
                for catalog in catalogs:
                    if catalog["name"] == self.catalog_name:
                        return catalog["guid"]
        print(f"Catalog with name {self.catalog_name} not found.")
        return None

# Example usage:
# client = ImportClient()
# client.verify_vars()
# client.main_import_process('/path/to/your/artifacts.zip')
