# Import Assets for Data Product Level 3


The purpose of this repository, notebook and the accompanying import client is to streamline the process of importing demo assets into the Data Product Hub Level Three environment. This process imports the two data source connections and the data governance artifacts leveraged in the lab.

To get started, simply update the `.env` file with: 
- `CPD_CLUSTER_HOST` - your Cloud Pak for Data (CPD) host
- `USERNAME` - username of Cloud Pak for Data Admin
- `PASSWORD` - password of Cloud Pak for Data Admin
- `CATALOG_NAME` - the name of the catalog you will be working with. 
  - Before you start, you will need to create a catalog inside of your Cloud Pak for Data environment.

> There is no need to change any other variables. The import client will handle the rest, ensuring a smooth and efficient import process.

# Install

```bash
cp .env.example .env
```

Fill in the .env file

Create the virtual environment with venv
```bash
python3 -m venv venv
```

Activate the virtual environment
```bash
source venv/bin/activate
```

Or create the virtual environment with conda

```bash
conda create -n dph-import python=3.10
conda activate dph-import
```

Install the dependencies
```bash
pip install -r requirements.txt
```

Run the import job
```bash
python import.py
```

If you have any questions reachout to Taylor Segell
- [Electronic Mail](mailto:taylorsegell@ibm.com)
- [Slack](https://ibm.enterprise.slack.com/team/U03FAV5TDPC)
