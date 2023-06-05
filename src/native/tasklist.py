from PySide6.QtGui import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QGroupBox, QScrollArea

from native.task import Task

class TaskList(QGroupBox):
    def __init__(self, title, objectName) -> None:
        super().__init__(title, objectName=objectName)
        self.tasks = list()

        self._contents = QWidget(self)
        self._scrollarea = QScrollArea()
        self._scrollarea.setWidget(self._contents)
        self._scrollarea.setWidgetResizable(True)

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self._contents.setLayout(self._layout)

        self.setFlat(True)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._scrollarea)
        self.layout().setContentsMargins(0,0,0,0)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self._layout.addWidget(task)