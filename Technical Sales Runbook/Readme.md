# IBM Data and AI

## Live Demos as a Service

This run book outlines the steps to setup and configure Cloud Pak for Data as a Service on IBM Cloud to support the **IBM Data and AI Live Demos** demonstrations and labs. The documentation applies to the production environments with a few exceptions, which are noted in the instructions. 

The tasks are organized by persona but you will perform all the tasks as the **Data Steward** administrator to setup, configure, and create all Cloud Pak for Data cloud services and objects (Platform connections, Virtualized data Sources and data, Catalogs, Business Glossary, Policies and rules etc.) This ensures that all services and objects are owned and administered by the **Data Steward** user who holds administration privileges.

## Cloud Account Management

## 1. Login to IBM Cloud

The production cloud acount is named **Techzone Outcomes**. Follow the instructions in the following sections to login to the appropriate cloud account using the supplied credentials. The **Data Steward** account is the administrator account for all environments.

### Production Data Steward Account

Login in to the **Techzone Outcomes** cloud account as the **Data Steward** administrator using the following credentials:

Login id = **Your data steward Login Id**

Password = **Your data steward password**

API Key = **Your data steward Id API Key**

### Production Business User Account

The **Business User** account is available in **production** to simulate what end users experience and to validate the demos and labs.

Login Id = **Your business user Login Id** 

Password = **Your business user password**

### Cloud Account API Keys

The API keys serve as the credentials for the **Watson Query** connection that is created in the **Governance** catalog that houses all governed virtualized data. It is also the key used by the outcomes reservation system to create and invite users, assign them to the **Business User** data access group and to assign **Viewer** service privileges for Watson Query, Watson Knowledge Catalog, Watson Studio and Watson OpenScale.

**TechZone Outcomes**

Data Steward API Key  = **Your data steward API Key**

Business User API Key = **Your business user API Key**

## 2. Create Cloud Resource Groups

### Cloud Pak for Data Outcomes

Create the following Cloud resource groups. This will be the resource group you select when creating all of the Cloud Pak for Data services in the upcoming sections, except for the **Outcomes Storage** service, defined in the next step.

1. Select the **Manage** menu from the IBM Cloud tool bar.
2. Select the **Account** menu item.
3. Click **Resource Groups** from the left side menu.
4. Click **Create**.
5. Enter Name = **Cloud Pak for Data Outcomes**.
6. Click **Create**.

### Outcomes Project Management

Create the following Cloud resource group. It will be the resource group you select when creating the **Outcomes Storage** cloud object storage service that will house all of our catalogs; Business, Governance and Platform assets catalog, and our projects that we use to build out the environment, the **Outcomes Runbook** and **Outcomes Catalog** projects.

1. Select the **Manage** menu from the IBM Cloud tool bar.
2. Select the **Account** menu item.
3. Click **Resource Groups** from the left side menu.
4. Click **Create**.
5. Enter Name = **Outcomes Project Management**.
6. Click **Create**.

## 3. Create Cloud Services

Create the following Cloud Pak for Data services from the **IBM Cloud** catalog, as described below, by typing the name of the service into the service catalog search area, selecting the service and then creating the service with the designated plan specified:

### Outcomes Cloud Object Storage

This cloud object storage service is used by the Data and AI team to create objects that need to be isolated from end users like our environment configuration projects, and all catalogs. This COS service is not visible or accessible to end users.

* Name = Outcomes Storage
* Plan = Standard
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

This cloud object storage service is used by all end users to create their projects and is the only cloud object storage that is visible for them to select when creating projects.

### Demo Cloud Object Storage

* Name = Demo Storage
* Plan = Standard
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Data Replication

* Name = Data Replication
* Plan = Lite
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### DataStage

* Name = DataStage
* Plan = Standard
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Databases for DataStax

* Name = Databases for DataStax
* RAM = 24 GB
* Disk = 360 GB
* Cores = 6
* Members = 3
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Databases for EDB

* Name = Databases for EDB
* RAM = 10 GB
* Disk = 100 GB
* Cores = 3
* Members = 3
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Databases for MongoDB

* Name = Databases for MongoDB
* Plan = Standard 
	
> Make sure you choose **standard** and not enterprise. The Enterprise
> edition uses SCRAM-> SHA-256 authentication and standard uses SCRAM
> SHA-1 and the CP4D MongoDB > driver only supports SCRAM-SHA-1.
	
* RAM = 24 GB
* Disk = 120 GB
* Cores = 6
* Members = 3
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Db2 Warehouse

* Name = Db2 Warehouse
* Plan = Flex One
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### IBM Cognos Dashboard Embedded

* Name = IBM Cognos Dashboard
* Plan = Pay as you go
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### IBM Match 360 for Watson

* Name = IBM Match 360
* Plan = Lite
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Machine Learning

* Name = Machine Learning
* Plan = v2 Professional
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Speech to Text

* Name = Speech to Text
* Plan = Plus
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Text to Speech

* Name = Text to Speech
* Plan = Standard
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Watson Assistant

* Name = Watson Assistant
* Plan = Plus
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Watson Discovery

* Name = Watson Discovery
* Plan = Enterprise
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Watson Knowledge Catalog

* Name = Watson Knowledge Catalog
* Plan = Enterprise
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Watson OpenScale

* Name = Watson OpenScale
* Plan = Standard v2
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Watson Studio

* Name = Watson Studio
* Plan = Enterprise v2
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

### Watson Query

* Name = Watson Query
* Plan = Enterprise
* Resource Group = Cloud Pak for Data Outcomes
* Tags = cpdaas and outcomes

## 4. Change Cloud Database Passwords

The cloud databases that were just created; Databases for DataStax, Databases for EDB and Databases for MongoDB, need to have their administrator passwords changed to administer them properly. Follow the steps below to set the admin password for these services:

1. Go to the IBM Cloud account left side menu.
2. Select **Resource List**.
3. Open the **Services and Software** category.

### Databases for DataStax Outcomes

1. Click on the **Databases for DataStax Outcomes** service.
2. Select the **Settings** tab.
3. Scroll down to the **Change Database Admin Password** section.
4. Copy and paste this password - **Your admin password** into the **New Password** field.
5. Click **Change Password**.
6. Click the **back** button on your browser to go back to the resource list.

### Databases for EDB Outcomes

1. Click on the **Databases for EDB Outcomes** service.
2. Select the **Settings** tab.
3. Scroll down to the **Change Database Admin Password** section
4. Copy and paste this password - **Your admin password** into the **New Password** field.
5. Click **Change Password**.
6. Click the **back** button on your browser to go back to the resource list.

### Databases for MongoDB Outcomes

1. Click on the **Databases for DataStax Outcomes** service.
2. Select the **Settings** tab.
3. Scroll down to the **Change Database Admin Password** section
4. Copy and paste this password - **Your admin password** into the **New Password** field.
5. Click **Change Password**.
6. Click the **back** button on your browser to go back to the resource list.

## Setup Cloud Account Security

Perform the following tasks as the **Data Steward** cloud account administrator to create the data access groups, and the Identify Access Management (IAM) policies that are needed for end users to perform the Cloud Pak for Data - Outcomes demonstrations:

1. Go to the IBM Cloud toolbar.
2. Select **Manage &gt; Access (IAM)**.

## 1. Create Business User Data Access Group

1. Select the **Access groups** menu item from the left side menu.
2. Click **Create**.
3. Enter a Name = **Business User**
4. Enter a Description = **This group includes all users who have requested access to the Cloud Pak for Data Outcomes demo environment. Users in this group are given read only access to the Cloud Pak for Data services and capabilities that are used in the demonstrations.** (including the period at the end).
5. Click **Create**.

## 2. Create Administrators Data Access Group

1. Select the **Access groups** menu item from the left side menu.
2. Click **Create**.
3. Enter a Name = **Administrators**
4. Enter a Description = **This group includes all users who have admin access to the Cloud Pak for Data Outcomes demo environment. Users in this group are given admin access to the Cloud Pak for Data services and capabilities that are used in the demonstrations.** (including the period at the end).
5. Click **Create**.

## 3. Create Service to Service Authorization

In order for **Watson Knowledge Catalog** and **Watson Query** to communicate and share a catalog for WQ to publish to, and for WQ to enforce WKC data protection rules, a service to service authorization has to be created in IAM. 

Follow the steps below to establish the authorization:

1. Select the **Authorizations** menu item from the left side menu.
2. Click **Create**.
3. Select the **Watson Knowledge Catalog** service from the Source service dropdown list.
4. Select the **Resources based on selected attributed** radio button.
5. Select the **Source resource group** checkbox.
6. Select the **Cloud Pak for Data** resource group from the dropdown list.
7. Select **Watson Query** from the Target service dropdown list.
8. Select the **Resources based on selected attributed** radio button.
9. Select the **Source resource group** checkbox.
10. Select the **Cloud Pak for Data** resource group from the dropdown list.
11. Click the checkbox in the **Service access** section next to **DataAccess (For Service to Service Authorization Only)**.
12. Click **Authorize**.

## 4. Create Watson Knowledge Catalog Business User Role

1. Select the **Roles** menu item from the left side menu.
2. Click **Create**.
3. Enter a Name = **Watson Knowledge Catalog Business User**
4. Enter a ID = **WKCUser**
5. Enter a Description = **Permissions for business users to use the Watson Knowledge Catalog service.** (including the period at the end).
6. Select **IBM Cloud Pak for Data** from the service dropdown list.
7. Select **All roles** from the view actions for dropdown list.
8. Click the **Add** link next to the following actions:
	* cp4d.catalog.access
	* cp4d.governance-artifacts.access
9. Click **Apply**.

## 5. Create Watson Knowledge Catalog Administrator Role

1. Select the **Roles** menu item from the left side menu.
2. Click **Create**.
3. Enter a Name = **Watson Knowledge Catalog Administrator**
4. Enter a ID = **WKCAdmin**
5. Enter a Description = **Permissions for administrators of the Watson Knowledge Catalog service.** (including the period at the end).
6. Select **IBM Cloud Pak for Data** from the service dropdown list.
7. Select **All roles** from the view actions for dropdown list.
8. Click the **Add** link next to the following actions:
   * cp4d.catalog.access
   * cp4d.catalog.manage
   * cp4d.data-protection-rules.manage
   * cp4d.governance-artifacts.access
   * cp4d.governance-categories.manage
   * cp4d.governance-workflows.manage
   * cp4d.wkc.reporting.manage
9. Click **Apply**.

## 6. Assign IAM Policies to Business User Group

Business users, users that have requested access to the demo environment using the Cloud Pak for Data - Outcomes reservation system, are given view only access to platform and service capabilities.

### Assign IAM Services Roles

1. Select the **Access groups** menu item from the left side menu.
2. Click the **Business User** group.
3. Click the **Access policies** tab.
4. Click the **Assign access** button.
5. Click the **IAM services** tile.
6. Select **All Identity and Access Enabled services** from the **Which service do you want to assign access to?** dropdown list.
7. Click the **Resources based on selected attributes** radio button.
8. Click the **Resource group** checkbox.
9. Select the **Cloud Pak for Data** resource group from the dropdown list.
10. Check the **Viewer** checkbox for **Platform access**.
11. Check the **Reader** checkbox for **Service access**.
12. Check the **Viewer** checkbox for **Resource group access**.
13. Click **Add**.
13. Click **Assign**.

### Assign Watson Knowledge Catalog User Role

1. Click the **Assign access** button.
2. Click the **IAM services** tile.
3. Select **IBM Cloud Pak for Data** from the **Which service do you want to assign access to?** dropdown list.
4. Scroll down to the bottom of the page to the **Custom access** section.
5. Click the **Watson Knowledge Catalog User** checkbox.
6. Click **Add**.
7. Click **Assign**.

### Assign Machine Learning Role

1. Click the **Assign access** button.
2. Click the **IAM services** tile.
3. Select **Machine Learning** from the **Which service do you want to assign access to?** dropdown list.
4. Click the **Resources based on selected attributes** radio button.
5. Click the **Service instance** checkbox.
6. Select **string equals** from the first dropdown list box.
7. Select the **Machine Learning Outcomes (b7b...)** instance from the service dropdown list.
	* There should only be one Machine Learning Outcomes instance in the list.
8. Check the **Editor** checkbox for **Platform access**.
9. Check the **Writer** checkbox for **Service access**.
10. Click **Add**.
11. Click **Assign**.

## 7. Assign IAM Policies to Administrator Group

Administrators, users that have assigned administrative privileges to the Cloud Pak for Data - Outcomes environment, are given full access to platform and service capabilities.

### Assign IAM Services Roles

1. Select the **Access groups** menu item from the left side menu.
2. Click the **Administrator** group.
3. Click the **Access policies** tab.
4. Click the **Assign access** button.
5. Click the **IAM services** tile.
6. Select **All Identity and Access Enabled services** from the **Which service do you want to assign access to?** dropdown list.
7. Click the **All resources** radio button.
8. Check the **Administrator** checkbox for **Platform access**.
9. Check the **Manager** checkbox for **Service access**.
10. Check the **Administrator** checkbox for **Resource group access**.
11. Click **Add**.
12. Click **Assign**.

