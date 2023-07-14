import time
from typing import Union
from PySide6.QtCore import *

from core.vector2 import Vector2
from core.taskdata import TaskData, TaskType
from core.imagedata import ImageData
from core.specdata import SpecData
from lib.native.stm import STM

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
        self.index = index
        self.signals = WorkerSignals()
        self.stm = STM()

    @Slot()
    def run(self):
        print(f"Task started : {self.task.inner}")
        time.sleep(1)

        self.set_stm_params(self.task.inner)
        result = self.start_procedure()

        self.signals.finished.emit(self.index)


    def set_stm_params(self, data: Union[ImageData, SpecData]):
        pos = Vector2(data.x_offset, data.y_offset)

        ## Bias
        self.stm.set_bias(data.bias)
        ## Set point
        self.stm.set_set_point(data.set_point)
        ## Size
        self.stm.set_scan_size(data.size)
        ## Position
        self.stm.set_scan_pos(pos)
        ## Line time
        self.stm.set_line_time(data.line_time)
        ## Lines per frame
        self.stm.set_lines_per_frace(data.lines_per_frame)
        ## Repetitions
        self.stm.set_scan_count(data.repetitions)

    def start_procedure(self):
        match self.task.dtype:
            case TaskType.Image:
                return self.stm.start_procedure('dI-dV Map Scan Speed')
            case _:
                return 'None'
            # case TaskType.Spectra:
                # self.stm.start_procedure('')