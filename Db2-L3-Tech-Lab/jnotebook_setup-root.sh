#!/bin/bash
#-------------------------------------------------------------------------------------------------#
#  NAME:     jnotebook_setup-root.sh                                                              #
#                                                                                                 #
#  PURPOSE:  This program is designed to install the libraries that are needed to set up and run  #
#            Jupyter Notebook on an Ubuntu Linux server.                                          #
#                                                                                                 #
#  USAGE:    1) Locate the following variable in the main() function of this file and assign it   #
#               the appropriate value:                                                            #
#                                                                                                 # 
#               userDir                                                                           #
#                                                                                                 #
#            2) Log in as the root user and issue the following command from a Linux terminal     #
#               window:                                                                           #
#                                                                                                 #
#               ./jnotebook_setup-root.sh                                                         #
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
#               environment setup up script log file (jnotebook_setup-root.log).                  #
#                                                                                                 #
#  PARAMETERS:  $1 - Log file name                                                                #
#                                                                                                 #
#  RETURNS:     None                                                                              #
#-------------------------------------------------------------------------------------------------#
function init_log_file
{
    # Create A New Log File And Write The Appropriate Header Information To It
    echo "#--------------------------------------------------------------------#"  > ${1} 2>&1
    echo "#  NAME:      jnotebook_setup-root.log                               #" >> ${1} 2>&1
    echo "#  CREATED:   ${timeStamp}                                    #" >> ${1} 2>&1
    echo "#                                                                    #" >> ${1} 2>&1
    echo "#  CONTENTS:  Log data produced by jnotebook_setup-root.sh           #" >> ${1} 2>&1
    echo "#--------------------------------------------------------------------#" >> ${1} 2>&1
    echo "" >> ${1} 2>&1

    # Change Permissions On The Log File So Anyone Can Access It
    chmod 777 ${1}
}


#-------------------------------------------------------------------------------------------------#
#  NAME:        setup_jupyter_notebook_env()                                                      #
#                                                                                                 #
#  PURPOSE:     This function installs the libraries and packages needed to work wit Jupyter      #
#               Notebooks (on Ubuntu Linux).                                                      #
#                                                                                                 #
#  PARAMETERS:  $1 - Log file name                                                                #
#               $2 - Python Virtual Environment location                                          #
#                                                                                                 #
#  RETURNS:     TRUE  (1) - Packages and libraries needed were installed                          #
#               FALSE (0) - One or more packages or libraries were not installed                  #
#-------------------------------------------------------------------------------------------------#
function setup_jupyter_notebook_env
{
    # Define All Local Variables Used
    local returnCode=${returnCode:=0}            # Function Return Code
    local errorFlag=${errorFlag:=0}              # Error Encountered Flag
    local outputMsg=${outputMsg:=''}             # Command Output Message Text

    # Initialize The Appropriate Memory Variables
    returnCode=${FALSE}
    errorFlag=${FALSE}
    virtualEnvLocation=${2}
 
     # Remove All Packages Currently Installed On The System That Are Not Needed   
    echo "Uninstalling all packages currently installed that are not needed." | tee -a ${1}
    outputMsg=$(apt-get -y autoremove 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not uninstall unneeded packages."
        errorFlag=${TRUE} 
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}
 
    # Upgrade All Packages Installed On The System   
    echo "Installing newer versions of all packages currently installed." | tee -a ${1}
    echo "(This may take a few minutes)."
    outputMsg=$(apt-get -y upgrade 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not upgrade packages."
        errorFlag=${TRUE} 
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}
    
    # Fix Any Broken Packages Or Package Dependencies Found
    echo "Fixing any broken packages and package dependencies found." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get --fix-broken install)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not fix broken packages and package dependencies."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}
      
    # Generate A New List Of All Packages Installed On The System
    echo "Updating the installed package list." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get update 2>&1)
    echo "${outputMsg} Done." >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not update the installed package list."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}
    
    # Install The PYTHON3 Linux Package
    echo "Installing the python3 package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install python3 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install python3."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The PYTHON3-PIP Package Manager
    echo "Installing the python3-pip package manager." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install python3-pip 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1  
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install python3-pip."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}
    
    # Upgrade The PYTHON3-PIP (PIP3) Linux Library
    echo "Upgrading the pip3 package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(python3 -m pip install --upgrade pip 2>&1) 
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not upgrade pip3."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The VIRTUALENV Linux Package (Used For Creating Virtual
    # Python Environments)
    echo "Installing the virtualenv package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(python3 -m pip install virtualenv 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install virtualenv."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # If The Jupyter Notebook Virtual Environment Directory Desired Already Exists, Remove It
    if [ -e ${virtualEnvLocation} ]; then
        echo "Removing the directory \"${virtualEnvLocation}\"." | tee -a ${logFile}
        echo "" >> ${1}
        outputMsg=$(rm -r ${virtualEnvLocation} 2>&1)
        echo "${outputMsg}" >> ${1} 2>&1
        if [[ ${outputMsg} =~ "E:" ]]; then
            echo "ERROR: Could not remove directory \"${virtualEnvLocation}\"."
            errorFlag=${TRUE}
            returnCode=${FALSE}
            return ${returnCode} 
        fi 
        echo ""      
    fi

    # Create A Jupyter Notebook Virtual Environment Directory
    outputMsg=$(mkdir -m 777 ${virtualEnvLocation} 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo "ERROR: Could not create the \"${virtualEnvLocation}\" directory." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        returnCode=${FALSE}
        return ${returnCode} 
    fi

    # Change The Permissions Of The Jupyter Notebook Virtual Environment Directory So Anyone
    # Can Access It
    outputMsg=$(chmod 777 ${virtualEnvLocation} 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo -e "ERROR: Could not change "
        echo "permissions for the \"${virtualEnvLocation}\" directory." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        returnCode=${FALSE}
        return ${returnCode} 
    fi

    # Generate A New List Of All Packages Installed On The System
    echo "Updating the installed package list." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get update 2>&1)
    echo "${outputMsg} Done." >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not update the installed package list."
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
        echo "Finished installing the libraries needed for Jupyter Notebook." | tee -a ${1}
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
logFile=${logFile:=''}                           # Log File Name
virtualEnvDir=${virtualEnvDir:=''}               # Jupyter Notebook Virtual Environment Directory
timeStamp=${timeStamp:=''}                       # Current Date And Time Value
outputMsg=${outputMsg:=''}                       # Command Output Message Text

# Initialize The Appropriate Memory Variables
currentDir=$(pwd)
userDir="/home/resanders"
logFile="${currentDir}/jnotebook_setup-root.log"
virtualEnvDir="${userDir}/JNotebook"
timeStamp=$(date '+%m-%d-%Y:%H-%M-%S')

# Clear The Screen
clear

# Create A Log File In The Current Directory And Write Header Information To It
init_log_file ${logFile}

# Display A "Setting Up" Message
date >> ${logFile} 2>&1
echo "Installing the libraries and packages needed for Jupyter Notebook. Please wait ..." | tee -a ${logFile}
echo "" | tee -a ${logFile}

# Install The Libraries And Packages Needed For Jupyter Notebook
setup_jupyter_notebook_env ${logFile} ${virtualEnvDir}
returnCode=$?
if [ ${returnCode} == ${FALSE} ]; then
    exit 1
fi

# Write The End Timestamp To the Log File
date >> ${logFile} 2>&1
echo "Done!" >> ${logFile}

# Display A "Finished" Message And Write A "Finished" Message To The Log File
echo "Done!"
echo ""
echo "Refer to the file \"${logFile}\" for more information."
echo ""

# Exit And Return Control To The Operating System
exit 0