### Assign Account Management Roles

1. Click the **Assign access** button.
2. Click the **Account management** tile.
3. Select **All Account Management services** from the **Which service do you want to assign access to?** dropdown list.
4. Check the **Administrator** checkbox for **Platform access**.
5. Click **Add**.
6. Click **Assign**.

## Cloud Pak for Data Tasks

## 1. Login to Cloud Pak for Data

The following tasks are done from the **Cloud Pak for Data** as a service application using the **Techzone Outcomes** cloud account as the **Data Steward** administrator.

Make sure you are in the **Techzone Outcomes** cloud account by ensuring it is selected in the top right corner of the UI.

Go to the [Cloud Pak for Data as a Service](https://dataplatform.cloud.ibm.com) home page and login with the **Data Steward** credentials provided in the first section of this document.

## 2. Enable Storage Delegation

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Administration &gt; Storage delegation**.

Perform the following steps for the **Demo Storage** instance:

1. Click the **Projects** button and set it to the green, on position.
2. Click the **Catalogs** button and set it to the green, on position.

**Note: - DO NOT** turn these flags on for the **Outcomes Storage** instance. They should remain turned off.

## 3. Create Catalogs

This section creates three catalogs; The **Business** catalog, **Platform assets catalog**, and the **Governance** catalog.

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Catalogs &gt; View all catalogs**.

### Create Business Catalog

This catalog contains all the governed and trusted data assets that are used by the business for analytics and AI. All users that are assigned to the **Business User** group are given *Viewer* access to this catalog.

1. Click **Create Catalog**.
2. Enter Name = **Business**
3. Enter Description = **This catalog stores governed assets used by the business for analytical and AI projects.**. (including the period at the end).
4. Check the box to **Enforce data policies**.
5. Click **OK** when prompted if you are sure you want to enforce policies.
6. Select the **Update original assets** duplicate asset handling option.
7. Select the **Cloud Object Storage** instance from the Object storage instance dropdown.
8. Click **Create**.
9. Select the **Access control** tab.
10. Scroll down and select **Add access groups**.
11. Select **Viewer** for the access level.
12. Start typing **bus** in the search area.
13. Click the **Business Users** access group.
14. Click **Add**.

### Create Governance Catalog

This catalog is only used by Data Virtualization and has no user access. Only the Data Steward user, assigned as the administrator, will have access to this catalog.

1. Click **Create Catalog**.
2. Enter Name = **Governance**
3. Enter Description = **This catalog stores governed data assets that are virtualized through Data Virtualization.** (including the period at the end)
4. Check the box to **Enforce data policies**.   
5. Click **OK** when prompted if you are sure you want to enforce policies.
6. Select the **Update original assets** duplicate asset handling option.
7. Select the **Cloud Object Storage** instance from the Object storage instance dropdown.
8. Click **Create**.

### Create Platform assets catalog

You must create the Platform assets catalog before you can create platform connections. This is only done once to allow for platform connections to be shared across the platform.

Users will only have read only access to the platform connections that are published to this catalog. 

**Note:** This catalog is not used or serve any purpose for **Cloud Pak for Data - Outcomes** demonstrations and labs, but is required for users to access and view **Platform connections** from the main menu.

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Data &gt; Platform connections**.
3. Click **Create Catalog**.
4. Select the **Cloud Object Storage** instance from the Object storage instance dropdown.
5. Click **Create**.
6. Select the **Access control** tab.
7. Scroll down and select **Add access groups**.
8. Select **Viewer** for the access level.
9. Start typing **bus** in the search area.
10. Click the **Business Users** access group.
11. Click **Add**.

## Create Governance Artifacts

This section creates all the governance artifacts needed to establish a data governance foundation. It builds out a fully published business glossary and defines and enforces data governance policies and rules. It uses a set of **CSV** files to import and create the artifacts. 

The files are located in this Cloud Pak for Data - Outcomes GitHub repository:

Download and unzip the **cpd-outcomes-governance.zip** file to a location on your desktop and remember where you put it. You will be instructed to select specific files that are contained in this file during the creation of the governance artifacts in the upcoming steps.

## 1. Create Categories

Categories have to be created before any other governance artifacts that require an assignment to a category are created. The only governance artifact that does not require an association to a category are data protection rules. Categories are like folders and are a high level umbrella and container for other governance artifacts. Categories also control all governance artifact access and security levels.

The import should succeed with 14 new categories. If the categories do not appear, go to the navigation main menu and select **Governance &gt; Categories**. 

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Governance &gt; Categories**.
3. Select **Add category &gt; Import from file**.
4. Select **Add file**.
5. Find and select the **governance-categories.csv** file from your download location.
6. Click **Open**.
7. Click **Next**.
8. Select **Replace all values**.
9. Select **Import**.
10. Select **Close**.
11. Select the **Refresh** button on your browser.
12. Select the **category explorer** icon in the top left corner to get a tree view.

The import should succeed with 14 new categories. If the categories do not appear, go to the navigation main menu and select **Governance &gt; Categories**. 

Select the category explorer icon in the top left corner. You should see 9 primary categories and 5 sub-categories:

- Banking
   - Mortgage
- Customer
- Data Privacy
   - Payment Card Industry
   - Personal Information
   - Personally Identifiable Information
   - Sensitive Personal Information
- Employee
- Insurance
- Location
- Person
- Transportation
- Universal

## 2. Update Classifications

1. Go to the Cloud Pak for Data **navigation** menu
2. Select **Governance &gt; Classifications**.
3. Select **Add classification &gt; Import from file**.
4. Click **Add file**.
5. Select the **governance-classifications.csv** file from your download location.
6. Click **Open**.
7. Click **Next**.
8. Select **Replace all values**.
9. Click **Import**.
10. Click **Go to Task**.
11. Click **Publish**.
12. Go to the Cloud Pak for Data **navigation** menu.
13. Select **Governance &gt; Classifications****.

You should see 4 new published classifications that are assigned to the **Data Privacy** category along side the 4 already published classifications of the same name that are assigned to the **[uncategorized]** category:

* Confidential
* Personal Information
* Personally Identifiable Information
* Sensitive Personal Information

The duplicate classifications assigned to the **[uncategorized]** category are no longer needed so we will delete them.

1. Click the **Edit** button.

	> Looks like a pencil icon next to the Sort criteria to the far right of the screen

2. Select the **check box** next to all classifications that are assigned to the **[uncategorized]** category.
3. Scroll **up** to the top of the screen.
4. Select **Mark for deletion**.

> You will see a dialog box indicating it was submitted for deletion. **Wait** a few seconds for the second dialog box to appear that has a link to the **task** you need to process.

6. Select the **task link** in the second dialog box.

    * This will take you directly to the **Mark for deletion** task.
    * If you miss the chance to click on the link from the dialog box:
        * Go to the main navigation menu and select **Governance &gt; Task inbox**.
        * Select the checkbox next to the classification deletion task.

7. Click **Delete**.
8. Go to the Cloud Pak for Data **navigation** menu.
9. Select **Governance &gt; Classifications**.

You should now see 4 published Classifications assigned to the **Data Privacy** category.

## 3. Create Data Classes

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Governance &gt; Data classes**.
3. Click **New data class**.
4. Click **Import from file**.
5. Click **Add file**.
6. Select the **governance-data-classes.csv** file from your download location.
7. Click **Open**.
8. Click **Next**.
9. Select **Replace all values**.
10. Click **Import**.
11. Click **Go to Task**.

> You should see 15 new data classes to publish.

12. Click **Publish**.
13. Go to the Cloud Pak for Data **navigation** menu.
14. Select **Governance &gt; Data classes**
15. Click the **Sort by** dropdown list.
16. Select **Last modified** .

> There should be 15 newly published data classes that are assigned to the **[uncategorized]** category that have a modification date of today.

## 4. Create Business Terms

Business terms have references to data classes and classifications and are referenced in governance rules, so they need to be imported after data classes and classifications but before importing or creating governance rules. 

Business terms can also be dependent on other business terms which establishes a parent child relationship between them. Therefore, we will import the parent business terms before importing all the other business terms.

There should be **NO** business terms in the business glossary at this point.

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Governance &gt; Business terms**.

### Import Parent Business Terms

1. Select **Add business term &gt; Import from file**.
2. Click **Add file**.
3. Select the **governance-business-terms-parent.csv** file from the download location.
4. Click **Open**.
5. Click **Next**.
6. Select **Replace all values**.
7. Click **Import**.
8. Click **Go to Task**.
9. Click **Publish**.
10. Go to the Cloud Pak for Data **navigation** menu.
11. Select **Governance &gt; Business terms**.

All business terms should be appearing as **Published**. Verify that there are **6** published business terms before proceeding to the next step because some of the business terms in the next import are dependent on them being published first.

### Import Child Business Terms

1. Select **Add business term &gt; Import from file**.
2. Click **Add file**.
3. Select the **governance-business-terms.csv** file from the download location.
4. Click **Open**.
5. Click **Next**.
6. Select **Replace all values**.
7. Click **Import**.
8. Click **Go to Task**.

> There should be 328 business term drafts waiting to be published...

9. Click **Publish**.
10. Go to the Cloud Pak for Data **navigation** menu.
11. Select **Governance &gt; Business terms**.

All business terms should be appearing as **Published**. Scroll to the bottom of the business term list and verify that there are now **328** published business terms.

## 5. Create Reference Data

The **CSV** files for reference data are included as part of the **cpd-outcomes-governance-artifacts.zip** file you downloaded and unzipped earlier.

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Governance &gt; Reference**.

Create the following reference data sets:

### Department Lookup

1. Select **Add reference data set &gt; New reference data set**.
2. Select the **DEPARTMENT_LOOKUP.csv** as the file to upload.
3. Enter **Department Lookup** (case sensitive) as the reference data name.
4. Select **Text** as the reference data type.
5. Click the **Change** category button.
6. Select the **Employee** category.
7. Click **Add**.
8. Copy and pastes this description: **Valid codes and values for all company departments.** including the period at the end).
9. Click **Next**.
10. Make sure the **First row as column header** is set to **On**.
11. Click **Select column** dropdown for the **DEPARTMENT_CODE** target column.
12. Select **Code**.
13. Click **Select column** dropdown for the **DEPARTMENT_EN** target column.
14. Select **Value**.
15. Click **Next**.
16. Click **Create**.

From the **About this reference data** panel on the right:

1. Click on the **plus sign +** next to Tags.
2. Click the **dropdown arrow** in the search tags area.
3. Select the **Employee** tag.
4. Click **Done**.
5. Click **Publish**.
6. Click **Publish**.

You will see an informational icon and message of **Draft preview** This artifact has a new published version.

1. Click **Reload artifact**.
2. Click the **Reference data** bread crumb in the top left corner.
    
	> This will take you back to the **Reference data** home page.

### Gender Lookup

1. Select **Add reference data set &gt; New reference data set**.
2. Select the **GENDER_LOOKUP.csv** as the file to upload.
3. Enter **Gender Lookup** (case sensitive) as the reference data name.
4. Select **Text** as the reference data type.
5. Click the **Change** category button.
6. Select the **Person** category.
7. Click **Add**.
8. Copy and pastes this description: **Valid codes and values for an individual's gender.** (including the period at the end).
9. Click **Next**.
10. Make sure the **First row as column header** is set to **On**.
11. Click **Select column** dropdown for the **GENDER_CODE** target column.
12. Select **Code**.
13. Click **Select column** dropdown for the **GENDER_EN** target column.
14. Select **Value**.
15. Select **Next**.
16. Click **Create**.

From the **About this reference data** panel on the right:

1. Click on the **plus sign +** next to Tags.
2. Click the **dropdown arrow** in the search tags area.
3. Select the **Customer** tag.
4. Select the **Employee** tag.
5. Type **Person** in the tag search area and Select the **Person** tag.
6. Click **Done**.
7. Click **Publish**.
8. Click **Publish**.

You will see an informational icon and message of **Draft preview** This artifact has a new published version.

1. Click **Reload artifact**.
2. Click the **Reference data** bread crumb in the top left corner.
    
    * This will take you back to the **Reference data** home page.

### Position Lookup

1. Select **Add reference data set > New reference data set**.
2. Select the **POSITION_LOOKUP.csv** as the file to upload.
3. Enter **Position Lookup** (case sensitive) as the reference data name.
4. Select **Text** as the reference data type.
5. Click the **Change** category button.
6. Select the **Employee** category.
7. Click **Add**.
8. Copy and pastes this description: **Valid codes and values for positions across the company.** (including the period at the end).
9. Click **Next**.
10. Make sure the **First row as column header** is set to **On**.
11. Click **Select column** dropdown for the **POSITION_CODE** target column.
12. Select **Code**.
13. Click **Select column** dropdown for the **POSITION_EN** target column.
14. Select **Value**.
15. Click **Next**.
16. Click **Create**.

From the **About this reference data** panel on the right:

1. Click on the **plus sign +** next to Tags.
2. Click the **dropdown arrow** in the search tags area.
3. Select the **Employee** tag.
4. Click **Done**.
5. Click **Publish**.
6. Click **Publish**.

You will see an informational icon and message of **Draft preview** This artifact has a new published version.

