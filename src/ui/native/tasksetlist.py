from typing import List

from PySide6.QtGui import Qt
from PySide6.QtWidgets import *

from core.tasksetdata import TaskSetData
from ui.native.taskset.taskset import TaskSet

class TaskSetList(QGroupBox):
    """
        Represents a group box containing a list of task sets.

        This class extends QGroupBox and provides a visual representation of a list of task sets. Each task set is displayed
        as a separate TaskSet widget, and users can add new task sets, remove task sets, and interact with individual tasks.

        Attributes:
            task_sets (List[TaskSet]): A list of TaskSet objects representing the individual task sets.
            all_tasks (List): A list containing all the tasks from all the task sets in the TaskSetList.
            _contents (QWidget): The widget that contains the list of task sets.
            _scrollarea (QScrollArea): The scroll area used to display the task sets.
            _layout (QVBoxLayout): The layout used to arrange the task sets in the scroll area.

    """
    
    def __init__(self, title, objectName) -> None:
        """
            Initialize the TaskSetList.

            Args:
                title (str): The title to be displayed on the group box.
                objectName: The object name used to identify the group box.
        """
        super().__init__(title, objectName=objectName)
        self.task_sets: List[TaskSet] = list()
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

    def add_task_set(self, data: TaskSetData):
        """
            Add a new task set to the TaskSetList.

            Args:
                data (TaskSetData): The TaskSetData object representing the data for the new task set.
        """
        task_set = TaskSet(name=data.name, data=data, idx=len(self.task_sets), dropFunc=self.drop_task)
        task_set.adjustTextWidth()

        self.task_sets.append(task_set)
        self.all_tasks.extend(task_set.tasks)
        self._layout.addWidget(task_set)

    def drop_task(self, idx):
        """
            Remove a task set from the TaskSetList.

            This method is called when a user requests to remove a task set. It prompts the user for confirmation before
            removing the task set.

            Args:
                idx (int): The index of the task set to be removed.
        """
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Remove Task")
        dlg.setText("Are you sure you want to remove this task?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)

        if dlg.exec_() == QMessageBox.Yes:
            self.task_sets.pop(idx)
            for (i, task_set) in enumerate(self.task_sets):
                task_set.setIndex(i)
            self._layout.takeAt(idx).widget().deleteLater()

