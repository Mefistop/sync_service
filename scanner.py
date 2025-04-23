import os
from datetime import datetime
from config import PATH

def get_all_files_from_path(user_path):
    if os.path.exists(user_path):
        file_list = {}
        with os.scandir(user_path) as files:
            for file in files:
                if file.is_file():
                    filename = file.name
                    modification_time_in_sec = file.stat().st_mtime
                    modification_datetime = datetime.fromtimestamp(modification_time_in_sec).strftime('%Y-%m-%d: %H:%M:%S')
                    print(filename, modification_datetime, sep='  |  ')
                    file_list[filename] = modification_datetime
    else:
        raise Exception('not exist')


if __name__ == '__main__':
    get_all_files_from_path(user_path=PATH)