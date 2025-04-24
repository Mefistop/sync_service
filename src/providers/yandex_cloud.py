import requests
from config import token
url_disk = 'https://cloud-api.yandex.net/v1/disk'
url_files = 'https://cloud-api.yandex.net/v1/disk/resources/files'


class CloudStorageApi:
    def __init__(self, token: str, remote_folder_name: str = "disk:"):
        self.headers = {"Accept": "application/json", "Authorization": f"OAuth {token}"}
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.session = requests.Session()
        self.remote_folder_name = remote_folder_name

    def _make_request(self, method, endpoint:str = '', **kwargs):
        url = f'{self.base_url}{endpoint}'
        response = self.session.request(
            method=method,
            url=url,
            headers=self.headers,
            **kwargs,
        )
        return response

    def get_info(self):
        params = {
            "limit": 1000,
            "fields": "items.name,items.path,items.size, items.modified",
        }
        response = self._make_request(method='get', endpoint='files', params=params)

        if response.status_code >= 400:
            print('Не удалось установить подключиться Яндекс Диску. Ошибка соединения.')
            return

        response_data = response.json()
        file_info_data = []
        for file in response_data['items']:
            if file["path"].startswith(f"disk:{self.remote_folder_name}"):
                file_info_data.append(file)
        return file_info_data

    def load(self, local_file_path: str, remote_file_name: str, overwrite: bool = False):
        params = {
            "path": f"{self.remote_folder_name}/{remote_file_name}",
            'overwrite': str(overwrite).lower()
        }
        response_for_upload = self._make_request(method='get', endpoint='upload', params=params)

        if response_for_upload.status_code >= 400:
            print(f"Файл '{local_file_path.split('/')[-1]}' не {['записан', "перезаписан"][overwrite]}. Ошибка: {response_for_upload.json()['message']}")
            return

        upload_info = response_for_upload.json()
        with open(local_file_path, 'rb') as file:
            response = self.session.request(
                method='put',
                url=upload_info['href'],
                data=file,
                headers=self.headers,
            )

        if response.status_code not in (201, 202):
            print(f"Файл '{local_file_path.split('/')[-1]}' не {['записан', "перезаписан"][overwrite]}. Ошибка: {response.json()['message']}")
            return
        print(f"Файл '{local_file_path.split('/')[-1]}' успешно {['записан', "перезаписан"][overwrite]}.")
        return True

    def reload(self, local_file_path: str, remote_file_name: str, overwrite: bool = True):
        return self.load(local_file_path, remote_file_name, overwrite)

    def delete(self, remote_file_name: str):
        params = {'path': f"{self.remote_folder_name}/{remote_file_name}"}
        response = self._make_request(method='delete', params=params)
        if response.status_code >= 400:
            message = response.json()['message']
            print(f"Файл '{remote_file_name}' не удален. Ошибка: {message}")
            return
        print(f"Файл '{remote_file_name}' успешно удален.")


if __name__ == "__main__":
    cloud = CloudStorageApi(token=token, remote_folder_name='/Загрузки')
    # Проверка get_info
    print("Проверка get_info")
    l = cloud.get_info()
    for i in l:
        print(i)

    print("Проверка load")
    cloud.load(
            local_file_path="/home/user/Downloads/Техническое задание «Сервис синхронизации файлов».docx",
            remote_file_name="Техническое задание «Сервис синхронизации файлов».docx",
        )
    # #
    # Проверка reload
    print("Проверка reload")
    cloud.reload(
            local_file_path="/home/user/Downloads/Техническое задание «Сервис синхронизации файлов».docx",
            remote_file_name="Техническое задание «Сервис синхронизации файлов».docx",
        )
    print('Проверка delete')
    cloud.delete(remote_file_name='Техническое задание «Сервис синхронизации файлов».docx')

