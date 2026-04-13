from pathlib import Path

__all__ = [
    "Filesystem_Conf"
]

class Filesystem_Conf:
    _working_dir: Path

    def __init__(self, _working_dir: Path):
        self._working_dir = _working_dir

    def get_dir_for_file_app(self):
        return self._working_dir.joinpath("files/apps")

    def get_dir_for_file_document(self):
        return self._working_dir.joinpath("files/documents")

    def get_dir_for_file_image(self):
        return self._working_dir.joinpath("files/images")

    def get_dir_for_file_video(self):
        return self._working_dir.joinpath("files/videos")

    def get_dir_for_file_audio(self):
        return self._working_dir.joinpath("files/audios")

    def get_dir_for_file_other(self):
        return self._working_dir.joinpath("files/other")