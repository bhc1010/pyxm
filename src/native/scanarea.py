import numpy as np

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from native.scanrect import ScanRectItem

class ScanArea(QGraphicsView):
    scan_rect_moved = Signal()
    scan_rect_resized = Signal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_size = 10
        self._zoom = 0
        self._scene = QGraphicsScene()
        self._scene.setSceneRect(QRect(-500., -500., 1000., 1000.))
        self.setScene(self._scene)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor('white'))
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.draw_grid()
        
        self.scan_rect = ScanRectItem(init_rect = QRectF(-50, -50, 100, 100), scene_limits = [-500, 500], min_size=0.120)
        self.scene().addItem(self.scan_rect)

        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
        self._current_view = self._scene.sceneRect()

    def draw_grid(self):
        pen = QPen()
        pen.setCosmetic(True)
        grid = np.linspace(-500, 500, 11)
        for tick in range(self._grid_size + 1):
            if tick == 0 or tick == round(self._grid_size / 2) or tick == self._grid_size:
                pen.setColor(QColor(50,50,50))
            else:
                pen.setColor(QColor(218, 220, 224))
            self._scene.addLine(grid[tick], -500., grid[tick], 500., pen)
            self._scene.addLine(-500., grid[tick], 500., grid[tick], pen)

    def resizeEvent(self, event):
        min_size = min(self.rect().width(), self.rect().height())
        self.resize(min_size, min_size)
        self.fitInView(self._current_view, Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.1
            self._zoom += 1
        else:
            factor = 0.9 
            self._zoom -= 1
        if self._zoom > 0:
            self.scale(factor, factor)
            self.scan_rect.handleSize /= factor
            self.scan_rect.handleSpace /= factor
            self.scan_rect.updateHandlesPos()
        else:
            self._zoom = 0
            self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
            self.scan_rect.handleSize = 18
            self.scan_rect.handleSpace = -9

        self.updateCurrentView()

    def showEvent(self, event):
        self.updateCurrentView()
        
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if Qt.MouseButton.LeftButton in event.buttons():
            if self.itemAt(event.pos()) == self.scan_rect:
                self.scan_rect_moved.emit()
        return super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event) -> None:
        self.updateCurrentView()
        return super().mouseReleaseEvent(event)

    def toggleDragMode(self):
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.setDragMode(QGraphicsView.NoDrag)
        else:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
    
    def updateCurrentView(self):
        self._current_view = self.mapToScene(self.viewport().rect()).boundingRect()