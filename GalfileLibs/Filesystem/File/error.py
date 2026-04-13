from enum import Enum, auto

__all__ = [
    "ErrorType"
]

class ErrorType(Enum):
    TRY_TO_DUPLICATE_WITH_SAME_FILEPATH = auto()
    TRY_TO_OVERWRITE_WITH_EXISTING_FILE = auto()
    THE_FILEPATH_IS_NOT_FOUND = auto()
    THE_DIRECTORY_IS_NOT_FOUND = auto()