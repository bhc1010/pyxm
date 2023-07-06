from core.bounds import Bounds
from core.exponentialnumber import ExponentialNumber
from core.selection import Selection

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class ScientificSpinBox(QLineEdit):
    _DECIMAL_POS = 5
    value_changed = Signal()

    def __init__(self, value: ExponentialNumber = ExponentialNumber.default(), bounds: Bounds = Bounds.default(), units: str = '[[unit]]', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value = value
        self.bounds = bounds
        self.units = units

        self.selection = Selection(-1, -1)
        self.update_text()
        self.setValidator(QRegularExpressionValidator(r'\\'))

        if 'width' not in kwargs:
            self.setFixedWidth(150)

    def setValue(self, value: ExponentialNumber) -> None:
        self.value = value
        self.update_text(emit=False)

    def setBounds(self, bounds: Bounds) -> None:
        self.bounds = bounds
        self.update_text(emit=False)

    def setBounds(self, lower: ExponentialNumber, upper: ExponentialNumber) -> None:
        self.bounds = Bounds(lower, upper)
        self.update_text(emit=False)

    def setUnits(self, units: str) -> None:
        self.units = units
        self.update_text(emit=False)

    def keyPressEvent(self, event) -> None:
        ##-------- Left Arrow ------------##
        if event.key() == Qt.Key.Key_Left:
            pos = self.cursorPosition()
            newPos = pos - 1
            if newPos > 0: 
                self.setSelection(newPos - 1, 1)
                if self.selectedText() in ['.', ' ']:
                    self.setSelection(max(newPos - 2, 0), 1)
            self.selection.update(self.selectionStart(), self.selectionEnd())

        ##-------- Right Arrow ------------##
        elif event.key() == Qt.Key.Key_Right:
            pos = self.cursorPosition()
            newPos = pos + 1
            if newPos <= len(self.text()) - 1:
                self.setSelection(pos, 1)
                if self.selectedText() in ['.', ' ']:
                    self.setSelection(pos + 1, 1)
            self.selection.update(self.selectionStart(), self.selectionEnd())

        ##-------- Up Arrow ------------##
        elif event.key() == Qt.Key.Key_Up:
            selected_grapheme = self.selectedText()
            pos = self.cursorPosition()
            if selected_grapheme.isdigit():
                greater_than_one = pos < self._DECIMAL_POS
                if greater_than_one:
                    step = 10 ** (self._DECIMAL_POS - pos - 1)
                else:
                    step = 10 ** (self._DECIMAL_POS - pos)

                self.value.sig = self.value.sig + step
                if self.value.sig > 1000.0:
                    self.value.sig /= 1000.0
                    self.value.exp += 3
                    
                    self.update_text()
                    self.setSelection(self.selection.start + 2, 1)
                    self.selection.shift(self._DECIMAL_POS - pos - 1)
                elif 0 < abs(self.value.sig) and abs(self.value.sig) < 1:
                    self.value.sig *= 1000.0
                    self.value.exp -= 3

                    self.update_text()
                    self.setSelection(max(self.selection.start - 4, 1), 1)
                    self.selection.shift(-4) 
                else:
                    self.update_text()
                    self.setSelection(self.selection.start, 1)
            elif selected_grapheme == '-':
                self.value.sig *= -1
                self.update_text()
                self.setSelection(self.selection.start, 1)
            elif selected_grapheme in ExponentialNumber.prefix_map.values():
                if self.value.exp < 3:
                    self.value.exp += 3
                    self.update_text()
                    self.setSelection(self.selection.start, 1)

        ##-------- Down Arrow ------------##
        elif event.key() == Qt.Key.Key_Down:
            selected_grapheme = self.selectedText()
            pos = self.cursorPosition()
            if selected_grapheme.isdigit():
                greater_than_one = pos < self._DECIMAL_POS
                if greater_than_one:
                    step = 10 ** (self._DECIMAL_POS - pos - 1)
                else:
                    step = 10 ** (self._DECIMAL_POS - pos)

                self.value.sig = self.value.sig - step
                if self.value.sig < -1000.0:
                    self.value.sig /= 1000.0
                    self.value.exp += 3

                    self.update_text()
                    self.setSelection(self.selection.start + 2, 1)
                    self.selection.shift(self._DECIMAL_POS - pos - 1)
                elif 0 < abs(self.value.sig) and abs(self.value.sig) < 1 - 0.0001:
                    self.value.sig *= 1000.0
                    self.value.exp -= 3

                    self.update_text()
                    self.setSelection(max(self.selection.start - 4, 1), 1)
                    self.selection.shift(-4) 
                else:
                    self.update_text()
                    self.setSelection(self.selection.start, 1)
            elif selected_grapheme == '+':
                self.value.sig *= -1
                self.update_text()
                self.setSelection(self.selection.start, 1)
            elif selected_grapheme in ExponentialNumber.prefix_map.values():
                if self.value.exp > -12:
                    self.value.exp -= 3
                    self.update_text()
                    self.setSelection(self.selection.start, 1)

    def update_text(self, emit=True):
        self.value = self.bounds.clamp(self.value)
        self._text = f'{abs(self.value.sig):07.3f} {self.value.prefix()}{self.units}'
        if self.value.sig >= 0:
            self._text = f'+{self._text}'
        else:
            self._text = f'-{self._text}'
        self.setText(self._text)
        if emit:
            self.value_changed.emit()