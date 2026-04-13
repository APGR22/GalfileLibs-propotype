from enum import Enum, auto
from .filesig import *

__all__ = [
    "FormatType",
    "Type"
]

class FormatType(Enum):
    #app
    BLENDER = ".blend"

    #document
    TXT = ".txt"
    PDF = ".pdf"

    #image
    BMP = ".bmp"
    PNG = ".png"
    JPG = ".jpg"

    #video
    MP4 = ".mp4"
    MKV = ".mkv"

    #audio
    MP3 = ".mp3"
    WAV = ".wav"
    OGG = ".ogg"

    #
    OTHER = 0

    @classmethod
    def get_type_by_data(cls, data: bytes):

        match FileSignatureType.get_type(data):
            # application
            case FileSignatureType.BLEND: return cls.BLENDER

            # document
            case FileSignatureType.PDF: return cls.PDF

            # images
            case FileSignatureType.BMP: return cls.BMP
            case FileSignatureType.PNG: return cls.PNG

            case FileSignatureType.JPG_0 | \
                FileSignatureType.JPG_1 | \
                FileSignatureType.JPG_2 | \
                FileSignatureType.JPG_3 | \
                FileSignatureType.JPG_4 | \
                FileSignatureType.JPEG_0 | \
                FileSignatureType.JPEG_1 | \
                FileSignatureType.JPEG_2 | \
                FileSignatureType.JPEG_3:
                return cls.JPG
            
            # video
            case FileSignatureType.MP4_0 | \
                FileSignatureType.MP4_1:
                return cls.MP4
            
            case FileSignatureType.MKV: return cls.MKV

            # audio
            case FileSignatureType.MP3_0 | \
                FileSignatureType.MP3_1 | \
                FileSignatureType.MP3_2 | \
                FileSignatureType.MP3_3:
                return cls.JPG

            case FileSignatureType.WAV: return cls.WAV
            case FileSignatureType.OGG: return cls.OGG

        return cls.OTHER

    @classmethod
    def get_type_by_ext(cls, ext: str):
        match ext:
            # application
            case cls.BLENDER.value: return cls.BLENDER
            # document
            case cls.TXT.value: return cls.TXT
            case cls.PDF.value: return cls.PDF
            # image
            case cls.BMP.value: return cls.BMP
            case cls.PNG.value: return cls.PNG
            case cls.JPG.value: return cls.JPG
            # video
            case cls.MP4.value: return cls.MP4
            case cls.MKV.value: return cls.MKV
            # audio
            case cls.MP3.value: return cls.MP3
            case cls.WAV.value: return cls.WAV
            case cls.OGG.value: return cls.OGG
        
        return cls.OTHER

class Type(Enum):
    APP = 0
    __APP = [
        FormatType.BLENDER,
    ]

    DOCUMENT = 1
    __DOCUMENT = [
        FormatType.TXT,
        FormatType.PDF,
    ]

    IMAGE = 2
    __IMAGE = [
        FormatType.BMP,
        FormatType.PNG,
        FormatType.JPG,
    ]

    VIDEO = 3
    __VIDEO = [
        FormatType.MP4,
        FormatType.MKV,
    ]

    AUDIO = 4
    __AUDIO = [
        FormatType.MP3,
        FormatType.WAV,
        FormatType.OGG,
    ]

    OTHER = 5

    @classmethod
    def get_type(cls, format_type: FormatType):
        if format_type in cls.__APP:
            return cls.APP
        elif format_type in cls.__DOCUMENT:
            return cls.DOCUMENT
        elif format_type in cls.__IMAGE:
            return cls.IMAGE
        elif format_type in cls.__VIDEO:
            return cls.VIDEO
        elif format_type in cls.__AUDIO:
            return cls.AUDIO

        return cls.OTHER