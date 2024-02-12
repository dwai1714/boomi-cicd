# mdm infra

## Configs

* All configs are managed config.toml

## Business Logic

All operations on Boomi MDM should be done using Boomi APIs. Boomi APIs use XML files as datasource for its operations
When any object is changed it should be applied to an env specific Boomi Account (example DEV)
When a code is merged to master it will change the DEV Boomi account
mdm_infra/manage_changes/merge_to_master.py is applied when any code is merged to master.
changelog.json keeps track of what file has been applied in a json format like
{
  "DEV": {1, "created_repo_1.py", 2, "updated_repo_1.py"},
  "QA": {},
  "PROD": {}
}
This file is only modified by pipeline and should not be touched by developers.

This code checks from changelog.json what are the files that were applied in the dev before and which file from
mdm_infra/manage_changes/versions has not been applied. Not that for one feature branch only one file should be applied.
Each developer when applying this change should create a file like version_x.py (it should be something more meaningful
name such as added_new_repository.py)
Each file should have two methods forward() and backward(). forward should apply the changes that the developer is
expecting to do and there should be an exactly opposite atomic function to revert the change in backward.
mdm_infra/manage_changes/versions/version1.py.sample
mdm_infra/manage_changes/versions/version2.py.sample
gives an example of how the files should be written

After certain cycles when it's time to move to higher environment like QA mdm_infra/manage_changes/promote.py
should be applied and this will make sure all the changes that were not applied to QA is applied one by one. If anything
fails it applies backward() and makes sure the env is clean

The way to deal with Boomi APIs is through functions defined in files that are in mdm_infra/src folder
There is documentation in each file that defines what each function is doing.

## Pipeline Logic
#TODO


## Deployment

* Create a Virtual Environment
* Clone the code
* pip install -r requirements.txt

## Prerequisites

The code has been extensively documented but to understand the code knowledge in following is a must

* Python
