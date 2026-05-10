from enum import Enum, auto

__all__ = [
    "ErrorType"
]

class ErrorType(Enum):
    #not found
    DIRECTORY_PATH_NOT_FOUND = auto()
    SOURCE_PATH_NOT_FOUND = auto()
    DESTINATION_PATH_NOT_FOUND = auto()
    DESTINATION_DIRECTORY_PARENT_PATH_NOT_FOUND = auto()

    #access
    PERMISSION_DENIED = auto()

    #changing
    CURRENTLY_WORKING_IN_THE_DIRECTORY = auto()

    THIS_PATH_IS_NOT_ABSOLUTE_PATH = auto()

    CANNOT_MOVE_ROOT_DIRECTORY = auto()

    #folder and file
    THE_FILEPATH_IS_DIRECTORY = auto()
    THE_PATH_HAS_ALREADY_EXISTS = auto()
    CANNOT_MAKE_DIRECTORY_TO_OVERWRITE_FILE = auto()