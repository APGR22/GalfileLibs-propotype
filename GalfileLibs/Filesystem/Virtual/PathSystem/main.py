from GalfileLibs.Filesystem.Virtual.File import File
from GalfileLibs.Filesystem.Virtual.Folder import Folder
from pathlib import Path
from .error import *
import GalfileLibs
import os

__all__ = [
    "VirtualPathSystem"
]

class VirtualPathSystem:
    __root: Folder
    __root_path: Path = Path("/")
    __curdir_ptr: Folder
    __curdir_path: Path

    def __init__(
        self,
        root: Folder,
        curdir_ptr: Folder,
        curdir_path: Path
    ):
        self.__root = root
        self.__curdir_ptr = curdir_ptr
        self.__curdir_path = curdir_path

    @classmethod
    def new(cls):
        root = Folder.new("/")
        curdir_ptr = root
        curdir_path = Path("/")

        return cls(
            root,
            curdir_ptr,
            curdir_path
        )

    def __normalize_to_path(self, path: str | Path) -> Path:
        if isinstance(path, str):
            path = Path(path)

        return path

    def __is_absolute(self, path: Path):
        path_s = path.as_posix()

        return path_s.startswith("/")
    
    def __resolve_to_absolute(self, path: Path):
        if not self.__is_absolute(path):
            path = self.__curdir_path.joinpath(path)

        return path

    def __resolve_levels(self, path: Path):
        if not self.__is_absolute(path):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_PATH_IS_NOT_ABSOLUTE_PATH
            )

        curdir = Path("") # empty
        for path_name in path.parts:
            match path_name:
                case ".":
                    continue
                case "..":
                    curdir = curdir.parent
                case _:
                    curdir = curdir.joinpath(path_name)

        return curdir

    def cd(self, to_path: str | Path):
        to_path = self.__normalize_to_path(to_path)

        # many code but more efficient than resolve to absolute first and then resolve levels

        curdir_folder_ptr = self.__curdir_ptr
        for path_name in to_path.parts:
            match path_name:
                case os.sep:
                    curdir_folder_ptr = self.__root
                case ".":
                    continue
                case "..":
                    folder_ptr = curdir_folder_ptr.get_parent()

                    if folder_ptr is None:
                        continue # means at root, skip

                    curdir_folder_ptr = folder_ptr

                    continue
                case _:
                    folder_ptr = curdir_folder_ptr.get_folder(path_name)

                    if folder_ptr is None:
                        raise GalfileLibs.System.Error.EnumException(
                            ErrorType.THE_DIRECTORY_IS_NOT_EXISTS
                        )

                    curdir_folder_ptr = folder_ptr

        self.__curdir_ptr = curdir_folder_ptr
        self.__curdir_path = to_path

    def pwd(self):
        return self.__curdir_path

    def mkdirs(self, new_path: str | Path):
        new_path = self.__normalize_to_path(new_path)
        new_path = self.__resolve_to_absolute(new_path)
        new_path = self.__resolve_levels(new_path)

        curdir_folder_ptr = self.__root
        for path_name in new_path.parts[1:]: # skip root
            folder_ptr = curdir_folder_ptr.get_folder(path_name)

            if folder_ptr is None:
                # create new
                folder_ptr = Folder.new(path_name)

                curdir_folder_ptr.append_folder(folder_ptr)

            curdir_folder_ptr = folder_ptr

    def rmdirs(self, old_path: str | Path, ignore_dir_not_exists_error: bool = False):
        old_path = self.__normalize_to_path(old_path)
        old_path = self.__resolve_to_absolute(old_path)
        old_path = self.__resolve_levels(old_path)

        if old_path == self.__root_path:
            self.__root.clear()
            self.__curdir_ptr = self.__curdir_ptr
            self.__curdir_path = Path(self.__root_path)
            return

        curdir_folder_ptr = self.__root
        for path_name in old_path.parts[1:]: # skip root
            folder_ptr = curdir_folder_ptr.get_folder(path_name)

            if folder_ptr is None:
                if not ignore_dir_not_exists_error:
                    raise GalfileLibs.System.Error.EnumException(
                        ErrorType.THE_DIRECTORY_IS_NOT_EXISTS
                    )
                
                return # finish
            
            curdir_folder_ptr = folder_ptr

        # sudah ke folder target
        folder_target_ptr = curdir_folder_ptr
        # balik ke parent
        curdir_folder_ptr: Folder = curdir_folder_ptr.get_parent() #type: ignore

        # hapus folder target
        curdir_folder_ptr.remove_folder(folder_target_ptr)

        # jika __curdir_path mengarah ke folder target ini maupun anaknya, ganti ke parent
        if self.__curdir_path == old_path or old_path in self.__curdir_path.parents:
            self.__curdir_path = old_path.parent
            self.__curdir_ptr = curdir_folder_ptr

    def cpdirs(self, src_dir_path: str | Path, dst_parent_dir_path: str ):
        src_dir_path

    def mvdirs(self):
        pass

    def mkfile(self):
        pass

    def rmfile(self):
        pass

    def cpfile(self):
        pass

    def mvfile(self):
        pass

    def tree(self):
        pass