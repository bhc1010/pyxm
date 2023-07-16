from PySide6 import QtGui
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from typing import List

from core.tasksetdata import TaskSetData
from core.taskdata import TaskData

class TaskSetInfo(QWidget):
    """
    Widget to display information about a TaskSet.

    This widget is used to display information about a TaskSet and its associated tasks.
    It includes details such as bias, set point, size, position, lines per frame, line time,
    repetitions, total tasks, and estimated time remaining.

    Attributes:
        task_items (List[QCheckBox]): A list of QCheckBox widgets representing each task item.
        background (QColor): The background color of the widget.
    """
    def __init__(self, data: TaskSetData, tasks: List[TaskData], remove_task_set_btn: QPushButton):
        """
        Initialize the TaskSetInfo widget.

        Args:
            data (TaskSetData): The TaskSetData containing information about the TaskSet.
            tasks (List[TaskData]): The list of TaskData representing individual tasks.
            remove_task_set_btn (QPushButton): The button to remove the TaskSet.
        """
        super().__init__(minimumHeight=0, maximumHeight=0)
        self.task_items = list()

        self.background = QColor(245, 245, 245)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self._content = QScrollArea()
        self._content.setStyleSheet('background: transparent')
        self._layout = QVBoxLayout(self._content)
        self._layout.setContentsMargins(20,5,20,10)
    
        sublayout = QGridLayout()
        bias = QLabel(f'Bias : {data.bias}V')
        set_point = QLabel(f"Set point: {data.set_point}A")
        size = QLabel(f"Size: {data.size}m")
        position = QLabel(f"Position: ({data.x_offset}m, {data.y_offset}m)")
        lines_per_frame = QLabel(f"Lines per frame: {data.lines_per_frame}")
        line_time = QLabel(f"Line time: {data.line_time.to_float()}s")
        sublayout.addWidget(bias, 0, 0)
        sublayout.addWidget(set_point, 0, 1)
        sublayout.addWidget(size, 1, 0)
        sublayout.addWidget(position, 1, 1)
        sublayout.addWidget(line_time, 2, 0)
        sublayout.addWidget(lines_per_frame, 2, 1)

        match data.sweep_parameter:
            case TaskSetData.SweepParameter.bias:
                bias.setText("Bias: -")
            case TaskSetData.SweepParameter.size:
                size.setText("Size: -")

        self._layout.addLayout(sublayout)
        repetitions = QLabel(f"Repetitions: {data.repetitions}")
        self._layout.addWidget(repetitions)
        self._layout.addWidget(QLabel(f"Total Tasks: {len(tasks)}"))
        self._layout.addWidget(QLabel(f"Time remaining: {data.time_to_finish}"))
        
        for task in tasks:
            task_item = QCheckBox(checked=True)
            match data.sweep_parameter:
                case TaskSetData.SweepParameter.bias:
                    task_item.setText(f'Bias: {task.inner.bias}V')
                case TaskSetData.SweepParameter.size:
                    task_item.setText(f'Size: {task.inner.size}m')
            self.task_items.append(task_item)
            self._layout.addWidget(self.task_items[-1])
        self._layout.addWidget(remove_task_set_btn)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self._content)
        self.layout().setContentsMargins(0,0,0,0)
            
    def paintEvent(self, e):
        """
        Event handler for painting the widget.

        This method is called automatically when the widget needs to be repainted.
        It is responsible for painting the background of the widget with rounded corners.

        Args:
            e (QPaintEvent): The paint event object.

        Returns:
            None

        Note:
            - This method is called automatically by the Qt framework and should not be called directly.
            - The method uses QPainter to draw the widget's background with rounded corners.
              It sets the background color based on the `background` attribute and applies anti-aliasing
              for smooth rendering.
        """
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        brush = QtGui.QBrush()
        brush.setStyle(Qt.SolidPattern)
        path = QtGui.QPainterPath()
        
        # Background
        brush.setColor(self.background)
        vertical_margin = 15
        background_rect = QRect(self.rect().left(), self.rect().top() - vertical_margin, self.rect().width(), self.rect().height() + vertical_margin)
        path.addRoundedRect(background_rect, 15, 15)
        painter.fillPath(path, brush)
