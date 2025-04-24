import os
from datetime import datetime
from typing import Dict, Any

def get_local_file_data(file: os.DirEntry)-> Dict[str, Any]:
    try:
        file_stat = file.stat()
        modification_time_in_sec = file_stat.st_mtime
        modified = datetime.fromtimestamp(modification_time_in_sec).strftime('%Y-%m-%d: %H:%M:%S')
        size = file_stat.st_size
        path = file.path
        return {"modified": modified, "size": size, "path": path}
    except OSError as e:
        print(f'Ошибка получения методанных для {file}: {e}')
        return
