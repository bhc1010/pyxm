from typing import Union, Callable
from dataclasses import dataclass
from enum import Enum

from core.imagedata import ImageData
from core.specdata import SpecData

TaskType = Enum('TaskType', ['Image', 'Spectra'])

@dataclass
class TaskData:
    dtype: TaskType
    inner: Union[ImageData, SpecData]
    completed: bool
    # procedure: Callable