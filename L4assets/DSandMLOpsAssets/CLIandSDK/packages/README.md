This folder includes a set of python packages used to access Cloud Pak for Data (CPD) 
and Cloud Pak for Data as a Service (CPDaaS).

The package can be zipped into a file that can then be used in a notebook.
From the package folder, execute the following commmand to create the zip file:

`zip -r cpdalllibs.zip cpdalllibs`

- cpdalllibs: folder including all packages
- cpdalllibs/cpdlib: folder for CPD-specific functions
- cpdalllibs/cpdaaslib: folder for CPDaaS-specific functions
- cpdalllibs/commonlib: folder for functions common to both CPD and CPDaaS
- cpdalllibs/cpdlibfms.py: file to include all the functions related to CPD
