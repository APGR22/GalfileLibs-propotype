from enum import Enum, auto

__all__ = [
    "ErrorType"
]

class ErrorType(Enum):
    THE_FILE_IS_ALREADY_EXISTED = auto()
    THE_FOLDER_IS_ALREADY_EXISTED = auto()
    THE_FOLDER_IS_POINTING_TO_SAME_ADDRESS = auto()