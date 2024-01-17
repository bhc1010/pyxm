from enum import Enum

class TaskSetStatus(Enum):
    """
    Enumeration representing the status of a TaskSet.

    This enumeration represents the possible status of a TaskSet, which can be Ready, Working, Finished, or Error.

    Attributes:
        Ready (int): The status representing that the TaskSet is ready.
        Working (int): The status representing that the TaskSet is currently being processed.
        Finished (int): The status representing that the TaskSet has finished its execution.
        Error (int): The status representing that an error occurred while processing the TaskSet.
    """
    Ready = 1
    Working = 2
    Finished = 3
    Error = 4