1. Click **Reload artifact**.
2. Click the **Reference data** bread crumb in the top left corner.
    
    * This will take you back to the **Reference data** home page.

### Termination Lookup

1. Select **Add reference data set > New reference data set**.
2. Select the **TERMINATION_LOOKUP.csv** as the file to upload.
3. Enter **Termination Lookup** (case sensitive) as the reference data name.
4. Select **Text** as the reference data type.
5. Click the **Change** category button.
6. Select the **Employee** category.
7. Click **Add**.
8. Copy and pastes this description: **Valid codes and values for employee terminations.** (including the period at the end).
9. Click **Next**.
10. Make sure the **First row as column header** is set to **On**.
11. Click **Select column** dropdown for the **TERMINATION_CODE** target column.
12. Select **Code**.
13. Click **Select column** dropdown for the **TERMINATION_REASON_EN** target column.
14. Select **Value**.
15. Click **Next**.
16. Click **Create**.

From the **About this reference data** panel on the right:

1. Click on the **plus sign +** next to Tags.
2. Click the **dropdown arrow** in the search tags area.
3. Select the **Employee** tag.
4. Click **Done**.
5. Click **Publish**.
6. Click **Publish**.

You will see an informational icon and message of **Draft preview** This artifact has a new published version.

1. Click **Reload artifact**.
2. Click the **Reference data** bread crumb in the top left corner.
   
    * This will take you back to the **Reference data** home page.

You should see 4 Reference data assets:

* Department Lookup
* Gender Lookup
* Position Lookup
* Termination Lookup

## 6. Create Governance Rules

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Governance &gt; Rules**.
3. Select **Add rule &gt; Import from file**.
3. Click **Add file**.
4. Select the **governance-rules.csv** file from the download location.
5. Click **Open**.
6. Click **Next**.
7. Select **Replace all values**.
8. Click **Import**.
9. Click **Go to Task**.
10. Click **Publish**.
11. Go to the Cloud Pak for Data **navigation** menu.
12. Select **Governance &gt; Rules**.

You should see **4** published governance rules with names that start with **All...**

## 7. Create Data Protection Rules

The data protection rules are created using the advanced data privacy masking features of Watson Knowledge Catalog.

### Create the Protect Credit Card Expiration Dates Rule

1. Select **Add rule &gt; New rule**.
2. Select **Data protection rule**.
3. Click **Next**.
4. Enter Name = **Protect Credit Card Expiration Dates**
5. Enter Business definition = **Protect all credit card expiration dates using the data privacy advanced masking method.** (including the period at the end).
6. Build the rule as follows:
    * Criteria = If **Data class** contains any **Credit Card Expiration Date**.
    * Action = then **mask data** in columns containing **Data class** of **Credit Card Expiration Date**.
    * Select **Obfuscate** in the *Select how to mask data:* section.
    * Check **Enable advanced masking options**.
    * Select **Identifier method** as the Obfuscate method.
    * Select **Irreversible masking** for the Reversibility option.
    * Select **Repeatable** for the Consistency option.
    * Select **No validation** for the Input validation option.
    * Turn **On** the Auto refresh preview.
7. Click **Create**.
8. Select the **Rules** bread crumb, in top left corner to return to Rules main page.

### Create the Protect Credit Card Numbers Rule

1. Select **Add rule &gt; New rule**.
2. Select **Data protection rule**.
3. Click **Next**.
4. Enter Name = **Protect Credit Card Numbers**
5. Enter Business definition = **Protect all credit card numbers using the data privacy advanced masking method.** (including the period at the end).
6. Build the rule as follows:
    * Criteria = If **Data class** contains any **Credit Card Number**.
    * Action = then **mask data** in columns containing **Data class** of **Credit Card Number**.
    * Select **Obfuscate** in the *Select how to mask data:* section.
    * Check **Enable advanced masking options**.
    * Select **Preserve format** as the Obfuscate method.
    * Select **Irreversible masking** for the Reversibility option.
    * Select **Repeatable** for the Consistency option.
    * Select **Input validation** for the Input validation option.
    * Turn **On** the Auto refresh preview.
7. Click **Create**.
8. Select the **Rules** bread crumb, in top left corner to return to Rules main page.

### Create the Protect Credit Card Validation Numbers Rule

1. Select **Add rule &gt; New rule**.
2. Select **Data protection rule**.
3. Click **Next**.
4. Enter Name = **Protect Credit Card Validation Numbers**
5. Enter Business definition = **Protect all credit card validation numbers using the data privacy advanced masking method.** (including the period at the end).
6. Build the rule as follows:
    * Criteria = If **Data class** contains any **Credit Card Validation Number**.
    * Action = then **mask data** in columns containing **Data class** of **Credit Card Validation Number**.
    * Select **Obfuscate** in the *Select how to mask data:* section.
    * Check **Enable advanced masking options**.
    * Select **Identifier method** as the Obfuscate method.
    * Select **Irreversible masking** for the Reversibility option.
    * Select **Repeatable** for the Consistency option.
    * Select **No validation** for the Input validation option.
    * Turn **On** the Auto refresh preview.
7. Click **Create**.
8. Select the **Rules** bread crumb, in top left corner to return to Rules main page.

### Create the Protect Email Addresses Rule

1. Select **Add rule &gt; New rule**.
2. Select **Data protection rule**.
3. Click **Next**.
4. Enter Name = **Protect Email Addresses**
5. Enter Business definition = **Protect all email addresses using the data privacy advanced masking method.** (including the period at the end).
6. Build the rule as follows:
    * Criteria = If **Data class** contains any **Email Address**.
    * Action = then **mask data** in columns containing **Data class** of **US Phone Number**.
    * Select **Obfuscate** in the *Select how to mask data:* section.
    * Check the box to **Enable advanced masking options**.
    * Select **Preserve format** as the Obfuscate method.
    * Select **Generate user name** for the User name format option.
    * Select **Custom** for the Domain name option.
    * Enter **outcomes.com** for the Custom value.
    * Select **Irreversible masking** for the Reversibility option.
    * Select **Repeatable** for the Consistency option.
    * Select **Input validation** for the Input validation option.
    * Turn **On** the Auto refresh preview.
7. Click **Create**.
8. Select the **Rules** bread crumb, in top left corner to return to Rules main page.

### Create the Protect Phone Numbers Rule

1. Select **Add rule &gt; New rule**.
2. Select **Data protection rule**.
3. Click **Next**.
4. Enter Name = **Protect International Phone Numbers**
5. Enter Business definition = **Protect all international phone numbers using the redaction masking method. There are no obfuscation masking options for the Phone Number data class. Obfuscation can only be applied to US Phone numbers.** (including the period at the end).
6. Build the rule as follows:
    * Criteria = If **Data class** contains any **Phone Number**.
    * Action = then **mask data** in columns containing **Data class** of **US Phone Number**.
    * Select **Redact** in the *Select how to mask data:* section.

<!-- 
These commands below do not apply because there is no advanced method for masking a a data class of Phone Number, it only applies to the US Phone Number data class and the phone numbers in the customer data are international phone numbers.

    * Check the box to **Enable advanced masking options**.
    * Select **Preserve format** as the Obfuscate method.
    * Select **Irreversible masking** for the Reversibility option.
    * Select **Repeatable** for the Consistency option.
    * Select **Input validation** for the Input validation option.
    * Turn **On** the Auto refresh preview.
-->
7. Click **Create**.
8. Select the **Rules** bread crumb, in top left corner to return to Rules main page.

### Create the Protect US Phone Numbers Rule

1. Select **Add rule &gt; New rule**.
2. Select **Data protection rule**.
3. Click **Next**.
4. Enter Name = **Protect US Phone Numbers**
5. Enter Business definition = **Protect all US phone numbers using the data privacy advanced masking method.** (including the period at the end).
6. Build the rule as follows:
    * Criteria = If **Data class** contains any **US Phone Number**.
    * Action = then **mask data** in columns containing **Data class** of **US Phone Number**.
    * Select **Obfuscate** in the *Select how to mask data:* section.
    * Check **Enable advanced masking options**.
    * Select **Preserve format** as the Obfuscate method.
    * Select **Irreversible masking** for the Reversibility option.
    * Select **Repeatable** for the Consistency option.
    * Select **No validation** for the Input validation option.
    * Turn **On** the Auto refresh preview.
7. Click **Create**.
8. Select the **Rules** bread crumb, in top left corner to return to Rules main page.

### Create the Protect US Social Security Numbers Rule

1. Select **Add rule &gt; New rule**.
2. Select **Data protection rule**.
3. Click **Next**.
4. Enter Name = **Protect US Social Security Numbers**
5. Enter Business definition = **Protect all US social security numbers using the data privacy advanced masking method.** (including the period at the end).
6. Build the rule as follows:
    * Criteria = If **Data class** contains any **US Social Security Number**.
    * Action = then **mask data** in columns containing **Data class** of **US Social Security Number**.
    * Select **Obfuscate** in the *Select how to mask data:* section.
    * Check **Enable advanced masking options**.
    * Select **Preserve format** as the Obfuscate method.
    * Select **Irreversible masking** for the Reversibility option.
    * Select **Repeatable** for the Consistency option.
    * Select **No validation** for the Input validation option.
    * Turn **On** the Auto refresh preview.
7. Click **Create**.
8. Select the **Rules** bread crumb, in top left corner to return to Rules main page.

## 8. Create Policies

The policies are created last because they have data protection and governance rules assigned to them. Therefore the rules have to be created first before the policy so that the rules can be assigned to the appropriate policies. For Outcomes, there is only one policy.

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Governance &gt; Policies**.
3. Select **Add policy &gt; Import from file**.
3. Click **Add file**.
4. Select the **governance-policies.csv** file from the download location.
5. Click **Open**.
6. Click **Next**.
7. Select **Replace all values**.
8. Click **Import**.
9. Click **Go to Task**.
10. Click **Publish**.
11. Go to the Cloud Pak for Data **navigation** menu.
12. Select **Governance &gt; Polices**.

You should see 1 published policy named **Protection of Sensitive Personal Information**.

### Assign Data Protection Rules to the Policy

1. Click the **Protection of Sensitive Personal Information** policy.
2. Scroll down to the **Data protection rules** section.
3. Click **Add data protection rules**.
4. Select the **Protect Credit Card Expiration Dates** rule.
5. Select the **Protect Credit Card Numbers** rule.
6. Select the **Protect Credit Card Validation Numbers** rule.
7. Select the **Protect Email Addresses** rule.
8. Select the **Protect Phone Numbers** rule.
9. Select the **Protect US Social Security Numbers** rule.
10. Click **Add**.
11. Click **Publish**.
12. Click **Publish**.

## Create Platform Connections

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Data &gt; Platform connections**.

## 1. Create Amazon Object Store Connection

1. Select **New connection**.
2. Type **amazon** in the search area.
3. Click the **Amazon S3** connector.
4. Click **Select**.
5. Enter the following properties:
 
* Name = Amazon Object Storage
* Description = **Amazon S3 Object Storage bucket that contains data files used for analytics and AI.** (including the period at the end)
* Bucket = cpd-outcomes-s3
* Endpoint URL = https://s3.us-east-2.amazonaws.com
* Region = us-east-2
* Credentials = Shared
* Authentication method = Basic credentials
* Access key = AKIA2EJTDLF7QCA4EK4P
* Secret key = 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

6. Click **Create**.

## 2. Create Cloud Object Store Connection

1. Select **New connection**.
2. Type **cloud** in the search area.
3. Click the **Cloud Object Storage** connector.
4. Click **Select**.
5. Enter the following properties:
    
* Name = Cloud Object Storage
* Description = **IBM Cloud Object Storage bucket that contains data files used for analytics and AI.** (including the period at the end)
* Bucket = **Your bucket**
* Login URL = **Your Login URL**
* Authentication method = Resource Instance Id, API Key, Access Key and Secret Key
* Resource instance Id = **Your resource instance Id**
* API key = **Your API Key**
* Access Key = **Your Access Key**
* Secret Key = **Your Secret Key**

> **Note** - The Resource Instance ID and API Key for the credential values are extracted from the JSON below:

**CPD-Outcomes-Storage-Content-Reader**
{
  **Your JSON**
}

6. Click **Create**.

## 3. Create Data Warehouse Connection

1. Click **New connection**.
2. Type **db2** in the search area.
3. Click the **Db2 Warehouse** connector.
4. Click **Select**.
5. Enter the following properties:
    
* Name = Data Warehouse
* Description = **Database that contains enterprise data needed by the business for analytics and AI.** (including the period at the end)
* Database = BLUDB
* Host = **Your Host**
* Port = 50001
* Authentication Method = Username and password
* Username = **Your Username**
* Password = **Your Password**
* Certificates = Port is SSL-enabled

6. Click **Create**.

## 4. Create Document Store Connection

1. Select **New connection**.
2. Type **mongo** in the search area.
3. Click the **MongoDB** connector.
4. Click **Select**.
5. Enter the following properties:
    
* Name = Document Store
* Description = **Data store that contains documents needed by the business for analytics and AI.** (including the period at the end)
* Database = DOCUMENT
* Hostname = **Your Hostname**
* Port = **Your Port**
* Authentication database = admin
* Username = **Your Username**
* Password = **Your Password**
* Certificates = Port is SSL-enabled

