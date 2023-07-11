from dataclasses import dataclass
from datetime import datetime
from core.exponentialnumber import ExponentialNumber

@dataclass
class ImageData:
    size: ExponentialNumber
    x_offset: ExponentialNumber
    y_offset: ExponentialNumber
    bias: ExponentialNumber
    set_point: ExponentialNumber
    line_time: ExponentialNumber
    lines_per_frame: int
    repetitions: int