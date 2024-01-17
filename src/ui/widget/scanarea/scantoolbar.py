from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ui.widget.togglebutton import ToggleButton
from ui.widget.scanarea.toolmode import ToolMode

class ScanAreaToolBar(QGraphicsWidget):
    _move_clicked = Signal()
    _edit_rect_clicked = Signal()
    _edit_spec_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.mode = ToolMode.Move

        # Move
        self.move = ToggleButton(objectName='arrows-alt', unchecked="#000", checked="#ff964f")
        self.move.setStyleSheet('QPushButton {background: transparent; border: 0px}')
        self.move.set_checked(True)
        moveP = QGraphicsProxyWidget()
        moveP.setWidget(self.move)
        
        # Edit ScanRect
        self.edit_rect = ToggleButton(objectName='vector-square', unchecked="#000", checked="#ff964f")
        self.edit_rect.setStyleSheet('QPushButton {background: transparent; border: 0px}')
        edit_rect_proxy = QGraphicsProxyWidget()
        edit_rect_proxy.setWidget(self.edit_rect)
        
        # Edit SpecLine
        self.edit_spec = ToggleButton(objectName='wave-square', unchecked="#000", checked="#ff964f")
        self.edit_spec.setStyleSheet('QPushButton {background: transparent; border: 0px}')
        edit_spec_proxy = QGraphicsProxyWidget()
        edit_spec_proxy.setWidget(self.edit_spec)

        toolbar_layout = QGraphicsLinearLayout(Qt.Orientation.Vertical)
        toolbar_layout.addItem(moveP)
        toolbar_layout.addItem(edit_rect_proxy)
        toolbar_layout.addItem(edit_spec_proxy)
        
        self.setLayout(toolbar_layout)
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        self.setZValue(1)

        self.move.clicked.connect(self.move_clicked)
        self.edit_rect.clicked.connect(self.edit_rect_clicked)
        self.edit_spec.clicked.connect(self.edit_spec_clicked)

    def move_clicked(self):
        if self.mode == ToolMode.Move:
            self.mode = ToolMode.Null
        else:
            self.mode = ToolMode.Move
        self.edit_rect.set_checked(False)
        self.edit_spec.set_checked(False)
        self._move_clicked.emit()

    def edit_rect_clicked(self):
        if self.mode == ToolMode.ScanRect:
            self.mode = ToolMode.Null
        else:
            self.mode = ToolMode.ScanRect
        self.move.set_checked(False)
        self.edit_spec.set_checked(False)
        self._edit_rect_clicked.emit()

    def edit_spec_clicked(self):
        if self.mode == ToolMode.SpecLine:
            self.mode = ToolMode.Null
        else:
            self.mode = ToolMode.SpecLine
        self.move.set_checked(False)
        self.edit_rect.set_checked(False)
        self._edit_spec_clicked.emit()