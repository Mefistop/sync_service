import time
from src.core.scanner import get_all_files_from_local_path
from src.providers.yandex_cloud import CloudStorageApi
from src.core.comparator import Comparator
from config import TOKEN, LOCAL_PATH
from src.utils.logger import logger

class SyncEngine:
    def __init__(self, local_path, token, remote_folder_name: str =""):
        self.local_path = local_path
        if not remote_folder_name:
            remote_folder_name = f'/{local_path.split('/')[-1]}'
        self.cloud_api = CloudStorageApi(token=token, remote_folder_name=remote_folder_name)
        self.comparator = self.compare_data()

    def get_local_files_data(self):
        local_files = get_all_files_from_local_path(user_path=self.local_path)
        return local_files


    def get_remote_files_data(self):
        remote_files = self.cloud_api.get_remote_files_data()
        return remote_files


    def compare_data(self):
        comparator = Comparator(
            local_files_data=self.get_local_files_data(),
            remote_files_data=self.get_remote_files_data(),
        )
        return comparator

    def load_local_files_to_cloud(self):
        comparator = self.comparator
        local_files_not_on_remotes = comparator.get_local_files_not_on_remotes()
        if local_files_not_on_remotes:
            for name, metadata in local_files_not_on_remotes.items():
                self.cloud_api.load(
                    local_file_path=metadata['path'],
                    remote_file_name = name,
                )
        else:
            logger.info("Отсуствуют новые локальные файлы для отправки на облако.")

    def load_modified_local_files_to_cloud(self):
        comparator = self.comparator
        local_modified_files = comparator.get_local_modified_files()
        if local_modified_files:
            for name, metadata in local_modified_files.items():
                self.cloud_api.reload(
                    local_file_path=metadata['path'],
                    remote_file_name = name,
                )
        else:
            logger.info("Отсуствуют измененные локальные файлы для отправки на облако.")

    def delete_remote_files_not_on_local(self):
        remote_files_not_on_local=self.comparator.get_remote_files_not_on_local()
        if remote_files_not_on_local:
            for name, metadata in remote_files_not_on_local.items():
                self.cloud_api.delete(
                    remote_file_name = name,
                )
        else:
            logger.info("Отсуствуют файлы из облака, не синхронизированные с локальной директорией.")

    def run_once(self):
        if self.comparator.check_local_path() and self.comparator.check_remote_path():
            self.load_local_files_to_cloud()
            self.load_modified_local_files_to_cloud()
            self.delete_remote_files_not_on_local()

    def run_periodical(self, interval_seconds: int):
        while True:
            logger.info(f'Программа синхронизации файлов начинает работу с директорией {self.local_path}.')
            self.run_once()
            logger.info(f"Синхронизация завершена. Ожидаю {interval_seconds} секунд до следующей итерации.")
            time.sleep(interval_seconds)



if __name__ == '__main__':
    api = SyncEngine(local_path= PATH, token=TOKEN, remote_folder_name='/Загрузи')
    api.run_periodical(500)
