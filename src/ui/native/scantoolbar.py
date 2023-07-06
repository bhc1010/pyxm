from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class ScanAreaToolBar(QGraphicsItem):
    def __init__(self):
        super().__init__()
        
        self.button = QGraphicsProxyWidget()
        self.button.setWidget(QPushButton("Test"))
        self.button.setFlag(QGraphicsItem.ItemIgnoresTransformations)