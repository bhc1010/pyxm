from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import PySide6.QtWidgets

from ui.widget.scanarea.speclinehandle import SpecLineHandle

class SpecLineItem(QGraphicsLineItem):
    _line_highlight_size = 30.

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.size = 0.
        self.x_offset = 0.
        self.y_offset = 0.
        self.angle = 0.
        self.density = 8

        self._center_color = QColor(255, 20, 10, 255)
        self._line_color = QColor(102, 157, 246)
        self._line_highlight_size = SpecLineItem._line_highlight_size
        self._handle_size = SpecLineHandle._handle_size
        self._handles = [SpecLineHandle(self), SpecLineHandle(self, rect=QRectF(0., 0., 10., 10.))]

        self.update_handles()
        self.update_line()

        self.toggle_flags(False)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def toggle_flags(self, val):
        self.setAcceptHoverEvents(val)
        self.setFlag(QGraphicsItem.ItemIsMovable, val)
        self.setFlag(QGraphicsItem.ItemIsSelectable, val)
        self.setFlag(QGraphicsItem.ItemIsFocusable, val)

        for h in self._handles:
            h.toggle_flags(val)

    def update_aspect(self, scale):
        for h in self._handles:
            x, y = h.pos().x(), h.pos().y()
            h.setPos(x * scale, y * scale)
        self.update_line()
        self.setPos(self.pos() * scale)

    def update_handles(self):
        s = self._handle_size
        for h in self._handles:
            h.setRect(QRectF(0., 0., s, s))
        self.update_line()

    def update_line(self):
        s = self._handle_size
        p0 = self._handles[0].pos()
        p1 = self._handles[1].pos()

        self.setLine(QLineF(p0.x() + s/2, 
                            p0.y() + s/2, 
                            p1.x() + s/2, 
                            p1.y() + s/2))

    def calculate_differential(self):
        p0 = self._handles[0].pos()
        p1 = self._handles[1].pos()
        dx = p1.x() - p0.x()
        dy = p1.y() - p0.y()
        return QPointF(dx, dy) / (self.density - 1)

    def set_initial(self, pos: QPointF):
        sp = self.mapFromScene(pos)
        for h in self._handles:
            h.setPos(sp)
        self.update_handles()

    def set_final(self, pos: QPointF):
        sp = self.mapFromScene(pos)
        self._handles[1].setPos(sp)
        self.update_handles()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.update_line()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self.update()

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).

        Args:
            moveEvent (QGraphicsSceneHoverEvent): The hover move event.
        """
        self.setCursor(Qt.UpArrowCursor)
        self._center_color.setAlpha(255)
        for h in self._handles:
            h._handle_color = SpecLineHandle._hover_color
            h.update()
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).

        Args:
            moveEvent (QGraphicsSceneHoverEvent): The hover leave event.
        """
        self.setCursor(Qt.OpenHandCursor)
        self._center_color.setAlpha(0)
        for h in self._handles:
            h._handle_color = SpecLineHandle._no_hover_color
            h.update()
        super().hoverLeaveEvent(moveEvent)

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.

        Args:
            painter (QPainter): The painter to use for painting.
            option (QStyleOptionGraphicsItem): Style options for the item.
            widget (QWidget): The widget to paint on.
        """
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self._line_color, 3.0, Qt.SolidLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(self.line())

        painter.setBrush(QBrush(self._line_color))
        dv = self.calculate_differential()
        spec_point = self._handles[0].pos()
        offset = QPointF(-self._handle_size/2, -self._handle_size/2)
        for _ in range(self.density - 2):
            spec_point += dv
            painter.drawEllipse(spec_point - offset, self._handle_size/3.5, self._handle_size/3.5)  

        pen = QPen(self._center_color, self._line_highlight_size, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawPoint(self.boundingRect().center())