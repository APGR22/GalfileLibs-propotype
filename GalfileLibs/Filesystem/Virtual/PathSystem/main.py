from GalfileLibs.Filesystem.Virtual.File import File
from GalfileLibs.Filesystem.Virtual.Folder import Folder
from pathlib import Path
from .error import *
import GalfileLibs
import os
import colorama
from .conf import *

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

    def __go_to_folder(self, folder_path: Path, ignore_dir_not_exists_error: bool = False):
        """
        Docstring for __go_to_folder
        
        :param self: Description
        :param folder_path: Description
        :type folder_path: Path
        :param ignore_dir_not_exists_error: Description
        :type ignore_dir_not_exists_error: bool
        :returns: Return the folder ptr if found
        :returns: Otherwise, return the parent of the folder that exists.
        """

        if not self.__is_absolute(folder_path):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_PATH_IS_NOT_ABSOLUTE_PATH
            )

        curdir_folder_ptr = self.__root
        for path_name in folder_path.parts[1:]: # skip root
            folder_ptr = curdir_folder_ptr.get_folder_in_name(path_name)

            if folder_ptr is None:
                if not ignore_dir_not_exists_error:
                    raise GalfileLibs.System.Error.EnumException(
                        ErrorType.THE_DIRECTORY_IS_NOT_EXISTS
                    )

                # finish because the target path isn't exists
                return curdir_folder_ptr
            
            curdir_folder_ptr = folder_ptr

        return curdir_folder_ptr
    
    def __tree(self, curdir_folder_ptr: Folder, indent: int = 4, buffer_indent_begin: str = ""):
        space = " "
        indent_arrow = ("-" * indent) + ">" + space
        indent_spaces = (" " * indent) + (space * 2)

        buffer_member_indent_begin = buffer_indent_begin + "|" + indent_arrow
        buffer_next_indent_begin = buffer_indent_begin + "|" + indent_spaces
        buffer_next_last_indent_begin = buffer_indent_begin + " " + indent_spaces

        files_ptr = curdir_folder_ptr.get_all_files()
        folders_ptr = curdir_folder_ptr.get_all_folders()

        items_ptr = files_ptr + folders_ptr
        items_ptr.sort(key=lambda item_ptr: item_ptr.get_name())
        items_length = len(items_ptr)

        for index, item_ptr in enumerate(items_ptr):
            name = item_ptr.get_name() + colorama.Fore.RESET

            if isinstance(item_ptr, File):
                name = Conf.colorFile + name
            else:
                name = Conf.colorFolder + name

            print(buffer_member_indent_begin + name)

            buffer_next = buffer_next_indent_begin
            if index == items_length-1:
                buffer_next = buffer_next_last_indent_begin

            if isinstance(item_ptr, Folder):
                self.__tree(item_ptr, indent, buffer_next)

    def cd(self, to_path: str | Path):
        to_path = self.__normalize_to_path(to_path)

        # many code but more efficient than resolve to absolute first and then resolve levels

        curdir_folder_ptr = self.__curdir_ptr
        for path_name in to_path.parts:
            match path_name:
                # resolve every meaning path
                case os.sep:
                    # /

                    curdir_folder_ptr = self.__root
                case ".":
                    # current

                    continue
                case "..":
                    # jump to parent

                    folder_ptr = curdir_folder_ptr.get_parent()

                    if folder_ptr is None:
                        continue # means at root, skip

                    curdir_folder_ptr = folder_ptr

                    continue
                case _:
                    # unknown path name, meaning it's a folder name

                    folder_ptr = curdir_folder_ptr.get_folder_in_name(path_name)

                    if folder_ptr is None:
                        raise GalfileLibs.System.Error.EnumException(
                            ErrorType.THE_DIRECTORY_IS_NOT_EXISTS
                        )

                    curdir_folder_ptr = folder_ptr

        self.__curdir_ptr = curdir_folder_ptr
        self.__curdir_path = self.__resolve_to_absolute(to_path)

        return curdir_folder_ptr

    def pwd(self):
        return self.__curdir_path

    def mkdirs(self, new_path: str | Path):
        new_path = self.__normalize_to_path(new_path)
        new_path = self.__resolve_to_absolute(new_path)
        new_path = self.__resolve_levels(new_path)

        curdir_folder_ptr = self.__root
        for path_name in new_path.parts[1:]: # skip root
            folder_ptr = curdir_folder_ptr.get_folder_in_name(path_name)

            if folder_ptr is None:
                # create new
                folder_ptr = Folder.new(path_name)
                # append to parent
                curdir_folder_ptr.append_folder(folder_ptr)

            curdir_folder_ptr = folder_ptr

        return curdir_folder_ptr

    def rmdirs(self, old_path: str | Path, ignore_dir_not_exists_error: bool = False):
        old_path = self.__normalize_to_path(old_path)
        old_path = self.__resolve_to_absolute(old_path)
        old_path = self.__resolve_levels(old_path)

        if old_path == self.__root_path:
            # root, just remove its children

            self.__root.clear()
            self.__curdir_ptr = self.__curdir_ptr
            self.__curdir_path = Path(self.__root_path)
            return

        # ke folder target
        folder_target_ptr = self.__go_to_folder(old_path, ignore_dir_not_exists_error)

        # balik ke parent
        curdir_folder_ptr: Folder = folder_target_ptr.get_parent() #type: ignore

        # hapus folder target
        curdir_folder_ptr.remove_folder(folder_target_ptr)

        # jika __curdir_path mengarah ke folder target ini maupun anaknya, ganti ke parent
        if self.__curdir_path == old_path or old_path in self.__curdir_path.parents:
            self.__curdir_path = old_path.parent
            self.__curdir_ptr = curdir_folder_ptr

    def cpdirs(self, src_dir_path: str | Path, dst_parent_dir_path: str | Path):
        src_dir_path = self.__normalize_to_path(src_dir_path)
        src_dir_path = self.__resolve_to_absolute(src_dir_path)
        src_dir_path = self.__resolve_levels(src_dir_path)

        dst_parent_dir_path = self.__normalize_to_path(dst_parent_dir_path)
        dst_parent_dir_path = self.__resolve_to_absolute(dst_parent_dir_path)
        dst_parent_dir_path = self.__resolve_levels(dst_parent_dir_path)

        if src_dir_path == dst_parent_dir_path:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_SRC_AND_DST_IS_SAME
            )

        src_dir_ptr = self.__go_to_folder(src_dir_path)

        dst_parent_dir_ptr = self.__go_to_folder(dst_parent_dir_path)

        dst_dir_ptr = src_dir_ptr.duplicate()

        dst_parent_dir_ptr.append_folder(dst_dir_ptr)

        return dst_dir_ptr

    def mvdirs(self, src_dir_path: str | Path, dst_parent_dir_path: str | Path):
        src_dir_path = self.__normalize_to_path(src_dir_path)
        src_dir_path = self.__resolve_to_absolute(src_dir_path)
        src_dir_path = self.__resolve_levels(src_dir_path)

        dst_parent_dir_path = self.__normalize_to_path(dst_parent_dir_path)
        dst_parent_dir_path = self.__resolve_to_absolute(dst_parent_dir_path)
        dst_parent_dir_path = self.__resolve_levels(dst_parent_dir_path)

        if src_dir_path == dst_parent_dir_path:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_SRC_AND_DST_IS_SAME
            )

        src_dir_ptr = self.__go_to_folder(src_dir_path)

        src_parent_dir_ptr: Folder = src_dir_ptr.get_parent() #type: ignore
        dst_parent_dir_ptr = self.__go_to_folder(dst_parent_dir_path)

        dst_parent_dir_ptr.append_folder(src_dir_ptr)
        src_parent_dir_ptr.remove_folder(src_dir_ptr)

        # jika __curdir_path mengarah ke folder target ini maupun anaknya, ganti ke parent
        if self.__curdir_path == src_dir_path or src_dir_path in self.__curdir_path.parents:
            self.__curdir_path = src_dir_path.parent
            self.__curdir_ptr = src_parent_dir_ptr

        return src_dir_ptr

    def mkfile(self, new_file_path: str | Path):
        new_file_path = self.__normalize_to_path(new_file_path)
        new_file_path = self.__resolve_to_absolute(new_file_path)
        new_file_path = self.__resolve_levels(new_file_path)

        folder_path = new_file_path.parent
        folder_ptr = self.__go_to_folder(folder_path)

        filename = new_file_path.name
        file = GalfileLibs.Filesystem.Virtual.File.File.new(filename)

        folder_ptr.append_file(file)

        return file

    def rmfile(self, old_file_path: str | Path):
        old_file_path = self.__normalize_to_path(old_file_path)
        old_file_path = self.__resolve_to_absolute(old_file_path)
        old_file_path = self.__resolve_levels(old_file_path)

        folder_path = old_file_path.parent
        folder_ptr = self.__go_to_folder(folder_path)

        filename = old_file_path.name
        file = folder_ptr.get_file_in_name(filename)

        if file is None:
            return False
        
        folder_ptr.remove_file(file)

        return True

    def cpfile(self, src_file_path: str | Path, dst_dir_path: str | Path):
        src_file_path = self.__normalize_to_path(src_file_path)
        src_file_path = self.__resolve_to_absolute(src_file_path)
        src_file_path = self.__resolve_levels(src_file_path)

        dst_dir_path = self.__normalize_to_path(dst_dir_path)
        dst_dir_path = self.__resolve_to_absolute(dst_dir_path)
        dst_dir_path = self.__resolve_levels(dst_dir_path)

        src_dir_path = src_file_path.parent

        if src_dir_path == dst_dir_path:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_SRC_AND_DST_IS_SAME
            )

        src_dir_ptr = self.__go_to_folder(src_dir_path)
        dst_dir_ptr = self.__go_to_folder(dst_dir_path)

        filename = src_file_path.name

        src_file_ptr = src_dir_ptr.get_file_in_name(filename)
        if src_file_ptr is None:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILE_IS_NOT_EXISTS
            )

        dst_file_ptr = src_file_ptr.duplicate()

        dst_dir_ptr.append_file(dst_file_ptr)

        return dst_file_ptr

    def mvfile(self, src_file_path: str | Path, dst_dir_path: str | Path):
        src_file_path = self.__normalize_to_path(src_file_path)
        src_file_path = self.__resolve_to_absolute(src_file_path)
        src_file_path = self.__resolve_levels(src_file_path)

        dst_dir_path = self.__normalize_to_path(dst_dir_path)
        dst_dir_path = self.__resolve_to_absolute(dst_dir_path)
        dst_dir_path = self.__resolve_levels(dst_dir_path)

        src_dir_path = src_file_path.parent

        if src_dir_path == dst_dir_path:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_SRC_AND_DST_IS_SAME
            )

        src_dir_ptr = self.__go_to_folder(src_dir_path)
        dst_dir_ptr = self.__go_to_folder(dst_dir_path)

        filename = src_file_path.name
        src_file_ptr = src_dir_ptr.get_file_in_name(filename)
        if src_file_ptr is None:
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILE_IS_NOT_EXISTS
            )

        dst_dir_ptr.append_file(src_file_ptr)
        src_dir_ptr.remove_file(src_file_ptr)

        return src_file_ptr

    def tree(self, dir_path: Path | str = "/"):
        dir_path = self.__normalize_to_path(dir_path)
        dir_path = self.__resolve_to_absolute(dir_path)
        dir_path = self.__resolve_levels(dir_path)

        dir_ptr = self.__go_to_folder(dir_path)

        print(Conf.colorFolder + dir_ptr.get_name() + colorama.Fore.RESET)

        self.__tree(dir_ptr)