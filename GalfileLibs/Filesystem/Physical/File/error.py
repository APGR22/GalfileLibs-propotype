from enum import Enum, auto

__all__ = [
    "ErrorType"
]

class ErrorType(Enum):
    THE_FILEPATH_IS_NOT_EXISTED = auto()
    THE_FILEPATH_IS_EXISTED = auto()
    THE_DIRECTORY_IS_NOT_EXISTED = auto()