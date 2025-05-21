from datetime import datetime, timedelta
from typing import Any, Dict, List


def get_remote_file_data(remote_file: Dict) -> Dict[str, Any]:
    size = remote_file["size"]
    path = remote_file["path"]
    modified = datetime.fromisoformat(remote_file["modified"]) + timedelta(hours=3)
    return {"modified": modified, "size": size, "path": path}


def get_all_remote_files_data(remote_files: List) -> Dict:
    remote_files_data = {}
    if remote_files is not None:
        for remote_file in remote_files:
            name = remote_file["name"]
            remote_file_metadata = get_remote_file_data(remote_file)
            remote_files_data[name] = remote_file_metadata
        return remote_files_data
    return None
