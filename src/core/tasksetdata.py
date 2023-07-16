from dataclasses import dataclass
from enum import Enum

from core.exponentialnumber import ExponentialNumber

@dataclass
class TaskSetData:
    """
        Represents the data for a set of STM tasks.

        This class represents the data required to define a set of Scanning Tunneling Microscope (STM) tasks.
        It contains various parameters such as size, offsets, bias, set point, line time, lines per frame,
        repetitions, and the parameter to be swept during the task set.

        Attributes:
            name (str): The name of the task set.
            size (ExponentialNumber): The size of the task set in meters.
            x_offset (ExponentialNumber): The X-offset of the task set in meters.
            y_offset (ExponentialNumber): The Y-offset of the task set in meters.
            bias (ExponentialNumber): The bias voltage in volts.
            set_point (ExponentialNumber): The set point current in Amperes.
            line_time (ExponentialNumber): The time taken to acquire each line in seconds.
            lines_per_frame (int): The number of lines per frame.
            repetitions (int): The number of repetitions for each task in the set.
            sweep_parameter (SweepParameter): The parameter to sweep during the task set (from the SweepParameter enum).
            sweep_start (ExponentialNumber): The starting value for the parameter sweep.
            sweep_stop (ExponentialNumber): The stopping value for the parameter sweep.
            sweep_step (ExponentialNumber): The step size for the parameter sweep.
            total_tasks (int): The total number of tasks in the set.
            time_to_finish (str): The estimated time required to finish the entire task set as a formatted string.
    """
    
    SweepParameter = Enum("SweepParameter", ["none", "bias", "set_point", "size", "x_offset", "y_offset"])
    """
        Enumeration for specifying the parameter to sweep during an STM task set.

        The SweepParameter enumeration defines the possible parameters that can be swept during an STM task set.
        It includes options such as none (no parameter sweep), bias, set_point, size, x_offset, and y_offset.
    """

    name: str
    size: ExponentialNumber
    x_offset: ExponentialNumber
    y_offset: ExponentialNumber
    bias: ExponentialNumber
    set_point: ExponentialNumber
    line_time: ExponentialNumber
    lines_per_frame: int
    repetitions: int
    sweep_parameter: SweepParameter
    sweep_start: ExponentialNumber
    sweep_stop: ExponentialNumber
    sweep_step: ExponentialNumber
    total_tasks: int
    time_to_finish: str
