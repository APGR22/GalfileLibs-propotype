from .error import *
import GalfileLibs
from pathlib import Path
from .conf import *

__all__ = [
    "Filesystem"
]

class Filesystem:
    #data-data file hingga metadata file/folder, disimpan di penyimpanan lokal dan diambil dengan pointer

    _path = GalfileLibs.Filesystem.Path.VirtPath()

    _folders: dict[Path, GalfileLibs.Filesystem.Folder.Folder] = {}
    _files: dict[Path, GalfileLibs.Filesystem.File.File] = {}

    _working_dir: Path

    __conf: Filesystem_Conf

    def __init__(self, working_dir_path: Path):
        self._working_dir = working_dir_path.joinpath("GalfileFilesystem")

        if not self._working_dir.is_dir():
            self._working_dir.mkdir(parents=True)

        self.__conf = Filesystem_Conf(self._working_dir)

    def isdir(self, path: str | Path):
        path = self._path._str_to_path(path)
        path = self._path._resolve_to_absolute(path)
        path = self._path._resolve_levels(path)

        return path in self._folders

    def isfile(self, path: str | Path):
        path = self._path._str_to_path(path)
        path = self._path._resolve_to_absolute(path)
        path = self._path._resolve_levels(path)

        return path in self._files

    def isexists(self, path: str | Path):
        return self.isdir(path) or self.isfile(path)

    def mkdirs(self, new_path: str | Path):
        new_paths_result = self._path.mkdirs(new_path)

        for path in new_paths_result:
            self._folders[path] = GalfileLibs.Filesystem.Folder.Folder()

    def rmdirs(self, old_path: str | Path):
        ret = self._path.rmdirs(old_path)
        if ret is None:
            # clear all because root is removed
            return

        old_paths_result = ret

        for path in old_paths_result:
            if self.isdir(path):
                self._folders.pop(path)
            else: # file
                self._files.pop(path)

    def mkfile(self, filepath: str | Path, overwrite: bool = False):
        is_new, new_filepath = self._path.touch(filepath)

    def rmfile(self, filepath: str | Path):
        ret = self._path.rmfile(filepath)
        if ret is None: # the file has removed or not created yet
            return

        old_filepath = ret

        self._files.pop(old_filepath)

    def cp(self, src_path: str | Path, dst_path: str | Path):
        old_paths_result, new_paths_result = self._path.cp(src_path, dst_path)

        for old_path, new_path in zip(old_paths_result, new_paths_result):
            if self.isdir(old_path):
                old_folder_ptr = self._folders[old_path]
                new_folder_ptr = old_folder_ptr.copy()

                self._folders[new_path] = new_folder_ptr
            else: # file
                old_file_ptr = self._files[old_path]
                new_file_ptr = old_file_ptr.duplicate(new_path.name)

                self._files[new_path] = new_file_ptr

    def mv(self, src_path: str | Path, dst_path: str | Path):
        old_paths_result, new_paths_result = self._path.mv(src_path, dst_path)

        for old_path, new_path in zip(old_paths_result, new_paths_result):
            if self.isdir(old_path):
                folder_moved_ptr = self._folders[old_path]

                self._folders.pop(old_path)

                self._folders[new_path] = folder_moved_ptr
            else: # file
                file_moved_ptr = self._files[old_path]

                self._files.pop(old_path)

                self._files[new_path] = file_moved_ptr

    def cd(self, path: str | Path):
        self._path.cd(path)

    def pwd(self):
        return self._path.pwd()

    def tree(self, path: str | Path | None = None, indent = 4):
        self._path.tree(path, indent)