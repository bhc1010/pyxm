from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from core.specdata import SpecData
from core.exponentialnumber import ExponentialNumber

@dataclass
class TaskData:
    name: str
    date: datetime
    repetitions: int
    total_images: int
    lines_per_frame: int
    time_to_finish: str
    size: ExponentialNumber
    x_offset: ExponentialNumber
    y_offset: ExponentialNumber
    set_point: ExponentialNumber
    scan_speed: ExponentialNumber
    line_time: ExponentialNumber
    start_voltage: ExponentialNumber
    stop_voltage: ExponentialNumber
    step_voltage: ExponentialNumber
    spec: Optional[List[SpecData]] = None
    images: Optional[List[List[float]]] = None