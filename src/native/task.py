from enum import Enum

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, Property
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy

import qtawesome as fa

def clamp10(value):
    return max(min(value, 1.0), 0.0)

class TaskBar(QtWidgets.QWidget):
    def __init__(self, value = 0.5, padding = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value = clamp10(value)
        self._background_color = None
        self._bar_color = None
        self._padding = padding
        self._paint_rect = QRect(QRect(self._padding, self._padding, self.size().width() - 2*self._padding, self.size().height() - 2*self._padding))
        self.setMinimumHeight(60)
        self.setMaximumHeight(80)

    def updateColor(self, status):
        match(status):
            case Task.Status.Ready:
                self._background_color = QColor(245, 245, 245)
                self._bar_color = QColor(200, 200, 200)
            case Task.Status.Working:
                self._background_color = QColor(102, 157, 246)
                self._bar_color = QColor(21, 101, 192)
            case Task.Status.Finished:
                self._background_color = QColor(66, 219, 99)
                self._bar_color = self._background_color
            case Task.Status.Error:
                self._background_color = QColor(255, 78, 78)
                self._bar_color = QColor(255, 41, 41)

    def getPaintRect(self):
        return self._paint_rect
    
    def setPaintRect(self, paint_rect):
        self._paint_rect = paint_rect
        self.update()

    paint_rect = Property(QRect, getPaintRect, setPaintRect)

    def resizeEvent(self, event) -> None:
        self.setPaintRect(QRect(self._paint_rect.top(), self._paint_rect.left(), self.size().width() - 2*self._padding, self.size().height() - 2*self._padding))

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        brush = QtGui.QBrush()
        brush.setStyle(Qt.SolidPattern)
        path = QtGui.QPainterPath()

        # Background
        brush.setColor(self._background_color)
        path.addRoundedRect(self._paint_rect, 15, 15)
        painter.fillPath(path, brush)

        path.clear()

        # Progress Bar
        brush.setColor(self._bar_color)
        _progress_rect = QRect(self._paint_rect)
        _progress_rect.setWidth(self._paint_rect.width() * self.value)
        path.addRoundedRect(_progress_rect, 15, 15)
        painter.fillPath(path, brush)

class TaskInput(QLineEdit):
    def __init__(self, text: str):
        super().__init__(text)
        self._text = text

        self.textChanged.connect(self.updateText)

    def updateText(self, text):
        self._text = text
    
    def elideText(self):
        padding = 8
        elidedText = self.fontMetrics().elidedText(self._text, Qt.TextElideMode.ElideRight, self.width() - padding)
        _text = self._text
        self.setText(elidedText)
        self.updateText(_text)
        self.setCursorPosition(0)

    def focusInEvent(self, event) -> None:
        self.setText(self._text)

        return super().focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        self.elideText()

        return super().focusOutEvent(event)

class Task(QtWidgets.QWidget):
    Status = Enum('Status', ['Ready', 'Working', 'Finished', 'Error'])

    def __init__(self, name: str):
        super().__init__()

        self.status = Task.Status.Ready
        
        self._icon = QLabel(pixmap=fa.icon('fa5.circle', color='black').pixmap(24, 24))
        self._name = TaskInput(name)
        self._name.textChanged.connect(self.adjustTextWidth)
        self._name.setStyleSheet('QLineEdit { background: transparent; color: black; border: 0px; }')
        self._options_btn = QPushButton(icon=fa.icon('fa5s.caret-left', color='black', scale_factor=2.0))
        self._options_btn.setFlat(True)
        self._task_bar = TaskBar(value=0.0)
        self._task_bar.updateColor(self.status)

        self._layout = QGridLayout(self)
        self._layout.addWidget(self._task_bar, 0, 0, 3, 7)
        self._layout.addWidget(QLabel(''), 1, 0, 1, 1)
        self._layout.addWidget(self._icon, 1, 1, 1, 1)
        self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 2, 1, 1)
        self._layout.addWidget(self._name, 1, 3, 1, 1)
        self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 4, 1, 1)
        self._layout.addWidget(self._options_btn, 1, 5, 1, 1)
        self._layout.addWidget(QLabel(''), 1, 6, 1, 1)
        self._layout.setContentsMargins(0,0,0,0)
        
        self._name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._options_btn.setMaximumWidth(30)

        self.installEventFilter(self)

        self._anim = QPropertyAnimation(self._task_bar, b"paint_rect")
        self._anim.setDuration(100)

        self._name.elideText()

    def setStatus(self, status: Status):
        self.status = status
        self._task_bar.updateColor(self.status)

    def eventFilter(self, obj, ev):
        if ev.type() == QtCore.QEvent.Enter:
            self._anim.setEndValue(self._task_bar.rect())
            self._anim.start()

        if ev.type() == QtCore.QEvent.Leave:
            self._anim.setEndValue(QRect(self._task_bar._padding, self._task_bar._padding, self.size().width() - 2*self._task_bar._padding, self.size().height() - 2*self._task_bar._padding))
            self._anim.start()

        return False
    
    def adjustTextWidth(self):
        width = self._name.fontMetrics().boundingRect(self._name.text()).width()
        padding = 25
        fixedWidth = min(width + padding, 0.6 * self.rect().width())
        self._name.setFixedWidth(fixedWidth)

    def resizeEvent(self, event) -> None:
        self.adjustTextWidth()
        return super().resizeEvent(event)
    