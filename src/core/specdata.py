from dataclasses import dataclass
from typing import List
from enum import Enum

SpecMode = Enum('SpecMode', ['Point', 'Line'])

@dataclass
class SpecData:
    mode: SpecMode
    start_voltage: float
    stop_voltage: float
    step_voltage: float
    values: List[List[float]]