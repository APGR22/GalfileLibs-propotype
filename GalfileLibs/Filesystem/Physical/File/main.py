from pathlib import Path
import GalfileLibs
from .error import *
import shutil
import hashlib

__all__ = [
    "FileStream",
]

class FileStream:
    __filepath: Path

    __data: bytes

    def __init__(self, filepath: Path, data: bytes):
        if not filepath.is_file():
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILEPATH_IS_NOT_EXISTED
            )

        self.__filepath = filepath.absolute()
        self.__data = data

    @classmethod
    def new(
        cls,
        filepath: Path,
        overwrite: bool = False
    ):
        if filepath.is_file() and not overwrite:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILEPATH_IS_EXISTED
            )

        # create
        with open(filepath, "wb"):
            pass

        empty_data = b""

        return cls(
            filepath,
            empty_data
        )

    @classmethod
    def open(
        cls,
        filepath: Path
    ):
        empty_data = b""

        filestream = cls(
            filepath,
            empty_data
        )

        filestream.load_to_stream()

        return filestream

    def exists(self):
        return self.__filepath.is_file()

    def read(self):
        return self.__data

    def write(self, data: bytes):
        self.__data = data

    def append(self, data: bytes):
        self.__data += data

    def load_to_stream(self):
        if not self.exists():
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILEPATH_IS_NOT_EXISTED
            )

        with open(self.__filepath, "rb") as file:
            self.__data = file.read()

    def save_to_local(self):
        with open(self.__filepath, "wb") as file:
            file.write(self.__data)

    def duplicate(self, new_name: str | None = None, new_dir_path: Path | None = None, overwrite: bool = False):
        if new_name is None:
            new_name = self.__filepath.name
        if new_dir_path is None:
            new_dir_path = self.__filepath.parent

        new_dir_path = new_dir_path.absolute()

        new_filepath = new_dir_path.joinpath(new_name)

        if new_filepath.is_file() and not overwrite:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILEPATH_IS_EXISTED
            )

        new_filestream = FileStream(
            new_filepath,
            self.__data
        )

        new_filestream.save_to_local()

        return new_filestream

    def move(self, new_dir_path: Path, overwrite: bool = False):
        if not new_dir_path.is_dir():
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_DIRECTORY_IS_NOT_EXISTED
            )

        new_dir_path = new_dir_path.absolute()

        name = self.__filepath.name
        new_filepath = new_dir_path.joinpath(name)
        old_filepath = self.__filepath

        if new_filepath.is_file() and not overwrite:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILEPATH_IS_EXISTED
            )

        if self.exists():
            shutil.move(old_filepath, new_filepath)

        self.__filepath = new_filepath

    def remove(self):
        self.__filepath.unlink(True)


    def get_path(self):
        return self.__filepath

    def get_dir(self):
        return self.__filepath.parent

    def get_checksum(self):
        hash = hashlib.sha256(self.__data)
        return hash.hexdigest()

    def is_same(self, other: FileStream):
        return\
            self.is_same_path(other) and\
            self.is_same_data(other)

    def is_same_path(self, other: FileStream):
        return self.__filepath == other.__filepath

    def is_same_data(self, other: FileStream):
        return self.__data == other.__data