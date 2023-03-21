
class DataStore:

    def __init__(self):
        self._data = {}
        self._data["files"] = []
        self._data["added_files"] = []

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def add_file(self, file: str):
        self._data["files"] = self._data["files"] + [file]

    def loop_unadded_files(self):
        unadded_files = set(self._data["files"]).difference(self._data["added_files"])
        for file in unadded_files:
            yield file

    def mark_file_as_added(self, file: str):
        self._data["added_files"] = self._data["added_files"] + [file]

    def remove_file(self, file: str):
        self._data["files"] = [x for x in self._data["files"] if x != file]
        self._data["added_files"] = [x for x in self._data["added_files"] if x != file]

