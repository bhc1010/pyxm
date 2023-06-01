from enum import Enum

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QSize, QRect, QPropertyAnimation, Property
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton

import qtawesome as fa

def clamp10(value):
    return max(min(value, 1.0), 0.0)

class TaskBar(QtWidgets.QWidget):
    def __init__(self, value = 0.5, padding = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value = clamp10(value)
        self.color = QColor(245, 245, 245)
        self._padding = padding
        self._paint_rect = QRect(QRect(self._padding, self._padding, self.size().width() - 2*self._padding, self.size().height() - 2*self._padding))
        self.setMinimumHeight(60)
        self.setMaximumHeight(80)

    def get_paint_rect(self):
        return self._paint_rect
    
    def set_paint_rect(self, paint_rect):
        self._paint_rect = paint_rect
        self.update()

    paint_rect = Property(QRect, get_paint_rect, set_paint_rect)

    def resizeEvent(self, event) -> None:
        self.set_paint_rect(QRect(self._paint_rect.top(), self._paint_rect.left(), self.size().width() - 2*self._padding, self.size().height() - 2*self._padding))

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        brush = QtGui.QBrush()
        brush.setStyle(Qt.SolidPattern)
        path = QtGui.QPainterPath()

        # Background
        brush.setColor(self.color)
        path.addRoundedRect(self._paint_rect, 15, 15)
        painter.fillPath(path, brush)

        path.clear()

        # Progress Bar
        brush.setColor(self.color)
        _progress_rect = QRect(self._paint_rect)
        _progress_rect.setWidth(self._paint_rect.width() * self.value)
        path.addRoundedRect(_progress_rect, 15, 15)
        painter.fillPath(path, brush)


class Task(QtWidgets.QWidget):
    Status = Enum('Status', ['Ready', 'Working', 'Finished'])

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._icon = QPushButton(icon=fa.icon('fa5.circle', color='black'))
        self._icon.setFlat(True)
        self._name = QLineEdit(name)
        self._name.setStyleSheet('QLineEdit { background: transparent; color: black; border: 0px; }')
        self._options_btn = QPushButton(icon=fa.icon('fa5s.caret-left', color='black', scale_factor=2.0))
        self._options_btn.setFlat(True)
        self._task_bar = TaskBar(value=0.0)

        self._layout = QGridLayout(self)
        self._layout.addWidget(self._task_bar, 0, 0, 3, 5)
        self._layout.addWidget(QLabel(''), 1, 0, 1, 1)
        self._layout.addWidget(self._icon, 1, 1, 1, 1)
        self._layout.addWidget(self._name, 1, 2, 1, 1)
        self._layout.addWidget(self._options_btn, 1, 3, 1, 1)
        self._layout.addWidget(QLabel(''), 1, 4, 1, 1)
        self._layout.setColumnStretch(2, 1)
        self._layout.setContentsMargins(0,0,0,0)
        
        self._name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._options_btn.setMaximumWidth(30)

        self.installEventFilter(self)

        self._anim = QPropertyAnimation(self._task_bar, b"paint_rect")
        self._anim.setDuration(100)

    def eventFilter(self, obj, ev):
        if ev.type() == QtCore.QEvent.Enter:
            self._anim.setEndValue(self._task_bar.rect())
            self._anim.start()

        if ev.type() == QtCore.QEvent.Leave:
            self._anim.setEndValue(QRect(self._task_bar._padding, self._task_bar._padding, self.size().width() - 2*self._task_bar._padding, self.size().height() - 2*self._task_bar._padding))
            self._anim.start()

        return False