5. Click **Create**.

## 5. Create Third Party Data Connection

1. Select **New connection**.
2. Type **post** in the search area.
3. Click the **PostgreSQL** connector.
4. Click **Select**.
5. Enter the following properties:
    
* Name = Third Party Data
* Description = **Database that contains third party data needed by the business for analytics and AI.** (including the period at the end)
* Database = **Your Database**
* Hostname = **Your Hostname**
* Port = **Your Port**
* Username = **Your Username**
* Password = **Your Password**
* Credentials = Port is SSL-enabled

6. Click **Create**.

## Setup Data Virtualization

## 1. Enable Data Governance

This section enables the data governance capabilities in Data Virtualization to protect sensitive personal information and to publish virtualized tables to a governed catalog, the **Governance** catalog.

Select **Settings &gt; Service Settings** from the Data Virtualization dropdown menu.

1. Select the **Governance** tab.
2. Click the **Enforce policies within Data Virtualization** to turn it on.
3. Click the **Enforce publishing to a governed catalog** to turn it on.
4. Select the **Governance** catalog.

## 2. Create Data Sources

Add the Data Virtualization data sources by using the connections that were just created in Platform connections by using the create from existing method.


1. Select **Virtualization &gt; Data Sources** from the Data Virtualization dropdown menu.
2. Click **Add connection**.
3. Click **Existing connection**.
4. Select **Third Party Data** connection.
5. Click **Add**.
6. Click **Add connection**.
7. Click **Existing connection**.
8. Select **Document Store** connection.
9. Click **Add**.
10. Click **Add connection**.
11. Click **Existing connection**.
12. Select **Data Warehouse** connection.
13. Click **Add**. 
14. Click **Add connection**.
15. Click **Existing connection**.
16. Select **Cloud Object Storage** connection.
17. Click **Add**.
18. Click **Add connection**.
19. Click **Existing connection**.
20. Select **Amazon Object Storage** connection.
21. Click **Add**.

## 3. Virtualize the Data

We only virtualize the tables needed for analytics and AI modeling tasks that will be used to create virtual views or that are added to projects so data transformation and preparation can be performed prior to doing analytics and AI tasks. For the Outcomes data fabric demonstrations, 12 tables will be virtualized.

1. Select **Virtualization &gt; Virtualize** from the Data Virtualization dropdown menu.
2. Click the **Search asset type** filter dropdown menu.
3. Select **Table**.
4. Select the **Settings** menu icon on far right next to the refresh icon.
5. Uncheck **Hostname:port** and **Columns**.

### Virtualize Banking Tables

1. Sort by **Table** in ascending order (Arrow pointing up).
2. Type **mortgage** in search area.
3. Select the checkbox next to the following **Banking** tables:
   
   * MORTGAGE_APPLICANT
   * MORTGAGE_APPLICATION
   * MORTGAGE_CANDIDATE

4. Click **Add to cart**.
5. Click the **x** at the end of the search area to clear it out.

### Virtualize Employee Tables

1. Sort by **Table** in ascending order (Arrow pointing up).
2. Type **employee** in search area.
3. Select the following **Employee** tables:
   
   * EMPLOYEE_HISTORY
   * EMPLOYEE
   * EMPLOYEE\_EXPENSE\_DETAIL
   * EMPLOYEE_SUMMARY

4. Click **Add to cart**.
5. Click the **x** at the end of the search area to clear it out.
6. Type **position** in the search area.
7. Select the checkbox next to the **POSITION_DEPARTMENT** table.
8. Click **Add to cart**.
9. Click the **x** at the end of the search area to clear it out.
10. Type **ranking** in the search area.
11. Select the checkbox next to the **RANKING_RESULTS** table.
12. Click **Add to cart**.
13. Click the **x** at the end of the search area to clear it out.
14. Type **training** in the search area.
15. Select the checkbox next to the **TRAINING_DETAILS** table.
16. Click **Add to cart**.
17. Click the **x** at the end of the search area to clear it out.

### Virtualize Customer Tables

1. Type **customer** in search area.
2. Select the checkbox next to the following **Customer** tables:
   
   * CUSTOMER
   * CUSTOMER_LOYALTY

3. Click **Add to cart**.
4. Click **View cart (12)**.

## Virtualize and Publish

Before we virtualize the tables and publish them to the **Governance** catalog we need to make a few changes to the virtualized table schema names instead of using the not so user friendly schema names that are automatically generated by the Watson Query service.

1. Click the **Virtutalized data** radio button in the **Assign to** section.

> **Note** - The **Publish to** section has automatically checked **Catalog** to publish to and has the **Governance** catalog automatically selected. This is due to the governance settings we set in the previous section.

## 1. Change Banking Tables Schema

1. Go to the first table in the list with a **Source schema** of **BANKING**.
2. Click the **X** to clear out the default **Schema** assigned.
3. Type **BANKING** (in uppercase) in the **Schema** name area and select **Create BANKING**.
4. Repeat the following steps for all the tables that have a **Source schema** of **BANKING**:
	
	* Click the **X** to clear out the default **Schema** assigned.
	* Select the **drop down arrow v** in the **Schema** name area.
	* Select the **BANKING** schema from the list of schema names.

## 2. Change Employee Tables Schema

1. Go to the first table in the list with a **Source schema** of **EMPLOYEE**.
2. Click the **X** to clear out the default **Schema** assigned.
3. Type **EMPLOYEE** (in uppercase) in the **Schema** name area and select **Create EMPLOYEE**.
4. Repeat the following steps for all the tables that have a **Source schema** of **EMPLOYEE**:
	
	* Click the **X** to clear out the default **Schema** assigned.
	* Select the **drop down arrow v** in the **Schema** name area.
	* Select the **EMPLOYEE** schema from the list of schema names.

## 3. Change Customer Tables Schema

1. Go to the first table in the list with a **Source schema** of **CUSTOMER**.
2. Click the **X** to clear out the default **Schema** assigned.
3. Type **CUSTOMER** (in uppercase) in the **Schema** name area and select **Create CUSTOMER**.
4. Repeat the following steps for all the tables that have a **Source schema** of **CUSTOMER**:
	
	* Click the **X** to clear out the default **Schema** assigned.
	* Select the **drop down arrow v** in the **Schema** name area.
	* Select the **CUSTOMER** schema from the list of schema names.

## 4. Virtualize the Tables

> **Note** - Before you select the button to Virtualize the tables, make sure that all of the tables have the new schema names you just assigned! 

> Watson Query has a mind of its own. Sometimes, for whatever reason, when you change the schema names, as I outline in the next section, Watson Query makes it look like the schema name has been changed, but when you select the **Virtualize** button, it is possible that one of the tables still has the old funky schema name assigned to it. Unfortunately, If that happens, there is no turning back or cancellation button. Therefore, you have to delete all the virtual tables one by one (no bulk delete option either...) and then go back to **Step 3** of this section and start the process all over again from selection to virtualization. It seems overkill, but trust me, it is important to our demo that it all be displayed correctly.

1. Click **Virtualize**.
2. Click **Confirm** but **do not** check the **Do not show this message again** checkbox.
    
	* Wait for all tables to be virtualized and published before proceeding to the next step. The **Virtualization Status** and **Publish Status** indicators for all 12 tables should have a **green** check mark next to them.
	* Also make sure that your schema changes are correct by scrolling down the list of tables and verifying that you have 3 tables with the BANKING schema, 2 tables with the CUSTOMER schema and 7 tables with the EMPLOYEE schema. 

3. Click **View virtualized data**.

There should be 12 virtualized tables in the **Virtualized data** section.

## 5. Grant User Role to Tables

1. Click the **Table** column header and sort the tables in ascending order.
2. Go to the **first table** in the list of virtualized tables.

	* Based on my experience on how Data Virtualization behaves, it should be the **CUSTOMER** or **CUSTOMER_LOYALTY** table since they were the last ones virtualized.

3. Click the **ellipses...** next to the table.
4. Click **Manage access**.
5. Select **Specific user**.
    
    * It should be selected as the default.

6. Select the **Roles** tab.
7. Click **Grant access**.
8. Select the **User** role.
9. Click **Add roles**.
10. Select the **Back** button.

Repeat steps 2-10 above for the remaining 11 virtualized tables. 

When you get to the 10th table in the list), select the **Items per page** control and click on 20 for the remaining 2 tables to show up in the list.

To verify you did not miss granting access to any tables:

1. Select **User management** from the Data Virtualization dropdown menu.
2. Click the **Roles** tab.

Make sure the **User** role has the number 12 listed in the **Granted access** column. 

Stay in the User Management section for the next task.a

## 5. Add CPD Business User Access

From the User Management section:

1. Click the **Users** tab.
2. Click **Grant access**.
3. Type in an email address = **cpd.business.user@gmail.com** 
4. Click the **User** role radio button.
5. Click **Create**.

> **Note** - It will take a couple of minutes (usually 1-2) for the user access to be assigned so be patient and wait until it completes!

## Validate Published Data Assets

We published the virtualized tables to the **Governance** catalog during the virtualization process so that any of the tables that contain sensitive information will be autonomously protected by the data protection rules defined. Data virtualization does some things automatically during publishing that need to be modified and verified. We will perform those steps in the following sections.

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Catalogs &gt; All catalog**.
3. Select the **Governance** catalog.

## 1. Update Data Virtualization Connection

Data virtualization automatically creates a connection to the Watson Query service in the **Governance** catalog when it publishes data assets to a governed catalog. However, the connection name is not very user friendly and is owned by a user named **unavailable**. We will change the name, description and owner in the following steps:

1. Click the **Filter by** dropdown.
2. Select **Connections**.
3. Click on the only **connection** in the data asset list.

 There should be one connection in the **Governance** catalog that is named **Data Virtualization_ea660a45-a34d-4961-afb9-39875a62e7b4** The connection name is always named "Data Virtualization" with the "Instance Id" (the value after the plus sign) of the Watson Query service it is associated with appended to the end. The instance id will be different for production and test.

4. Click the **Asset** tab.
5. Click **here** to edit the connection details.
6. Clear out the **Name**.
7. Enter a new Name = **Watson Query**.
8. Enter a Description = **Connection to the Watson Query data virtualization service in the Cloud Pak for Data Outcomes resource group in this cloud account.** (including the period at the end).
9. Click **Credentials** from the left side menu.
10. Select the **Authentication Method** and choose **API Key**.
11. Enter an API Key of:

    > Prod = UcBbBseZBsuE6ITZAHU5Suo7yf8LdwhkaKk22lHkxz2V

    > Test = syQkhcXhJMkvqrMQtfYZzU1y7Nf9rxirEcAmrYJovEBB

12. Check the box **Port is SSL-enabled**.
13. Click the **Test connection** button. 

    > The test should succeed. If not, go back and re-check all the entries to make sure you copied and pasted them correctly. When it does succeed you can proceed to the next step to create it.

14. Click **Save**.
15. Click the **Governance** cookie in the menu to get back to the main page of the catalog.

## 2. Validate Data Profiles

We need to ensure the 12 tables that were published have been profiled. This is especially important for the 3 tables that contain sensitive data; **MORTGAGE_APPLICANT, CUSTOMER and EMPLOYEE**. They have to have all their columns classified correctly because the data protection rules are triggered based on data class. If the columns that contain sensitive data are not classified correctly, like a US Social Security Number or Credit Card Number, the data protection rules will not recognize them as such and therefore they will not be masked.

From the **Assets** section of the catalog, verify that there are 12 tables. They should be sorted in alphabetical order by "schema.table name". Starting from the first table in the list, do the following:

1. Click on the **Name** of the first data asset in the list.

> **Note** - The first table should be the BANKING.MORTGAGE_APPLICANT table.

2. Click on the **Profile** tab.

> **Note** - You should see a profile created for every data asset. If not, click the **Create profile** button. The profile will take a while to create in the background so you do not have to wait for it to complete. Create the profile and move on to the next data asset in the list. If profiles continue to fail to be created, open up a support ticket because there is an issue with the Watson Knowledge Catalog data profiling job.

3. Click the **Governance** cookie in the menu to get back to the main page of the catalog to select the next table in the list.
4. Repeat steps 1-3 above for the remaining 11 tables.

## 3. Validate Sensitive Data Classes

From the data asset list we need to go back to the profile for the 3 tables that contain sensitive information and check their column classifications.

### MORTGAGE_APPLICANT

1. Click on the **BANKING.MORTGAGE_APPLICANT** data asset.
2. Click on the **Profile** tab.
3. Scroll to the **right**.

1. Click the classification dropdown on the **EDUCATION** column.
2. Select **View all**.
3. Type in **edu**.
4. Select **Education Status**.
5. Click **Add**.

1. Click the classification dropdown on the **EMPLOYMENT_STATUS** column.
2. Select **View all**.
3. Type in **emp**.
4. Select **Employment Status**.
5. Click **Add**.

Click the **Governance** cookie in the menu to get back to the main page of the catalog to process the next table.

### CUSTOMER

