from enum import Enum

class TaskSetStatus(Enum):
    Ready = 1
    Working = 2
    Finished = 3
    Error = 4