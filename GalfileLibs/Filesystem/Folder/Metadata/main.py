from pathlib import Path

__all__ = [
    "Filesystem_Folder_Metadata"
]

class Filesystem_Folder_Metadata:
    __metadata_path: Path

    

    def __init__(
        self,
        metadata_path: Path
    ):
        self.__metadata_path = metadata_path