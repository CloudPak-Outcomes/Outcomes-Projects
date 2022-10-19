#!/bin/bash
#-------------------------------------------------------------------------------------------------#
#  NAME:     jnotebook_install-user.sh                                                            #
#                                                                                                 #
#  PURPOSE:  This program is designed to install the libraries that are needed to install Jupyter #
#            Notebook software on an Ubuntu Linux server.                                         #
#                                                                                                 #
#  USAGE:    1) Locate the following variable in the main() function of this file and assign it   #
#               the appropriate value:                                                            #
#                                                                                                 # 
#               virtualEnvDir                                                                     #
#                                                                                                 #
#            2) Log in as the Jupyter Notebook user and issue the following command from a Linux  #
#               terminal window:                                                                  #
#                                                                                                 #
#               ./jnotebook_install-user.sh                                                       #
#                                                                                                 #
#-------------------------------------------------------------------------------------------------#
#                      DISCLAIMER OF WARRANTIES AND LIMITATION OF LIABILITY                       #
#                                                                                                 #
#  (C) COPYRIGHT International Business Machines Corp. 2017, 2018, & 2022. All Rights Reserved    #
#  Licensed Materials - Property of IBM                                                           #
#                                                                                                 #
#  US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP   #
#  Schedule Contract with IBM Corp.                                                               #
#                                                                                                 #
#  The following source code ("Sample") is owned by International Business Machines Corporation   #
#  or one of its subsidiaries ("IBM") and is copyrighted and licensed, not sold. You may use,     #
#  copy, modify, and distribute the Sample in any form without payment to IBM, for the purpose of #
#  assisting you with the installation of Db2 on a Ubuntu Linux server.                           #
#                                                                                                 #
#  The Sample code is provided to you on an "AS IS" basis, without warranty of any kind. IBM      #
#  HEREBY EXPRESSLY DISCLAIMS ALL WARRANTIES, EITHER EXPRESS OR IMPLIED, INCLUDING, BUT NOT       #
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.    #
#  Some jurisdictions do not allow for the exclusion or limitation of implied warranties, so the  #
#  above limitations or exclusions may not apply to you. IBM shall not be liable for any damages  #
#  you suffer as a result of using, copying, modifying or distributing the Sample, even if IBM    #
#  has been advised of the possibility of such damages.                                           #
#-------------------------------------------------------------------------------------------------#
#  HISTORY: 02AUG2022 - Initial Coding                                           Roger E. Sanders #
#-------------------------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------------------#
#  NAME:        init_log_file()                                                                   #
#                                                                                                 #
#  PURPOSE:     This function writes the appropriate header information to the Jupyter Notebook   #
#               installation script log file (jnotebook_install-user.log).                        #
#                                                                                                 #
#  PARAMETERS:  $1 - Log file name                                                                #
#                                                                                                 #
#  RETURNS:     None                                                                              #
#-------------------------------------------------------------------------------------------------#
function init_log_file
{
    # Create A New Log File And Write The Appropriate Header Information To It
    echo "#--------------------------------------------------------------------#"  > ${1} 2>&1
    echo "#  NAME:      jnotebook_install-user.log                             #" >> ${1} 2>&1
    echo "#  CREATED:   ${timeStamp}                                    #" >> ${1} 2>&1
    echo "#                                                                    #" >> ${1} 2>&1
    echo "#  CONTENTS:  Log data produced by jnotebook_setup-user.sh           #" >> ${1} 2>&1
    echo "#--------------------------------------------------------------------#" >> ${1} 2>&1
    echo "" >> ${1} 2>&1

    # Change Permissions On The Log File So Anyone Can Access It
    chmod 777 ${1}
}


