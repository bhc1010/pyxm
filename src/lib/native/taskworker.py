from PySide6.QtCore import *
from core.taskdata import TaskData

import time


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    '''
    finished = Signal()  # QtCore.Signal
    error = Signal(tuple)

class TaskWorker(QRunnable):
    """
    Worker thread for STM tasks
    """
    
    def __init__(self, data: TaskData):
        super().__init__()
        self.data = data
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        print("Thread started")
        time.sleep(5)
        self.signals.finished.emit()