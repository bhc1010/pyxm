from dataclasses import dataclass
from enum import Enum

from core.exponentialnumber import ExponentialNumber

SweepParameter = Enum("SweepParameter", ["bias", "size", "position"])

@dataclass
class TaskSetData:
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