#-------------------------------------------------------------------------------------------------#
#  NAME:        install_jupyter_notebook()                                                        #
#                                                                                                 #
#  PURPOSE:     This function installs the Jupyter Notebook, along with libraries needed to work  #
#               with IBM Db2 (on Ubuntu Linux).                                                   #
#                                                                                                 #
#  PARAMETERS:  $1 - Log file name                                                                #
#               $2 - Python virtual environment location                                          #
#               $3 - User home directory                                                          #
#                                                                                                 #
#  RETURNS:     TRUE  (1) - Packages and libraries needed were installed                          #
#               FALSE (0) - One or more packages or libraries were not installed                  #
#-------------------------------------------------------------------------------------------------#
function install_jupyter_notebook
{
    # Define All Local Variables Used
    local returnCode=${returnCode:=0}            # Function Return Code
    local errorFlag=${errorFlag:=0}              # Error Encountered Flag
    local outputMsg=${outputMsg:=''}             # Command Output Message Text
    local virtualEnvDir=${virtualEnvDir:=''}     # Python Virtual Environment Location
    local cfgFileName=${cfgFileName:=''}         # Python Configuration File Name
    local searchStr=${searchStr:=''}             # Python Configuration File Search String
    local replaceStr=${replaceStr:=''}           # Python Configuration File Replace String
                    
    # Initialize The Appropriate Memory Variables
    returnCode=${FALSE}
    errorFlag=${FALSE}
    virtualEnvDir=${2}
    cfgFileName="${3}/.jupyter/jupyter_notebook_config.py"
    searchStr="# c.NotebookApp.use_redirect_file = True"
    replaceStr="c.NotebookApp.use_redirect_file = False"   
      
    # Move To The Jupyter Notebook Virtual Environment Directory
    cd ${virtualEnvDir}

    # Create A Python-Jupyter Notebook Virtual Environment (Named "notebook_env")
    echo "Creating a Python-Jupyter Notebook virtual environment." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(virtualenv notebook_env 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not create a Python-Jupyter Notebook virtual environment."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Activate The Python-Jupyter Notebook Virtual Environment Just Created
    echo "Activating the Python-Jupyter Notebook virtual environment." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(source notebook_env/bin/activate 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not activate a Python-Jupyter Notebook virtual environment."
        errorFlag=${TRUE}
    fi
    echo ""

    # Install Jupyter Notebook In The Python-Jupyter Notebook Virtual Environment Created Earlier
    echo "Installing the Jupyter Notebook package in the virtual environment." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(python3 -m pip install jupyter 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install jupyter."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}
    
    # If A Jupyter Notebook Default Configuration File Exists, Delete It
    if [ -e ${cfgFileName} ]; then
        echo "Removing the file \"${cfgFileName}\"." | tee -a ${logFile}
        echo "" >> ${1}
        outputMsg=$(rm -r ${cfgFileName} 2>&1)
        echo "${outputMsg}" >> ${1} 2>&1
        if [[ ${outputMsg} =~ "E:" ]]; then
            echo "ERROR: Could not remove file \"${cfgFileName}\"."
            errorFlag=${TRUE}
            returnCode=${FALSE}
            return ${returnCode} 
        fi 
        echo ""      
    fi

    # Generate A Jupyter Notebook Default Configuration File
    echo "Generating the default Jupyter Notebook configuration file." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(jupyter notebook --generate-config 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not generate the default Jupyter Notebook configuration file."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # If The Jupyter Notebook Default Configuration File Was Created Successfully, Modify It
    if [ -e ${cfgFileName} ]; then
        echo "Updating the file \"${cfgFileName}\"." | tee -a ${logFile}
        echo "" >> ${1}
        outputMsg=$(sed -i "s/${searchStr}/${replaceStr}/" ${cfgFileName} 2>&1)
        echo "${outputMsg}" >> ${1} 2>&1
        if [[ ${outputMsg} =~ "E:" ]]; then
            echo "ERROR: Could not update file \"${cfgFileName}\"."
            errorFlag=${TRUE}
            returnCode=${FALSE}
            return ${returnCode} 
        fi 
        echo ""      
    fi

    # Install The PyHamcrest Library In The Python-Jupyter Notebook Virtual Environment
    echo "Installing the PyHamcrest libary in the virtual environment." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(python3 -m pip install PyHamcrest 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install ibm_db."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}
    
    # Install The IBM_DB Library In The Python-Jupyter Notebook Virtual Environment
    echo "Installing the ibm_db libary in the virtual environment." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(python3 -m pip install ibm_db 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install ibm_db."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Write An Appropriate Message To The Log File
    if [[ ${errorFlag} -eq ${TRUE} ]]; then
        echo "Problem(s) encountered. Refer to the file \"${1}\" for more information."
        returnCode=${FALSE}
    else
        date >> ${1} 2>&1
        echo "Finished installing Jupyter Notebook." | tee -a ${1}
        echo "" | tee -a ${1}
        returnCode=${TRUE}
    fi

    # Return The Appropriate Value To The Calling Function
    return ${returnCode}
}


#=================================================================================================#
#  NAME:        main()                                                                            #
#                                                                                                 #
#  PURPOSE:     This is the main body of the script.                                              #
#                                                                                                 #
#  PARAMETERS:  $1 - Script key word                                                              #
#               $2 - Option                                                                       #
#                                                                                                 #
#  RETURNS:     0 - The script executed successfully                                              #
#               1 - The script did NOT execute successfully                                       #
#=================================================================================================#

# Define All Variables Used
TRUE=${TRUE:=1}                                  # Boolean TRUE
FALSE=${FALSE:=0}                                # Boolean FALSE

currentDir=${currentDir:=''}                     # Current Working Directory
userDir=${userDir:=''}                           # User Home Directory
profileFile=${profileFile:=''}                   # User Profile File Name
logFile=${logFile:=''}                           # Log File Name
virtualEnvDir=${virtualEnvDir:=''}               # Jupyter Notebook Virtual Environment Directory
timeStamp=${timeStamp:=''}                       # Current Date And Time Value

# Initialize The Appropriate Memory Variables
currentDir=$(pwd)
userDir=${HOME}
profileFile="${HOME}/.bashrc"
logFile="${currentDir}/jnotebook_install-user.log"
virtualEnvDir="${HOME}/JNotebook"
timeStamp=$(date '+%m-%d-%Y:%H-%M-%S')

# Clear The Screen
clear

# Create A Log File In The Current Directory And Write Header Information To It
init_log_file ${logFile}

# Display A "Setting Up" Message
date >> ${logFile} 2>&1
echo "Installing the Jupyter Notebook software. Please wait ..." | tee -a ${logFile}
echo "" | tee -a ${logFile}

# Add The Location Of The Scripts "pip", "pip3", And "pip3.10", Which Are Installed In The User's
# ".local/bin" Directory To The PATH Environment Variable
export PATH="$PATH:${HOME}/.local/bin"
echo "" >> ${profileFile} 2>&1
echo "# set PATH so it includes user's private bin if it exists" >> ${profileFile} 2>&1
echo "if [ -d \"\$HOME/.local/bin\" ] ; then" >> ${profileFile} 2>&1
echo "    PATH=\"\$HOME/.local/bin:\$PATH\"" >> ${profileFile} 2>&1
echo "fi" >> ${profileFile} 2>&1
echo "" >> ${profileFile} 2>&1

# Install The Jupyter Notebook Libraries Needed For Ubuntu Linux
install_jupyter_notebook ${logFile} ${virtualEnvDir} ${userDir}
returnCode=$?
if [ ${returnCode} == ${FALSE} ]; then
    exit 1
fi

# Write The End Timestamp To the Log File
date >> ${logFile} 2>&1
echo "Done!" >> ${logFile}

# Display A "Finished" Message And Write A "Finished" Message To The Log File
echo "Done!"
echo "Refer to the file \"${logFile}\" for more information."
echo "" | tee -a ${logFile}
echo "To start Jupyter run the following commands:" | tee -a ${logFile}
echo "" | tee -a ${logFile}
echo "   source ${profileFile}" | tee -a ${logFile}
echo "   jupyter notebook" | tee -a ${logFile}
echo "" | tee -a ${logFile}

# Exit And Return Control To The Operating System
exit 0
