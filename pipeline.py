import os
from pathlib import Path
from cicd import merge_to_master, promote

root_path = Path(__file__).parent.parent
print(root_path)
versions_path = f"{root_path}/mdm_infra/manage_actual_changes/versions"
changelog_path = f"{root_path}/mdm_infra/manage_actual_changes/"
environment = os.environ['ENV']
if __name__ == '__main__':
    if environment == "DEV":
        merge_to_master.apply_changes(versions_path, changelog_path)
    else:
        promote.apply_changes(versions_path, changelog_path)

"""pip install https://raw.githubusercontent.com/dwai1714/boomi_cicd/main/dist/boomi_cicd-0.1.0-py3-none-any.whl"""
