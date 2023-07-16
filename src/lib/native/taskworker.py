import time
from typing import Union
from PySide6.QtCore import *

from core.vector2 import Vector2
from core.taskdata import TaskData
from core.imagedata import ImageData
from core.specdata import SpecData
from lib.native.stm import STM

class WorkerSignals(QObject):
    """
        Defines the signals available from a running worker thread.

        This class defines the signals emitted by the Worker thread when it is running a task. It provides two signals:

        Attributes:
            finished: Signal emitted when the worker thread has finished its task.
            error: Signal emitted if an error occurs during the execution of the worker thread.
    """

    finished = Signal()  # QtCore.Signal
    error = Signal(tuple)

class TaskWorker(QRunnable):
    """
        Worker thread for STM tasks.

        This class represents a worker thread responsible for running STM tasks in the background. It is designed to be
        executed in a QThreadPool to perform time-consuming tasks without freezing the main GUI thread.

        Attributes:
            task (TaskData): The STM task to be executed.
            signals (WorkerSignals): A QObject that defines signals to communicate with the main thread.
            stm (STM): An instance of the STM class responsible for controlling the STM device.

        Methods:
            run(): The main method of the worker thread that runs the task.
            set_stm_params(data: Union[ImageData, SpecData]): Sets STM parameters for the given data.
            start_procedure(): Starts the STM procedure based on the task type.
    """

    def __init__(self, task: TaskData):
        """
            Initializes the TaskWorker.

            Args:
                task (TaskData): The STM task to be executed.
        """
        super().__init__()
        self.task = task
        self.signals = WorkerSignals()
        self.stm = STM()

    @Slot()
    def run(self):
        """
            Runs the STM task.

            This method is the main entry point for the worker thread. It executes the STM task defined in the 'task' attribute.
        """
        print(f"Task started : {self.task.inner.bias}")

        self.set_stm_params(self.task.inner)
        time.sleep(5)
        # result = self.start_procedure()

        self.signals.finished.emit()

    def set_stm_params(self, data: Union[ImageData, SpecData]):
        """
            Sets the STM parameters based on the given data.

            Args:
                data (Union[ImageData, SpecData]): The data containing the parameters to be set in the STM device.
        """
        pos = Vector2(data.x_offset.to_float(), data.y_offset.to_float())

        ## Bias
        self.stm.set_bias(data.bias.to_float())
        ## Set point
        self.stm.set_setpoint(data.set_point.to_float())
        ## Size
        self.stm.set_scan_size(data.size.to_float())
        ## Position
        self.stm.set_scan_pos(pos)
        ## Line time
        self.stm.set_line_time(data.line_time.to_float())
        ## Lines per frame
        self.stm.set_lines_per_frace(data.lines_per_frame)
        ## Repetitions
        self.stm.set_scan_count(data.repetitions)

    def start_procedure(self):
        """
            Starts the STM procedure based on the task type.

            Returns:
                str: The result of the STM procedure.
        """
        match self.task.dtype:
            case TaskData.TaskType.Image:
                return self.stm.start_procedure('dI-dV Map Scan Speed')
            case _:
                return 'None'
            # case TaskType.Spectra:
                # self.stm.start_procedure('')
