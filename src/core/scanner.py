import os
from config import LOCAL_PATH
from src.utils.utils import get_local_file_data
from typing import Dict, Optional
from src.utils.logger import logger

def get_all_files_from_local_path(user_path: str)->Optional[Dict]:
    """Scans the specified local directory and retrieves metadata for all files."""
    if os.path.exists(user_path):
        files_data = {}
        with os.scandir(user_path) as files:
            for file in files:
                if file.is_file():
                    file_metadata = get_local_file_data(file)
                    if file_metadata:
                        files_data[file.name] = file_metadata
        return files_data
    else:
        logger.error(f"Ошибка сканирования локального диска: директории '{user_path}' не существует")


if __name__ == '__main__':
    data = get_all_files_from_local_path(user_path=LOCAL_PATH)
    for i in data.items():
        print(i)