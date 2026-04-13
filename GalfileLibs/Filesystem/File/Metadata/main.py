from pathlib import Path

__all__ = [
    "Metadata"
]

class Metadata:
    "Nanti dilanjutkan setelah selesai dengan class File"
    __metadata_path: Path

    def __init__(
        self,
        metadata_path: Path
    ):
        self.__metadata_path = metadata_path