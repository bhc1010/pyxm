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

    finished = Signal()
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
            set_stm_params(data: Union[ImageData, SpecData]) -> None: Sets STM parameters for the given data.
            start_procedure() -> str: Starts the STM procedure based on the task type.
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
    def run(self) -> None:
        """
            Runs the STM task.

            This method is the main entry point for the worker thread. It executes the STM task defined in the 'task' attribute.
        """
        print(f"Task started : {self.task.inner.bias}")

        self.set_stm_params(self.task.inner)
        result = self.start_procedure()

        self.signals.finished.emit()

    def set_stm_params(self, data: Union[ImageData, SpecData]) -> None:
        """
            Sets the STM parameters based on the given data.

            Args:
                data (Union[ImageData, SpecData]): The data containing the parameters to be set in the STM device.

            This method sets various parameters on the STM device to configure it for the specific STM task to be performed.
            It takes an instance of ImageData or SpecData as input and extracts relevant information to configure the STM.

            For ImageData:
            - Bias: The bias voltage applied during scanning.
            - Setpoint: The setpoint current for the feedback loop.
            - Scan Size: The size of the scanning area in nanometers.
            - Scan Position: The position (x, y) of the scanning area in nanometers.
            - Line Time: The time taken to acquire one line of data.
            - Lines Per Frame: The number of lines to be scanned to complete one frame.
            - Repetitions: The number of times the scan is repeated.

            For SpecData:
            (Currently not implemented)

            Note: This method does not execute the STM procedure; it only configures the STM device for the task.

            Returns:
                None
        """
        pos = Vector2(data.x_offset.to_float(), -data.y_offset.to_float())

        # Set Bias
        self.stm.set_bias(data.bias.to_float())

        # Set Setpoint
        self.stm.set_setpoint(data.set_point.to_float())

        # Set Scan Size
        self.stm.set_scan_size(data.size.to_float())

        # Set Scan Position
        self.stm.set_scan_pos(pos)

        # Set Line Time
        self.stm.set_line_time(data.line_time.to_float())

        # Set Lines Per Frame
        self.stm.set_lines_per_frame(data.lines_per_frame)

        # Set Repetitions
        self.stm.set_scan_count(data.repetitions)

    def start_procedure(self) -> str:
        """
            Starts the STM procedure based on the task type.

            Returns:
                str: The result of the STM procedure.

            This method initiates the STM procedure based on the type of task specified in the 'task' attribute.
            Currently, only the 'Image' task type is implemented.

            For Image task:
            The method starts the STM procedure for 'dI-dV Map Scan Speed'.

            For other task types:
            (Currently not implemented)

            The result of the STM procedure, if available, is returned as a string.

            Note: The method returns 'None' for task types other than 'Image' as they are not implemented yet.
        """
        match self.task.dtype:
            case TaskData.TaskType.Image:
                return self.stm.start_procedure('dI-dV Map Scan Speed')
            case _:
                return 'None'
            # case TaskType.Spectra:
                # self.stm.start_procedure('')
