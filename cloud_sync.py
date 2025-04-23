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
        if response.status_code >= 400:
            raise Exception(f'Api request failed: {response.status_code} - {response.text}')
        if response.text:
            return response.json()


    def get_info(self):
        params = {
            "limit": 1000,
            "fields": "items.name,items.path,items.size, items.modified",
        }
        response = self._make_request(method='get', endpoint='files', params=params)
        data = []
        for file in response['items']:
            if file["path"].startswith(f"disk:{self.remote_folder_name}"):
                data.append(file)
        return data


    def load(self, local_file_path: str, remote_file_name: str, overwrite: bool = False):
        params = {
            "path": f"{self.remote_folder_name}/{remote_file_name}",
            'overwrite': str(overwrite).lower()
        }
        upload_info = self._make_request(method='get', endpoint='upload', params=params)

        with open(local_file_path, 'rb') as file:
            response = self.session.request(
                method='put',
                url=upload_info['href'],
                data=file,
                headers=self.headers

            )
        if response.status_code not in (201, 202):
            raise Exception(f'File upload failed: {response.status_code} - {response.text}')
        return True


    def reload(self, local_file_path: str, remote_file_name: str, overwrite: bool = True):
        return self.load(local_file_path, remote_file_name, overwrite)


    def delete(self, remote_file_name: str):
        params = {'path': f"{self.remote_folder_name}/{remote_file_name}"}
        response = self._make_request(method='delete', params=params)
        print(response)




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
    print("Файл успешно загружен!")

    # Проверка reload
    print("Проверка reload")
    cloud.reload(
            local_file_path="/home/user/Downloads/Техническое задание «Сервис синхронизации файлов».docx",
            remote_file_name="Техническое задание «Сервис синхронизации файлов».docx",
        )
    print("Файл успешно перезагружен!")
    print('Проверка delete')
    cloud.delete(remote_file_name='Техническое задание «Сервис синхронизации файлов».docx')

