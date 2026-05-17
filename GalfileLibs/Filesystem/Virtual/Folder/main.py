import GalfileLibs
from GalfileLibs.Filesystem.Virtual.File import File
from .error import *
import copy
import json

__all__ = [
    "Folder"
]

class Folder:
    __name: str
    __files: list[File]
    __folders: list[Folder]

    __parent: Folder | None

    def __init__(
        self,
        name: str,
        files: list[File],
        folders: list[Folder],
        parent: Folder | None
    ):
        self.__name = name
        self.__files = files
        self.__folders = folders
        self.__parent = parent

    @classmethod
    def new(cls, name: str):
        empty_files: list[File] = []
        empty_folders: list[Folder] = []
        unknown_parent = None

        return cls(
            name,
            empty_files,
            empty_folders,
            unknown_parent
        )

    @classmethod
    def from_load_json_obj(cls, json_obj: dict[
            str,
            str | list
        ]):
        if json_obj["type"] != "folder":
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_JSON_OBJECT_IS_NOT_FOLDER_TYPE
            )

        name: str = json_obj["name"] #type: ignore
        files: list[dict[str, str]] = json_obj["files"] #type: ignore
        folders: list[
            dict[
                str,
                str | list
            ]
        ] = json_obj["folders"] #type: ignore

        files_ptr: list[File] = []
        folders_ptr: list[Folder] = []
        empty_parent = None

        clss = cls(
            name,
            files_ptr,
            folders_ptr,
            empty_parent
        )

        for file in files:
            file_ptr = File.from_load_json_obj(file)

            files_ptr.append(file_ptr)

        for folder in folders:
            folder_ptr = Folder.from_load_json_obj(folder)
            folder_ptr.__parent = clss

            folders_ptr.append(folder_ptr)

        return clss

    @classmethod
    def from_load_json(cls, json_data: str):
        json_obj: dict[
            str,
            str | list[
                dict[str, str]
            ]
        ] = json.loads(json_data)

        return cls.from_load_json_obj(json_obj)

    def _get_json_obj(self) -> dict[str, str]:
        json_obj = {}
        json_obj["type"] = "folder"
        json_obj["name"] = self.__name

        files: list[
            dict[str, str]
        ] = []
        for __file in self.__files:
            files.append(__file._get_json_obj())

        json_obj["files"] = files

        folders: list[
            dict[str, str]
        ] = []
        for __folder in self.__folders:
            folders.append(__folder._get_json_obj())

        json_obj["folders"] = folders

        return json_obj

    def get_index_of_file(self, file: File):
        for index, __file in enumerate(self.__files):
            if __file is file:
                return index

        return -1
    
    def get_index_of_file_in_name(self, filename: str):
        for index, __file in enumerate(self.__files):
            if __file.get_name() == filename:
                return index

        return -1

    def get_index_of_folder(self, folder: Folder):
        for index, __folder in enumerate(self.__folders):
            if __folder is folder:
                return index

        return -1

    def get_index_of_folder_in_name(self, foldername: str):
        for index, __folder in enumerate(self.__folders):
            if __folder.get_name() == foldername:
                return index

        return -1

    def has_file(self, file: File):
        return self.get_index_of_file(file) != -1
    
    def has_filename(self, filename: str):
        return self.get_index_of_file_in_name(filename) != -1

    def has_folder(self, folder: Folder):
        return self.get_index_of_folder(folder) != -1

    def has_foldername(self, foldername: str):
        return self.get_index_of_folder_in_name(foldername) != -1

    def has_parent(self):
        return self.__parent is not None

    def append_file(self, file: File, ignore_file_exists_error: bool = False):
        if self.has_file(file) and not ignore_file_exists_error:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILE_IS_ALREADY_EXISTED
            )

        if self.has_filename(file.get_name()) and not ignore_file_exists_error:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILENAME_IS_ALREADY_EXISTED
            )

        if self.has_foldername(file.get_name()):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_NAME_IS_ALREADY_EXISTED
            )

        self.__files.append(file)

    def append_folder(self, folder: Folder, ignore_folder_exists_error: bool = False):
        if folder is self:
            # pengecekan hanya ke ini saja
            # sisanya bisa dijadikan sebagai symlink (mungkin), tapi tidak disarankan
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FOLDER_IS_POINTING_TO_SAME_ADDRESS
            )

        if self.has_folder(folder) and not ignore_folder_exists_error:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FOLDER_IS_ALREADY_EXISTED
            )

        if self.has_foldername(folder.get_name()) and not ignore_folder_exists_error:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FOLDERNAME_IS_ALREADY_EXISTED
            )

        if self.has_filename(folder.get_name()):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_NAME_IS_ALREADY_EXISTED
            )

        self.__folders.append(folder)
        folder.__parent = self # menjadi orang tua asuhnya

    def remove_file(self, file: File):
        index = self.get_index_of_file(file)
        if index == -1:
            return False

        self.__files.pop(index)

        return True

    def remove_folder(self, folder: Folder):
        index = self.get_index_of_folder(folder)
        if index == -1:
            return False

        self.__folders.pop(index)

        return True

    def clear(self):
        self.__files.clear()
        self.__folders.clear()

    def duplicate(self):
        return Folder(
            self.__name,
            copy.deepcopy(self.__files),
            copy.deepcopy(self.__folders),
            self.__parent
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

    def get_file_in_name(self, filename: str):
        file_index = self.get_index_of_file_in_name(filename)
        if file_index == -1:
            return None

        return self.__files[file_index]

    def get_folder_in_name(self, foldername: str):
        folder_index = self.get_index_of_folder_in_name(foldername)
        if folder_index == -1:
            return None

        return self.__folders[folder_index]
    
    def get_all_files(self):
        return copy.copy(self.__files)
    
    def get_all_folders(self):
        return copy.copy(self.__folders)

    def get_parent(self):
        return self.__parent

    def is_same_name(self, other: Folder):
        return self.__name == other.__name
    
    def dump_json(self):
        return json.dumps(self._get_json_obj(), indent=4)