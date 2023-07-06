import PySide6.QtCore
from PySide6.QtWidgets import QPushButton
import qtawesome as fa

class ToggleButton(QPushButton):

    def __init__(self, objectName, unchecked='#fff', checked="#9badca"):
        super().__init__(objectName=objectName)
        
        self._unchecked = unchecked
        self._checked = checked

        self._icon = fa.icon(f'fa5s.{self.objectName()}', color=self._unchecked)
        self.setIcon(self._icon)
        self.setCheckable(True)

        self.clicked.connect(self.toggle)

    def setColor(self, color):
        self._icon = fa.icon(f'fa5s.{self.objectName()}', color=color)
        self.setIcon(self._icon)

    def toggle(self):
        if self.isChecked():
            self.setColor(self._checked)
        else:
            self.setColor(self._unchecked)

    def enterEvent(self, event) -> None:
        if not self.isChecked():
            self.setColor(self._checked)

        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        if not self.isChecked():
            self.setColor(self._unchecked)

        return super().leaveEvent(event)