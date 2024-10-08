import hashlib


class CheckSum:
    def __init__(self, file_path):
        self.file_path = file_path

    def md5(self):
        hash_md5 = hashlib.md5()
        with open(self.file_path, "rb") as f:
            # fix memory issue, sometimes it is not able to fit the whole file in memory
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
