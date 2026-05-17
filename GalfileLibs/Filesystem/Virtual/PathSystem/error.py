from enum import Enum, auto

__all__ = [
    "ErrorType"
]

class ErrorType(Enum):
    THE_PATH_IS_NOT_ABSOLUTE_PATH = auto()

    THE_DIRECTORY_IS_NOT_EXISTS = auto()
    THE_DIRECTORY_IS_A_ROOT = auto()

    THE_FILE_IS_NOT_EXISTS = auto()

    THE_SRC_AND_DST_IS_SAME = auto()