1. Click on the **CUSTOMER** data asset.
2. Click on the **Profile** tab.
3. Scroll to the **right**.

1. Click the classification dropdown on the **STATE_CODE** column.
2. Select **View all**.
3. Type in **state/**.
4. Select **State/Providence Code**.
5. Click **Add**.

1. Click the classification dropdown on the **POSTAL_CODE** column.
2. Select **View all**.
3. Type in **postal**.
4. Select **Postal Code**.
5. Click **Add**.

1. Click the classification dropdown on the **EDUCATION** column.
2. Select **View all**.
3. Type in **edu**.
4. Select **Education Status**.
5. Click **Add**.

1. Click the classification dropdown on the **LOCATION_CODE** column.
2. Select **View all**.
3. Type in **code**.
4. Select **Code**.
5. Click **Add**.

1. Click the classification dropdown on the **INCOME** column.
2. Select **View all**.
3. Type in **income**.
4. Select **Income**.
5. Click **Add**.

1. Click the classification dropdown on the **CREDIT_CARD_TYPE** column.
2. Select **View all**.
3. Type in **credit**.
4. Select **Credit Card Network**.
5. Click **Add**.

1. Click the classification dropdown on the **CREDIT_CARD_CVV** column.
2. Select **View all**.
3. Type in **credit**.
4. Select **Credit Card Validation Number**.
5. Click **Add**.

1. Click the classification dropdown on the **CREDIT_CARD_EXPIRY** column.
2. Select **View all**.
3. Type in **credit**.
4. Select **Credit Card Expiration Date**.
5. Click **Add**.

Click the **Governance** cookie in the menu to get back to the main page of the catalog to process the next table.

### EMPLOYEE

1. Click on the **EMPLOYEE** data asset.
2. Click on the **Profile** tab.

1. Click the classification dropdown on the **EMPLOYEE_CODE** column.
2. Select **Identifier**.
3. Click the classification dropdown on the **FIRST_NAME_MB** column.
4. Select **First Name**.

1. Click the classification dropdown on the **GENDER_CODE** column.
2. Select **View all**.
3. Type in **gender**.
4. Select **Gender**.
5. Click **Add**.

1. Click the classification dropdown on the **WORK_PHONE** column.
2. Select **View all**.
3. Type in **phone**.
4. Select **Phone Number**.
5. Click **Add**.

1. Click the classification dropdown on the **EXTENSION** column.
2. Select **View all**.
3. Type in **text**.
4. Select **Text**.
5. Click **Add**.

1. Click the classification dropdown on the **FAX** column.
2. Select **View all**.
3. Type in **phone**.
4. Select **Phone Number**.
5. Click **Add**.

1. Click the classification dropdown on the **COMMUTE_TIME** column.
2. Select **View all**.
3. Type in **quantity**.
4. Select **Quantity**.
5. Click **Add**.

## Configure Watson OpenScale and Studio

## 1. Create Outcomes Runbook Project

Everything is now in place to build out the **Business** catalog with the proper connections, data assets, associated metadata from the business glossary, and data protection rules in place to protect sensitive and personally identifiable information. We will build out the catalog using a project that was populated using **metadata import** and **metadata enrichment** features.

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Projects &gt; view all projects**.
3. Click **New project +**.
4. Click **Create a project from a sample file**.
5. Click **browse** to upload the project file.
6. Select the **Outcomes-Runbook-Project-CPDaaS.zip** file from your download location.
7. Enter a Name = **Outcomes Runbook**.
8. Enter a Description = **Administrative project used to configure and manage Cloud Pak for Data Outcomes.** (including the period at the end).
9. Click **Create**.

> You will see a dialog box with the message that the **Outcomes Runbook project is being created...**.

10. Click **View new project**.

> The project should create successfully and have 10 assets.

## Populate Business Catalog

Data Warehouse - Import the cloud object storage files that are published to the Business catalog.

## 1. Create Outcomes Catalog Project

Everything is now in place to build out the **Business** catalog with the proper connections, data assets, associated metadata from the business glossary, and data protection rules in place to protect sensitive and personally identifiable information. We will build out the catalog using a project that was populated using **metadata import** and **metadata enrichment** features.

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Projects &gt; view all projects**.
3. Click **New project +**.
4. Click **Create a project from a sample file**.
5. Click **browse** to upload the project file.
6. Select the **Outcomes-Catalog-Project-CPDaaS.zip** file from your download location.
7. Enter a Name = **Outcomes Catalog**.
8. Enter a Description = **Administrative project used to configure the Business catalog for Cloud Pak for Data Outcomes.** (including the period at the end).
9. Click **Create**.

> You will see a dialog box with the message that the **Business Catalog project is being created...**. 

10. Click **View new project**.

> The project should create successfully and have 47 data assets.

## Connection Metadata

Each connection in the project has been assigned a name, description, and tags so they will be carried over into the **Business** catalog when they are published. The table below contains this metadata in case of lose. This is for reference only.

|Connection|Description|Tags|Business Terms|
|----------|-----------|----|--------------|
|Amazon Object Storage|Amazon Cloud Object Storage bucket that contains data files used for analytics and AI.|Employee Warehouse|
|Cloud Object Storage|IBM Cloud Object Storage bucket that contains data files used for analytics and AI.|Employee Warehouse|
|Data Warehouse|Database that contains enterprise data needed by the business for analytics and AI projects.|Banking Customer Employee Mortgage Sensitive|Email Phone Number Credit Card Number Credit Card Expiration Date Credit Card Validation Number|
|Document Store|Data store that contains documents needed by the business for analytics and AI.|Employee|
|Third Party Data|Database that contains third party data needed by the business for analytics and AI.|Banking Customer Employee Mortgage|

## Data Asset Metadata

Each data asset in the project has been assigned a name, description, and tags so they will be carried over into the **Business** catalog when they are published. The table below contains this metadata in case of lose. This is for reference only.

|Data Asset                  |Description                            |Tags               |
|----------------------------|---------------------------------------|-------------------|
|CUSTOMER                    |Official and current Customer master.  |Customer Sensitive |
|CUSTOMER_ACTIVITY           |Customer stock trading transaction activity.|Customer      |
|CUSTOMER_ATTRITION          |Customer churn risk assessment.        |Customer           |
|CUSTOMER_LOYALTY            |Customers participating in the loyalty rewards program. Includes sales by quarter and customer satisfaction data.            |Customer           |
|CUSTOMER_OFFERS             |Special offers made to customers who are churn risks.|Customer|
|DEPARTMENT_LOOKUP           |Valid department codes and values.     |Employee           |
|EMPLOYEE                    |Official and current Employee master.  |Employee Sensitive Warehouse|
|EMPLOYEE\_EXPENSE_DETAIL    |Detailed employee expense transactions.|Employee           |
|EMPLOYEE\_EXPENSE_PLAN      |Yearly expense totals by month, organization and expense type.|Employee|
|EMPLOYEE_HISTORY            |Historical record of all employee position and manager changes.|Employee|
|EMPLOYEE_SUMMARY            |Historical record of employee salary changes and vacation and sick days taken throughout the year.|Employee|
|EMPLOYEE_SURVEY             |Anonymous historical record of employee survey submissions.|Employee|
|EMPLOYEE\_SURVEY_FINAL      |Final survey results compiled by employee for use by the data analytics team.|Employee|
|EMPLOYEE\_SURVEY_RESULTS    |Employee survey results compiled by organization, satisfaction index topic.|Employee|
|EMPLOYEE\_SURVEY_TARGETS    |Employee survey benchmarks and targets by year by topic.|Employee|
|EMPLOYEE\_SURVEY_TOPIC      |Employee survey topics in 29 different languages.|Employee|
|EXPENSE_GROUP               |Valid codes and values for expense groups.|Employee|
|EXPENSE_TYPE                |Expense types by group, unit and account.|Employee|
|EXPENSE_UNIT                |Valid expense unit codes and values.|Employee|
|GENDER_LOOKUP               |Valid gender codes and values.|Employee|
|MODELING_RECORDS            |Employee records used to perform AI to determine employee attrition.|Employee|
|MORTGAGE_APPLICANT          |Applicants that have applied for a mortgage who are potential customers.|Banking Mortgage Sensitive|
|MORTGAGE_APPLICATION        |Data entered on a mortgage application by a mortgage applicant.|Banking Mortgage|
|MORTGAGE_CANDIDATE          |Mortgage candidate information associated with a mortgage application.|Banking Mortgage|
|ORGANIZATION                |Valid organization codes and names and associated parent organizations.|Employee|
|POSITION_DEPARTMENT         |Association table combining all position data with department data.|Employee|
|POSITION_LOOKUP             |Valid codes and values for employee positions.|Employee|
|POSITION_SUMMARY            |Historical record of positions held by employees.|Employee|
|RANKING                     |Valid codes and values of employee performance rankings.|Employee|
|RANKING_RESULTS             |Historical record of employee rankings by year.|Employee|
|RECRUITMENT                 |A historical record of all employee recruitment activity with relationships to the Organization, Branch and Position hired into.|Employee|
|RECRUITMENT_MEDIUM          |Valid codes and values for the types of medium used to recruit employees.|Employee|
|RECRUITMENT_TYPE            |Valid codes and values for valid recruitment methods used to recruit employees.|Employee|
|SATISFACTION_INDEX          |Valid codes, values, ranges and description of employee satisfaction results.|Employee|
|SUCCESSION_DETAILS          |Historical record of employee succession transactions.|Employee|
|SUCCESSOR_STATUS            |Valid codes and values for employee successor status.|Employee|
|TERMINATION_LOOKUP          |Valid codes and values for employment termination.|Employee|
|TRAINING                    |Detailed course information available for employee training.|Employee|
|TRAINING_DETAILS            |All training courses taken by date and their associated expense codes.|Employee|
|WAREHOUSE_SHIFTS            |Shift information for all departments within the warehouse.|Employee Warehouse|
|WAREHOUSE_STAFF             |All employee that work as staff members in the warehouse processing orders.|Employee Warehouse|
|WAREHOUSE_STAFFING          |The days of the week and maximum shifts that staff members are available to work warehouse shifts.|Employee Warehouse|

## Publish Assets to Business Catalog

We will now publish the 47 data assets from the project to the **Business Catalog**. Every asset in the project should have the metadata outline in the tables above already applied; tags and descriptions.

> **Note** - Watson Knowledge Catalog has a strange, and frankly speaking, random means of publishing bulk items form a project to a catalog. They do not always appear in the order you have chosen to publish.

The assets will be published in a specific order, as stated below, so that the **Recently Added** category in the catalog gets populated properly with the tables that are searched for, and that are used in the analytics project, appearing as the most recent tables added to the catalog. This helps during the demo so end users can see and find the tables we want them too fast and easily. 

## 1. Publish Connections

We will publish the data connections first, in the order they are listed in the instructions below. This will put them at the very bottom of the recently added list and in the order they are used in our demos and not interfere with the primary data assets we want to appear first in that category.

> **Note** - Tags are case sensitive so all the tags need to be entered in mixed case as instructed. This is to ensure consistency as they appear in the catalog and there are not duplicate tags created in the tags selection dropdown in the catalog that are the same but in different cases.

From the **Assets** tab using the **Asset type** filter on the left:

1. Click **Data access**.
2. Click **Connection**.

### Publish Amazon Object Storage

1. Click the checkbox next to **Amazon Object Storage**.
2. Click **Publish to catalog**.
3. Select the **Business** catalog as the Target.
4. Click in the **tags** area.
5. Enter **Employee** and click the **+** sign.
6. Enter **Warehouse** and click the **+** sign.
7. Click **Publish**.

### Publish Cloud Object Storage

1. Uncheck the checkbox next to **Amazon Object Storage**.
2. Click the checkbox next to **Cloud Object Storage**.
3. Click **Publish to catalog**.
4. Select the **Business** catalog as the Target.
5. Click in the **tags** area.
6. Enter **Employee** and click the **+** sign.
7. Enter **Warehouse** and click the **+** sign.
8. Click **Publish**.

### Publish Document Store

1. Uncheck the checkbox next to **Cloud Object Storage**.
2. Click the checkbox next to **Document Store**.
3. Click **Publish to catalog**.
4. Select the **Business** catalog as the Target.
5. Click in the **tags** area.
6. Enter **Employee** and click the **+** sign.
7. Click **Publish**.

### Publish Third Party Data

1. Uncheck the checkbox next to **Document Store**.
2. Click the checkbox next to **Third Party Data**.
3. Click **Publish to catalog**.
4. Select the **Business** catalog as the Target.
5. Click in the **tags** area.
6. Enter **Banking** and click the **+** sign.
7. Enter **Customer** and click the **+** sign.
8. Enter **Employee** and click the **+** sign.
9. Enter **Mortgage** and click the **+** sign.
10. Click **Publish**.

### Publish Data Warehouse

1. Uncheck the checkbox next to **Third Party Data**.
2. Click the checkbox next to **Data Warehouse**.
3. Click **Publish to catalog**.
4. Select the **Business** catalog as the Target.
5. Click in the **tags** area.
6. Enter **Banking** and click the **+** sign.
7. Enter **Customer** and click the **+** sign.
8. Enter **Employee** and click the **+** sign.
9. Enter **Mortgage** and click the **+** sign.
10. Enter **Sensitive** and click the **+** sign.
11. Click **Publish**.
12. Uncheck the checkbox next to **Data Warehouse**.

## 2. Publish Data Assets

We will publish the majority of the data assets (36) in one bulk operation and then selectively publish a handful (6) of tables that we want to appear as the most recent in the **Recently added** featured assets category in the **Business** catalog. These data assets are key to our demo scripts and several of them contain sensitive data, so they need to be published selectively and last so that they appear first in that category list and are at the forefront and easily found and accessed.

### Bulk Publish

From the **Assets** tab using the **Asset type** filter on the left:

1. Click **Data**.
2. Click **Data asset**.
3. Click **Name** column to sort in ascending order (arrow pointing up).
4. Click **Items per page** at the bottom of the list.
5. Select **100**.
6. Click the high level checkbox next to **Name** to select all data assets.
7. Find the following tables in the list and **uncheck** them:

	* CUSTOMER
    * CUSTOMER_LOYALTY
    * EMPLOYEE
    * WAREHOUSE_STAFF
	* WAREHOUSE_STAFF_AVAILABILITY
    * WAREHOUSE_SHIFTS

8. Click **Publish to catalog**.
9. Select the **Business** catalog.
10. Click **Publish**.

     > Wait for the **"36 assets have been successfully published to the catalog."** message to clear before proceeding.

11. Click the **refresh** button on the toolbar.

    > This will reset all the checkboxes in the list in preparation for the next step.

Publish the following tables one at a time in the order listed.

### Publish CUSTOMER_LOYALTY

1. Click the checkbox next to the **CUSTOMER_LOYALTY** data asset.
2. Click **Publish to catalog**.
3. Select the **Business** catalog.
4. Click **Publish**.

     > Wait for the **"1 asset has been successfully published to the catalog."** message to clear before proceeding.

5. Uncheck the checkbox next to **CUSTOMER_LOYALTY**.

### Publish CUSTOMER

1. Click the checkbox next to the **CUSTOMER** data asset.
2. Click **Publish to catalog**.
3. Select the **Business** catalog.
4. Click **Publish**.

     > Wait for the **"1 asset has been successfully published to the catalog."** message to clear before proceeding.

5. Uncheck the checkbox next to **CUSTOMER**.

### Publish EMPLOYEE

1. Click the checkbox next to the **EMPLOYEE** data asset.
2. Click **Publish to catalog**.
3. Select the **Business** catalog.
4. Click **Publish**.

     > Wait for the **"1 asset has been successfully published to the catalog."** message to clear before proceeding.

5. Uncheck the checkbox next to **EMPLOYEE**.

### Publish WAREHOUSE_SHIFTS

1. Click the checkbox next to the **WAREHOUSE_SHIFTS** data asset.
2. Click **Publish to catalog**.
3. Select the **Business** catalog.
4. Click **Publish**.

    > Wait for the **"1 asset has been successfully published to the catalog."** message to clear before proceeding.

5. Uncheck the checkbox next to **WAREHOUSE_SHIFTS**.

### Publish WAREHOUSE_STAFFING

1. Click the **WAREHOUSE_STAFFING** data asset.
2. Click **Publish to catalog**.
3. Select the **Business** catalog.
4. Click **Publish**.

     > Wait for the **"1 asset has been successfully published to the catalog."** message to clear before proceeding.

5. Uncheck the checkbox next to **WAREHOUSE_STAFFING**.

### Publish WAREHOUSE_STAFF

1. Click the **WAREHOUSE_STAFF** data asset.
2. Click **Publish to catalog**.
3. Select the **Business** catalog.
4. Click **Publish**.

    > Wait for the **"1 asset has been successfully published to the catalog."** message to clear before proceeding.

5. Uncheck the checkbox next to **WAREHOUSE_STAFF**.

## Add Metadata to Business Catalog Assets

In this section we add additional metadata like tags, relationships, governance artifacts, and reviews to cataloged assets so users can better understand data content and to contribute to the knowledge base of the search engine to make it for users to find what they are looking for.

1. Go to the Cloud Pak for Data **navigation** menu.
2. Select **Catalog &gt; Business**.

## 1. Add Metadata to Data Warehouse

1. Scroll down the list of data assets.
2. Find the **Data Warehouse** connection in the list.
3. Click the **Data Warehouse** connection.

### Add Governance Artifacts

From the **Overview** tab:
    
1. Go to the **Governance Artifacts** section.
2. Click the **plus sign +** next to **Business terms**.
3. From the business term list, select the checkbox next to the following business terms:
    
    * Email Address
    * Credit Card Expiration Date
    * Credit Card Number
    * Credit Card Validation Number
    * Phone Number
    * US Phone Number
    * US Social Security Number

3. Click **Add**.

### Add Related Assets

1. Go to the **Related assets** section.
2. Click the **Add asset +** button.
3. Select **Contains**.
4. Select **Next**.
5. Select the following tables:
  
    * CUSTOMER_ACTIVITY
    * CUSTOMER_ATTRITION
    * CUSTOMER_OFFERS
    * DEPARTMENT_LOOKUP
    * EMPLOYEE_EXPENSE_DETAIL
    * EMPLOYEE_EXPENSE_PLAN
    * EMPLOYEE_HISTORY
    * EMPLOYEE_SUMMARY
    * EXPENSE_GROUP
    * EXPENSE_TYPE
    * EXPENSE_UNIT
    * GENDER_LOOKUP
    * MODELING_RECORDS
    * ORGANIZATION
    * POSITION_DEPARTMENT
    * POSITION_LOOKUP
    * POSITION_SUMMARY
    * RANKING
    * RANKING_RESULTS
    * SATISFACTION_INDEX

6. Click **Add**.
7. Click the **Add asset +** button.
8. Select **Contains**.
9. Select **Next**.
10. Select the following tables:

    * SUCCESSION_DETAILS
    * SUCCESSOR_STATUS
    * TRAINING
    * TRAINING_DETAILS
    * TERMINATION_LOOKUP

11. Click **Add**.

### Add a Review

1. Click the **Review** tab.
2. Give a **5 Star** rating by clicking the fifth star to the far right.
3. Click in the review **text area**.
4. Copy and paste the following text between the quotes below in the review text area **without** the quotes and **include** the period.

    "Contains all governed, trusted and quality data approved and published by the data governance team to use for analytical and AI projects. Some of the data is sensitive but data protection rules are in place to govern it."

1. Click **Submit**.
2. Click the **Business** bread crumb on the toolbar to get back to the list.

## 2. Add Metadata to EMPLOYEE

1. Scroll **down** the asset list.
2. Find the **EMPLOYEE** data asset.
3. Click the **EMPLOYEE** data asset.

### Add Governance Artifacts

From the **Overview** tab:

1. Go to the **Governance Artifacts** section.
2. Click the **plus sign +** next to **Business terms**.
3. From the business term list, select the checkbox next to the following business terms:
    
    * Email Address
    * Phone Number
    * US Social Security Number

4. Click **Add**.
5. Click the **plus sign +** next to **Classifications**.
6. From the Classification list, select the checkbox next to the following classifications:

    * Personal Information
    * Personally Identifiable Information
    * Sensitive Personal Information

7. Click **Add**.

### Add Related Assets

1. Go to the **Related assets** section.
2. Click the **Add asset +** button.
3. Select **Is related to**.
4. Select **Next**.
5. Select the **EMPLOYEE_EXPENSE\_DETAIL** data asset.
6. Select the **EMPLOYEE_HISTORY** data asset.
7. Select the **EMPLOYEE_SUMMARY** data asset.
8. Select the **MODELING_RECORDS** data asset.
9. Select the **POSITION_DEPARTMENT** data asset.
10. Select the **RANKING_RESULTS** data asset.
11. Select the **TRAINING_DETAIL** data asset.
12. Click **Add**.
13. Click the **Add asset +** button.
14. Select **Is contained in**.
15. Select **Next**.
16. Enter **data** in the search area.
17. Select the **Data Warehouse** connection.
18. Click **Add**.

### Update Data Classifications

1. Click the **Profile** tab.

In this section we update all columns that have incorrect or unassigned data classes for the **EMPLOYEE** data asset. You will go to every column in the table below and do the following:

1. Click the **data class** dropdown arrow in the data class area.
2. Click **View all** from the data class list.

Update the data classes for the columns in the table below as described. 

After each update:

1. Click **Add**.

|Column Name|Search Criteria|Data Class|
|-------------|----------|-------------|
|FIRST_NAME\_MB|first|First Name|
|GENDER_CODE|gender|Gender|
|WORK_PHONE|phone|Phone Number|
|EXTENSION|text|Text|
|GENDER_CODE|gender|Gender|
|FAX|phone|Phone Number|
|COMMUTE_TIME|qu|Quantity|

### Assign Business Terms

1. Click the **Asset** tab.

In this section we assign a business term to every column in the **EMPLOYEE** data asset. You will go to every column in the data asset and do the following:

1. Click the **Column information** icon that looks like an **eye** on the column.
2. Click the **edit** icon next to Business terms.

Assign each column to the corresponding business term using the table below. 

After each assignment:

1. Click **Apply**.
2. Click **Close**.

|Column Name|Search Criteria|Business Term|  
|-------------|----------|-------------|
|EMPLOYEE_CODE|employee|Employee Code|
|FIRST_NAME|first|First Name|
|FIRST_NAME_MB|first|First Name|
|LAST_NAME|last|Last Name|
|LAST_NAME_MB|last|Last Name|
|DATE_HIRED|hired|Data Hired|
|TERMINATION_DATE|termination|Termination Date|
|TERMINATION_CODE|termination|Termination Code|
|BIRTH_DATE|birth|Data of Birth|
|GENDER_CODE|gender|Gender|
|WORK_PHONE|work|Work Phone|
|EXTENSION|extension|Extension|
|FAX|phone|Phone Number|
|EMAIL|email|Email Address|
|SSN|social|US Social Security Number|
|COMMUTE_TIME|commute|Commute Time|

### Add a Review

1. Click the **Review** tab.
2. Give a **5 Star** rating by clicking the fifth star to the far right.
3. Click in the review **text area**.
4. Copy and paste the following text between the quotes below in the review text area **without** the quotes and **include** the period.

	"Contains governed and trusted employee data to use for business analytical projects. This is the full company employee record master. It contains sensitive and personal information, but the data governance office has defined data protection rules to govern that information."

5. Click **Submit**.
6. Click the **Business** bread crumb on the toolbar to get back to the list.

## 3. Add Metadata to CUSTOMER

1. Scroll down the list of data assets.
2. Find the **CUSTOMER** data asset in the list.
3. Click the **CUSTOMER** data asset.

### Add Governance Artifacts

From the **Overview** tab:
    
1. Go to the **Governance Artifacts** section.
2. Click the **plus sign +** next to **Business terms**.
3. From the business term list, select the checkbox next to the following business terms:

    * Credit Card Number
    * Credit Card Expiration Date
    * Credit Card Validation Number

3. Click **Add**.
4. Click the **plus sign +** next to **Classifications**.
5. From the Classification list, select the checkbox next to the following classifications:

    * Personal Information
    * Personally Identifiable Information
    * Sensitive Personal Information

6. Click **Add**.

### Add Related Assets

1. Go to the **Related assets** section.
1. Click the **Add asset +** button.
2. Select **Is related to**.
3. Select **Next**.
4. Select the **CUSTOMER_ACTIVITY** data asset.
5. Select the **CUSTOMER_ATTRITION** data asset.
6. Select the **CUSTOMER_LOYALTY** data asset.
7. Select the **CUSTOMER_OFFERS** data asset.
8. Click **Add**.
9. Click the **Add asset +** button.
10. Select **Is contained in**.
11. Select **Next**.
12. Enter **data** in the search area.
13. Select the **Data Warehouse** connection.
14. Select the **Third Party Date** connection.
15. Click **Add**.

### Update Data Classifications

1. Click the **Profile** tab.

In this section we update all columns that have incorrect or unassigned data classes for the **CUSTOMER** data asset. You will go to every column in the table below and do the following:

1. Click the **data class** dropdown arrow in the data class area.
2. Click **View all** from the data class list.

Update the data classes for the columns in the table below as outlined. 

After each update:

1. Click **Add**.

|Column Name|Search Criteria|Data Class|
|-------------|----------|-------------|
|CUSTOMER_ID|ident|Identifier|
|STATE_CODE|state/|State/Province Code|
|POSTAL_CODE|post|Postal Code|
|EDUCATION|edu|Education Status|
|LOCATION|code|Code|
|INCOME|qu|Quantity|
|CREDIT_CARD_TYPE|credit|Credit Card Network|
|CREDIT_CARD_CVV|credit|Credit Card Validation Number|
|CREDIT_CARD_EXPIRY|credit|Credit Card Expiration Date|

### Assign Business Terms

1. Click the **Asset** tab.

In this section we assign a business term to every column in the **CUSTOMER** data asset. You will go to every column in the data asset and do the following:

1. Click the 	**Column information** icon that looks like an **eye** on the column.
2. Click the **edit** icon next to Business terms.

Assign each column to the corresponding business term using the table below. 

After each assignment:

1. Click **Apply**.
2. Click **Close**.

|Column Name|Search Criteria|Business Term|
|-------------|----------|-------------|
|CUSTOMER_ID|customer|Customer ID|
|LOYALTY_NBR|loyal|Loyalty Number|
|FIRST_NAME|first|First Name|
|LAST_NAME|last|Last Name|
|CUSTOMER_NAME|name|Person Name|
|COUNTRY|country|Country Name|
|STATE_NAME|state|State / Province Name|
|STATE_CODE|state|State / Province Code|
|CITY|city|City|
|LATITUDE|lat|Latitude|
|LONGITUDE|long|Longitude|
|POSTAL_CODE|post|Postal Code|
|GENDER|gender|Gender|
|EDUCATION|education|Education Status|
|LOCATION_CODE|location|Location Code|
|INCOME|income|Income|
|MARITAL_STATUS|marital|Legal Marital / Civil Status|
|CREDIT_CARD_TYPE|credit|Credit Card Network|
|CREDIT_CARD_NUMBER|credit|Credit Card Number|
|CREDIT_CARD_CVV|credit|Credit Card Validation Number|
|CREDIT_CARD_EXPIRY|credit|Credit Card Expiration Date|
|CREDIT_CARD_CVV|credit|Credit Card Validation Number|
|CREDIT_CARD_EXPIRY|credit|Credit Card Expiration Date|

### Add a Review

1. Click the **Review** tab.
2. Give a **5 Star** rating by clicking the fifth star to the far right.
3. Click in the review **text area**.
4. Copy and paste the following text between the quotes below in the review text area **without** the quotes and **include** the period.

    "Contains governed and trusted customer data to use for business analytical projects. This is the full company customer record master. It contains sensitive and personal information, but the data governance office has defined data protection rules to govern that information."

1. Click **Submit**.
2. Click the **Business** bread crumb on the toolbar to get back to the list.

## 4. Add Metadata to CUSTOMER_LOYALTY

1. Scroll down the list of data assets.
2. Find the **CUSTOMER_LOYALTY** data asset in the list.
3. Click the **CUSTOMER_LOYALTY** data asset.

### Add Governance Artifacts

From the **Overview** tab:
    
1. Go to the **Governance Artifacts** section.
2. Click the **plus sign +** next to **Business terms**.
3. Enter **satisfaction** into the search area.
4. From the business term list, select the checkbox next to the following business terms:

    * Satisfaction Rating
    * Satisfaction Reason

5. Click **Add**.
6. Click the **plus sign +** next to **Classifications**.
7. From the Classification list, select the checkbox next to the following classification:
    
    * Confidential

6. Click **Add**.

### Add Related Assets

1. Go to the **Related assets** section.
2. Click the **Add asset+** button.
3. Select **Is contained in**.
4. Select **Next**.
5. Enter **third** in the search area.
6. Select the **Third Party Data** connection.
7. Click **Add**.

### Update Data Classifications

1. Click the **Profile** tab.

In this section we update all columns that have incorrect or unassigned data classes for the **CUSTOMER_LOYALTY** data asset. You will go to every column in the table below and do the following:

1. Click the **data class** dropdown arrow in the data class area.
2. Click **View all** from the data class list.

Update the data classes for the columns in the table below as outlined. 

After each update:

1. Click **Add**.

|Column Name|Search Criteria|Data Class|
|-------------|----------|-------------|
|LOYALTY_NBR|ident|Identifier|
|ORDER_YEAR|year|Year|
|QUARTER|qu|Quarter|
|MONTHS_AS_MEMBER|qu|Quantity|
|LOYALTY_STATUS|code|Code|
|PRODUCT_LINE|text|Text|
|COUPON_RESPONSE|text|Text|
|COUPON_COUNT|qu|Quantity|
|QUANTITY_SOLD|qu|Quantity|
|UNIT_SALES_PRICE|curr|Currency|
|UNIT_COST|curr|Currency|
|REVENUE|qu|Quantity|
|PLANNED_REVENUE|qu|Quantity|
|SHIPPING_DAYS|qu|Quantity|
|CUSTOMER_LIFETIME_VALUE|qu|Quantity|
|LOYALTY_COUNT|qu|Quantity|
|BACKORDER_STATUS|code|Code|
|SATISFACTION_RATING|code|Code|
|SATISFACTION_REASON|text|Text|

### Assign Business Terms

1. Click the **Asset** tab.

In this section we assign a business term to every column in the **CUSTOMER** data asset. You will go to every column in the data asset and do the following:

1. Click the 	**Column information** icon that looks like an **eye** on the column.
2. Click the **edit** icon next to Business terms.

Assign each column to the corresponding business term using the table below. 

After each assignment:

1. Click **Apply**.
2. Click **Close**.

|Column Name|Search Criteria|Business Term|
|-------------|----------|-------------|
|LOYALTY_NBR|loyal|Loyalty Number|
|ORDER_YEAR|year|Order Year|
|QUARTER|loyal|Loyalty Quarter|
|MONTHS_AS_MEMBER|months|Months As Member|
|LOYALTY_STATUS|loyal|Loyalty Status|
|PRODUCT_LINE|prod|Product Line|
|COUPON_RESPONSE|coupon|Coupon Response|
|COUPON_COUNT|coupon|Coupon Count|
|QUANTITY_SOLD|quantity|Quantity Sold|
|UNIT_SALES_PRICE|unit|Unit Sale Price|
|UNIT_COST|unit|Unit Cost|
|REVENUE|rev|Revenue|
|PLANNED_REVENUE|rev|Planned Revenue|
|SHIPPING_DAYS|ship|Shipping Days|
|CUSTOMER_LIFETIME_VALUE|life|Customer Lifetime Value|
|LOYALTY_COUNT|loyal|Loyalty Count|
|BACKORDER_STATUS|back|Backorder Status|
|SATISFACTION_RATING|sat|Satisfaction Rating|
|SATISFACTION_REASON|sat|Satisfaction Reason|

### Add a Review

1. Click the **Review** tab.
2. Give a **5 Star** rating by clicking the fifth star to the far right.
3. Click in the review **text area**.
4. Copy and paste the following text between the quotes below in the review text area **without** the quotes and **include** the period.

    "Contains governed and trusted customer sales, order, revenue, and satisfaction data to use for business analytical projects. This is the complete year to year, by quarter information for all customers that is used by the executive management team."

1. Click **Submit**.
2. Click the **Business** bread crumb on the toolbar to get back to the list.

## 5. Add Metadata to WAREHOUSE_STAFF

1. Scroll down the list of data assets.
2. Find the **WAREHOUSE_STAFF** data asset in the list.
3. Click the **WAREHOUSE_STAFF** data asset.

### Add Governance Artifacts

From the **Overview** tab:
    
1. Go to the **Governance Artifacts** section.
2. Click the **plus sign +** next to **Business terms**.
3. From the business term list, select the checkbox next to the following business terms:
    
    * Pay Rate
    * Skill Set
    * Skill Experience
    * Skill Rating

3. Click **Add**.
4. Click the **plus sign +** next to **Classifications**.
5. From the Classification list, select the checkbox next to the following classifications:
    
    * Confidential

6. Click **Add**.

### Add Related Assets

1. Go to the **Related assets** section.
1. Click the **Add asset +** button.
2. Select **Is related to**.
3. Select **Next**.
4. Select the **WAREHOUSE_SHIFTS** data asset.
5. Select the **WAREHOUSE_STAFFING** data asset.
6. Click **Add**.
7. Click the **Add asset +** button.
8. Select **Is contained in**.
9. Enter **ware** in the search area.
10. Select **Next**.
11. Select the **Cloud Object Storage** connection.
12. Select the **Amazon Object Storage** connection.
13. Click **Add**.

### Update Data Classifications

1. Click the **Profile** tab.

In this section we update all columns that have incorrect or unassigned data classes for the **WAREHOUSE_STAFF** data asset. You will go to every column in the table below and do the following:

1. Click the **data class** dropdown arrow in the data class area.
2. Click **View all** from the data class list.

Update the data classes for the columns in the table below as outlined. 

After each update:

1. Click **Add**.

|Column Name|Search Criteria|Data Class|
|-------------|----------|-------------|
|EMPLOYEE_CODE|ident|Identifier|
|PAY_RATE|code|Code|
|SKILL_SET|text|Text|
|DAYS_OFF|text|Text|
|SKILL_EXPERIENCE|qu|Quantity|
|SKILL_RATING|code|Code|

### Assign Business Terms

1. Click the **Asset** tab.

In this section we assign a business term to every column in the **CUSTOMER** data asset. You will go to every column in the data asset and do the following:

1. Click the **Column information** icon that looks like an **eye** on the column.
2. Click the **edit** icon next to Business terms.

Assign each column to the corresponding business term using the table below. 

After each assignment:

1. Click **Apply**.
2. Click **Close**.

|Column Name|Search Criteria|Business Term|
|-------------|----------|-------------|
|EMPLOYEE_CODE|employee|Employee Code|
|PAY_RATE|pay|Pay Rate|
|SKILL_SET|skill|Skill Set|
|DAYS_OFF|days|Days Off|
|SKILL_EXPERIENCE|skill|Skill Experience|
|SKILL_RATING|skill|Skill Rating|

### Add a Review

1. Click the **Review** tab.
2. Give a **4 Star** rating by clicking the fifth star to the far right.
3. Click in the review **text area**.
4. Copy and paste the following text between the quotes below in the review text area **without** the quotes and **include** the period.

    "Contains up to date information about all employees who are staff members that work in the warehouse processing customer orders. It can be used for analytics and AI but it does not contain the employee's name so it must be combined with the EMPLOYEE data."

1. Click **Submit**.
2. Click the **Business** bread crumb on the toolbar to get back to the list.

## 6. Add Metadata to WAREHOUSE_STAFFING

1. Scroll down the list of data assets.
2. Find the **WAREHOUSE_STAFFING** data asset in the list.
3. Click the **WAREHOUSE_STAFFING** data asset.

### Add Governance Artifacts

From the **Overview** tab:
    
1. Go to the **Governance Artifacts** section.
2. Click the **plus sign +** next to **Business terms**.
3. From the business term list, select the checkbox next to the following business terms:
    
    * Day
    * Max Shifts

3. Click **Add**.

### Add Related Assets

1. Go to the **Related assets** section.
1. Click the **Add asset +** button.
2. Select **Is related to**.
3. Select **Next**.
4. Select the **WAREHOUSE_SHIFTS** data asset.
5. Click **Add**.
6. Click the **Add asset +** button.
7. Select **Is contained in**.
8. Enter **ware** in the search area.
9. Select **Next**.
10. Select the **Cloud Object Storage** connection.
11. Select the **Amazon Object Storage** connection.
12. Click **Add**.

### Update Data Classifications

1. Click the **Profile** tab.

In this section we update all columns that have incorrect or unassigned data classes for the **WAREHOUSE_STAFFING** data asset. You will go to every column in the table below and do the following:

1. Click the **data class** dropdown arrow in the data class area.
2. Click **View all** from the data class list.

Update the data classes for the columns in the table below as outlined. 

After each update:

1. Click **Add**.

|Column Name|Search Criteria|Data Class|
|-------------|----------|-------------|
|EMPLOYEE_CODE|ident|Identifier|
|DAY|day|Day|
|MAX_SHIFTS|qu|Quantity|

### Assign Business Terms

1. Click the **Asset** tab.

In this section we assign a business term to every column in the **CUSTOMER** data asset. You will go to every column in the data asset and do the following:

1. Click the **Column information** icon that looks like an **eye** on the column.
2. Click the **edit** icon next to Business terms.

Assign each column to the corresponding business term using the table below. 

After each assignment:

1. Click **Apply**.
2. Click **Close**.

|Column Name|Search Criteria|Business Term|
|-------------|----------|-------------|
|EMPLOYEE_CODE|employee|Employee Code|
|DAY|day|Day|
|MAX_SHIFTS|max|Max Shifts|

### Add a Review

1. Click the **Review** tab.
2. Give a **4 Star** rating by clicking the fifth star to the far right.
3. Click in the review **text area**.
4. Copy and paste the following text between the quotes below in the review text area **without** the quotes and **include** the period.

    "Contains accurate availability; days of the week and maximum number of shifts, for employees who are staff members in the warehouse to optimize the schedule needed to maximize customer order fulfillment. However, it only contains the employee code so it must be combined with the EMPLOYEE data asset."

1. Click **Submit**.
2. Click the **Business** bread crumb on the toolbar to get back to the list.

## 7. Add Metadata to WAREHOUSE_SHIFTS

1. Scroll down the list of data assets.
2. Find the **WAREHOUSE_SHIFTS** data asset in the list.
3. Click the **WAREHOUSE_SHIFTS** data asset.

### Add Governance Artifacts

From the **Overview** tab:
    
1. Go to the **Governance Artifacts** section.
2. Click the **plus sign +** next to **Business terms**.
3. From the business term list, select the checkbox next to the following business terms:
    
    * Shift Day
    * Shift Start Hour
    * Shift End Hour
    * Shift Duration
    * Skill Required

3. Click **Add**.

### Add Related Assets

1. Go to the **Related assets** section.
2. Click the **Add asset +** button.
3. Select **Is contained in**.
4. Select **Next**.
5. Select the **Cloud Object Storage** connection.
6. Select the **Amazon Object Storage** connection.
7. Click **Add**.

### Update Data Classifications

1. Click the **Profile** tab.

In this section we update all columns that have incorrect or unassigned data classes for the **WAREHOUSE_SHIFTS** data asset. You will go to every column in the table below and do the following:

1. Click the **data class** dropdown arrow in the data class area.
2. Click **View all** from the data class list.

Update the data classes for the columns in the table below as outlined. 

After each update:

1. Click **Add**.

|Column Name|Search Criteria|Data Class|
|-------------|----------|-------------|
|SHIFT_ID|ident|Identifier|
|DEPARTMENT|text|Text|
|SHIFT_DAY|day|Day|
|SHIFT_START_HOUR|hour|Hour|
|SHIFT_END_HOUR|hour|Hour|
|SHIFT_MIN_HOURS|qu|Quantity|
|SHIFT_MAX_HOURS|qu|Quantity|
|SKILL_REQUIRED|text|Text|
|SHIFT_DURATION|qu|Quantity|
|DAY_CODE|code|Code|
|SHIFT_START_WEEK|date|Date|
|SHIFT_START_DATE|date|Date|
|SHIFT_END_DATE|date|Date|

### Assign Business Terms

1. Click the **Asset** tab.

In this section we assign a business term to every column in the **CUSTOMER** data asset. You will go to every column in the data asset and do the following:

1. Click the **Column information** icon that looks like an **eye** on the column.
2. Click the **edit** icon next to Business terms.

Assign each column to the corresponding business term using the table below. 

After each assignment:

1. Click **Apply**.
2. Click **Close**.

|Column Name|Search Criteria|Business Term|
|-------------|----------|-------------|
|SHIFT_ID|ident|Shift Identifier|
|DEPARTMENT|depart|Department|
|SHIFT_DAY|day|Shift Day|
|SHIFT_START_HOUR|hour|Shift Start Hour|
|SHIFT_END_HOUR|hour|Shift End Hour|
|SHIFT_MIN_HOURS|min|Shift Minimum Hours|
|SHIFT_MAX_HOURS|max|Shift Max Hours|
|SKILL_REQUIRED|skill|Skill Requirement|
|SHIFT_DURATION|skill|Skill Experience|
|DAY_CODE|code|Day Code|
|SHIFT_START_WEEK|shift|Shift Start Week|
|SHIFT_START_DATE|shift|Shift Start Date|
|SHIFT_END_DATE|shift|Shift End Date|

### Add a Review

1. Click the **Review** tab.
2. Give a **4 Star** rating by clicking the fifth star to the far right.
3. Click in the review **text area**.
4. Copy and paste the following text between the quotes below in the review text area **without** the quotes and **include** the period.

    "Contains valid and current shift information needed to optimize the best staffing schedule to maximize customer order fulfillment. However, it is only useful for analysis when combined with the EMPLOYEE, WAREHOUSE_STAFF and WAREHOUSE_STAFFING data assets."

1. Click **Submit**.
2. Click the **Business** bread crumb on the toolbar to get back to the list.

## 8. Add Metadata to MORTGAGE_APPLICANT

1. Scroll **down** the asset list.
2. Find the **MORTGAGE_APPLICANT** data asset in the list.
3. Click the **MORTGAGE_APPLICANT** data asset.

### Add Governance Artifacts

From the **Overview** tab:
    
1. Go to the **Governance Artifacts** section.
2. Click the **plus sign +** next to **Business terms**.
3. From the business term list, select the checkbox next to the following business terms:
    * Email Address
    * US Phone Number
    * US Social Security Number
4. Click **Add**.
5. Click the **plus sign +** next to **Classifications**.
6. From the Classification list, select the checkbox next to the following classifications:

    * Personal Information
    * Personally Identifiable Information
    * Sensitive Personal Information

7. Click **Add**.

### Add Related Assets

1. Go to the **Related assets** section.
2. Click the **Add asset +** button.
3. Select **Is related to**.
4. Select **Next**.
5. Enter **mortgage** in the search area.
6. Select the **MORTGAGE_APPLICATION** data asset.
7. Select the **MORTGAGE_CANDIDATE** data asset.
8. Click **Add**.
9. Click the **Add asset +** button.
10. Select **Is contained in**.
11. Enter **data** in the search area.
12. Select **Next**.
13. Select the **Data Warehouse** connection.
14. Click **Add**.

### Update Data Classifications

1. Click the **Profile** tab.

In this section we update all columns that have incorrect or unassigned data classes for the **MORTGAGE_APPLICANT** data asset. You will go to every column in the table below and do the following:

1. Click the **data class** dropdown arrow in the data class area.
2. Click **View all** from the data class list.

Update the data Classes for the columns in the table below as described. 

After each update:

1. Click **Add**.

|Column Name|Search Criteria|Data Class|
|-------------|----------|-------------|
|EDUCATION|edu|Education Status|
|EMPLOYMENT_STATUS|employ|Employment Status|

### Assign Business Terms

1. Click the **Asset** tab.

In this section we assign a business term to every column in the **MORTGAGE_APPLICANT** data asset. You will go to every column in the data asset and do the following:

1. Click the **Column information** icon that looks like an **eye** on the column.
2. Click the **edit** icon next to Business terms.

Assign each column to the corresponding business term using the table below. 

After each assignment:

1. Click **Apply**.
2. Click **Close**.

|Column Name|Search Criteria|Business Term|  
|-------------|----------|-------------|
|ID|id|Application ID|
|NAME|person|Person Name|
|STREET_ADDRESS|address|Address|
|CITY|city|City|
|STATE|state|US State Name|
|STATE_CODE|state|US State Code|
|ZIP_CODE|zip|US Zip Code|
|EMAIL_ADDRESS|email|Email Address|
|PHONE_NUMBER|phone|US Phone Number|
|GENDER|gender|Gender|
|SOCIAL_SECURITY\_NUMBER|social|US Social Security Number|
|EDUCATION|education|Education Status|
|EMPLOYMENT_STATUS|employment|Employment Status|
|MARITAL_STATUS|marital|Legal Marital / Civil Status|

### Add a Review

1. Click the **Review** tab.
2. Give a **5 Star** rating by clicking the fifth star (farthest start to the right).
3. Click inside the review **text area**.
4. Copy and paste the following text between the quotes below in the review text area **without** the quotes and **include** the period.

	"Contains governed and trusted data related to mortgage applicants to use for the mortgage default analytics project. It contains sensitive information but it is masked, with real data replaced with fictional by contextually correct data that will not affect analytical results."

5. Click **Submit**.
6. Click the **Business** bread crumb on the toolbar to get back to the list.

## 9. Add Metadata to MORTGAGE_APPLICATION

1. Scroll **down** the asset list.
2. Find the **MORTGAGE_APPLICATION** data asset in the list.
3. Click the **MORTGAGE_APPLICATION** data asset.

### Add Governance Artifacts

From the **Overview** tab:
    
1. Go to the **Governance Artifacts** section.
2. Click the **plus sign +** next to **Classifications**.
3. From the Classification list, select the checkbox next to the following classifications:
    
    * Confidential

4. Click **Add**.

### Add Related Assets

1. Go to the **Related assets** section.
2. Click the **Add asset +** button.
3. Select **Is related to**.
4. Select **Next**.
5. Enter **mortgage** in the search area.
5. Select the **MORTGAGE_CANDIDATE** data asset.
6. Click **Add**.
7. Click the **Add asset +** button.
8. Select **Is contained in**.
9. Select **Next**.
10. Enter **data** in the search area.
11. Select the **Data Warehouse** connection.
12. Click **Add**.

### Update Data Classifications

1. Click the **Profile** tab.

In this section we update all columns that have incorrect or unassigned data classes for the **MORTGAGE_APPLICATION** data asset. You will go to every column in the table below and do the following:

1. Click the **data class** dropdown arrow in the data class area.
2. Click **View all** from the data class list.

Update the data classes for the columns in the table below as described. 

After each update:

1. Click **Add**.

|Column Name|Search Criteria|Data Class|
|-------------|----------|-------------|
|INCOME|qu|Income|
|RESIDENCE|text|Residence|
|YRS_AT\_CURRENT\_ADDRESS|qu|Quantity|
|YRS_WITH\_CURRENT\_EMPLOYER|qu|Quantity|
|NUMBER_OF\_CARDS|qu|Quantity|
|CREDITCARD_DEBT|qu|Quantity|
|LOAN_AMOUNT|qu|Quantity|
|LOANS|qu|Quantity|
|SALEPRICE|qu|Quantity|
|LOCATION|code|Code|

### Assign Business Terms

1. Click the **Asset** tab.

In this section we assign a business term to every column in the **MORTGAGE_APPLICATION** data asset. You will go to every column in the data asset and do the following:

1. Click the **Column information** icon that looks like an **eye** on the column.
2. Click the **edit** icon next to Business terms.

Assign each column to the corresponding business term using the table below. 

After each assignment:

1. Click **Apply**.
2. Click **Close**.

|Column Name|Search Criteria|Business Term|
|-------------|----------|-------------|
|ID|id|Applicant ID|
|INCOME|income|Income|
|APPLIEDONLINE|applied|Applied Online|
|RESIDENCE|reside|Residence|
|YRS_AT\_CURRENT\_ADDRESS|years at|Years At Current Address|
|YRS_WITH\_CURRENT\_EMPLOYER|years with|Years With Current Employer|
|NUMBER_OF\_CARDS|number of|Number of Cards|
|CREDITCARD_DEBT|credit|Credit Card Debt|
|LOANS|loans|Number of Loans|
|LOAN_AMOUNT|amount|Mortgage Loan Amount|
|SALEPRICE|price|Property Sale Price|
|LOCATION|location|Location Code|

### Add a Review

1. Click the **Review** tab.
2. Give a **4 Star** rating by clicking the fourth star to the far right.
3. Click in the review **text area**.
4. Copy and paste the following text between the quotes below in the review text area **without** the quotes and **include** the period.

	"Contains information needed to perform accurate mortgage default analysis. However, for deeper and more accurate analysis, it could use more information related to the applicant, so it must be used in conjunction with the MORTGAGE_APPLICANT data."

5. Click **Submit**.
6. Click the **Business** bread crumb on the toolbar to return to the list.

## 10. Add Metadata to MORTGAGE_CANDIDATE

1. Scroll **down** the asset list.
2. Click **Show more**.
3. Find the **MORTGAGE_CANDIDATE** data asset in the list.
4. Click the **MORTGAGE_CANDIDATE** data asset.

### Add Related Assets

1. Go to the **Related assets** section.
2. Click the **Add asset +** button.
3. Select **Is contained in**.
4. Select **Next**.
5. Enter **third** in the search area.
6. Select the **Third Party Data** connection.
7. Click **Add**.

### Assign Business Terms

1. Click the **Asset** tab.

In this section we assign a business term to every column in the **MORTGAGE_CANDIDATE** data asset. You will go to every column in the data asset and do the following:

1. Click the **Column information** icon that looks like an **eye** on the column.
2. Click the **edit** icon next to Business terms.

Assign each column to the corresponding business term using the table below. 

After each assignment:

1. Click **Apply**.
2. Click **Close**.

|Column Name|Search Criteria|Business Term|
|-------------|----------|-------------|
|ID|id|Applicant ID|
|DEFAULT_CANDIDATE|default|Default Candidate|

1. Click the **Business** bread crumb on the toolbar to return to the list.

## 11. Add Metadata to Document Store

From the **Filter by** section:

1. Click the **Any asset type** filter dropdown.
2. Select **Connections**.
3. Click **Document Store** connection.

### Add Related Assets

1. Go to the **Related assets** section.
2. Click the **Add asset +** button.
3. Select **Contains**.
4. Select **Next**.
5. Enter **survey** in the search area.
6. Select **EMPLOYEE_SURVEY** data asset.
7. Select **EMPLOYEE_SURVEY_TOPIC** data asset.
8. Select **EMPLOYEE_SURVEY_FINAL** data asset.
9. Select **EMPLOYEE_SURVEY_RESULTS** data asset.
10. Select **EMPLOYEE_SURVEY_TARGETS** data asset.
11. Click **Add**.
12. Click the **back** button on your browser to go back to the list.

## 12. Add Metadata to Third Party Data

If not selected, from the **Filter by** section:

1. Click the **Any asset type** filter dropdown.
2. Select **Connections**.
3. Click **Third Party Data** connection.

### Add Related Assets

1. Go to the **Related assets** section.
2. Click the **Add asset +** button.
3. Select **Contains**.
4. Select **Next**.
5. Enter **recruit** in the search area.
6. Select **RECRUITMENT** data asset.
7. Select **RECRUITMENT_TYPE** data asset.
8. Select **RECRUITMENT_MEDIUM** data asset.
9. Click **Add**.

Click the **Business** bread crumb on the toolbar to return to the list.

Congratulations you have completed the Cloud Pak for Data Outcomes SaaS demo environment!
