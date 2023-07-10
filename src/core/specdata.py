from dataclasses import dataclass
from enum import Enum

SpecMode = Enum('SpecMode', ['Point', 'Line', 'Region'])

@dataclass
class SpecData:
    mode: SpecMode
    start: float
    stop: float
    step: float
    delay_time: float