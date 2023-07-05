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

    def __init__(self,  init_rect: QRectF, scene_limits: float, min_size: float):
        """
        Initialize the shape.
        """
        super().__init__(init_rect)
        self.scene_limits = scene_limits  
        self.min_size = min_size  
        self.handles = {}
        self.handleSize = +18
        self.handleSpace = -9
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.handle_color = QColor(0,0,0)
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
        self.handle_color = QColor(255, 0, 0)
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.handle_color = QColor(0, 0, 0)
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
            
            o = self.handleSize + self.handleSpace
            bbox = self.scene_inner_rect()
            offset = 0.5*bbox.width()
            pos = bbox.center()
            x, y = pos.x(), pos.y()
            limit_lower = self.scene_limits[0] + offset
            limit_upper = self.scene_limits[1] - offset
            scene_limit_lower = self.scene_limits[0] + offset
            scene_limit_upper = self.scene_limits[1] - offset
            if x < limit_lower:
                self.setX(scene_limit_lower)
            elif x > limit_upper:
                self.setX(scene_limit_upper)

            if y < limit_lower:
                self.setY(scene_limit_lower)
            elif y > limit_upper:
                self.setY(scene_limit_upper)

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
    
    def scene_inner_rect(self):
        """
        Returns the scene space bounding rect of the shape (excluding the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.sceneBoundingRect().adjusted(o, o, -o, -o)
        

    def in_bounds(self, bbox) -> bool:
        limit_lower = self.scene_limits[0]
        limit_upper = self.scene_limits[1]
        if bbox.left() < limit_lower or bbox.right() > limit_upper:
            return False
        elif bbox.top() < limit_lower or bbox.bottom() > limit_upper:
            return False
        else:
            return True

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
        self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
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

        if rect.width() > self.min_size:
            old_rect = self.rect()
            self.setRect(rect)
            if not self.in_bounds(self.scene_inner_rect()):
                self.setRect(old_rect)
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

        pen.setColor(QColor(0,0,0,0))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.handle_color))
        painter.setPen(pen)
        for _, rect in self.handles.items():
            painter.drawRect(rect)