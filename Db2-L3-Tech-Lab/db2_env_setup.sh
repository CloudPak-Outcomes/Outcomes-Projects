#!/bin/bash
#-------------------------------------------------------------------------------------------------#
#  NAME:     db2_env_setup.sh                                                                     #
#                                                                                                 #
#  PURPOSE:  This program is designed to install the libraries that are needed to set up and run  #
#            IBM Db2 Community Edition, and then install the IBM Db2 software, on an Ubuntu       #
#            Linux server.                                                                        #
#                                                                                                 #
#  USAGE:    1) Locate the following variables in the main() function of this file and assign     #
#               them the appropriate values:                                                      #
#                                                                                                 # 
#               Db2CodeFile                                                                       #
#               Db2InstallDir                                                                     #
#                                                                                                 #
#            2) Log in as the root user and issue the following command from a Linux terminal     #
#               window (after moving to the directory where the .tar file and this file are       #
#               stored - typically the Downloads directory):                                      #
#                                                                                                 #
#               ./db2_env_setup.sh                                                                #
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
#  HISTORY: 16MAY2018 - Initial Coding                                           Roger E. Sanders #
#           07JUN2018 - Added Error Checking and Db2 Install           Shruthi Subbaiah Machimada #
#           02SEP2022 - Added Modifications for Installing Db2 V11.5             Roger E. Sanders #
#-------------------------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------------------#
#  NAME:        init_log_file()                                                                   #
#                                                                                                 #
#  PURPOSE:     This function writes the appropriate header information to the Db2 environment    #
#               setup up script log file (db2_env_setup.log).                                     #
#                                                                                                 #
#  PARAMETERS:  $1 - Log file name                                                                #
#                                                                                                 #
#  RETURNS:     None                                                                              #
#-------------------------------------------------------------------------------------------------#
function init_log_file
{
    # Create A New Log File And Write The Appropriate Header Information To It
    echo "#--------------------------------------------------------------------#"  > ${1} 2>&1
    echo "#  NAME:      db2_env_setup.log                                      #" >> ${1} 2>&1
    echo "#  CREATED:   ${timeStamp}                                    #" >> ${1} 2>&1
    echo "#                                                                    #" >> ${1} 2>&1
    echo "#  CONTENTS:  Log data produced by db2_env_setup.sh                  #" >> ${1} 2>&1
    echo "#--------------------------------------------------------------------#" >> ${1} 2>&1
    echo "" >> ${1} 2>&1

    # Change Permissions On The Log File So Anyone Can Access It
    chmod 777 ${1}
}


#-------------------------------------------------------------------------------------------------#
#  NAME:        install_db2_prereq_libraries()                                                    #
#                                                                                                 #
#  PURPOSE:     This function installs the Db2 prerequisite libraries needed (for Ubuntu Linux).  #
#                                                                                                 #
#  PARAMETERS:  $1 - Log file name                                                                #
#                                                                                                 #
#  RETURNS:     TRUE  (1) - Packages and libraries needed were installed                          #
#               FALSE (0) - One or more packages or libraries were not installed                  #
#-------------------------------------------------------------------------------------------------#
function install_db2_prereq_libraries
{
    # Define All Local Variables Used
    local returnCode=${returnCode:=0}            # Function Return Code
    local errorFlag=${errorFlag:=0}              # Error Encountered Flag
    local outputMsg=${outputMsg:=''}             # Command Output Message Text

    # Initialize The Appropriate Memory Variables
    returnCode=${FALSE}
    errorFlag=${FALSE}
 
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
   
    # Install The LIBAIO1 Linux Library
    echo "Installing the libaio1 package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install libaio1 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install libaio1."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The BINUTILS Linux Library
    echo "Installing the binutils package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install binutils 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1  
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install binutils."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The ZLIB1G Linux Library
    echo "Installing the zlib1g-dev package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install zlib1g-dev 2>&1) 
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install zlib1g-dev."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The LIBPAM0G:I386 Linux Library
    echo "Installing the libpam0g:i386 package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install libpam0g:i386 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install libpam0g:i386."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The LIBSTDC++:I386 Linux Library
    echo "Installing the libstdc++6:i386 package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install libstdc++6:i386 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install libstdc++6:i386."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The LIBLOGGER-SYSLOG-PERL Linux Library (For TSA MP)
    echo "Installing the liblogger-syslog-perl package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install liblogger-syslog-perl 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install liblogger-syslog-perl."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The KSH Linux Library (For TSA MP)
    echo "Installing the ksh package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install ksh 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install ksh."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The OPENSSH-SERVER Linux Library (For Data Server Manager)
    echo "Installing the openssh-server package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install openssh-server 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1 
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install openssh-server."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Install The NET-TOOLS Linux Library (For Data Server Manager)
    echo "Installing the net-tools package." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y install net-tools 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not install net-tools."
        errorFlag=${TRUE}
    fi
    echo "" >> ${1}
    echo "" | tee -a ${1}

    # Remove Packages That Are No Longer Needed
    echo "Removing dependency packages that are no longer needed." | tee -a ${1}
    echo "" >> ${1}
    outputMsg=$(apt-get -y autoremove 2>&1)
    echo "${outputMsg}" >> ${1} 2>&1
    if [[ ${outputMsg} =~ "E:" ]]; then
        echo "ERROR: Could not remove unused packages."
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

    # Write An Appropriate Message To The Log File
    if [[ ${errorFlag} -eq ${TRUE} ]]; then
        echo "Problem(s) encountered. Refer to the file \"${1}\" for more information."
        returnCode=${FALSE}
    else
        date >> ${1} 2>&1
        echo "Finished installing the libraries needed for Db2." | tee -a ${1}
        echo "" | tee -a ${1}
        returnCode=${TRUE}
    fi

    # Return The Appropriate Value To The Calling Function
    return ${returnCode}
}


