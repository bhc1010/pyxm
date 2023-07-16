import numpy as np
from enum import Enum
from typing import Callable, List

from PySide6 import QtCore
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import qtawesome as fa

from core.exponentialnumber import ExponentialNumber
from core.tasksetdata import TaskSetData
from core.taskdata import TaskData
from core.imagedata import ImageData

from ui.native.taskset.tasksetbar import TaskSetBar
from ui.native.taskset.tasksetinput import TaskSetInput
from ui.native.taskset.tasksetinfo import TaskSetInfo
from ui.native.taskset.tasksetstatus import TaskSetStatus

class TaskSet(QWidget):
    """
        Widget representing a TaskSet.

        This widget represents a TaskSet, which contains multiple tasks to be executed.

        Attributes:
            Status (Enum): An enumeration representing the status of the TaskSet (Ready, Working, Finished, or Error).
            status (Status): The current status of the TaskSet.
            index (int): The index of the TaskSet.
            data (TaskSetData): The data associated with the TaskSet.
            tasks (List[TaskData]): A list of TaskData objects representing individual tasks in the TaskSet.
            todo (List[TaskData]): A list of tasks that are yet to be completed.
            total_todo (int): The total number of tasks to be completed.
            dropFunc (Callable): A function to call when the TaskSet is dropped.
            _selected (bool): A flag indicating whether the TaskSet is selected (expanded).
            _content (QWidget): The content widget containing the TaskSet's information.
            _task_bar (TaskSetBar): The progress bar for the TaskSet.
            _icon (QLabel): An icon label representing the TaskSet.
            _name (TaskSetInput): The name input field for the TaskSet.
            _drag (QLabel): A drag icon label for the TaskSet.
            _remove_task_set_btn (QPushButton): A button to remove the TaskSet.
            _info (TaskSetInfo): The widget displaying detailed information about the TaskSet.
            _content_layout (QGridLayout): The layout for the content widget.
            _layout (QGridLayout): The main layout for the TaskSet widget.
            _task_bar_hover_anim (QPropertyAnimation): Animation for the progress bar on hover.
            _info_anim (QParallelAnimationGroup): Animation group for expanding/collapsing the detailed information.
    """

    def __init__(self, name: str, data: TaskSetData, idx: int, dropFunc: Callable):
        """
            Initialize the TaskSet widget.

            Args:
                name (str): The name of the TaskSet.
                data (TaskSetData): The data associated with the TaskSet.
                idx (int): The index of the TaskSet.
                dropFunc (Callable): A function to call when the TaskSet is dropped.
        """
        super().__init__()
        self.status = TaskSetStatus.Ready
        self.index = idx
        self.data = data
        self.tasks: List[TaskData] = self.create_tasks(data)
        self.todo: List[TaskData] = list()
        self.total_todo = 1
        self.dropFunc = dropFunc
        self._selected = False

        self.setMaximumHeight(60)
        self._content = QWidget()
        self._task_bar = TaskSetBar()
        self._task_bar.updateColor(self.status)
        self._icon = QLabel(pixmap=fa.icon('fa5.circle', color='black').pixmap(24, 24))
        self._icon.setFixedWidth(24)
        self._name = TaskSetInput(name)
        self._name.textChanged.connect(self.adjustTextWidth)
        self._name.setStyleSheet('QLineEdit { background: transparent; color: black; border: 0px;}')
        self._drag = QLabel(pixmap=fa.icon('fa5s.ellipsis-v', color='black').pixmap(24,24))
        self._drag.setFixedWidth(20)
        self._content.setFixedHeight(self._task_bar.rect().height())

        self._content_layout = QGridLayout(self._content)
        self._content_layout.addWidget(self._task_bar, 0, 0, 3, 7)
        self._content_layout.addItem(QSpacerItem(10, 60), 1, 0)
        self._content_layout.addWidget(self._icon, 1, 1)
        self._content_layout.addItem(QSpacerItem(10, 60, QSizePolicy.Expanding, QSizePolicy.Expanding), 1, 2)
        self._content_layout.addWidget(self._name, 1, 3)
        self._content_layout.addItem(QSpacerItem(10, 60, QSizePolicy.Expanding, QSizePolicy.Expanding), 1, 4)
        self._content_layout.addWidget(self._drag, 1, 5)
        self._content_layout.addItem(QSpacerItem(10, 60), 1, 6)
        self._content_layout.setContentsMargins(0,0,0,0)
        
        self._remove_task_set_btn = QPushButton("Remove Task Set")
        self._remove_task_set_btn.clicked.connect(self.dropSelf)
        self._info = TaskSetInfo(self.data, self.tasks, self._remove_task_set_btn)

        self._layout = QGridLayout(self)
        self._layout.addWidget(self._info, 1, 0)
        self._layout.addWidget(self._content, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)

        self.installEventFilter(self)

        self._task_bar_hover_anim = QPropertyAnimation(self._task_bar, b"paint_rect")
        self._task_bar_hover_anim.setDuration(100)
        
        self._info_anim = QParallelAnimationGroup(self)
        self.setInfoAnimation()
        
    def create_tasks(self, data: TaskSetData) -> List[TaskData]:
        """
            Create tasks based on the TaskSetData.

            Args:
                data (TaskSetData): The data associated with the TaskSet.

            Returns:
                List[TaskData]: A list of TaskData objects representing individual tasks in the TaskSet.
        """
        tasks = list()
        match data.sweep_parameter:
            case TaskSetData.SweepParameter.none:
                img = ImageData(data)
                tasks.append(TaskData(inner=img, dtype=TaskData.TaskType.Image, completed=False, index=0))
            case TaskSetData.SweepParameter.bias:
                bias_range = np.arange(start=data.sweep_start.to_float(), stop=data.sweep_stop.to_float() + data.sweep_step.to_float(), step=data.sweep_step.to_float()) 
                for i, bias in enumerate(bias_range):
                    img = ImageData(data)
                    img.bias = ExponentialNumber.from_float(bias)
                    tasks.append(TaskData(inner=img, dtype=TaskData.TaskType.Image, completed=False, index=i))
            case TaskSetData.SweepParameter.size:
                size_range = np.arange(start=data.sweep_start.to_float(), stop=data.sweep_stop.to_float() + data.sweep_step.to_float(), step=data.sweep_step.to_float())
                for i, size in enumerate(size_range):
                    img = ImageData(data)
                    img.size = ExponentialNumber.from_float(size)
                    tasks.append(TaskData(inner=img, dtype=TaskData.TaskType.Image, completed=False, index=i))

        return tasks

    def setInfoAnimation(self):
        """
            Set up the animation for expanding/collapsing the detailed information.

            Returns:
                None
        """
        self._info_anim.clear()
        self._info_anim.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self._info_anim.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self._info_anim.addAnimation(QPropertyAnimation(self._info, b"maximumHeight"))
        
        collapsed_height = self.sizeHint().height() - self._info.maximumHeight()
        content_height = self._info._layout.sizeHint().height()

        anims = [self._info_anim.animationAt(i) for i in range(self._info_anim.animationCount())]
        for anim in anims[:-1]:
            anim.setDuration(250)
            anim.setStartValue(collapsed_height)
            anim.setEndValue(collapsed_height + content_height)  
        anims[-1].setStartValue(0)
        anims[-1].setEndValue(content_height)

        self._name.elideText()

    def setStatus(self, status: TaskSetStatus):
        """
            Set the status of the TaskSet.

            Args:
                status (Status): The new status of the TaskSet.

            Returns:
                None
        """
        self.status = status
        self._task_bar.updateColor(status)
        self.update_task_bar()

    def eventFilter(self, obj, ev):
        """
            Filter and handle events.

            Args:
                obj: The object that triggered the event.
                ev: The event.

            Returns:
                bool: True if the event is handled; False otherwise.
        """
        if ev.type() == QtCore.QEvent.Enter:
            if not self._selected:
                self._task_bar_hover_anim.setEndValue(self._task_bar.rect())
                self._task_bar_hover_anim.start()

        if ev.type() == QtCore.QEvent.Leave:
            if not self._selected:
                self._task_bar_hover_anim.setEndValue(QRect(self._task_bar._padding, self._task_bar._padding, self._content.size().width() - 2*self._task_bar._padding, self._content.size().height() - 2*self._task_bar._padding))
                self._task_bar_hover_anim.start()
            
        if ev.type() == QtCore.QEvent.MouseButtonPress:
            self._lastpos = ev.pos()
            
        if ev.type() == QtCore.QEvent.MouseButtonRelease:
            widget_on_press = obj.childAt(ev.pos())
            widget_on_release = obj.childAt(self._lastpos)
            
            if widget_on_press == self._task_bar and widget_on_press == widget_on_release:
                if not self._selected:
                    self._selected = True
                    self._info_anim.setDirection(QtCore.QAbstractAnimation.Forward)
                    self._task_bar._vertical_margin = 10
                else:
                    self._selected = False
                    self._info_anim.setDirection(QtCore.QAbstractAnimation.Backward)
                    self._task_bar._vertical_margin = 0
                    
                self._info_anim.start()

        return False
    
    def adjustTextWidth(self):
        """
            Adjust the width of the name input field based on the text size.

            Returns:
                None
        """
        width = self._name.fontMetrics().boundingRect(self._name.text()).width()
        padding = 25
        fixedWidth = min(width + padding, 0.6 * self.rect().width())
        self._name.setFixedWidth(fixedWidth)

    def update_task_bar(self):
        """
            Update the progress bar representing the completion of tasks.

            Returns:
                None
        """
        completed_tasks = [task for task in self.tasks if task.completed]
        val = len(completed_tasks) / self.total_todo
        self._task_bar.value = val
        self._task_bar.repaint()

    def setIndex(self, i):
        """
            Set the index of the TaskSet.

            Args:
                i (int): The new index.

            Returns:
                None
        """
        self.index = i

    def dropSelf(self):
        """
            Remove the TaskSet.

            Returns:
                None
        """
        self.dropFunc(self.index)

    def resizeEvent(self, event) -> None:
        """
            Event handler for resizing the widget.

            Args:
                event: The resize event.

            Returns:
                None
        """
        self.adjustTextWidth()
        return super().resizeEvent(event)
