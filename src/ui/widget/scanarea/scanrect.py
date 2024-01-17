from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ScanRectItem(QGraphicsRectItem):
    """
    Custom QGraphicsRectItem representing a resizable and movable rectangle in the QGraphicsView.

    This class provides a custom QGraphicsRectItem with interactive resizing and movement capabilities.
    The rectangle can be resized from its handles and moved within the scene. It emits signals when selected,
    resized, and moved.

    Attributes:
        handleTopLeft (int): Identifier for the top-left resize handle.
        handleTopMiddle (int): Identifier for the top-middle resize handle.
        handleTopRight (int): Identifier for the top-right resize handle.
        handleMiddleLeft (int): Identifier for the middle-left resize handle.
        handleMiddleRight (int): Identifier for the middle-right resize handle.
        handleBottomLeft (int): Identifier for the bottom-left resize handle.
        handleBottomMiddle (int): Identifier for the bottom-middle resize handle.
        handleBottomRight (int): Identifier for the bottom-right resize handle.
        _handleSize (int): Size of the resize handles.
        handleCursors (dict): Dictionary mapping resize handle identifiers to their corresponding cursor types.

    Signals:
        handleMoved: Signal emitted when the handle is moved.
        shapeResized: Signal emitted when the shape is resized.
        shapeMoved: Signal emitted when the shape is moved.
    """
    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8
    
    _handleSize = 25

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
        Initialize the ScanRectItem.

        Args:
            init_rect (QRectF): Initial bounding rectangle for the ScanRectItem.
            scene_limits (float): Limit of the scene area where the ScanRectItem can be moved.
            min_size (float): Minimum size of the ScanRectItem.
        """
        super().__init__(init_rect)
        self.scene_limits = scene_limits  
        self.min_size = min_size  
        self.handles = {}
        self.handleSize = ScanRectItem._handleSize
        self.handleSpace = -int(0.5*ScanRectItem._handleSize)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.handle_color = QColor(0,0,0)
        self.toggle_flags(False)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.updateHandlesPos()

    def toggle_flags(self, val):
        self.setAcceptHoverEvents(val)
        self.setFlag(QGraphicsItem.ItemIsMovable, val)
        self.setFlag(QGraphicsItem.ItemIsSelectable, val)
        self.setFlag(QGraphicsItem.ItemIsFocusable, val)


    def handleAt(self, point):
        """
        Returns the resize handle below the given point.

        Args:
            point (QPointF): The point where to check for a handle.

        Returns:
            int or None: The identifier of the handle below the given point, or None if no handle is found.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).

        Args:
            moveEvent (QGraphicsSceneHoverEvent): The hover move event.
        """
        self.handle_color = QColor(255, 20, 10)
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).

        Args:
            moveEvent (QGraphicsSceneHoverEvent): The hover leave event.
        """
        self.handle_color = QColor(0, 0, 0)
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.

        Args:
            mouseEvent (QGraphicsSceneMouseEvent): The mouse press event.
        """
        self.mousePressPos = mouseEvent.pos()
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.

        Args:
            mouseEvent (QGraphicsSceneMouseEvent): The mouse move event.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent)
        else:
            super().mouseMoveEvent(mouseEvent)
            
            bbox = self.scene_inner_rect()
            offset = 0.5*bbox.width()
            pos = bbox.center()
            x, y = pos.x(), pos.y()

            # Keep within bounds
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

        Args:
            mouseEvent (QGraphicsSceneMouseEvent): The mouse release event.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).

        Returns:
            QRectF: The bounding rect of the ScanRectItem.
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)
    
    def scene_inner_rect(self):
        """
        Returns the scene space bounding rect of the shape (excluding the resize handles).

        Returns:
            QRectF: The scene space bounding rect of the ScanRectItem.
        """
        o = self.handleSize + self.handleSpace
        return self.sceneBoundingRect().adjusted(o, o, -o, -o)
        

    def in_bounds(self, bbox) -> bool:
        """
        Check if the bounding box is within the scene limits.

        Args:
            bbox (QRectF): The bounding box to check.

        Returns:
            bool: True if the bounding box is within the scene limits, False otherwise.
        """
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

    def interactiveResize(self, mouseEvent: QMouseEvent):
        """
        Perform shape interactive resize.

        Args:
            mouseEvent (QMouseEvent): The mouse event for the resize operation.
        """
        rect = self.rect()
        mousePos = mouseEvent.pos()
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
            old_pos = self.pos()

            # Set new rect
            self.setRect(rect)
            if Qt.KeyboardModifier.ShiftModifier not in mouseEvent.modifiers():
                self.setPos(self.mapToScene(new_center))
            if not self.in_bounds(self.scene_inner_rect()):
                self.setRect(old_rect)
                self.setPos(old_pos)
            self.updateHandlesPos()

            # Resize specline
            scale = self.rect().width() / old_rect.width()
            self.scene().adjust_spec_line.emit(scale)

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.

        Returns:
            QPainterPath: The shape of the ScanRectItem.
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

        Args:
            painter (QPainter): The painter to use for painting.
            option (QStyleOptionGraphicsItem): Style options for the item.
            widget (QWidget): The widget to paint on.
        """
        pen = QPen(QColor(102, 157, 246), 3.0, Qt.SolidLine)
        pen.setCosmetic(True)

        painter.setBrush(QBrush(QColor(102, 157, 246, 25)))
        painter.setPen(pen)
        painter.drawRect(self.rect())

        pen.setColor(QColor(0,0,0,0))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.handle_color))
        painter.setPen(pen)
        for _, rect in self.handles.items():
            painter.drawRect(rect)
