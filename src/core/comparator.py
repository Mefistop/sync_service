from config import TOKEN

from src.providers.yandex_cloud import CloudStorageApi


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
            "local_files_not_on_remotes": self.get_local_files_not_on_remotes(),
            "locally_modified_files": self.get_local_modified_files(),
            "remote_files_not_on_local": self.get_remote_files_not_on_local(),
        }
        return self.comparison_result

    def get_local_files_not_on_remotes(self):
        """
        Retrieve files that exist locally but are missing on the remote storage.
        """
        local_files_not_on_remotes = {}
        if self.local_files:
            for local_file, data in self.local_files.items():
                if local_file not in self.remote_files:
                    local_files_not_on_remotes[local_file] = data

        return local_files_not_on_remotes

    def get_local_modified_files(self):
        """
        Retrieve files that have been modified locally compared to their remote counterparts.
        """
        locally_modified_files = {}
        if self.local_files:
            for local_file, data in self.local_files.items():
                if self.is_modified_local_file(file=local_file, data=data):
                    locally_modified_files[local_file] = data
        return locally_modified_files

    def is_modified_local_file(self, file, data):
        """Check local file is modified"""
        if (
            file in self.remote_files
            and data["modified"] > self.remote_files[file]["modified"]
        ):
            return True
        return False

    def get_remote_files_not_on_local(self):
        """
        Retrieve files that exist on the remote storage but are missing locally.
        """
        remote_files_not_on_local = {}
        if self.remote_files:
            for remote_file, data in self.remote_files.items():
                if remote_file not in self.local_files:
                    remote_files_not_on_local[remote_file] = data

        return remote_files_not_on_local

    def check_local_path(self):
        """Check exist the local path"""
        if self.local_files:
            return True
        return False

    def check_remote_path(self):
        """Check exist the remote path"""
        if self.remote_files is not None:
            return True
        return False


if __name__ == "__main__":
    api = CloudStorageApi(token=TOKEN, remote_folder_name="/Загрузки")
