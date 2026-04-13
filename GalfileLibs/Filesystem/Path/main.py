from pathlib import Path
import copy
from .error import *
import GalfileLibs
from dataclasses import dataclass
from .conf import *
import colorama

__all__ = [
    "VirtPath"
]

@dataclass
class Filesystem_PathContent:
    name: str
    folders: dict[str, Filesystem_PathContent]
    files: list[str]
    parent: Filesystem_PathContent | None

class VirtPath:
    _root_path_s = "/"
    _root_path = Path(_root_path_s)

    # apakah perlu ketergantungan atau sendiri-sendiri seperti sebelumnya?
    # mending sendiri-sendiri saja

    # on "/"
    _directories: dict[str, Filesystem_PathContent] = {}

    _folder_pointers: dict[Path, Filesystem_PathContent] = {}

    def __init__(self):
        self.init()

    def init(self):
        self._directories[self._root_path_s] = self.__new_directory(self._root_path_s)

        self._root_dir = self._directories[self._root_path_s]
        self._folder_pointers[self._root_path] = self._root_dir

        self._curdir_path = copy.deepcopy(self._root_path)
        self._curdir_dir = self._root_dir

    def __reset(self):
        self._directories.clear()
        self._folder_pointers.clear()

        self.init()

    def __new_directory(
            self,
            name: str,
            parent: Filesystem_PathContent | None = None
        ) -> Filesystem_PathContent:
        dir_ptr = Filesystem_PathContent(
            name = name,
            folders = {},
            files = [],
            parent = parent # type: ignore
        )

        return dir_ptr

    def _str_to_path(self, path: str | Path) -> Path:
        if type(path) == str:
            path = Path(path)

        return path #type: ignore

    def _is_absolute(self, p: Path):
        path_s = str(p)

        if path_s.startswith(self._root_path_s):
            return True

        return False

    def _resolve_levels(self, p: Path):
        if not self._is_absolute(p):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THIS_PATH_IS_NOT_ABSOLUTE_PATH
            )

        paths = p.parts

        curdir = copy.deepcopy(self._root_path) # start from root
        for path in paths:
            match path:
                case ".":
                    continue
                case "..":
                    curdir = curdir.parent
                case _:
                    curdir = curdir.joinpath(path)

        return curdir

    def _resolve_to_absolute(self, path: Path):
        if not self._is_absolute(path):
            path = self._curdir_path.joinpath(path)

        return path

    def _remove_root_part(self, path: Path):
        if not self._is_absolute(path):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THIS_PATH_IS_NOT_ABSOLUTE_PATH
            )

        path_s = str(path)

        path_s = path_s[1:]
        path = Path(path_s)

        return path

    def _is_path_root(self, path: Path):
        return str(path) == self._root_path_s

    def isdir(self, path: str | Path):
        path = self._str_to_path(path)
        path = self._resolve_to_absolute(path)
        path = self._resolve_levels(path)

        return path in self._folder_pointers

    def isfile(self, path: str | Path):
        path = self._str_to_path(path)
        path = self._resolve_to_absolute(path)
        path = self._resolve_levels(path)

        if self._is_path_root(path):
            return False

        if self.isdir(path):
            return False

        if not self.isdir(path.parent):
            return False

        path_parent_ptr = self._folder_pointers[path.parent]

        return path.name in path_parent_ptr.files

    def isexists(self, path: str | Path):
        path = self._str_to_path(path)
        path = self._resolve_to_absolute(path)
        path = self._resolve_levels(path)

        return self.isdir(path) or self.isfile(path)

    def mkdirs(self, new_path: str | Path):
        new_path = self._str_to_path(new_path)
        new_path = self._resolve_to_absolute(new_path)
        new_path = self._resolve_levels(new_path)

        if self._is_path_root(new_path):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.PERMISSION_DENIED
            )

        new_path = self._remove_root_part(new_path)

        parent_dir_ptr = self._root_dir
        full_path = copy.deepcopy(self._root_path)

        new_paths_result: list[Path] = []

        for path_name in new_path.parts:
            if path_name not in parent_dir_ptr.folders:
                parent_dir_ptr.folders[path_name] = self.__new_directory(path_name, parent_dir_ptr)

            # next

            parent_dir_ptr = parent_dir_ptr.folders[path_name]
            full_path = full_path.joinpath(path_name)

            if full_path not in self._folder_pointers:
                self._folder_pointers[full_path] = parent_dir_ptr

                new_paths_result.append(full_path)

        return new_paths_result

    def __rmdirs_recursive(
            self,
            cursor_parent_dir_ptr: Filesystem_PathContent,
            parent_path: Path,
            old_paths_result: list[Path] | None = None
        ):
        if old_paths_result is None:
            old_paths_result = []

        self._folder_pointers.pop(parent_path)

        old_paths_result.append(parent_path) # folder
        # files
        for filename in cursor_parent_dir_ptr.files:
            old_paths_result.append(parent_path.joinpath(filename))

        for child_dir_name, child_dir_ptr in cursor_parent_dir_ptr.folders.items():
            path = parent_path.joinpath(child_dir_name)

            if path not in self._folder_pointers:
                continue

            self.__rmdirs_recursive(
                child_dir_ptr,
                path,
                old_paths_result
            )

    def rmdirs(self, old_path: str | Path):
        old_path = self._str_to_path(old_path)
        old_path = self._resolve_to_absolute(old_path)
        old_path = self._resolve_levels(old_path)

        old_paths_result: list[Path] = []

        if self._is_path_root(old_path):
            # just reset bro
            self.__reset()
            return

        # the user want has removed or not created yet
        if old_path not in self._folder_pointers:
            return old_paths_result

        dir_parent_ptr: Filesystem_PathContent = self._folder_pointers[old_path].parent # type: ignore

        #start from target
        cursor_dir_ptr = self._folder_pointers[old_path]
        full_path = copy.deepcopy(old_path)

        self.__rmdirs_recursive(
            cursor_dir_ptr,
            full_path,
            old_paths_result
        )

        dir_parent_ptr.folders.pop(old_path.name)

        return old_paths_result

    def __cp_mv_operation_begin(self, src_path: Path, dst_path: Path):
        """
        :returns:
            src_path is exists\n
            dst_path has dst_name
        """

        # if src_path is dir:
        #   if dst_path is dir, then src_path joinpath to dst_path
        #   if dst_path is file, then error because can't overwrite directory to file
        #   if dst_path isn't exists but directory exists, then make the name become dst_name
        # if src_path is file:
        #   if dst_path is dir, then src_path joinpath to dst_path
        #   if dst_path is file, then make the src_name become the dst_name (overwrite)
        #   if dst_path isn't exists but directory exists, then make the name become dst_name

        if not self.isdir(dst_path.parent):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.DESTINATION_DIRECTORY_PARENT_PATH_NOT_FOUND
            )

        if self.isdir(src_path):
            if self.isfile(dst_path):
                raise GalfileLibs.System.Error.EnumException(
                    ErrorType.CANNOT_MAKE_DIRECTORY_TO_OVERWRITE_FILE
                )
        elif self.isfile(src_path):
            if self.isfile(dst_path):
                dst_path = dst_path.parent.joinpath(src_path.name) #overwrite
        else: #doesn't exists
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.SOURCE_PATH_NOT_FOUND
            )

        if self.isdir(dst_path):
            dst_path = dst_path.joinpath(src_path.name)
            # print(dst_path)

        return (src_path, dst_path)

    def __cp_mv_update_new_labels_recursive(
            self,
            dst_path: Path,
            dst_dir_ptr: Filesystem_PathContent,
            new_paths_result: list[Path] | None = None
        ):
        if new_paths_result is None:
            new_paths_result = []

        self._folder_pointers[dst_path] = dst_dir_ptr

        dst_dir_ptr.parent = self._folder_pointers[dst_path.parent]

        new_paths_result.append(dst_path) # folder

        # files
        for filename in dst_dir_ptr.files:
            new_paths_result.append(dst_path.joinpath(filename))

        # next
        for folder_name, folder_dir_ptr in dst_dir_ptr.folders.items():
            self.__cp_mv_update_new_labels_recursive(
                dst_path.joinpath(folder_name),
                folder_dir_ptr,
                new_paths_result
            )

    def __cp_get_old_labels_recursive(
            self,
            src_path: Path,
            src_dir_ptr: Filesystem_PathContent,
            old_paths_result: list[Path]
        ):
        old_paths_result.append(src_path) # folder

        # files
        for file_name in src_dir_ptr.files:
            old_paths_result.append(src_path.joinpath(file_name))

        # next
        for folder_name in src_dir_ptr.folders:
            self.__cp_get_old_labels_recursive(
                src_path.joinpath(folder_name),
                src_dir_ptr.folders[folder_name],
                old_paths_result
            )

    def cp(self, src_path: str | Path, dst_path: str | Path):
        src_path = self._str_to_path(src_path)
        src_path = self._resolve_to_absolute(src_path)
        src_path = self._resolve_levels(src_path)

        dst_path = self._str_to_path(dst_path)
        dst_path = self._resolve_to_absolute(dst_path)
        dst_path = self._resolve_levels(dst_path)

        src_path, dst_path = self.__cp_mv_operation_begin(src_path, dst_path)

        dst_parent_dir_ptr = self._folder_pointers[dst_path.parent]
        dst_name = dst_path.name

        new_paths_result: list[Path] = []
        old_paths_result: list[Path] = []

        if self.isdir(src_path):
            src_dir_ptr = self._folder_pointers[src_path]

            self.__cp_get_old_labels_recursive(
                src_path,
                src_dir_ptr,
                old_paths_result
            )

            dir_copied_ptr = copy.deepcopy(src_dir_ptr)

            dir_copied_ptr.name = dst_name
            dst_parent_dir_ptr.folders[dst_name] = dir_copied_ptr

            # start from dst result
            self.__cp_mv_update_new_labels_recursive(
                dst_path,
                dir_copied_ptr,
                new_paths_result
            )
        else: # file
            dst_parent_dir_ptr.files.append(dst_name)

            new_paths_result.append(dst_path)

        return (old_paths_result, new_paths_result)

    def __mv_remove_old_labels_recursive(
            self,
            src_path: Path,
            src_dir_ptr: Filesystem_PathContent,
            old_paths_result: list[Path] | None = None
        ):
        if old_paths_result is None:
            old_paths_result = []

        self._folder_pointers.pop(src_path)

        old_paths_result.append(src_path) # folder

        # files
        for filename in src_dir_ptr.files:
            old_paths_result.append(src_path.joinpath(filename))

        # next
        for folder_name, folder_dir_ptr in src_dir_ptr.folders.items():
            self.__mv_remove_old_labels_recursive(
                src_path.joinpath(folder_name),
                folder_dir_ptr,
                old_paths_result
            )

    def mv(self, src_path: str |Path, dst_path: str | Path):
        src_path = self._str_to_path(src_path)
        src_path = self._resolve_to_absolute(src_path)
        src_path = self._resolve_levels(src_path)

        dst_path = self._str_to_path(dst_path)
        dst_path = self._resolve_to_absolute(dst_path)
        dst_path = self._resolve_levels(dst_path)

        src_path, dst_path = self.__cp_mv_operation_begin(src_path, dst_path)

        src_parent_dir_ptr = self._folder_pointers[src_path.parent]

        dst_parent_dir_ptr = self._folder_pointers[dst_path.parent]
        dst_name = dst_path.name

        old_paths_result: list[Path] = []
        new_paths_result: list[Path] = []

        if self.isdir(src_path):
            dir_moved_ptr = self._folder_pointers[src_path]
            src_parent_dir_ptr.folders.pop(src_path.name)

            self.__mv_remove_old_labels_recursive(
                src_path, 
                self._folder_pointers[src_path], 
                old_paths_result
            )

            dir_moved_ptr.name = dst_name
            dir_moved_ptr.parent = dst_parent_dir_ptr

            dst_parent_dir_ptr.folders[dst_name] = dir_moved_ptr

            # start from dst result
            self.__cp_mv_update_new_labels_recursive(dst_path, dir_moved_ptr, new_paths_result)
        else: # file
            src_parent_dir_ptr.files.remove(src_path.name)
            dst_parent_dir_ptr.files.append(dst_name)

            old_paths_result.append(src_path)
            new_paths_result.append(dst_path)

        return (old_paths_result, new_paths_result)

    def touch(self, filepath: str | Path):
        filepath = self._str_to_path(filepath)
        filepath = self._resolve_to_absolute(filepath)
        filepath = self._resolve_levels(filepath)

        if self._is_path_root(filepath):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.PERMISSION_DENIED
            )

        if self.isfile(filepath):
            return (False, filepath)

        if not self.isdir(filepath.parent):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.DESTINATION_DIRECTORY_PARENT_PATH_NOT_FOUND
            )

        if self.isdir(filepath):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILEPATH_IS_DIRECTORY
            )

        parent_dir_ptr = self._folder_pointers[filepath.parent]
        parent_dir_ptr.files.append(filepath.name)

        return (True, filepath)

    def rmfile(self, old_filepath: str | Path):
        old_filepath = self._str_to_path(old_filepath)
        old_filepath = self._resolve_to_absolute(old_filepath)
        old_filepath = self._resolve_levels(old_filepath)

        # termasuk root
        if self.isdir(old_filepath):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.THE_FILEPATH_IS_DIRECTORY
            )

        if not self.isdir(old_filepath.parent):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.DIRECTORY_PATH_NOT_FOUND
            )

        # that user want and do nothing
        if not self.isfile(old_filepath):
            return None

        old_filepath_parent_dir_ptr = self._folder_pointers[old_filepath.parent]
        old_filepath_parent_dir_ptr.files.remove(old_filepath.name)

        return old_filepath

    def cd(self, path: str | Path):
        path = self._str_to_path(path)
        path = self._resolve_to_absolute(path)
        path = self._resolve_levels(path)

        if not self.isdir(path):
            raise GalfileLibs.System.Error.EnumException(
                ErrorType.DIRECTORY_PATH_NOT_FOUND
            )

        self._curdir_dir = self._folder_pointers[path]
        self._curdir_path = path

    def pwd(self):
        return self._curdir_path

    def __tree_recursive(
            self,
            cursor: Filesystem_PathContent,
            indent: int,
            buffer_indent_begin: str = ""
        ):
        space = " "
        indent_arrow = ("-" * indent) + ">" + space
        indent_spaces = (" " * indent) + (space * 2)

        buffer_member_indent_begin = buffer_indent_begin + "|" + indent_arrow
        buffer_next_indent_begin = buffer_indent_begin + "|" + indent_spaces
        buffer_next_last_indent_begin = buffer_indent_begin + " " + indent_spaces

        #must cached first to sorted for nice print tree
        list_items: dict[str, Filesystem_PathContent | str] = {}
        list_items_length = 0

        for folder in cursor.folders.keys():
            list_items[folder] = cursor.folders[folder]
            list_items_length += 1

        for file in cursor.files:
            list_items[file] = ""
            list_items_length += 1

        index = 0
        last_index = list_items_length - 1
        for key_name, value in sorted(list_items.items(), key=lambda item: item[0]):
            name = key_name + colorama.Fore.RESET
            text = buffer_member_indent_begin

            #if file
            if value == "":
                name = Conf.colorFile + name
                text += name
                print(text)
                continue

            #folder
            name = Conf.colorFolder + name
            text += name
            print(text)

            #next because of folder
            if index == last_index:
                self.__tree_recursive(
                    cursor.folders[key_name],
                    indent,
                    buffer_next_last_indent_begin
                )
            else:
                self.__tree_recursive(
                    cursor.folders[key_name],
                    indent,
                    buffer_next_indent_begin
                )

            index += 1

    def tree(self, path: str | Path | None = None, indent: int = 4):
        if path is None:
            path = self._curdir_path

        path = self._str_to_path(path)
        path = self._resolve_to_absolute(path)
        path = self._resolve_levels(path)

        path_name = path.name
        if self._is_path_root(path):
            path_name = self._root_path_s

        text = Conf.colorFolder + path_name + colorama.Fore.RESET
        print(text)

        cursor = self._folder_pointers[path]
        self.__tree_recursive(cursor, indent)
