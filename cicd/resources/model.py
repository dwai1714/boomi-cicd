from __future__ import annotations

import os

import requests
import xmltodict

from cicd.resources.repository import Repository
from cicd.utils.log import get_logger
from cicd.utils.utility import get_config

logger = get_logger(__name__)


class Model:
    """

    Args:
        file_name : The xml file that should be processed
        repository_name : Repository name (required)
        account_id : Boomi Account ID (defined in config file as env variable)
        cloud_id : Boomi Cloud ID (defined in config file as env variable)
        base64_credentials : Credentials (defined in config file as env variable)
        endpoint_url : Boomi End Point (defined in config file as env variable)
    """

    def __init__(
        self, model_name: str, config_file_path: str , file_name: str = None, repository_name: str = None,
        account_id: str = None,
        cloud_id: str = None, base64_credentials: str = None, endpoint_url: str = None,
    ):

        config = get_config(config_file_path)
        self.environment = os.environ['ENV']

        self.file_name = file_name
        self.model_name = model_name
        self.repository_name = repository_name
        self.repository = Repository(self.repository_name)
        self.repository_id = self.repository.get_repo_id()

        if account_id is None:
            self.account_id = config[self.environment]['account_id']
        if cloud_id is None:
            self.cloud_id = config[self.environment]['cloud_id']
        if base64_credentials is None:
            self.base64_credentials = config[self.environment]['base64_credentials']
            self.headers = {
                'Authorization': 'Basic %s' % self.base64_credentials,
                'Content-Type': 'application/xml',
            }
        if endpoint_url is None:
            self.endpoint_url = config[self.environment]['endpoint_url']

    def create_model(self):
        """
        Create a model

        Returns:
            content of response
        """
        url = f'{self.endpoint_url}/{self.account_id}/models'
        if self.file_name is None:
            raise RuntimeError('Create and update model needs valid xml')
        with open(self.file_name, 'rb') as payload:
            dict_xml = (xmltodict.parse(payload))
            model_name_from_file = dict_xml['mdm:CreateModelRequest']['mdm:name']
            if self.model_name != model_name_from_file:
                raise RuntimeError(
                    'model names in file and object are different',
                )
            if self.get_model_id_from_name() is not None:
                raise RuntimeError('model with same name exists')

        with open(self.file_name, 'rb') as payload:
            response = requests.post(
                url=url, headers=self.headers, data=payload,
            )
            if response.status_code != 200:
                logger.info(f'Response is {response.content}')
                raise RuntimeError('Response is not 200. Exiting')
            return response, response.content

    def get_model_id_from_name(self):
        """
        get a model id from model name

        Returns:
            content of response
        """
        url = f'{self.endpoint_url}/{self.account_id}/models/?name={self.model_name}'
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            dict_xml = (xmltodict.parse(response.content))
            return dict_xml['mdm:Models']['mdm:Model']['mdm:id']
        return None

    def update_model(self):
        """
        Update a model

        Returns:
            content of response
        """
        model_id = self.get_model_id_from_name()
        url = f'{self.endpoint_url}/{self.account_id}/models/{model_id}'
        if self.file_name is None:
            raise RuntimeError('Create and update model needs valid xml')
        with open(self.file_name, 'rb') as payload:
            response = requests.put(
                url=url, headers=self.headers, data=payload,
            )
            if response.status_code != 200:
                logger.info(f'Response is {response.content}')
                raise RuntimeError('Response is not 200. Exiting')
        return response, response.content

    def delete_model(self):
        """
        Args:

        Returns:
            response of the call
        """
        model_id = self.get_model_id_from_name()
        url = f'{self.endpoint_url}/{self.account_id}/models/{model_id}'
        response = requests.delete(url=url, headers=self.headers)
        if response.status_code != 200:
            logger.info(f'Response is {response.content}')
            raise RuntimeError('Response is not 200. Exiting')
        return response, response.content

    def publish_model(self, notes: str):
        """

        Args:
            notes : notes for publishing this model

        Returns:
            response of the call
        """
        data = f"""<mdm:PublishModelRequest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:mdm="http://mdm.api.platform.boomi.com/">
            <mdm:notes>{notes}</mdm:notes>
            </mdm:PublishModelRequest> """
        model_id = self.get_model_id_from_name()
        url = f'{self.endpoint_url}/{self.account_id}/models/{model_id}/publish'
        response = requests.post(url=url, headers=self.headers, data=data)
        if response.status_code != 200:
            logger.info(f'Response is {response.content}')
            raise RuntimeError('Response is not 200. Exiting')
        return response, response.content

    def deploy_model(self):
        """
        Deploys a model to a repository
        Returns:
            response of the call
        """
        model_id = self.get_model_id_from_name()
        url = f'{self.endpoint_url}/{self.account_id}/universe/{model_id}/deploy?repositoryId={self.repository_id}'
        response = requests.post(url=url, headers=self.headers)
        if response.status_code != 200:
            logger.info(f'Response is {response.content}')
            raise RuntimeError('Response is not 200. Exiting')
        return response, response.content

    def undeploy_model(self):
        """
                UnDeploy a model to a repository
                Returns:
                    response of the call
        """
        model_id = self.get_model_id_from_name()
        url = f'{self.endpoint_url}/{self.account_id}/repositories/{self.repository_id}/universe/{model_id}'
        response = requests.delete(url=url, headers=self.headers)
        if response.status_code != 200:
            logger.info(f'Response is {response.content}')
            raise RuntimeError('Response is not 200. Exiting')
        return response, response.content
