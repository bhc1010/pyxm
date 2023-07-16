from typing import Union, Callable
from dataclasses import dataclass
from enum import Enum

from core.imagedata import ImageData
from core.specdata import SpecData

TaskType = Enum('TaskType', ['Image', 'Spectra'])

@dataclass
class TaskData:
    """
        Represents the data for an STM task.

        This class represents the data required to define an STM task. It contains the task type, which can be 'Image'
        or 'Spectra', and the inner data, which can be either an ImageData or SpecData object, depending on the task type.

        Attributes:
            dtype (TaskType): The type of the task, which can be either 'Image' or 'Spectra'.
            inner (Union[ImageData, SpecData]): The inner data object containing the specific parameters for the task.
            completed (bool): A flag indicating whether the task has been completed (True) or not (False).
            index (int): The index of the task in a task set or a list of tasks.
            procedure (Callable): A callable representing the procedure to be executed for the task.

    """

    dtype: TaskType
    inner: Union[ImageData, SpecData]
    completed: bool
    index: int
    # procedure: Callable
