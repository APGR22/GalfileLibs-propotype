from enum import Enum

__all__ = [
    "Exception",
    "EnumException"
]

class Exception(BaseException):
    def __init__(self, text: str):
        raise BaseException(text)

class EnumException(BaseException):
    def __init__(self, value: Enum):
        raise BaseException(f"{value.name}: {value.value}")