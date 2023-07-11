import time
from PySide6.QtCore import *

from core.taskdata import TaskData, TaskType


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    '''
    finished = Signal(int)  # QtCore.Signal
    error = Signal(tuple)

class TaskWorker(QRunnable):
    """
    Worker thread for STM tasks
    """
    
    def __init__(self, task: TaskData, index: int):
        super().__init__()
        self.task = task
        self.index = int
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        print("Thread started")
        # match self.task.dtype:
        #     case TaskType.Image:
        #         for (attr, val) in self.task.inner.__dict__.items():
        #             print(f'{attr}: {val}')
        time.sleep(1)
        self.signals.finished.emit(self.index)