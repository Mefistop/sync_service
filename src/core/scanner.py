import os
from config import LOCAL_PATH
from src.utils.logger import logger
from datetime import datetime, timezone


class Scanner:
    def __init__(self, local_path: str):
        self.local_path = local_path
        logger.info(f'Программа синхронизации файлов начинает работу с директорией {self.local_path}.')

    def get_files_from_local_path(self):
        """Scans the specified local directory and retrieves metadata for all files."""
        if os.path.exists(self.local_path):
            files_data = {}
            with os.scandir(self.local_path) as files:
                for file in files:
                    if file.is_file():
                        file_metadata = self.get_file_metadata(file)
                        if file_metadata:
                            files_data[file.name] = file_metadata
            return files_data
        else:
            logger.error(f"Ошибка сканирования локального диска: директории '{self.local_path}' не существует")

    @staticmethod
    def get_file_metadata(file):
        """Retrieves metadata for file"""
        try:
            file_stat = file.stat()
            modification_time_in_sec = file_stat.st_mtime
            modified = datetime.fromtimestamp(modification_time_in_sec).replace(tzinfo=timezone.utc)
            size = file_stat.st_size
            path = file.path
            return {"modified": modified, "size": size, "path": path}
        except OSError as e:
            logger.error(f'Ошибка получения методанных для {file}: {e}')


if __name__ == '__main__':
    pass