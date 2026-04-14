import GalfileLibs
from GalfileLibs.Filesystem.Virtual.File import File
from .error import *
import copy

__all__ = [
    "Folder"
]

class Folder:
    __name: str
    __files: list[File]
    __folders: list[Folder]

    def __init__(
        self,
        name: str,
        files: list[File],
        folders: list[Folder]
    ):
        self.__name = name
        self.__files = files
        self.__folders = folders

    @classmethod
    def new(cls, name: str):
        empty_files: list[File] = []
        empty_folders: list[Folder] = []

        return cls(
            name,
            empty_files,
            empty_folders
        )

    def get_index_of_file(self, file: File):
        for index, __file in enumerate(self.__files):
            if __file.is_same_name(file):
                return index

        return -1

    def get_index_of_folder(self, folder: Folder):
        for index, __folder in enumerate(self.__folders):
            if __folder.is_same_name(folder):
                return index

        return -1

    def has_file(self, file: File):
        return self.get_index_of_file(file) != -1

    def has_folder(self, folder: Folder):
        return self.get_index_of_folder(folder) != -1

    def append_file(self, file: File, ignore_existing_error: bool = False):
        if self.has_file(file) and not ignore_existing_error:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILE_IS_ALREADY_EXISTED
            )

        self.__files.append(file)

    def append_folder(self, folder: Folder, ignore_existing_error: bool = False):
        if folder is self:
            # pengecekan hanya ke ini saja
            # sisanya bisa dijadikan sebagai symlink (mungkin), tapi tidak disarankan
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FOLDER_IS_POINTING_TO_SAME_ADDRESS
            )

        if self.has_folder(folder) and not ignore_existing_error:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FOLDER_IS_ALREADY_EXISTED
            )

        self.__folders.append(folder)

    def remove_file(self, file: File):
        index = self.get_index_of_file(file)
        if index == -1:
            return

        self.__files.pop(index)

    def remove_folder(self, folder: Folder):
        index = self.get_index_of_folder(folder)
        if index == -1:
            return

        self.__folders.pop(index)

    def duplicate(self):
        return Folder(
            self.__name,
            copy.deepcopy(self.__files),
            copy.deepcopy(self.__folders)
        )

    def get_name(self):
        return self.__name

    def get_dir_size(self):
        size = 0
        for __file in self.__files:
            size += __file.get_size()

        return size

    def get_tree_size(self):
        size = self.get_dir_size()

        # recursive
        for __folder in self.__folders:
            size += __folder.get_tree_size()

        return size

    def get_file(self, filename: str):
        for __file in self.__files:
            if __file.get_name() == filename:
                return __file

    def get_folder(self, foldername: str):
        for __folder in self.__folders:
            if __folder.__name == foldername:
                return __folder

    def is_same_name(self, other: Folder):
        return self.__name == other.__name