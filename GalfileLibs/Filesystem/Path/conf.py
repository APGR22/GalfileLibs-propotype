import colorama
from dataclasses import dataclass

__all__ = [
    "Conf"
]

@dataclass
class Conf:
    colorFile = colorama.Fore.BLUE
    colorFolder = colorama.Fore.YELLOW