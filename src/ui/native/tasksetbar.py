from PySide6 import QtGui
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from ui.native.taskset import TaskSet

class TaskSetBar(QWidget):
    """
    Custom progress bar widget for TaskSet.

    This widget represents a custom progress bar for the TaskSet. It visualizes the progress
    of the TaskSet with rounded rectangles indicating the completed portion.

    Attributes:
        value (float): The progress value of the TaskSet, ranging from 0.0 to 1.0.
        _background_color (QColor): The background color of the progress bar.
        _bar_color (QColor): The color of the completed portion of the progress bar.
        _padding (int): The padding around the progress bar.
        _paint_rect (QRect): The rectangle used for painting the progress bar.
        _vertical_margin (int): Vertical margin added to the progress bar.
    """
    def __init__(self, value=0.0, padding=5, *args, **kwargs):
        """
        Initialize the TaskSetBar widget.

        Args:
            value (float, optional): The progress value of the TaskSet. Defaults to 0.0.
            padding (int, optional): The padding around the progress bar. Defaults to 5.
        """
        super().__init__(*args, **kwargs)

        self.value = max(min(value, 1.0), 0.0)
        self._background_color = None
        self._bar_color = None
        self._padding = padding
        self._paint_rect = QRect(QRect(self._padding, self._padding, self.size().width() - 2 * self._padding, self.size().height() - 2 * self._padding))
        self._vertical_margin = 0
        self.setFixedHeight(60)

    def updateColor(self, status):
        """
        Update the colors of the progress bar based on the TaskSet status.

        Args:
            status (TaskSet.Status): The status of the TaskSet.
        """
        match (status):
            case TaskSet.Status.Ready:
                self._background_color = QColor(235, 235, 235)
                self._bar_color = QColor(200, 200, 200)
            case TaskSet.Status.Working:
                self._background_color = QColor(102, 157, 246)
                self._bar_color = QColor(91, 141, 221)
            case TaskSet.Status.Finished:
                self._background_color = QColor(66, 219, 99)
                self._bar_color = self._background_color
            case TaskSet.Status.Error:
                self._background_color = QColor(255, 78, 78)
                self._bar_color = QColor(255, 41, 41)

    def getPaintRect(self):
        """
        Get the paint rectangle used for drawing the progress bar.

        Returns:
            QRect: The paint rectangle.
        """
        return self._paint_rect
    
    def setPaintRect(self, paint_rect):
        """
        Set the paint rectangle used for drawing the progress bar.

        Args:
            paint_rect (QRect): The paint rectangle.
        """
        self._paint_rect = paint_rect
        self.update()

    paint_rect = Property(QRect, getPaintRect, setPaintRect)

    def resizeEvent(self, event) -> None:
        """
        Event handler for resizing the widget.

        Args:
            event (QResizeEvent): The resize event.

        Returns:
            None
        """
        self.setPaintRect(QRect(self._paint_rect.top(), self._paint_rect.left(), self.size().width() - 2 * self._padding, self.size().height() - 2 * self._padding))

    def paintEvent(self, e):
        """
        Event handler for painting the widget.

        Args:
            e (QPaintEvent): The paint event.

        Returns:
            None
        """
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        brush = QtGui.QBrush()
        brush.setStyle(Qt.SolidPattern)
        path = QtGui.QPainterPath()
        
        # Background
        brush.setColor(self._background_color)
        self._paint_rect.setHeight(self._paint_rect.height() + self._vertical_margin)
        path.addRoundedRect(self._paint_rect, 15, 15)
        painter.fillPath(path, brush)

        path.clear()

        # Progress Bar
        brush.setColor(self._bar_color)
        _progress_rect = QRect(self._paint_rect)
        _progress_rect.setWidth(self._paint_rect.width() * self.value)
        _progress_rect.setHeight(_progress_rect.height() + self._vertical_margin)
        path.addRoundedRect(_progress_rect, 15, 15)
        painter.fillPath(path, brush)