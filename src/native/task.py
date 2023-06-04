from enum import Enum

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QSize, QRect, QPropertyAnimation, Property, QObject, QParallelAnimationGroup
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QFrame, QWidget, QVBoxLayout, QScrollArea, QSizePolicy

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
        self.setFixedHeight(60)

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

        self._selected = False
        self.setMaximumHeight(60)


        self._content = QWidget()
        self._task_bar = TaskBar(value=0.0)
        self._icon = QPushButton(icon=fa.icon('fa5.circle', color='black'))
        self._icon.setFlat(True)
        self._name = QLineEdit(name)
        self._name.setStyleSheet('QLineEdit { background: transparent; color: black; border: 0px; }')
        self._options_btn = QPushButton(icon=fa.icon('fa5s.caret-left', color='black', scale_factor=2.0))
        self._options_btn.setFlat(True)        
        self._content.setFixedHeight(self._task_bar.rect().height())

        self._content_layout = QGridLayout(self._content)
        self._content_layout.addWidget(self._task_bar, 0, 0, 3, 5)
        self._content_layout.addWidget(QLabel(''), 1, 0, 1, 1)
        self._content_layout.addWidget(self._icon, 1, 1, 1, 1)
        self._content_layout.addWidget(self._name, 1, 2, 1, 1)
        self._content_layout.addWidget(self._options_btn, 1, 3, 1, 1)
        self._content_layout.addWidget(QLabel(''), 1, 4, 1, 1)
        self._content_layout.setColumnStretch(2, 1)
        self._content_layout.setContentsMargins(0,0,0,0)
        
        self._info = QScrollArea(minimumHeight=0, maximumHeight=0)
        self._info.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        self._info_layout = QGridLayout(self._info)
        self._info_layout.setContentsMargins(0,0,0,0)
        
        for i in range(5):
            self._info_layout.addWidget(QLabel(f'{i}'), i, 0, 1, 1)
        
        self._layout = QGridLayout(self)
        self._layout.addWidget(self._info, 1, 0)
        self._layout.addWidget(self._content, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self.setStyleSheet('border: 0px')
        
        self._name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._options_btn.setMaximumWidth(30)

        self.installEventFilter(self)

        self._task_bar_anim = QPropertyAnimation(self._task_bar, b"paint_rect")
        self._task_bar_anim.setDuration(100)
        
        self._info_anim = QParallelAnimationGroup(self)
        self.setInfoAnimation()
        
    def setInfoAnimation(self):
        self._info_anim.clear()
        self._info_anim.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self._info_anim.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self._info_anim.addAnimation(QPropertyAnimation(self._info, b"maximumHeight"))
        
        collapsed_height = self.sizeHint().height() - self._info.maximumHeight()
        content_height = self._info_layout.sizeHint().height()
        
        print(f'collapsed: {collapsed_height}')
        print(f'content: {content_height}')
        
        anims = [self._info_anim.animationAt(i) for i in range(self._info_anim.animationCount())]
        
        for anim in anims[:-1]:
            anim.setDuration(500)
            anim.setStartValue(collapsed_height)
            anim.setEndValue(collapsed_height + content_height)
            
        anims[-1].setStartValue(0)
        anims[-1].setEndValue(content_height)
        

    def eventFilter(self, obj, ev):
        
        if ev.type() == QtCore.QEvent.Enter:
            if not self._selected:
                self._task_bar_anim.setEndValue(self._task_bar.rect())
                self._task_bar_anim.start()

        if ev.type() == QtCore.QEvent.Leave:
            if not self._selected:
                self._task_bar_anim.setEndValue(QRect(self._task_bar._padding, self._task_bar._padding, self._content.size().width() - 2*self._task_bar._padding, self._content.size().height() - 2*self._task_bar._padding))
                self._task_bar_anim.start()
            
        if ev.type() == QtCore.QEvent.MouseButtonPress:
            if not self._selected:
                self._selected = True
                self._info_anim.setDirection(QtCore.QAbstractAnimation.Forward)
            else:
                self._selected = False
                self._info_anim.setDirection(QtCore.QAbstractAnimation.Backward)
                
            self._info_anim.start()

        return False