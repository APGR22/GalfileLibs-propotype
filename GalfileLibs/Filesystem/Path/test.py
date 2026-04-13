from GalfileLibs.Filesystem.Path import *
# from GalfileLibs.Filesystem import *

path = VirtPath()
path.mkdirs("azhar5/tes/what")
path.mkdirs("azhar/tes/what")
path.mkdirs("azhar/wh/at")
path.mkdirs("azhar/to")
path.touch("azhar/to/op")
path.touch("azhar/to/op5")
# path.rmdirs("/azhar")
path.tree("/")

# for path_name, path_dir in path._folder_pointers.items():
#     print(path_name, "\t\t", path_dir.__class__, end="\n")

path.cp("/azhar/to", "/azhar/tes")
# path.cp("/azhar/to", "/azhar/to/op")
path.cp("/azhar/to", "/azhar/to/to")

path.cp("/azhar/to/op", "/azhar/tes")
path.cp("/azhar/to/op", "/azhar/to5")
path.cp("/azhar/to/op", "/azhar/to/to")

path.mv("/azhar/to/op", "/azhar/to/op_renamed")
path.mv("/azhar/wh", "/azhar5")

path.tree("/")