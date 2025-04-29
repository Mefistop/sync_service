import os
from config import PATH
from src.utils.utils import get_local_file_data
from typing import Dict, Any, List

def get_all_files_from_local_path(user_path: str)->Dict:
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
        print(f'Ошибка сканирования локального диска: {user_path} не существует')


if __name__ == '__main__':
    data = get_all_files_from_local_path(user_path=PATH)
    for i in data.items():
        print(i)