import GalfileLibs
from pathlib import Path
import platform

if platform.system() == "Windows":
    dir_path = Path("E:/Programs/Projects/File Manager/Cloud/Galfile/Library/test")
else:
    dir_path = Path("/run/media/azhar/Programs/Programs/Projects/File Manager/Cloud/Galfile/Library/test")

file = GalfileLibs.Filesystem.File.File.new("to.txt", dir_path, True)

file.save_to_local()
file.rename("tes.txt", True)
file.write(b"Halo")
file.save_to_local()

# file.remove()

# print(file.get_stat())

folder = GalfileLibs.Filesystem.Folder.Folder.new("folder_test")

folder.append_file(file)
folder.append_file(file)
folder.print_files()

file.remove()

# masih mengembangkan Folder