from PySide6.QtCore import QRect
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene

from PySide6 import QtWidgets, QtCore

class ScanArea(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_size = 10
        self._zoom = 0
        self._scene = QGraphicsScene()
        self._scene.setSceneRect(QRect(0., 0., 1000., 1000.))
        self.setScene(self._scene)

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor('white'))
        # self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.draw_grid()
        self.fitInView(self._scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self._current_view = self._scene.sceneRect()

    def draw_grid(self):
        for tick in range(self._grid_size + 1):
            if tick == 0 or tick == round(self._grid_size / 2) or tick == self._grid_size:
                self._scene.addLine(tick*100, 0., tick*100, 1000., QColor(50, 50, 50))
                self._scene.addLine(0., tick*100, 1000., tick*100, QColor(50, 50, 50))
                continue
            self._scene.addLine(tick*100, 1., tick*100, 1000., QColor(218, 220, 224))
            self._scene.addLine(1., tick*100, 1000., tick*100, QColor(218, 220, 224))

    def resizeEvent(self, event):
        min_size = min(self.rect().width(), self.rect().height())
        self.resize(min_size, min_size)
        self.fitInView(self._current_view, QtCore.Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.1
            self._zoom += 1
        else:
            factor = 0.9 
            self._zoom -= 1
        print(self._zoom)
        if self._zoom > 0:
            self.scale(factor, factor)
        else:
            self._zoom = 0
            self.fitInView(self._scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

        self.updateCurrentView()

    def showEvent(self, event):
        self.updateCurrentView()
        
    def mouseReleaseEvent(self, event) -> None:
        self.updateCurrentView()
        return super().mouseReleaseEvent(event)

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        else:
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
    
    def updateCurrentView(self):
        self._current_view = self.mapToScene(self.viewport().rect()).boundingRect()