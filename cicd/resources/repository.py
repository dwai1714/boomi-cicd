
from __future__ import annotations

import os
from typing import List

import requests
import xmltodict
from cicd.utils.log import get_logger
from cicd.utils.utility import get_config

logger = get_logger(__name__)


class Repository:
    """
    Args:
        repository_name : Repository name (required)
        config_file_path : toml file to get account_id etc for an env
        account_id : Boomi Account ID (defined in config file as env variable)
        cloud_id : Boomi Cloud ID (defined in config file as env variable)
        base64_credentials : Credentials (defined in config file as env variable)
        endpoint_url : Boomi End Point (defined in config file as env variable)
    """

    def __init__(
            self, repository_name: str, config_file_path: str, account_id: str = None,
            cloud_id: str = None, base64_credentials: str = None, endpoint_url: str = None,
            ):

        config = get_config(config_file_path)
        self.environment = os.environ['ENV']
        self.repository_name: str = repository_name
        self.model_ids = self.get_models_from_repo()
        if account_id is None:
            self.account_id = config[self.environment]['account_id']
        if cloud_id is None:
            self.cloud_id = config[self.environment]['cloud_id']
        if base64_credentials is None:
            self.base64_credentials = config[self.environment]['base64_credentials']
            self.headers = {
                'Authorization': 'Basic %s' % self.base64_credentials,
            }
        if endpoint_url is None:
            self.endpoint_url = config[self.environment]['endpoint_url']

    def create_repo(self):
        """
        Create  MDM Repo

        Returns:
            content of response (something like b'10a5e7bd-fc48-4ad4-ad1c-467f3cc43f51'
        """
        url = f'{self.endpoint_url}/{self.account_id}/clouds/{self.cloud_id}/repositories/{self.repository_name}/create'
        response = requests.post(url=url, headers=self.headers)
        if response.status_code != 200:
            logger.info(f'Response is {response.content}')
            raise RuntimeError('Response is not 200. Exiting')
        return response, response.content

    def get_repo_id(self):
        """
        get the ID of  MDM Repo

        Returns:
            matches name and returns repo id
        """
        url = f'{self.endpoint_url}/{self.account_id}/repositories'
        response = requests.get(url=url, headers=self.headers)
        dict_xml = (xmltodict.parse(response.content))
        repo_list = dict_xml['mdm:Repositories']['mdm:Repository']
        if isinstance(repo_list, list):
            for cell in repo_list:
                repo_id = cell['@id']
                repo_name = cell['@name']
                if repo_name == self.repository_name:
                    return repo_id
        elif isinstance(repo_list, dict):
            repo_id = repo_list['@id']
            repo_name = repo_list['@name']
            if repo_name == self.repository_name:
                return repo_id

    def delete_repo(self):
        """
        delete a MDM Repo

        Returns:
            content of response
        """
        repo_id = self.get_repo_id()
        url = f'{self.endpoint_url}/{self.account_id}/repositories/{repo_id}'
        response = requests.delete(url=url, headers=self.headers)
        if response.status_code != 200:
            logger.info(f'Response is {response.content}')
            raise RuntimeError('Response is not 200. Exiting')
        return response, response.content

    def get_models_from_repo(self) -> List[str]:
        """
        Get all model IDs present in the repository.

        Returns:
            A list of model IDs.
        """
        repo_id = self.get_repo_id()
        url = f'{self.endpoint_url}/{self.account_id}/repositories/{repo_id}'
        response = requests.get(url=url, headers=self.headers)
        dict_xml = xmltodict.parse(response.content)
        model_list = dict_xml.get('mdm:Repository', {}).get('mdm:Universe', [])
        if isinstance(model_list, dict):
            model_list = [model_list]
        return [model['@id'] for model in model_list]

    def delete_repo_with_models(self):
        """
        Undeploy all models associated with the repository and then delete the repository.

        Returns:
            Content of response
        """
        repo_id = self.get_repo_id()
        for model_id in self.model_ids:
            undeploy_url = f'{self.endpoint_url}/{self.account_id}/repositories/{repo_id}/universe/{model_id}'
            undeploy_response = requests.delete(url=undeploy_url, headers=self.headers)
            if undeploy_response.status_code != 200:
                logger.info(f'Undeploy response is {undeploy_response.content}')
                raise RuntimeError('Undeploy response is not 200. Exiting')

        delete_url = f'{self.endpoint_url}/{self.account_id}/repositories/{repo_id}'
        response = requests.delete(url=delete_url, headers=self.headers)
        if response.status_code != 200:
            logger.info(f'Response is {response.content}')
            raise RuntimeError('Response is not 200. Exiting')
