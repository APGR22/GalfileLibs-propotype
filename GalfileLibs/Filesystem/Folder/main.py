from pathlib import Path
from .Metadata import *
import GalfileLibs

__all__ = [
    "Folder"
]

class Folder:

    __name: str
    __files: list[GalfileLibs.Filesystem.File.File]

    def __init__(
            self,
            name: str,
            files: list[GalfileLibs.Filesystem.File.File],
        ):
        self.__name = name
        self.__files = files

    @classmethod
    def new(
            cls,
            name: str,
        ):
        empty_files = []
        return cls(
            name,
            empty_files
        )
    
    def get_index_of_file(
            self,
            file: GalfileLibs.Filesystem.File.File
        ):
        """
        Docstring for get_index_of_file

        :param self: Description
        :param file: Description
        :type file: GalfileLibs.Filesystem.File.File
        :return: Index of the file if found, otherwise -1
        """

        for index, internal_file in enumerate(self.__files):
            if internal_file.is_same(file):
                return index

        return -1

    def has_file(
            self,
            file: GalfileLibs.Filesystem.File.File
        ):
        return self.get_index_of_file(file) != -1

    def append_file(
            self,
            file: GalfileLibs.Filesystem.File.File
        ):
        if self.has_file(file):
            return

        self.__files.append(file)

    def remove_file(
            self,
            file: GalfileLibs.Filesystem.File.File
        ):
        index = self.get_index_of_file(file)
        if index == -1:
            return

        self.__files.pop(index)

    def append_files(
            self,
            files: list[GalfileLibs.Filesystem.File.File]
        ):
        for file in files:
            if self.has_file(file):
                continue

            self.__files.append(file)

    def remove_files(
            self,
            files: list[GalfileLibs.Filesystem.File.File]
        ):
        for file in files:
            index = self.get_index_of_file(file)
            if index == -1:
                return

            self.__files.pop(index)

    def print_files(self):
        print(self.__name)
        for file in self.__files:
            print("\t" + str(file.get_path()))

    def copy(self):
        # untuk sementara
        # return Folder()
        pass