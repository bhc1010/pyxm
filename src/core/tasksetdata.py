from dataclasses import dataclass
from typing import List
from datetime import datetime
from core.task import Task
from core.exponentialnumber import ExponentialNumber

@dataclass
class TaskSetData:
    name: str
    date: datetime
    repetitions: int
    total_tasks: int
    lines_per_frame: int
    time_to_finish: str
    size: ExponentialNumber
    x_offset: ExponentialNumber
    y_offset: ExponentialNumber
    set_point: ExponentialNumber
    scan_speed: ExponentialNumber
    line_time: ExponentialNumber
    tasks: List[Task]