from PySide6 import QtCore, QtGui, QtWidgets


class RotateGroupBox(QtWidgets.QGroupBox):
    """Create content to fill the widget"""

    def __init__(self, parent=None):
        super(RotateGroupBox, self).__init__(parent)

        self.setTitle("Rotation")

        self.l_rotate = QtWidgets.QSpinBox()
        self.l_rotate.setRange(0, 360)

        self.r_rotate = QtWidgets.QSpinBox()
        self.r_rotate.setRange(0, 360)

        self.l_label = QtWidgets.QLabel("Left: ")
        self.r_label = QtWidgets.QLabel("Right: ")

        layout = QtWidgets.QVBoxLayout(self)

        l1 = QtWidgets.QHBoxLayout()
        l1.setContentsMargins(0, 0, 0, 0)
        l1.addWidget(self.l_label)
        l1.addWidget(self.l_rotate)

        l2 = QtWidgets.QHBoxLayout()
        l2.setContentsMargins(0, 0, 0, 0)
        l2.addWidget(self.r_label)
        l2.addWidget(self.r_rotate)

        layout.addLayout(l1)
        layout.addLayout(l2)


class PropertyBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PropertyBox, self).__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.backgroundColor = QtGui.QColor("salmon")
        self.foregroundColor = QtGui.QColor("red")
        self.borderRadius = 10

        gr1 = RotateGroupBox()
        gr2 = RotateGroupBox()
        gr3 = RotateGroupBox()
        gr4 = RotateGroupBox()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(gr1)
        layout.addWidget(gr2)
        layout.addWidget(gr3)
        layout.addWidget(gr4)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(self.foregroundColor)
        painter.setBrush(self.backgroundColor)
        rect = QtCore.QRectF(
            QtCore.QPoint(),
            self.size() - 0.5 * painter.pen().width() * QtCore.QSize(1, 1),
        )
        painter.drawRoundedRect(rect, self.borderRadius, self.borderRadius)


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.m_widgets = dict()
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def addFixedWidget(self, widget, alignment):
        widget.setParent(self.viewport())
        self.m_widgets[widget] = alignment

    def showEvent(self, event):
        self._update_fixed_widgets()
        super(GraphicsView, self).showEvent(event)

    def resizeEvent(self, event):
        self._update_fixed_widgets()
        super(GraphicsView, self).resizeEvent(event)

    def _update_fixed_widgets(self):
        r = self.viewport().rect()
        for w, a in self.m_widgets.items():
            p = QtCore.QPoint()

            if a & QtCore.Qt.AlignHCenter:
                p.setX((r.width() - w.width()) / 2)
            elif a & QtCore.Qt.AlignRight:
                p.setX(r.width() - w.width())

            if a & QtCore.Qt.AlignVCenter:
                p.setY((r.height() - w.height()) / 2)
            elif a & QtCore.Qt.AlignBottom:
                p.setY(r.height() - w.height())
            w.move(p)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    scene = QtWidgets.QGraphicsScene()
    window = GraphicsView()
    window.resize(1000, 500)
    window.setScene(scene)
    window.addFixedWidget(
        PropertyBox(), QtCore.Qt.AlignRight | QtCore.Qt.AlignTop
    )
    rect = QtWidgets.QGraphicsRectItem()
    rect.setRect(0, 0, 200, 200)
    # rect.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
    scene.addItem(rect)
    window.show()
    sys.exit(app.exec())