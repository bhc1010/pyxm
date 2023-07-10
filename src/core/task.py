from dataclasses import dataclass
from typing import Union, Callable

from core.imagedata import ImageData
from core.specdata import SpecData

@dataclass
class Task:
    data: Union[ImageData, SpecData]
    procedure: Callable