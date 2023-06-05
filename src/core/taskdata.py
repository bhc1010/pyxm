from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from core.specdata import SpecData
from core.exponentialnumber import ExponentialNumber

@dataclass
class TaskData:
    name: str
    date: datetime
    time_to_finish: float
    lines_per_frame: int
    size: ExponentialNumber
    x_offset: ExponentialNumber
    y_offset: ExponentialNumber
    scan_speed: ExponentialNumber
    line_time: ExponentialNumber
    start_voltage: ExponentialNumber
    stop_voltage: ExponentialNumber
    step_voltage: ExponentialNumber
    spec: Optional[List[SpecData]] = None
    images: Optional[List[List[float]]] = None