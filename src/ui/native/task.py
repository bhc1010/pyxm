import numpy as np
from typing import Union

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import qtawesome as fa

from core.imagedata import ImageData
from core.specdata import SpecData

class Task(QCheckBox):
    def __init__(self, text: str, data: Union[ImageData, SpecData]):
        super().__init__(text, checked=True)
        self.data = data