#-------------------------------------------------------------------------------------------------#
#  NAME:        create_db2_users()                                                                #
#                                                                                                 #
#  PURPOSE:     This function creates the users and groups that are needed by Db2.                #
#                                                                                                 #
#  PARAMETERS:  $1 - Log file name                                                                #
#                                                                                                 #
#  RETURNS:     TRUE  (1) - The users and groups needed were successfully created                 #
#               FALSE (0) - The users and groups needed were not created                          #
#-------------------------------------------------------------------------------------------------#
function create_db2_users
{
    # Define All Local Variables Used
    local returnCode=${returnCode:=0}            # Function Return Code
    local errorFlag=${errorFlag:=0}              # Error Encountered Flag
    local outputMsg=${outputMsg:=''}             # Command Output Message Text

    # Initialize The Appropriate Memory Variables
    returnCode=${FALSE}
    errorFlag=${FALSE}
  
    # Create A User Group Named "db2iadm1"
    echo "Creating a group named \"db2iadm1\"." | tee -a ${1}
    outputMsg=$(groupadd db2iadm1 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ] && [ ${returnCode} != 9 ]; then
        echo "ERROR: Could not create the \"db2iadm1\" group." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        errorFlag=${TRUE} 
    fi
    echo "" | tee -a ${1}

    # Create A User Group Named "db2fadm1"
    echo "Creating a group named \"db2fadm1\"." | tee -a ${1}
    outputMsg=$(groupadd db2fadm1 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ] && [ ${returnCode} != 9 ]; then
        echo "ERROR: Could not create the \"db2fadm1\" group." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        errorFlag=${TRUE} 
    fi
    echo "" | tee -a ${1}

    # Create A User Named "db2inst1"
    echo "Creating a user named \"db2inst1\" (with a home directory)." | tee -a ${1}
    outputMsg=$(useradd -g db2iadm1 -m -d /home/db2inst1 -s /bin/bash db2inst1 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ] && [ ${returnCode} != 9 ]; then
        echo "ERROR: Could not create a user named \"db2inst1\"." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        errorFlag=${TRUE} 
    fi

    # Set The Password For The User Just Created To "ibmdb2"
    outputMsg=$(echo -e "ibmdb2\nibmdb2" | passwd db2inst1 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo "ERROR: Could not assign a password to the user named \"db2inst1\"." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        errorFlag=${TRUE}
    else
        echo "  Password for user \"db2inst1\" has been set to \"ibmdb2\"." | tee -a ${1}
    fi
    echo "" | tee -a ${1}

    # Create A User Named "db2fenc1"
    echo "Creating a user named \"db2fenc1\" (with a home directory)." | tee -a ${1}
    outputMsg=$(useradd -g db2fadm1 -m -d /home/db2fenc1 -s /bin/bash db2fenc1 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ] && [ ${returnCode} != 9 ]; then
        echo "ERROR: Could not create a user named \"db2fenc1\"." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        errorFlag=${TRUE} 
    fi

    # Set The Password For The User Just Created To "ibmdb2" 
    outputMsg=$(echo -e "ibmdb2\nibmdb2" | passwd db2fenc1 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo "ERROR: Could not create a user named \"db2fenc1\"." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        errorFlag=${TRUE} 
    else
        echo "  Password for user \"db2fenc1\" has been set to \"ibmdb2\"." | tee -a ${1}
    fi
    echo "" | tee -a ${1}

    # Write An Appropriate Message To The Log File
    if [[ ${errorFlag} -eq ${TRUE} ]]; then
        echo "Problem(s) encountered. Refer to the file \"${1}\" for more information."
        returnCode=${FALSE}
    else
        date >> ${1} 2>&1
        echo "Finished creating the users and groups needed for Db2." | tee -a ${1}
        echo "" | tee -a ${1}
        returnCode=${TRUE}
    fi

    # Return The Appropriate Value To The Calling Function
    return ${returnCode}
}


#-------------------------------------------------------------------------------------------------#
#  NAME:        install_db2()                                                                     #
#                                                                                                 #
#  PURPOSE:     This function installs the Db2 software and creates an instance and instance      #
#               user.                                                                             #
#                                                                                                 #
#  PARAMETERS:  $1 - Log file name                                                                #
#               $2 - Db2 tarball file name                                                        #
#               $3 - Db2 installation software location                                           #
#               $4 - Db2 software installation directory                                          #
#                                                                                                 #
#  RETURNS:     TRUE  (1) - Db2 was successfully installed                                        #
#               FALSE (0) - Db2 was not installed                                                 #
#-------------------------------------------------------------------------------------------------#
function install_db2
{
    # Define All Local Variables Used
    local returnCode=${returnCode:=0}            # Function Return Code
    local errorFlag=${errorFlag:=0}              # Error Encountered Flag
    local outputMsg=${outputMsg:=''}             # Command Output Message Text
    local fileName=${fileName:=''}               # Current Working File Name
    local softwareDir=${softwareDir:=''}         # Db2 Installation Software Location (Directory)
    local installDir=${installDir:=''}           # Db2 Software Installation Directory
    local TivoliDir=${TivoliDir:=''}             # Tivoli Installation Software Location (Directory)
    
    # Initialize The Appropriate Memory Variables
    returnCode=${FALSE}
    errorFlag=${FALSE}
    fileName=${2}
    softwareDir=${3}
    installDir="${4}/instance"
  
    # Untar The File That Contains The Db2 Software, Then Delete It
    if [ -f ${fileName} ]; then
        echo "Untaring the file \"${fileName}\"." | tee -a ${1}
        outputMsg=$(tar -xvf ${fileName} 2>&1)
        returnCode=$?
        if [ ${returnCode} != 0 ]; then
            echo "ERROR: Could not untar the file \"${fileName}\"." | tee -a ${1}
            echo "  ${outputMsg}" >> ${1} 2>&1
            returnCode=${FALSE}
            return ${returnCode} 
        else
            echo "${outputMsg}" >> ${1} 2>&1
            rm ${fileName} 2>&1
        fi
        echo "" | tee -a ${1}
    fi
    
    # Create A Software Storage Directory
    outputMsg=$(mkdir ${softwareDir} 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo "ERROR: Could not create the \"${softwareDir}\" directory." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        returnCode=${FALSE}
        return ${returnCode} 
    fi

    # Change The Permissions Of The Software Storage Directory So Anyone Can Access It
    outputMsg=$(chmod 777 ${softwareDir} 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo -e "ERROR: Could not "
        echo "change permissions for the \"${software_Dir}\" directory." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        returnCode=${FALSE}
        return ${returnCode} 
    fi

    # Move The Db2 Installation Software To The Software Storage Directory
    softwareDir="${softwareDir}/ibm-db2"
    outputMsg=$(mv server_dec ${softwareDir} 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo -e "ERROR: Could not "
        echo "move the Db2 software to the \"${softwareDir}\" directory." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        returnCode=${FALSE}
        return ${returnCode} 
    fi

    # Change The Permissions Of The Db2 Installation Software Storage Directory So Anyone
    # Can Access It
    outputMsg=$(chmod 777 -R ${softwareDir} 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo "ERROR: Could not change permissions for the \"${softwareDir}\" directory." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        returnCode=${FALSE}
        return ${returnCode} 
    fi

    # Move To The Directory Where The Db2 Installation Software Resides
    cd ${softwareDir}

    # Install The Db2 Software
    echo "Running the program \"db2_install\"." | tee -a ${1}
    outputMsg=$(echo -e "yes\nSERVER" | ./db2_install -y -f NOTSAMP 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo "ERROR: Problem encountered running the \"db2_install\" program." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        returnCode=${FALSE}
        return ${returnCode}
    fi
    echo "${outputMsg}" >> ${1} 2>&1
    echo "" | tee -a ${1}

    # Move To The Directory Where The Tivoli System Automation for Multiplatforms (SA MP) 
    # Software Resides
    TivoliDir="${softwareDir}/db2/linuxamd64/tsamp"
    cd ${TivoliDir}

    # Install The Tivoli SA MP Software
    echo "Running the program \"installSAM\"." | tee -a ${1}
    outputMsg=$(./installSAM --noprereqcheck --noliccheck --silent 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo "ERROR: Problem encountered running the \"installSAM\" program." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        returnCode=${FALSE}
        return ${returnCode}
    fi
    echo "${outputMsg}" >> ${1} 2>&1 
    echo "" | tee -a ${1}

    # Move To The Directory Where The Software Needed To Create A Db2 Instance Resides
    cd ${installDir}

    # Create A Db2 Instance
    echo "Creating a Db2 instance named \"db2inst1\"." | tee -a ${1}
    outputMsg=$(./db2icrt -u db2fenc1 db2inst1 2>&1)
    returnCode=$?
    if [ ${returnCode} != 0 ]; then
        echo "ERROR: Problem encountered creating a Db2 instance." | tee -a ${1}
        echo "  ${outputMsg}" >> ${1} 2>&1
        returnCode=${FALSE}
        return ${returnCode} 
    fi
    echo "${outputMsg}" >> ${1} 2>&1
    echo "" | tee -a ${1}

    # Return The Appropriate Value To The Calling Function
    returnCode=${TRUE}
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
logFile=${logFile:=''}                           # Log File Name
Db2CodeFile=${Db2CodeFile:=''}                   # Db2 Install Code TAR File Name
timeStamp=${timeStamp:=''}                       # Current Date And Time Value

# Initialize The Appropriate Memory Variables
currentDir=$(pwd)
logFile="${currentDir}/db2_env_setup.log"
Db2CodeFile="${currentDir}/v11.5.7_linuxx64_server_dec.tar"
Db2SoftwareDir="/home/Software"
Db2InstallDir="/opt/ibm/db2/V11.5/"
timeStamp=$(date '+%m-%d-%Y:%H-%M-%S')

# Clear The Screen
clear

# If The File Containing The Db2 Developer Edition Software Does Not Exist, Display An Error Message 
# And Return Control To The Operating System
if [ ! -f ${Db2CodeFile} ]; then
    echo "ERROR: Unable to locate the file \"${Db2CodeFile}\"." | tee -a ${logFile}
    echo "" | tee -a ${logFile}
    exit 1
fi

# Create A Log File In The Current Directory And Write Header Information To It
init_log_file ${logFile}

# Display A "Setting Up" Message
date >> ${logFile} 2>&1
echo "Setting up the Db2 prerequisite software needed. Please wait ..." | tee -a ${logFile}
echo "" | tee -a ${logFile}

# Install The Db2 Prerequisite Libraries Needed For Ubuntu Linux
install_db2_prereq_libraries ${logFile}
returnCode=$?
if [ ${returnCode} == ${FALSE} ]; then
    exit 1
fi

# Create The Users Needed For Db2
date >> ${logFile} 2>&1
echo "Creating the appropriate Db2 instance users and groups. Please wait ..." | tee -a ${logFile}
echo "" | tee -a ${logFile}
create_db2_users ${logFile}
returnCode=$?
if [ ${returnCode} == ${FALSE} ]; then
    exit 1
fi

# Install The Db2 Software And Create A Default Db2 Instance
date >> ${logFile} 2>&1
echo "Installing the Db2 software and creating a Db2 instance. Please wait ..." | tee -a ${logFile}
echo "" | tee -a ${logFile}
install_db2 ${logFile} ${Db2CodeFile} ${Db2SoftwareDir} ${Db2InstallDir}
returnCode=$?
if [ ${returnCode} == ${FALSE} ]; then
    exit 1
fi

# Write The End Timestamp To the Log File
date >> ${logFile} 2>&1
echo "Finished installing db2." >> ${logFile}

# Display A "Finished" Message And Write A "Finished" Message To The Log File
echo "Finished! Refer to the file \"${logFile}\" for more information."
echo ""

# Exit And Return Control To The Operating System
exit 0
