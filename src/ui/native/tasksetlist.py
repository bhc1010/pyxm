from PySide6.QtGui import Qt
from PySide6.QtWidgets import *

from core.tasksetdata import TaskSetData
from ui.native.taskset import TaskSet

class TaskSetList(QGroupBox):
    def __init__(self, title, objectName) -> None:
        super().__init__(title, objectName=objectName)
        self.task_sets = list()
        self.all_tasks = list()

        self._contents = QWidget(self)
        self._scrollarea = QScrollArea()
        self._scrollarea.setWidget(self._contents)
        self._scrollarea.setWidgetResizable(True)
        self._scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setSpacing(3)
        self._layout.setContentsMargins(0,0,5,0)
        self._contents.setLayout(self._layout)

        self.setFlat(True)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._scrollarea)
        self.layout().setContentsMargins(0,0,0,0)

    def add_task_set(self, task_set_name, task_set_data: TaskSetData):
        task_set = TaskSet(name=task_set_name, data=task_set_data, idx=len(self.task_sets), dropFunc=self.drop_task)
        task_set.adjustTextWidth()

        self.task_sets.append(task_set)
        self.all_tasks.append(task_set.data.tasks)
        self._layout.addWidget(task_set)

    def drop_task(self, idx):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Remove Task")
        dlg.setText("Are you sure you want to remove this task?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)

        if dlg.exec_() == QMessageBox.Yes:
            self.tasks.pop(idx)
            for (i, task) in enumerate(self.tasks):
                task.setIndex(i)
            self._layout.takeAt(idx).widget().deleteLater()

