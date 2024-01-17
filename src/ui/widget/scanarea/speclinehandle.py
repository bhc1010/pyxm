from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class SpecLineHandle(QGraphicsRectItem):
    _handle_size = 30.0
    _hover_color = QColor(255, 20, 10)
    _no_hover_color = QColor(0, 0, 0)

    def __init__(self, parent, rect: QRectF = QRectF(0., 0., 0., 0.)):
        super().__init__(parent)
        self.parent = parent
        self.setRect(rect)
        self._handle_color = SpecLineHandle._no_hover_color

        self.toggle_flags(True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def toggle_flags(self, val):
        self.setAcceptHoverEvents(val)
        self.setFlag(QGraphicsItem.ItemIsMovable, val)
        self.setFlag(QGraphicsItem.ItemIsSelectable, val)
        self.setFlag(QGraphicsItem.ItemIsFocusable, val)

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).

        Args:
            moveEvent (QGraphicsSceneHoverEvent): The hover move event.
        """
        self._handle_color = SpecLineHandle._hover_color
        self.setCursor(Qt.CrossCursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).

        Args:
            moveEvent (QGraphicsSceneHoverEvent): The hover leave event.
        """
        self._handle_color = SpecLineHandle._no_hover_color
        self.setCursor(Qt.OpenHandCursor)
        super().hoverLeaveEvent(moveEvent)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)
        self.parent.update_line()

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.

        Args:
            painter (QPainter): The painter to use for painting.
            option (QStyleOptionGraphicsItem): Style options for the item.
            widget (QWidget): The widget to paint on.
        """
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self._handle_color, 2.0, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawRect(self.rect())