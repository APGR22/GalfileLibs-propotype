import GalfileLibs
from pathlib import Path
import platform

if platform.system() == "Windows":
    dir_path = Path("E:/Programs/Projects/File Manager/Cloud/Galfile/Library/test")
else:
    dir_path = Path("/run/media/azhar/Programs/Programs/Projects/File Manager/Cloud/Galfile/Library/test")

file_path = dir_path.joinpath("tes.txt")

filesystem = GalfileLibs.Filesystem.Virtual.PathSystem.VirtualPathSystem.new()

filesystem.mkdirs("/run/media/azhar")

filesystem.cd("/run/media/azhar")
print(filesystem.pwd())

filesystem.rmdirs("/run/media")
print(filesystem.pwd())