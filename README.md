# Outcomes-Projects
This repository contains a set of zip files used to setup the CP4D Outcomes environment.

It also contains the demo project zip files that are loaded by TUMS when a reservation is made.

#### `project-preload-input.json` file
This file identifies the available CP4D Outcomes demos. It is used to identify the project demo files.
If the files are more recent than the ones in TUMS, they are uploaded.

This file is also uploaded to TUMS if it is more recent than the on in TUMS.

When adding project demo files (.zip) to this directory, make sure to modify the json file last.
This way, we can't run into a situation where a demo is identified but no projects zip files
are available in TUMS.

