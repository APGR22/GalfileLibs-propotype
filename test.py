import GalfileLibs
from pathlib import Path
import platform

if platform.system() == "Windows":
    dir_path = Path("E:/Programs/Projects/File Manager/Cloud/Galfile/Library/test")
else:
    dir_path = Path("/run/media/azhar/Programs/Programs/Projects/File Manager/Cloud/Galfile/Library/test")

file_path = dir_path.joinpath("tes.txt")

file = GalfileLibs.Filesystem.Virtual.File.File.new("nama file")
file.write(b"isi file dengan berbagai konten")

folder = GalfileLibs.Filesystem.Virtual.Folder.Folder.new("nama folder")
folder.append_file(file)

file_ptr = folder.get_file(file.get_name())
print(file_ptr is file)

print(folder.get_tree_size())

file2 = GalfileLibs.Filesystem.Virtual.File.File.new("nama file 2")
file2.write(file.read())

folder2 = GalfileLibs.Filesystem.Virtual.Folder.Folder.new("nama folder 2")
folder2.append_file(file2)

folder.append_folder(folder2)

print(folder.get_tree_size())

folder_1 = folder.duplicate()
folder2.append_folder(folder_1)

print(folder.get_tree_size())