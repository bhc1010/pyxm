from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class ScanAreaToolBar(QGraphicsWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.button = QGraphicsProxyWidget()
        self.button.setWidget(QPushButton("Test"))
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)