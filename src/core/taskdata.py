from dataclasses import dataclass
from typing import List
from datetime import datetime
from specdata import SpecData

@dataclass
class TaskData:
    name: str
    date: datetime
    lines_per_frame: int
    size: float
    x_offset: float
    y_offset: float
    scan_speed: float
    line_time: float
    start_voltage: float
    stop_voltage: float
    step_voltage: float
    spec: List[SpecData]
    images: List[List[float]]