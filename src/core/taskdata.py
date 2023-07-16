from typing import Union, Callable
from dataclasses import dataclass
from enum import Enum

from core.imagedata import ImageData
from core.specdata import SpecData

@dataclass
class TaskData:
    """
    Represents the data for a Scanning Tunneling Microscope (STM) task.

    This class represents the data required to define an STM task. It contains the task type, which can be 'Image'
    or 'Spectra', and the inner data, which can be either an ImageData or SpecData object, depending on the task type.

    Attributes:
        dtype (TaskType): The type of the task, which can be either 'Image' or 'Spectra' (from the TaskType enum).
        inner (Union[ImageData, SpecData]): The inner data object containing the specific parameters for the task.
        completed (bool): A flag indicating whether the task has been completed (True) or not (False).
        index (int): The index of the task in a task set or a list of tasks.
        procedure (Callable): A callable representing the procedure to be executed for the task.

    """

    TaskType = Enum('TaskType', ['Image', 'Spectra'])
    """
    Enumeration for the different types of Scanning Tunneling Microscope (STM) tasks.

    The TaskType enumeration defines the possible types of STM tasks, which include Image and Spectra tasks.
    """

    dtype: TaskType
    inner: Union[ImageData, SpecData]
    completed: bool
    index: int
    # procedure: Callable
