import GalfileLibs
from pathlib import Path
import platform

if platform.system() == "Windows":
    dir_path = Path("E:/Programs/Projects/File Manager/Cloud/Galfile/Library/test")
else:
    dir_path = Path("/run/media/azhar/Programs/Programs/Projects/File Manager/Cloud/Galfile/Library/test")

file_path = dir_path.joinpath("tes.txt")

file = GalfileLibs.Filesystem.Virtual.File.File.new("nama file")
file.write(b"azhar")