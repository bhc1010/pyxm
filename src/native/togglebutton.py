import PySide6.QtCore
from PySide6.QtWidgets import QPushButton
import qtawesome as fa

class ToggleButton(QPushButton):
    _unchecked = '#fff'
    _checked = '#9badca'

    def __init__(self, objectName):
        super().__init__(objectName=objectName)

        self._icon = fa.icon(f'fa5s.{self.objectName()}', color=ToggleButton._unchecked)
        self.setIcon(self._icon)
        self.setCheckable(True)

        self.clicked.connect(self.toggle)

    def setColor(self, color):
        self._icon = fa.icon(f'fa5s.{self.objectName()}', color=color)
        self.setIcon(self._icon)

    def toggle(self):
        if self.isChecked():
            self.setColor(ToggleButton._checked)
        else:
            self.setColor(ToggleButton._unchecked)

    def enterEvent(self, event) -> None:
        if not self.isChecked():
            self.setColor(ToggleButton._checked)

        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        if not self.isChecked():
            self.setColor(ToggleButton._unchecked)

        return super().leaveEvent(event)