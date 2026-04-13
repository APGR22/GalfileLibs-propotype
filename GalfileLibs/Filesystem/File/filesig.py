from enum import Enum

__all__ = [
    "FileSignatureType"
]

class FileSignatureType(Enum):
    """
    See https://en.wikipedia.org/wiki/List_of_file_signatures
    """

    # applications
    BLEND = b"\x42\x4C\x45\x4E\x44\x45\x52"

    # documents
    PDF = b"\x25\x50\x44\x46\x2D"

    # images
    BMP = b"\x42\x4D"

    PNG = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"

    JPG_0 = JPEG_0 = b"\xFF\xD8\xFF\xDB"
    JPG_1 = JPEG_1 = b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01"
    JPG_2 = JPEG_2 = b"\xFF\xD8\xFF\xEE"
    JPG_3 = JPEG_3 = b"\xFF\xD8\xFF\xE1??\x45\x78\x69\x66\x00\x00"
    JPG_4 = b"FF\xD8\xFF\xE0"

    # videos
    MP4_0 = b"\x66\x74\x79\x70\x69\x73\x6F\x6D"
    MP4_1 = b"\x66\x74\x79\x70\x4D\x53\x4E\x56"

    MKV = b"\x1A\x45\xDF\xA3"

    # audios
    MP3_0 = b"\xFF\xFB"
    MP3_1 = b"\xFF\xF3"
    MP3_2 = b"\xFF\xF2"
    MP3_3 = b"\x49\x44\x33"

    WAV = b"\x52\x49\x46\x46????\x57\x41\x56\x45"

    OGG = b"\x4F\x67\x67\x53"

    __RECHECK_SYMBOL = "?" #how to handle "?"?

    @classmethod
    def sig_in_data(cls, data: bytes, type: FileSignatureType):
        return type.value in data

    @classmethod
    def sigs_in_data(cls, data: bytes, checktypes: list[FileSignatureType]):
        for sig in checktypes:
            if cls.sig_in_data(data, sig):
                return True
            
        return False

    @classmethod
    def get_type(cls, data: bytes):
        # application
        if cls.sig_in_data(data, cls.BLEND): return cls.BLEND

        # document
        elif cls.sig_in_data(data, cls.PDF): return cls.PDF

        # image
        elif cls.sig_in_data(data, cls.BMP): return cls.BMP
        elif cls.sig_in_data(data, cls.PNG): return cls.PNG

        elif cls.sig_in_data(data, cls.JPG_0): return cls.JPG_0
        elif cls.sig_in_data(data, cls.JPG_1): return cls.JPG_1
        elif cls.sig_in_data(data, cls.JPG_2): return cls.JPG_2
        elif cls.sig_in_data(data, cls.JPG_3): return cls.JPG_3
        elif cls.sig_in_data(data, cls.JPG_4): return cls.JPG_4

        elif cls.sig_in_data(data, cls.JPEG_0): return cls.JPEG_0
        elif cls.sig_in_data(data, cls.JPEG_1): return cls.JPEG_1
        elif cls.sig_in_data(data, cls.JPEG_2): return cls.JPEG_2
        elif cls.sig_in_data(data, cls.JPEG_3): return cls.JPEG_3

        # video
        elif cls.sig_in_data(data, cls.MP4_0): return cls.MP4_0
        elif cls.sig_in_data(data, cls.MP4_1): return cls.MP4_1

        elif cls.sig_in_data(data, cls.MKV): return cls.MKV

        # audio
        elif cls.sig_in_data(data, cls.MP3_0): return cls.MP3_0
        elif cls.sig_in_data(data, cls.MP3_1): return cls.MP3_1
        elif cls.sig_in_data(data, cls.MP3_2): return cls.MP3_2
        elif cls.sig_in_data(data, cls.MP3_3): return cls.MP3_3

        elif cls.sig_in_data(data, cls.WAV): return cls.WAV

        elif cls.sig_in_data(data, cls.OGG): return cls.OGG