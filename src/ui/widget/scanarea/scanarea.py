import PySide6.QtGui
import PySide6.QtWidgets
import numpy as np

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ui.widget.scanarea.scanrect import ScanRectItem
from ui.widget.scanarea.specline import SpecLineItem
from ui.widget.scanarea.speclinehandle import SpecLineHandle
from ui.widget.scanarea.scantoolbar import ScanAreaToolBar
from ui.widget.scanarea.toolmode import ToolMode

class GraphicsScene(QGraphicsScene):
    adjust_spec_line = Signal(float)

class ScanArea(QGraphicsView):
    """
    QGraphicsView for displaying and interacting with the scan area.

    This class provides a QGraphicsView that displays a scan area with a grid and allows interaction with the scan rectangle.
    The scan rectangle can be moved and resized within the scan area, and signals are emitted when these actions occur.

    Attributes:
        scan_rect_moved (Signal): Signal emitted when the scan rectangle is moved.
        scan_rect_resized (Signal): Signal emitted when the scan rectangle is resized.
    """
    scan_rect_moved = Signal()
    scan_rect_resized = Signal()
    
    def __init__(self, size:float, *args, **kwargs):
        """
        Initialize the ScanArea QGraphicsView.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._grid_size = 10
        self._zoom = 0
        self._size = size
        self._scene = GraphicsScene()
        self._scene.setSceneRect(QRect(-size/2, -size/2, size, size))
        self.setScene(self._scene)
        
        self.toolbar = ScanAreaToolBar()
        self.toolbar.setPos(-self._size/2 + 12.5, -self._size/2 + 12.5)
        self.toolbar._move_clicked.connect(self.enable_drag)
        self.toolbar._edit_rect_clicked.connect(self.enable_rect)
        self.toolbar._edit_spec_clicked.connect(self.enable_spec)
        self._scene.addItem(self.toolbar)

        self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor('white'))
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.draw_grid()
        
        self.scan_rect = ScanRectItem(init_rect = QRectF(-50, -50, 100, 100), scene_limits = [-self._size/2, self._size/2], min_size=0.120)
        self.spec_line = SpecLineItem(parent=self.scan_rect)
        self._scene.adjust_spec_line.connect(self.spec_line.update_aspect)
        self._new_spec_line = False

        self.scan_rect.setZValue(0.99)
        self.scene().addItem(self.scan_rect)

        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
        self._current_view = self._scene.sceneRect()

    def draw_grid(self):
        """
        Draw grid lines in the scene.

        This method draws grid lines within the scan area scene.
        """
        pen = QPen()
        pen.setCosmetic(True)
        half_size = self._size/2
        grid = np.linspace(-half_size, half_size, 11)
        for tick in range(self._grid_size + 1):
            if tick == 0 or tick == round(self._grid_size / 2) or tick == self._grid_size:
                pen.setColor(QColor(50,50,50))
            else:
                pen.setColor(QColor(218, 220, 224))
            self._scene.addLine(grid[tick], -half_size, grid[tick], half_size, pen)
            self._scene.addLine(-half_size, grid[tick], half_size, grid[tick], pen)

    def resizeEvent(self, event):
        """
        Resize event handler for the QGraphicsView.

        This method is called when the QGraphicsView is resized, and it adjusts the view to keep the current scene
        in focus and maintain the aspect ratio.

        Args:
            event (QResizeEvent): The resize event.
        """
        min_size = min(self.rect().width(), self.rect().height())
        self.resize(min_size, min_size)
        self.fitInView(self._current_view, Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        """
        Wheel event handler for zooming.

        This method is called when the mouse wheel is scrolled, and it handles zooming in and out of the scan area.

        Args:
            event (QWheelEvent): The wheel event.
        """
        if event.angleDelta().y() > 0:
            self.zoom_factor = 1.1
            self._zoom += 1
        else:
            self.zoom_factor = 0.9 
            self._zoom -= 1
        if self._zoom > 0:
            self.scale(self.zoom_factor, self.zoom_factor)
            self.scan_rect.handleSize /= self.zoom_factor
            self.scan_rect.handleSpace /= self.zoom_factor
            self.scan_rect.updateHandlesPos()

            self.spec_line._line_highlight_size /= self.zoom_factor
            self.spec_line._handle_size /= self.zoom_factor
            self.spec_line.update_handles()
        else:
            self._zoom = 0
            self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
            self.scan_rect.handleSize = ScanRectItem._handleSize
            self.scan_rect.handleSpace = -int(0.5*ScanRectItem._handleSize)
            self.spec_line._line_highlight_size = SpecLineItem._line_highlight_size
            self.spec_line._handle_size = SpecLineHandle._handle_size

        self.update_current_view()
        self.update_toolbar()

    def showEvent(self, event):
        """
        Show event handler.

        This method is called when the QGraphicsView is shown, and it updates the current view.

        Args:
            event (QShowEvent): The show event.
        """
        self.update_current_view()
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.toolbar.mode == ToolMode.SpecLine:
            sp = self.mapToScene(event.pos())
            item = self._scene.itemAt(sp, self.viewportTransform())
            if item not in self.toolbar.childItems():
                if item is not self.spec_line and item not in self.spec_line.childItems():
                    self.spec_line.set_initial(sp)
                    self._new_spec_line = True

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Mouse move event handler.

        This method is called when the mouse is moved within the QGraphicsView, and it handles updating the tool bar
        based on the mouse position.

        Args:
            event (QMouseEvent): The mouse move event.
        """
        super().mouseMoveEvent(event)
        if Qt.MouseButton.LeftButton in event.buttons():
            match self.toolbar.mode:
                case ToolMode.Move:
                    self.update_toolbar()
                case ToolMode.ScanRect:
                    if self.itemAt(event.pos()) == self.scan_rect:
                        self.scan_rect_moved.emit()
                case ToolMode.SpecLine:
                    if self._new_spec_line:
                        self.spec_line.set_final(self.mapToScene(event.pos()))

        
    def mouseReleaseEvent(self, event) -> None:
        """
        Mouse release event handler.

        This method is called when a mouse button is released within the QGraphicsView.

        Args:
            event (QMouseEvent): The mouse release event.
        """
        if self._new_spec_line:
            self._new_spec_line = False
        self.update_current_view()
        return super().mouseReleaseEvent(event)
    
    def update_current_view(self):
        """
        Update the current view.

        This method updates the current view based on the visible area of the QGraphicsView.
        """
        self._current_view = self.mapToScene(self.viewport().rect()).boundingRect()
        
    def update_toolbar(self):
        """
        Update the position of the tool bar.

        This method updates the position of the tool bar based on the mouse position.

        Returns:
            None
        """
        padding = self.mapToScene(QPoint(10, 10))
        top_left = self.mapToScene(self.viewport().rect()).boundingRect().topLeft()
        self.toolbar.setPos((top_left + padding)/2)

    def enable_drag(self):
        if self.toolbar.mode == ToolMode.Move:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        else:
            self.setCursor(Qt.ArrowCursor)
            self.setDragMode(QGraphicsView.NoDrag)
        
        self.scan_rect.toggle_flags(False)
        self.spec_line.toggle_flags(False)

    def enable_rect(self):
        if self.toolbar.mode == ToolMode.ScanRect:
            self.scan_rect.toggle_flags(True)
        else: 
            self.scan_rect.toggle_flags(False)

        self.setCursor(Qt.ArrowCursor)
        self.setDragMode(QGraphicsView.NoDrag)
        self.spec_line.toggle_flags(False)

    def enable_spec(self):
        if self.toolbar.mode == ToolMode.SpecLine:
            self.spec_line.toggle_flags(True)
        else:
            self.spec_line.toggle_flags(False)
        self.setCursor(Qt.ArrowCursor)
        self.setDragMode(QGraphicsView.NoDrag)
        self.scan_rect.toggle_flags(False)