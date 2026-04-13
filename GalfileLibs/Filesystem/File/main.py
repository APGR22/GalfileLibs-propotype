from pathlib import Path
from .type import *
from .error import *
import GalfileLibs
import shutil
import hashlib

__all__ = [
    "File"
]

class File:
    __filepath: Path

    __data: bytes
    __format_type: FormatType

    def __init__(
            self,
            filepath: Path,
            data: bytes,
            format_type: FormatType
        ):
        self.__filepath = filepath
        self.__data = data
        self.__format_type = format_type

    @classmethod
    def new(
            cls,
            name: str,
            dir_path: Path,
            overwrite: bool = False
        ):
        """
        :param dir_path: Must be exists when refresh data nor save to local
        """

        filepath = dir_path.joinpath(name)
        empty_data = b""
        format_type = FormatType.get_type_by_ext(filepath.suffix)

        if filepath.is_file() and not overwrite:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.TRY_TO_OVERWRITE_WITH_EXISTING_FILE
            )

        return cls(
            filepath,
            empty_data,
            format_type
        )

    @classmethod
    def open(
            cls,
            filepath: Path
        ):
        if not filepath.is_file():
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILEPATH_IS_NOT_FOUND
            )

        data = b""
        with open(filepath, "rb") as file:
            data = file.read()

        format_type = FormatType.get_type_by_ext(filepath.suffix)

        return cls(
            filepath,
            data,
            format_type
        )

    def __is_data_empty(self):
        return len(self.__data) == 0

    def is_exists(self):
        return self.__filepath.is_file()

    def rename(self, new_name: str, overwrite: bool = False):
        dir = self.__filepath.parent
        new_filepath = dir.joinpath(new_name)

        if new_filepath.is_file() and not overwrite:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.TRY_TO_OVERWRITE_WITH_EXISTING_FILE
            )

        result = self.__filepath.rename(new_filepath)

        self.__filepath = result

    def refresh_data_from_local(self):
        if not self.is_exists():
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILEPATH_IS_NOT_FOUND
            )

        with open(self.__filepath, "rb") as file:
            self.__data = file.read()

    def write(self, data: bytes):
        self.__data = data

    def append(self, data: bytes):
        self.__data += data

    def read(self):
        return self.__data

    def save_to_local(self):
        if not self.__filepath.parent.is_dir():
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_DIRECTORY_IS_NOT_FOUND
            )

        with open(self.__filepath, "wb") as file:
            file.write(self.__data)

    def remove(self):
        self.__filepath.unlink(True)

    def duplicate(self, new_name: str | None = None, new_dir_path: Path | None = None):
        if new_name is None:
            new_name = self.__filepath.name
        if new_dir_path is None:
            new_dir_path = self.__filepath.parent

        new_dir_path = new_dir_path.absolute()

        new_filepath = new_dir_path.joinpath(new_name)

        if new_filepath == self.__filepath:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.TRY_TO_DUPLICATE_WITH_SAME_FILEPATH
            )

        return File(
            new_filepath,
            self.__data,
            self.__format_type
        )
    
    def move(self, new_dir_path: Path):
        if not new_dir_path.is_dir():
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_DIRECTORY_IS_NOT_FOUND
            )
        
        new_dir_path = new_dir_path.absolute()

        name = self.__filepath.name
        new_filepath = new_dir_path.joinpath(name)
        old_filepath = self.__filepath

        # for across filesystem
        shutil.move(old_filepath, new_filepath)

        self.__filepath = new_filepath

    def get_path(self):
        return self.__filepath

    def get_dir(self):
        return self.__filepath.parent

    def set_format_type_by_data(self):
        self.__format_type = FormatType.get_type_by_data(self.__data)

    def set_format_type_by_ext(self):
        self.__format_type = FormatType.get_type_by_ext(self.__filepath.suffix)

    def get_format_type(self):
        return self.__format_type

    def get_type(self):
        return Type.get_type(self.__format_type)

    def get_checksum(self):
        hash = hashlib.sha256(self.__data)
        return hash.hexdigest()

    def get_stat(self):
        return self.__filepath.stat()

    def is_same(
            self,
            other: GalfileLibs.Filesystem.File.File    
        ):
        return self.__filepath == other.get_path()