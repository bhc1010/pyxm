from dataclasses import dataclass
from datetime import datetime
from core.exponentialnumber import ExponentialNumber

@dataclass
class ImageData:
    name: str
    date: datetime
    repetitions: int
    lines_per_frame: int
    time_to_finish: str
    size: ExponentialNumber
    x_offset: ExponentialNumber
    y_offset: ExponentialNumber
    bias: ExponentialNumber
    set_point: ExponentialNumber
    scan_speed: ExponentialNumber
    line_time: ExponentialNumber