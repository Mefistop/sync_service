import os
from datetime import datetime, timedelta
from typing import Dict, Any, List

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


def get_remote_file_data(remote_file: Dict) -> Dict[str, Any]:
    size = remote_file['size']
    path = remote_file['path']
    modified = datetime.fromisoformat(remote_file['modified']) + timedelta(hours=3)
    modified_str = modified.strftime('%Y-%m-%d: %H:%M:%S')
    return {"modified": modified_str, "size": size, "path": path}


def get_all_remote_files_data(remote_files: List) -> Dict:
    remote_files_data = {}
    if remote_files is not None:
        for remote_file in remote_files:
            name = remote_file['name']
            remote_file_metadata = get_remote_file_data(remote_file)
            remote_files_data[name] = remote_file_metadata
        return remote_files_data
    return None
