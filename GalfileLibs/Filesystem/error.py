from enum import Enum, auto

class Filesystem_ErrorType(Enum):
    FileNotFound = auto()
    FolderNotFound = auto()
    FileIsExists = auto()