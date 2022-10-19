# Run as regular user (resanders)

#-------------------------------------------------------------------------------------------------#
# NOTE: As part of installation, run this command:                                                #
#     jupyter notebook --generate-config                                                          #
#                                                                                                 #
# This will create the following file:                                                            #
#     /home/resanders/.jupyter/jupyter_notebook_config.py                                         #
#                                                                                                 #
# Open this file and locate the following line:                                                   #
#     # c.NotebookApp.use_redirect_file = True                                                    #
#                                                                                                 #
# Change the line to this:                                                                        #
#     c.NotebookApp.use_redirect_file = False                                                     #
#                                                                                                 #
# This can be done programatically by executing the following code in a shell script:             #
#                                                                                                 #
# userDir=${HOME}                                                                                 #
# cfgFileName="${3}/.jupyter/jupyter_notebook_config.py"                                          #
# searchStr="# c.NotebookApp.use_redirect_file = True"                                            #
# replaceStr="c.NotebookApp.use_redirect_file = False"                                            #
# sed -i "s/${searchStr}/${replaceStr}/" ${cfgFileName}                                           #
#-------------------------------------------------------------------------------------------------#

jupyter notebook --notebook-dir=/home/resanders/JNotebook --ip='*' --port=8888 --allow-root
