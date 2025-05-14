import requests
from config import TOKEN
from src.utils.utils import get_all_remote_files_data
from src.utils.logger import logger


class CloudStorageApi:
    def __init__(self, token: str, remote_folder_name: str = ""):
        """
        Initializes the CloudStorageApi instance.

        Args:
            token (str): The OAuth token for authentication with the cloud storage API.
            remote_folder_name (str, optional): The name of the remote folder to use. Defaults to "".

        Attributes:
            headers (dict): HTTP headers for API requests, including the authorization token.
            base_url (str): The base URL for the cloud storage API.
            session (requests.Session): A session object for making HTTP requests.
            remote_folder_name (str): The validated or created remote folder name.
        """
        self.headers = {"Accept": "application/json", "Authorization": f"OAuth {token}"}
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.session = requests.Session()
        self.remote_folder_name = self.check_remote_folder(remote_folder_name=remote_folder_name)

    def _make_request(self, method, endpoint:str = '', **kwargs):
        """A private helper method to make HTTP requests to the cloud storage API."""
        url = f'{self.base_url}{endpoint}'
        response = self.session.request(
            method=method,
            url=url,
            headers=self.headers,
            **kwargs,
        )
        return response

    def get_info(self):
        """Retrieves information about files in the remote folder."""
        params = {
            "limit": 1000,
            "fields": "items.name,items.path,items.size, items.modified",
        }

        response = self._make_request(method='get', endpoint='files', params=params)

        if response.status_code >= 400:
            logger.error(f"Не удалось установить подключиться Яндекс Диску. Ошибка {response.json()['message']}.")
            return None

        response_data = response.json()
        file_info_data = []
        for file in response_data['items']:
            if file["path"].startswith(f"disk:{self.remote_folder_name}"):
                file_info_data.append(file)
        return file_info_data

    def get_remote_files_data(self):
        """Retrieves detailed data about all files in the remote folder."""
        remote_files = self.get_info()
        return get_all_remote_files_data(remote_files)


    def load(self, local_file_path: str, remote_file_name: str, overwrite: bool = False):
        """Uploads a file from the local system to the remote storage."""
        params = {
            "path": f"{self.remote_folder_name}/{remote_file_name}",
            'overwrite': str(overwrite).lower()
        }
        response_for_upload = self._make_request(method='get', endpoint='upload', params=params)

        if response_for_upload.status_code >= 400:
            logger.error(f"Файл '{local_file_path.split('/')[-1]}' не {['записан', 'перезаписан'][overwrite]}. Ошибка: {response_for_upload.json()['message']}")
            return None

        upload_info = response_for_upload.json()
        url = upload_info['href']
        return self.load_file_to_remote(local_file_path=local_file_path, url=url, overwrite=overwrite)


    def load_file_to_remote(self, url, local_file_path: str, overwrite):
        """Uploads a file from the local system to the remote storage."""
        try:
            with open(local_file_path, 'rb') as file:
                response = self.session.request(
                    method='put',
                    url=url,
                    data=file,
                    headers=self.headers,
                    timeout=30,
                )
            if response.status_code not in (201, 202):
                logger.error(
                    f"Файл '{local_file_path.split('/')[-1]}' не {['записан', 'перезаписан'][overwrite]}. Ошибка: {response.json()['message']}"
                )
                return None
            logger.info(f"Файл '{local_file_path.split('/')[-1]}' успешно {['записан', 'перезаписан'][overwrite]}.")
            return True

        except requests.exceptions.ConnectionError:
            logger.error(f"Загрузка файла '{local_file_path.split('/')[-1]}' превысила лимит времени (60 секунд).")
            return None

        except Exception as e:
            logger.error(f"Произошла ошибка при загрузке файла '{local_file_path.split('/')[-1]}': {str(e)}")
            return None



    def reload(self, local_file_path: str, remote_file_name: str, overwrite: bool = True):
        """ Overwrites an existing file on the remote storage with a new version."""
        return self.load(local_file_path, remote_file_name, overwrite)

    def delete(self, remote_file_name: str):
        """Deletes a file from the remote storage."""
        params = {'path': f"{self.remote_folder_name}/{remote_file_name}"}
        response = self._make_request(method='delete', params=params)
        if response.status_code >= 400:
            message = response.json()['message']
            logger.error(f"Файл '{remote_file_name}' не удален. Ошибка: {message}")
            return None
        logger.info(f"Файл '{remote_file_name}' успешно удален.")

    def is_exist_remote_folder(self, remote_folder_name):
        """Checks if a remote folder exists."""
        params = {'path': f'{remote_folder_name}'}
        response = self._make_request(method='get', params=params)
        if response.status_code >= 400:
            message = response.json()['message']
            logger.error(f"Директория '{remote_folder_name}' на облаке не существует. Ошибка: {message}")
            return False
        return True

    def create_remote_folder(self, remote_folder_name):
        """Creates a new folder on the remote storage."""
        params = {'path': f'{remote_folder_name}'}
        response = self._make_request(method='put', params=params)
        if response.status_code >= 400:
            message = response.json()['message']
            logger.error(f"Директория '{remote_folder_name}' на облаке не создана. Ошибка: {message}.")
            return False
        logger.info(f"Директория '{remote_folder_name}' успешно создана.")
        return remote_folder_name

    def check_remote_folder(self, remote_folder_name):
        """Ensures that a remote folder exists, creating it if necessary"""
        if not self.is_exist_remote_folder(remote_folder_name=remote_folder_name):
            return self.create_remote_folder(remote_folder_name= remote_folder_name)
        return remote_folder_name


if __name__ == "__main__":
    pass