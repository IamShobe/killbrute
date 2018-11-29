import os

import hashlib
from functools import lru_cache
from zipfile import ZipFile


class Cypher(object):
    def __init__(self, required_array):
        self.required_array = required_array

    def is_good(self, pass_phrase):
        raise NotImplementedError("Abstract method called")

    def cleanup(self):
        pass


class MD5Cypher(Cypher):
    def is_good(self, pass_phrase):
        phrase = hashlib.md5(bytes(pass_phrase, "utf-8")).hexdigest()
        if phrase in self.required_array:
            self.required_array.remove(phrase)
            return phrase


class SHA224Cypher(Cypher):
    def is_good(self, pass_phrase):
        phrase = hashlib.sha224(bytes(pass_phrase, "utf-8")).hexdigest()
        if phrase in self.required_array:
            self.required_array.remove(phrase)
            return phrase


class NoCypher(Cypher):
    def is_good(self, pass_phrase):
        if pass_phrase in self.required_array:
            self.required_array.remove(pass_phrase)
            return pass_phrase


class ZipCypher(Cypher):
    def __init__(self, required_array):
        super(ZipCypher, self).__init__(required_array)
        self.zip_cache = {}

    def get_zip_file(self, path):
        if path not in self.zip_cache:
            self.zip_cache[path] = ZipFile(path)

        return self.zip_cache[path]

    def is_good(self, pass_phrase):
        if not os.path.exists("./temp_folder"):
            os.mkdir("./temp_folder")

        for zip_path in self.required_array:
            try:
                zf = self.get_zip_file(zip_path)
                zf.extractall(pwd=bytes(pass_phrase, "utf-8"),
                              path="./temp_folder")
                self.required_array.remove(zip_path)
                return zip_path
            except Exception as e:
                pass

    def cleanup(self):
        for zip_file in self.zip_cache.values():
            zip_file.close()
