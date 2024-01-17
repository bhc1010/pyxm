from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class RectPreview(QGraphicsRectItem):  
    def __init__(self, rect: QRect, color: QColor = QColor(255, 242, 153)):
        super().__init__(rect)
        self.color = color

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.

        Args:
            painter (QPainter): The painter to use for painting.
            option (QStyleOptionGraphicsItem): Style options for the item.
            widget (QWidget): The widget to paint on.
        """
        pen = QPen(self.color, 3.0, Qt.SolidLine)
        pen.setCosmetic(True)

        painter.setBrush(QBrush(QColor(self.color.red(), self.color.green(), self.color.blue(), 20)))
        painter.setPen(pen)
        painter.drawRect(self.rect())