import GalfileLibs
from pathlib import Path
import platform

from GalfileLibs.Filesystem.Virtual.File.main import File

if platform.system() == "Windows":
    dir_path = Path("E:/Programs/Projects/File Manager/Cloud/Galfile/Library/test")
else:
    dir_path = Path("/run/media/azhar/Programs/Programs/Projects/File Manager/Cloud/Galfile/Library/test")

file_path = dir_path.joinpath("tes.txt")

filesystem = GalfileLibs.Filesystem.Virtual.PathSystem.VirtualPathSystem.new()

filesystem.mkdirs("run/media/azhar/Windows")
filesystem.mkdirs("run/media/azhar/Linux")

filesystem.cd("run/media/azhar")

file_ptr = filesystem.mkfile("Windows/azhar_file")

file_ptr.write(b"Halo")

file_cp_ptr = filesystem.cpfile("Windows/azhar_file", "Linux")

file_ptr.write(b"H")
file_cp_ptr.write(b"konni")

filesystem.mvdirs("Windows", "../../")

filesystem.tree()

root_ptr = filesystem.cd("/")
root_json = root_ptr.dump_json()

root_back = GalfileLibs.Filesystem.Virtual.Folder.Folder.from_load_json(root_json)

# print(root_back.get_folder_in_name("run").get_folder_in_name("media").get_parent().get_name()) #type: ignore

filesystem.cd("run/media/azhar")
filesystem_json = filesystem.dump_json()

filesystem_back = GalfileLibs.Filesystem.Virtual.PathSystem.VirtualPathSystem.from_load_json(filesystem_json)

print(filesystem_back.cd(".").get_name())