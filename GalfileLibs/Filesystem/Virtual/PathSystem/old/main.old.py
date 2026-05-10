from pathlib import Path
import copy
from GalfileLibs.System.Error import *
from .error import *
from .conf import *
import colorama

__all__ = [
    "Filesystem_Path"
]

class Filesystem_Path:
    def __init__(self):
        self._root = Path("/")
        self._curdir = copy.deepcopy(self._root)

        # /
        #  -> folder1
        #    -> folder2
        #  -> folder3
        #  -> folder4
        self._directories: dict[Path, list[str]] = {
            self._root: []
        }

    def _resolve_levels(self, p: Path):
        if not self._is_absolute(p):
            raise EnumException(
                ErrorType.THIS_PATH_IS_NOT_ABSOLUTE_PATH
            )

        paths = p.parts

        curdir = copy.deepcopy(self._root) # start from root
        for path in paths:
            match path:
                case ".":
                    continue
                case "..":
                    curdir = curdir.parent
                case _:
                    curdir = curdir.joinpath(path)

        return curdir

    def _is_absolute(self, p: Path):
        p_s = str(p)
        root_s = str(self._root)

        if p_s.startswith(root_s):
            return True
        
        return False

    def _resolve_to_absolute(self, path: Path):
        if not self._is_absolute(path):
            path = self._curdir.joinpath(path)

        return path

    def mkdirs(self, new_path: str | Path):
        if type(new_path) == str:
            new_path = Path(new_path)

        # temp
        curdir: Path = Path("")
        if self._is_absolute(new_path): # type: ignore
            curdir = copy.deepcopy(self._root)
        else:
            curdir = copy.deepcopy(self._curdir)

        paths = new_path.parts #type: ignore
        paths_result: list[Path] = []
        for path in paths:
            match path:
                case ".":
                    continue
                case "..":
                    curdir = curdir.parent
                    continue
                case _:
                    curdir = curdir.joinpath(path)

            path_s = path
            path = Path(path)

            # parent
            if curdir.parent not in self._directories:
                self._directories[curdir.parent] = []

                paths_result.append(curdir.parent)

            # member and not root
            if path_s not in self._directories[curdir.parent] and path_s != str(self._root):
                self._directories[curdir.parent].append(path_s)

            # current
            if curdir not in self._directories:
                self._directories[curdir] = []

                paths_result.append(curdir)

        return paths_result

    def __rmdirs_recursive(self, target: Path, old_paths_result: list[Path]):
        parent = target.parent
        children = self._directories[target]

        old_paths_result.append(target)

        # parent
        if parent in self._directories:
            self._directories[parent].remove(target.name)

        # target
        self._directories.pop(target)

        # children
        if children == []:
            return

        for child in children:
            self.__rmdirs_recursive(target.joinpath(child), old_paths_result)

    def rmdirs(self, old_path: str | Path):
        if type(old_path) == str:
            old_path = Path(old_path)

        old_path_s = str(old_path)

        old_paths_result: list[Path] = []

        if old_path_s == str(self._root):
            #reset all
            self.__init__()

            old_paths_result.append(self._root)
            return old_paths_result

        if old_path_s == str(self._curdir):
            raise EnumException(
                ErrorType.CURRENTLY_WORKING_IN_THE_DIRECTORY
            )

        target = self._resolve_to_absolute(old_path) #type: ignore
        target = self._resolve_levels(target)

        if target in self._directories:
            self.__rmdirs_recursive(target, old_paths_result)

        return old_paths_result

    def cd(self, path: str | Path):
        if type(path) == str:
            path = Path(path)

        curdir = copy.deepcopy(self._curdir)

        paths = path.parts # type: ignore
        for path in paths:
            match path:
                case ".":
                    continue
                case "..":
                    curdir = curdir.parent
                case "/":
                    curdir = copy.deepcopy(self._root)
                case _:
                    curdir = curdir.joinpath(path)

            if curdir not in self._directories:
                raise EnumException(
                    ErrorType.DIRECTORY_PATH_NOT_FOUND
                )

        self._curdir = curdir

    def pwd(self):
        return str(self._curdir)

    def __tree_recursive_generator(self, p: Path, indent: int, buffer_indent_begin = ""):
        paths = self._directories[p]

        indent_arrow = ("-" * indent) + ">"
        indent_spaces = " " * indent

        last_index = len(paths)-1

        for index, path in enumerate(paths):
            full_path = p.joinpath(path)

            #colorize
            color = Conf.colorFile
            if self.isDir(full_path):
                color = Conf.colorFolder

            #text
            str_path = color + path + colorama.Fore.RESET

            text = str_path

            yield buffer_indent_begin + "|" + indent_arrow + text

            #recursive
            if not self.isDir(full_path):
                continue

            next_buffer_indent_begin = ""
            if index == last_index:
                next_buffer_indent_begin = buffer_indent_begin + " " + indent_spaces
            else:
                next_buffer_indent_begin = buffer_indent_begin + "|" + indent_spaces

            next_buffer_indent_begin += " "

            for string in self.__tree_recursive_generator(full_path, indent, next_buffer_indent_begin):
                yield string

    def __tree_generator(self, path: str | Path | None = None, indent: int = 4):
        yield f"{Conf.colorFolder}.{colorama.Fore.RESET}"

        for string in self.__tree_recursive_generator(path, indent): # type: ignore
            yield string

    def tree(self, path: str | Path | None = None, indent = 4):
        if path is None:
            path = copy.deepcopy(self._curdir)
        if type(path) == str:
            path = Path(path)

        path = self._resolve_to_absolute(path) #type: ignore
        path = self._resolve_levels(path)

        print(path)

        for string in self.__tree_generator(path, indent):
            print(string)

    def touch(self, filepath: str | Path) -> Path:
        if type(filepath) == str:
            filepath = Path(filepath)

        filepath = self._resolve_to_absolute(filepath) #type: ignore
        filepath = self._resolve_levels(filepath)

        directory: Path = filepath.parent #type: ignore
        filename: str = filepath.name #type: ignore

        if not self.isDir(directory):
            raise EnumException(
                ErrorType.DIRECTORY_PATH_NOT_FOUND
            )

        cursor = self._directories[directory]
        cursor.append(filename)

        return filepath #type: ignore

    def isFile(self, path: str | Path):
        if type(path) == str:
            path = Path(path)

        path = self._resolve_to_absolute(path) #type: ignore
        path = self._resolve_levels(path)

        directory: Path = path.parent #type: ignore
        target_filename: str = path.name #type: ignore

        # is directory path
        if self.isDir(path):
            return False

        # is parent doesn't exists
        if not self.isDir(directory):
            return False

        # is file doesn't exists
        if target_filename not in self._directories[directory]:
            return False

        return True

    def isDir(self, path: str | Path):
        if type(path) == str:
            path = Path(path)

        path = self._resolve_to_absolute(path) #type: ignore
        path = self._resolve_levels(path)

        if path not in self._directories:
            return False

        return True

    def isExists(self, path: str | Path):
        if type(path) == str:
            path = Path(path)

        if not self.isDir(path) and not self.isFile(path):
            return False

        return True

    def __cp_mv_operation_begin(self, src_path: Path, dst_path: Path):
        # if src_path is dir:
        #   if dst_path is dir, then src_path joinpath to dst_path
        #   if dst_path is file, then error because can't overwrite directory to file
        #   if dst_path isn't exists but directory exists, then make the name become dst_name
        # if src_path is file:
        #   if dst_path is dir, then src_path joinpath to dst_path
        #   if dst_path is file, then make the src_name become the dst_name (overwrite)
        #   if dst_path isn't exists but directory exists, then make the name become dst_name
        pass

    def __cp_dir_copy_recursive(self, src_path: Path, directories_temp: dict[Path, list[str]]):
        src_children = self._directories[src_path]

        # directories_temp[cursor_path].append(src_path.name)
        if src_path not in directories_temp:
            directories_temp[src_path] = copy.deepcopy(src_children)

        for src_child in src_children:
            src_child = src_path.joinpath(src_child)

            if src_child in self._directories:
                self.__cp_dir_copy_recursive(src_child, directories_temp)

    def __cp_dir_paste_recursive(self, dst_path: Path, directories_temp: dict[Path, list[str]], cursor_path: Path):
        new_path = dst_path.joinpath(cursor_path.name)
        cursor_path_children = directories_temp[cursor_path]

        new_path_parent = new_path.parent
        new_path_parent_children = self._directories[new_path_parent]

        if new_path.name not in new_path_parent_children:
            new_path_parent_children.append(new_path.name)

        self._directories[new_path] = cursor_path_children

        for cursor_path_child in cursor_path_children:
            cursor_path_child = cursor_path.joinpath(cursor_path_child)

            if not self.isDir(cursor_path_child):
                continue

            self.__cp_dir_paste_recursive(new_path, directories_temp, cursor_path_child)

    def cp(self, src_path: str | Path, dst_path: str | Path):
        if type(src_path) == str:
            src_path = Path(src_path)
        if type(dst_path) == str:
            dst_path = Path(dst_path)

        src_path = self._resolve_to_absolute(src_path) #type:ignore
        dst_path = self._resolve_to_absolute(dst_path) #type:ignore

        src_path = self._resolve_levels(src_path)
        dst_path = self._resolve_levels(dst_path)
        
        if not self.isDir(dst_path):
            raise EnumException(
                ErrorType.DESTINATION_PATH_NOT_FOUND
            )

        if self.isDir(src_path):
            #hindari masalah penyalinan rekursif tanpa batas

            directories_temp: dict[Path, list[str]] = {}

            self.__cp_dir_copy_recursive(src_path, directories_temp)
            cursor_path = self._root.joinpath(src_path.name)
            self.__cp_dir_paste_recursive(dst_path, directories_temp, cursor_path)

        elif self.isFile(src_path):
            dst_directory = dst_path.parent
            dst_directory_children = self._directories[dst_directory]

            if not self.isDir(dst_directory):
                raise EnumException(
                    ErrorType.DESTINATION_DIRECTORY_PARENT_PATH_NOT_FOUND
                )

            dst_directory_children.append(src_path.name)
        else:
            raise EnumException(
                ErrorType.SOURCE_PATH_NOT_FOUND
            )

    # can be move, can be rename
    def mv(self, src_path: str | Path, dst_path: str | Path):
        if type(src_path) == str:
            src_path = Path(src_path)
        if type(dst_path) == str:
            dst_path = Path(dst_path)

        src_path = self._resolve_to_absolute(src_path) #type:ignore
        dst_path = self._resolve_to_absolute(dst_path) #type:ignore

        src_path = self._resolve_levels(src_path)
        dst_path = self._resolve_levels(dst_path)

        if str(src_path) == str(self._root):
            raise EnumException(
                ErrorType.CANNOT_MOVE_ROOT_DIRECTORY
            )

        if self.isDir(src_path):
            pass
        elif self.isFile(src_path):
            src_directory = src_path.parent
            src_directory_children = self._directories[src_directory]

            dst_directory = dst_path.parent
            dst_directory_children = self._directories[dst_directory]

            if not self.isDir(dst_directory):
                raise EnumException(
                    ErrorType.DESTINATION_DIRECTORY_PARENT_PATH_NOT_FOUND
                )

            src_name = src_path.name
            dst_name = dst_path.name

            src_directory_children.remove(src_name)
            dst_directory_children.append(dst_name)
        else:
            raise EnumException(
                ErrorType.SOURCE_PATH_NOT_FOUND
            )