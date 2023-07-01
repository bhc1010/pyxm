from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem


class ScanRectItem(QGraphicsRectItem):

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = +8.0
    handleSpace = -4.0

    handleCursors = {
        handleTopLeft: Qt.SizeFDiagCursor,
        handleTopMiddle: Qt.SizeVerCursor,
        handleTopRight: Qt.SizeBDiagCursor,
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomLeft: Qt.SizeBDiagCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }

    def __init__(self, scene_limits: float, init_rect: QRectF):
        """
        Initialize the shape.
        """
        super().__init__(init_rect)
        self.scene_limits = scene_limits
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)
            bbox = self.sceneBoundingRect()
            offset = 0.5*bbox.width()
            pos = bbox.center()
            x, y = pos.x(), pos.y()
            limit = self.scene_limits - offset
            scene_limit = 0.5*self.scene_limits - offset
            if x < offset:
                self.setX(-scene_limit)
            elif x > limit:
                self.setX(scene_limit)

            if y < offset:
                self.setY(-scene_limit)
            elif y > limit:
                self.setY(scene_limit)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        rect = self.rect()
        dx = mousePos.x() - self.mousePressPos.x()
        dy = mousePos.y() - self.mousePressPos.y()
        diff = QPointF(dx, dy)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleTopLeft:
            newTopLeft = self.mousePressRect.topLeft() + diff
            newRect = QRectF(self.mousePressRect)
            newRect.setTopLeft(newTopLeft)
            newHeight = newRect.height()
            newWidth = newRect.width()
            
            if newHeight < newWidth:
                newTopLeft = self.mousePressRect.topLeft() + QPointF(dy, dy)
            else:
                newTopLeft = self.mousePressRect.topLeft() + QPointF(dx, dx)

            rect.setTopLeft(newTopLeft)

        elif self.handleSelected == self.handleTopRight:
            newTopRight = self.mousePressRect.topRight() + diff
            newRect = QRectF(self.mousePressRect)
            newRect.setTopRight(newTopRight)
            newHeight = newRect.height()
            newWidth = newRect.width()
            
            if newHeight < newWidth:
                newTopRight = self.mousePressRect.topRight() + QPointF(-dy, dy)
            else:
                newTopRight = self.mousePressRect.topRight() + QPointF(dx, -dx)

            rect.setTopRight(newTopRight)

        elif self.handleSelected == self.handleBottomLeft:
            newBottomLeft = self.mousePressRect.bottomLeft() + diff
            newRect = QRectF(self.mousePressRect)
            newRect.setBottomLeft(newBottomLeft)
            newHeight = newRect.height()
            newWidth = newRect.width()
            
            if newHeight < newWidth:
                newBottomLeft = self.mousePressRect.bottomLeft() + QPointF(-dy, dy)
            else:
                newBottomLeft = self.mousePressRect.bottomLeft() + QPointF(dx, -dx)

            rect.setBottomLeft(newBottomLeft)

        elif self.handleSelected == self.handleBottomRight:
            newBottomRight = self.mousePressRect.bottomRight() + diff
            newRect = QRectF(self.mousePressRect)
            newRect.setBottomRight(newBottomRight)
            newHeight = newRect.height()
            newWidth = newRect.width()
            
            if newHeight < newWidth:
                newBottomRight = self.mousePressRect.bottomRight() + QPointF(dy, dy)
            else:
                newBottomRight = self.mousePressRect.bottomRight() + QPointF(dx, dx)

            rect.setBottomRight(newBottomRight)

        center = self.rect().center()
        new_center = rect.center()
        rect.translate(center - new_center)

        self.setRect(rect)
        # self.setPos(new_center.toSceneCoordinates())
        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addRect(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        pen = QPen(QColor(102, 157, 246), 3.0, Qt.SolidLine)
        pen.setCosmetic(True)

        painter.setBrush(QBrush(QColor(102, 157, 246, 5)))
        painter.setPen(pen)
        painter.drawRect(self.rect())

        pen.setColor('red')
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(pen)
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawRect(rect)