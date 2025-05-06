from src.providers.yandex_cloud import CloudStorageApi
from src.utils.utils import get_all_remote_files_data
from config import token, PATH
from scanner import get_all_files_from_local_path



class Comparator:

    def __init__(self, local_files_data, remote_files_data):
        """
        Initialize the Comparator class with local and remote file data.
        """
        self.local_files = local_files_data
        self.remote_files = remote_files_data
        self.comparison_result = {}

    def get_comparison_results(self):
        """
        Compare local and remote files and generate a report.
        The report includes:
        - Files present locally but missing on the remote storage.
        - Files that have been modified locally compared to their remote counterparts.
        - Files present on the remote storage but missing locally.
        """
        self.comparison_result = {
            "local_files_not_on_remotes":self.get_local_files_not_on_remotes(),
            "locally_modified_files": self.get_local_modified_files(),
            "remote_files_not_on_local": self.get_remote_files_not_on_local()
        }
        return self.comparison_result

    def get_local_files_not_on_remotes(self):
        """
        Retrieve files that exist locally but are missing on the remote storage.
        """
        local_files_not_on_remotes = {}
        for local_file, data in self.local_files.items():
            if local_file not in self.remote_files:
                local_files_not_on_remotes[local_file] = data

        return local_files_not_on_remotes

    def get_local_modified_files(self):
        """
        Retrieve files that have been modified locally compared to their remote counterparts.
        """
        locally_modified_files = {}
        for local_file, data in self.local_files.items():
            if local_file in self.remote_files and data['modified'] > self.remote_files[local_file]['modified']:
                locally_modified_files[local_file] = data

        return locally_modified_files

    def get_remote_files_not_on_local(self):
        """
        Retrieve files that exist on the remote storage but are missing locally.
        """
        remote_files_not_on_local = {}
        for remote_file, data in self.remote_files.items():
            if remote_file not in self.local_files:
                remote_files_not_on_local[remote_file] = data

        return remote_files_not_on_local


if __name__ == '__main__':

    api = CloudStorageApi(token=token, remote_folder_name='/Загрузки')
    remote_files = api.get_info()
    remote_data = get_all_remote_files_data(remote_files)
    print(remote_data)
    local_data = get_all_files_from_local_path(user_path=PATH)
    print(local_data)
    compare = Comparator(local_files_data=local_data, remote_files_data=remote_data)
    data =compare.get_comparison_results()
    for i, v in data.items():
        print(i, v)
