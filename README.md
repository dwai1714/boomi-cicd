# Helper Tool for Boomi CICD

## Problem Statement

All operations on Boomi MDM should be done using Boomi APIs. Boomi APIs use XML files as datasource for its operations
When any object is changed it should be applied to an env specific Boomi Account (example DEV)
Since all operations on Boomi is done using XML files, the atomic changes can not be done using a python tool like Alembic
This tool mimicks Alemgic and can be used by teams that uses Boomi.
When any element such as Model or Source is created it should be created using a XML file.
But changes to this model or source is again done using another XML file which applies the changes
example:
Create a model, then add or delete one or multiple fields. This needs multiple API calls with different versions of the XML
The problem is when the dev code needs to be promoted to QA or Prod all the changes that is done on Dev should be
sequentially applied else there will be a mismatch of fields/versions between the two environments

## Business Logic
This tool has all the implementation of different Boomi API calls (Model, Repository, Source etc.).
All the API calls are in the resources directory
To use this tool you need to pip install boomi_cicd-0.1.0-py3-none-any.whl from the dist directory to your workspace
For simplicity’s sake create a versions directory in your project.
To create an atomic change file use the following command
```commandline
create-file  ~/roompot/mdm_infra/manage_actual_changes/versions your_file_name
```
This will create a version file with two methods
forward - This is where you should apply all your changes. You can chain function calls
example: create_repository, create_model
backward - This is where you should write a exactly opposite function so that if any exception occurs in
forward call this method is called which nullifies all the changes and keeps your environment intact.
You should have a file called changelog.json and this file keeps track of what has been applied in any environment
{
  "DEV": {1, "created_repo_1.py", 2, "updated_repo_1.py"},
  "QA": {},
  "PROD": {}
}
This file is only modified by pipeline and should not be touched by developers.

This code checks from changelog.json what are the files that were applied in the dev before and which file from
your versions directory has not been applied. For one feature branch only one file should be applied.

After certain cycles when it's time to move to higher environment like QA mdm_infra/manage_changes/promote.py
should be applied and this will make sure all the changes that were not applied to QA is applied one by one. If anything
fails it applies backward() and makes sure the env is clean


## Pipeline Logic
The pipeline code should call the following CLI command inside the shell script
```commandline
pipeline  path/to/versions/  path/to/changelog.json
```
Once this is successful, you should run the integration tests etc.
If the integration tests fail
```commandline
pipeline  path/to/versions/  path/to/changelog.json --rollback
```
This will roll back all the changes made if you hae created the backward function properly

## Manual Update
To do a manual update you can short circuit the pipeline (which is very risky) and should be used only when necessary
```commandline
manual_pipeline  file_name path/to/versions/
```
for manual rollback
```commandline
manual_pipeline  file_name path/to/versions/ --rollback
```

## Enviornment variables

* ENV - The environment (DEV, QA, PROD)
* LOG_LEVEL - Log level you want to set

## Prerequisites

The code has been extensively documented but to understand the code knowledge in following is a must

* Python
