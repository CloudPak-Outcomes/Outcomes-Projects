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
        
        # PSQL  specific variables
        self.psql_username = os.getenv("PSQL_DB_USERNAME")
        self.psql_password = os.getenv("PSQL_DB_PASSWORD")
        self.psql_database = os.getenv("PSQL_DB_DATABASE")
        self.psql_host = os.getenv("PSQL_DB_HOST")
        self.psql_port = os.getenv("PSQL_DB_PORT")
        self.psql_name = "Customer Data - PostgreSQL"
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
        self.db2_id, self.cos_id, self.psql_id = self.fetch_resource_ids()
        
        
        # Metadata enrichment Parameters
        self.mde_objective = {
            "enrichment_options": {
            "structured": {
                "profile": True,
                "assign_terms": True,
                "analyze_quality": True
                }
            },
            "governance_scope": self.get_category_ids(),
            "sampling": {
            "structured": {
                "method": "TOP",
                "analysis_method": "FIXED",
                "sample_size": {
                    "name": "BASIC",
                    "options": {
                        "row_number": 1000,
                        "classify_value_number": 100
                        }
                    }
                }
            },
            "datascope_of_reruns": "DELTA"
            }
        
        
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
                if resource['entity']['name'] == self.db2_name:
                    db2_id = resource['metadata']['asset_id']
                elif resource['entity']['name'] == self.cos_name:
                    cos_id = resource['metadata']['asset_id']
                elif resource['entity']['name'] == self.psql_name:
                    psql_id = resource['metadata']['asset_id']

            return db2_id, cos_id, psql_id
        else:
            print("Failed to fetch resource IDs. Bearer token not obtained.")
            return None, None



    def get_categories(self):
        """
        Retrieves category artifacts

        Args:
            artifact_ids (List[str]): List of artifact IDs of categories.

        Returns:
            dict: Category hierarchy paths for the given artifact IDs if the request is successful, otherwise None.
        """
        url = f"{self.base_url}/v3/search?query=metadata.artifact_type:category"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_bearer_token()}'
        }

        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200:
            #print('Category hierarchy paths retrieved successfully.')
            return response.json()
        else:
            print('Failed to retrieve category hierarchy paths:', response.status_code, response.text)
            return None

    def get_category_ids(self):
        categories_json = self.get_categories()
        cat_list=[]
        for i in range(5):
            row = categories_json['rows'][i] if i < len(categories_json['rows']) else None
            if row:
                artifact_id = row.get('artifact_id')
                if artifact_id:
                    cat_list.append({"type": "CATEGORY", "id": artifact_id})
        return cat_list



    def publish_metadata_enrichment_assets(self, metadata_enrichment_area_id, publish_scope = "all_assets", asset_ids=None, filter_criteria=None):
        """
        Publish assets of a Metadata Enrichment Area to a catalog.

        Args:
            metadata_enrichment_area_id (str): ID of the metadata enrichment area asset.
            publish_scope (str): Publish scope, allowable values: 'all_assets', 'selected_assets'.
            catalog_id (str): ID of the catalog to publish assets to.
            duplicate_action (str): Action if asset already exists, allowable values: 'IGNORE', 'REPLACE', 'UPDATE'.
            asset_ids (list): List of asset IDs to publish. Required if publish_scope is 'selected_assets'.
            filter_criteria (dict): Filter criteria for assets. Required if publish_scope is 'selected_assets'.

        Returns:
            dict: The response of the publish request if successful, otherwise None.
        """



        headers = {
            'Authorization': f'Bearer {self.get_bearer_token()}',
            'Content-Type': 'application/json'
        }

        payload = {
            "catalog": self.catalog_id,
            "duplicate_action": "update"
        }

        if publish_scope == "selected_assets":
            if asset_ids:
                payload["asset_ids"] = asset_ids
            if filter_criteria:
                payload["filter"] = {"search_criteria": filter_criteria}

        url = f'https://{self.cpd_cluster_host}/v2/metadata_enrichment/metadata_enrichment_area/{metadata_enrichment_area_id}/publish_assets?project_id={self.project_id}&publishScope={publish_scope}'

        response = requests.post(url, json=payload, headers=headers, verify=False)
        try:
            response_json = response.json()
            print(f'Publish Assets Response: {response.status_code}, {response_json}')
            return response_json
        except requests.JSONDecodeError:
            print(f'Error in Publish Assets Response: {response.status_code}, {response.text}')
            return None


    
    def create_and_run_metadata_enrichment(self, name, mdi_id, enrichment_assets=None, description=None, enrichImmediate=True, job_name=None, job_schedule=None, publish_job_id=None, publish_job_name=None, publish_job_schedule=None, tags=None):
        """
        Create and run a metadata enrichment job.

        Args:
            name (str): Name of the metadata enrichment asset.
            objective (object): Objective of the metadata enrichment.
            target_catalog_id (str): ID of the catalog to store metadata enrichment assets.
            mdi_id (str): ID of the metadata import.
            enrichment_assets (list): IDs of assets to enrich metadata.
            description (str): Description of the metadata enrichment area asset. Default is None.
            enrichImmediate (bool): Whether to run enrichment immediately after area creation. Default is True.
            job_name (str): Name of the metadata enrichment job. Default is None.
            job_schedule (str): Schedule for the metadata enrichment job. Default is None.
            publish_job_id (str): ID of the metadata publish job. Default is None.
            publish_job_name (str): Name of the metadata publish job. Default is None.
            publish_job_schedule (str): Schedule for the metadata publish job. Default is None.
            tags (list): List of tags. Default is None.

        Returns:
            dict: The response of the metadata enrichment creation if successful, otherwise None.
        """
        

        bearer_token = self.get_bearer_token()

        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            "name": name,
            "objective": self.mde_objective,
            "target_catalog_id": self.catalog_id,
            "data_scope": {
                "enrichment_assets": enrichment_assets,
                "container_assets": {
                    "metadata_import": [mdi_id]
                }
            },
            "enrichImmediate": enrichImmediate
        }

        if description:
            payload["description"] = description

        if job_name or job_schedule:
            payload["job"] = {}
            if job_name:
                payload["job"]["name"] = job_name
            if job_schedule:
                payload["job"]["schedule"] = job_schedule

        if publish_job_id or publish_job_name or publish_job_schedule:
            payload["publish_job"] = {}
            if publish_job_id:
                payload["publish_job"]["id"] = publish_job_id
            if publish_job_name:
                payload["publish_job"]["name"] = publish_job_name
            if publish_job_schedule:
                payload["publish_job"]["schedule"] = publish_job_schedule

        if tags:
            payload["data_scope"]["tags"] = tags

        url = f'https://{self.cpd_cluster_host}/v2/metadata_enrichment/metadata_enrichment_area?project_id={self.project_id}'

        response = requests.post(url, json=payload, headers=headers, verify=False)
        try:
            response_json = response.json()
            print(f'{name}: Metadata Enrichment Creation Response: {response.status_code}')
            return response_json
        except requests.JSONDecodeError:
            print(f'Error in Metadata Enrichment Creation Response: {response.status_code}, {response.text}')
            return None


    def update_mde_settings(self):
        """
        Update the settings for metadata enrichment.

        Args:
            mde_settings (dict): The metadata enrichment settings.

        Returns:
            dict: The updated settings data.
        """

        # Metadata enrichment settings
        mde_settings = {
        'advanced_profiling': {'unique_value_table': {'count': 1000}},
        'semantic_expansion': {'name_expansion': True,
                                'name_expansion_configuration': {'assignment_threshold': 0.9,
                                                                'suggestion_threshold': 0.75},
                                'description_generation': True,
                                'description_generation_configuration': {'assignment_threshold': 0.9,
                                                                        'suggestion_threshold': 0.75}},
        'term_assignment': {'class_based_assignments': False,
                            'term_assignment_threshold': 0.9,
                            'term_suggestion_threshold': 0.75,
                            'name_matching': True,
                            'ml_based_assignments_default': False,
                            'ml_based_assignments_custom': False,
                            'evaluate_negative_assignments': True,
                            'default_ml_configuration': {'catalog_id': self.catalog_id,
                                                            'scope': 'catalog'},
                            'llm_based_assignments': False},
        'structured_profiling': {'null_threshold': 0.05,
                                    'uniqueness_threshold': 0.95,
                                    'constant_threshold': 0.99,
                                    'quality_score_threshold': 0.8,
                                    'data_class_assignment_threshold': 0.75,
                                    'data_class_suggestion_threshold': 0.25,
                                    'dq_exceptions_database': {'count': 100}},
        'key_analysis': {'pk_shallow_analysis_config': {'min_confidence': 0.8},
                            'fk_shallow_analysis_config': {'min_confidence': 0.8,
                                                        'auto_selection': False,
                                                        'auto_selection_threshold': 0.9}}
        }
        
        
        
        headers = {
            'Authorization': f'Bearer {self.get_bearer_token()}',
            'Content-Type': 'application/json'
        }
        
        endpoint = f"https://{self.cpd_cluster_host}/v2/metadata_enrichment/metadata_enrichment_area/settings"
        params = {
            'project_id': self.project_id
        }
        
        response = requests.put(endpoint, headers=headers, params=params, json=mde_settings)
        
        # Print response status code and text for debugging
        if response.status_code == 200:
            print("Metadata enrichment settings updated successfully.")
            return None


    def get_metadata_import_details(self, metadata_import_id):
        """
        Retrieve details of a metadata import.

        Args:
            metadata_import_id (str): Id of the metadata import asset.
            project_id (str): Id of the project.

        Returns:
            dict: Details of the metadata import if the request is successful, otherwise None.
        """
        url = f"{self.base_url}/v2/metadata_imports/{metadata_import_id}"
        
        # Query parameters
        params = {
            'project_id': self.project_id
        }

        # Headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.get_bearer_token()}'
        }

        response = requests.get(url, headers=headers, params=params, verify=False)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve metadata import details: {response.status_code}")
            print(response.text)
            return None

    def create_and_run_metadata_import(self, connection_id, paths_scope, name="Metadata Import"):
        """
        Create a metadata import, create a job, patch the metadata import, and run the job.

        Args:
            connection_id (str): The connection ID for the import.
            paths_scope (list): List of paths for the metadata import scope.
            name (str): Name of the metadata import. Defaults to "Metadata Import".

        Returns:
            dict: The response of the job run if successful, otherwise None.
        """
        # Replace with actual values
        cpd_url = self.cpd_cluster_host
        project_id = self.project_id

        # Get the bearer token
        bearer_token = self.get_bearer_token()

        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        }

        # 1. Create an MDI
        mdi_url = f'https://{cpd_url}/v2/metadata_imports?project_id={project_id}'
        mdi_payload = {
            "connection_id": connection_id,
            "name": name,
            "project_id": project_id,
            "target_project_id": project_id,
            "import_type": "metadata",
            "scope": {"paths": paths_scope},
            "extra_properties": {
                "include_primary_key": "true",
                "exclude_tables": "false",
                "metadata_from_catalog_table_only": "true",
                "include_foreign_key": "false",
                "exclude_views": "false"
            }
        }
        mdi_response = requests.post(mdi_url, json=mdi_payload, headers=headers)
        try:
            mdi_response_json = mdi_response.json()
            print(f'MDI Creation Response: {mdi_response.status_code}')
        except requests.JSONDecodeError:
            print(f'Error in MDI Creation Response: {mdi_response.status_code}, {mdi_response.text}')
            mdi_response_json = {}

        mdi_id = mdi_response_json.get('metadata', {}).get('asset_id')
        

        # Proceed only if MDI creation was successful
        if mdi_id:
            # 2. Create a job
            job_url = f'https://{cpd_url}/v2/jobs?project_id={project_id}'
            job_payload = {
                "job": {
                    "asset_ref": mdi_id,
                    "name": name+" Job",
                    "description": " ",
                    "configuration": {}
                }
            }
            job_response = requests.post(job_url, json=job_payload, headers=headers)
            try:
                job_response_json = job_response.json()
                print(f'Job Creation Response: {job_response.status_code}')
                
            except requests.JSONDecodeError:
                print(f'Error in Job Creation Response: {job_response.status_code}, {job_response.text}')
                job_response_json = {}

            job_id = job_response_json.get('metadata', {}).get('asset_id')

            # Proceed only if job creation was successful
            if job_id:
                # 3. Patch metadata Import with the job id
                patch_url = f'https://{cpd_url}/v2/metadata_imports/{mdi_id}?project_id={project_id}'
                patch_payload = {
                    "job_id": job_id
                }
                patch_response = requests.patch(patch_url, json=patch_payload, headers=headers)
                try:
                    patch_response_json = patch_response.json()
                    print(f'Patch MDI Response: {patch_response.status_code}')
                except requests.JSONDecodeError:
                    print(f'Error in Patch MDI Response: {patch_response.status_code}, {patch_response.text}')
                    patch_response_json = {}

                # Proceed only if patching was successful
                if patch_response.status_code == 200:
                    # 4. Run the Job (create a job-run)
                    run_url = f'https://{cpd_url}/v2/jobs/{job_id}/runs?project_id={project_id}&job_id={job_id}'
                    run_payload = {
                        "job_run": {}
                    }
                    run_response = requests.post(run_url, json=run_payload, headers=headers)
                    try:
                        run_response_json = run_response.json()
                        print(f'Run Job Response: {run_response.status_code}')
                        print()
                        return mdi_id, run_response_json
                    except requests.JSONDecodeError:
                        print(f'Error in Run Job Response: {run_response.status_code}, {run_response.text}')
                        print('Detailed error information:', run_response.text)
                else:
                    print('Failed to patch MDI with job ID, terminating the process.')
            else:
                print('Job creation failed, terminating the process.')
        else:
            print('MDI creation failed, terminating the process.')

        return None


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
            "project_id": self.project_id,
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
        

    def define_cos_connection(self, bearer, catalog=True):
        """
        Define a connection to Cloud Object Storage (COS).

        Args:
            bearer (str): Bearer token for authentication.
        """
        if catalog == True:
            url = f"{self.base_url}/v2/connections?catalog_id={self.catalog_id}"
        else:
            url = f"{self.base_url}/v2/connections?project_id={self.project_id}"
        
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
            self.cos_id = data.get('metadata', {}).get('asset_id')  
        else:
            print(f"Failed to define connection with status code {response.status_code}")
            print(response.text)

    def define_db2_connection(self, bearer, catalog=True):
        """
        Define a connection to a DB2 Warehouse.

        Args:
            bearer (str): Bearer token for authentication.
        """
        if catalog == True:
            url = f"{self.base_url}/v2/connections?catalog_id={self.catalog_id}"
        else:
            url = f"{self.base_url}/v2/connections?project_id={self.project_id}"
        
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
            self.db2_id = data.get('metadata', {}).get('asset_id')  
        else:
            print(f"Failed to define connection with status code {response.status_code}")
            print(response.text)

    def define_psql_connection(self, bearer,catalog=True):
        """
        Define a connection to a PostgreSQL Database.

        Args:
            bearer (str): Bearer token for authentication.
        """
        if catalog == True:
            url = f"{self.base_url}/v2/connections?catalog_id={self.catalog_id}"
        else:
            url = f"{self.base_url}/v2/connections?project_id={self.project_id}"
        
        headers = {
            "Authorization": f"Bearer {bearer}",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "Skip-Enforcement": "false"
        }

        # Request body
        payload = {
            "datasource_type": self.psql_datasource_type,
            "name": self.psql_name,
            "description": self.psql_description,
            "properties": {
                "database": self.psql_database,
                "password": self.psql_password,
                "port": self.psql_port,
                "host": self.psql_host,
                "username": self.psql_username
            },
            "origin_country": self.origin_country,
            "data_source_definition_searchable": f"{self.host}|{self.db_port}|{self.database}"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

        if response.status_code == 200 or response.status_code == 201:
            print(f"Connection to {bold_blue_start} PostgreSQL{reset} defined successfully!")
            data = response.json()
            self.psql_id = data.get('metadata', {}).get('asset_id')  
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
                    wip_message = "🚧🚧 Import process is still in progress. Checking again in 60 seconds... 🚧🚧"
                    print(wip_message)
                    print()
                    time.sleep(60)

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
