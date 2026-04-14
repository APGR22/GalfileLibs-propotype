from pathlib import Path
import hashlib

__all__ = [
    "File"
]

class File:
    __name: str

    __data: bytes

    def __init__(
        self,
        name: str,
        data: bytes
    ):
        self.__name = name
        self.__data = data

    @classmethod
    def new(
        cls,
        name: str
    ):
        empty_data = b""
        return cls(
            name,
            empty_data
        )

    def rename(self, new_name: str):
        self.__name = new_name

    def read(self):
        return self.__data

    def write(self, data: bytes):
        self.__data = data

    def append(self, data: bytes):
        self.__data += data

    def duplicate(self):
        return File(
            self.__name,
            self.__data
        )

    def get_name(self):
        return self.__name

    def get_size(self):
        return len(self.__data)

    def get_checksum(self):
        hash = hashlib.sha256(self.__data)
        return hash.hexdigest()

    def is_same(self, other: File):
        return\
            self.is_same_name(other) and\
            self.is_same_data(other)

    def is_same_name(self, other: File):
        return self.__name == other.__name

    def is_same_data(self, other: File):
        return self.__data == other.__data