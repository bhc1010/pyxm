from core.bounds import Bounds
from core.exponentialnumber import ExponentialNumber
from core.selection import Selection

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class ScientificSpinBox(QLineEdit):
    """
        A custom QLineEdit widget for handling scientific numbers with exponential notation.

        This class provides a custom QLineEdit widget that can display and edit scientific numbers using exponential notation.
        It allows the user to use arrow keys to navigate through the text, change the value, and handle scientific prefixes.

        Class attributes:
            _DECIMAL_POS (int): The default position of the decimal point.
            value_changed (Signal): Signal emitted when the value of the ScientificSpinBox changes.

        Signals:
            value_changed: Emitted when the value of the ScientificSpinBox changes.

        Args:
            value (ExponentialNumber): The initial value of the ScientificSpinBox.
            bounds (Bounds): The bounds for the valid range of the ScientificSpinBox.
            units (str): The units to be displayed with the value.

        Attributes:
            value (ExponentialNumber): The current value of the ScientificSpinBox.
            bounds (Bounds): The bounds for the valid range of the ScientificSpinBox.
            units (str): The units to be displayed with the value.
            selection (Selection): The current selection within the ScientificSpinBox.

        Methods:
            setValue: Set the value of the ScientificSpinBox.
            setBounds: Set the bounds for the valid range of the ScientificSpinBox.
            setUnits: Set the units to be displayed with the value of the ScientificSpinBox.
            keyPressEvent: Handle key presses and modify the value accordingly.
            update_text: Update the text displayed in the ScientificSpinBox.
    """
    _DECIMAL_POS = 5
    value_changed = Signal()

    def __init__(self, value: ExponentialNumber = ExponentialNumber.default(), bounds: Bounds = Bounds.default(), units: str = '[[unit]]', *args, **kwargs):
        """
            Initialize the ScientificSpinBox.

            Args:
                value (ExponentialNumber): The initial value of the ScientificSpinBox.
                bounds (Bounds): The bounds for the valid range of the ScientificSpinBox.
                units (str): The units to be displayed with the value.
        """
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
        """
            Set the value of the ScientificSpinBox.

            Args:
                value (ExponentialNumber): The new value to set for the ScientificSpinBox.
        """
        self.value = value
        self.update_text(emit=False)

    def setBounds(self, bounds: Bounds) -> None:
        """
            Set the bounds for the value of the ScientificSpinBox.

            This method allows setting the lower and upper bounds for the valid value range
            of the ScientificSpinBox. Any value outside this range will be clamped to the nearest bound.

            Args:
                bounds (Bounds): An instance of the Bounds class representing the lower and upper bounds.

            Example:
                bounds = Bounds(ExponentialNumber(0.001), ExponentialNumber(1000.0))
                spin_box.setBounds(bounds)
        """
        self.bounds = bounds
        self.update_text(emit=False)

    def setBounds(self, lower: ExponentialNumber, upper: ExponentialNumber) -> None:
        """
            Set the bounds for the value of the ScientificSpinBox.

            This method allows setting the lower and upper bounds for the valid value range
            of the ScientificSpinBox. Any value outside this range will be clamped to the nearest bound.

            Args:
                lower (ExponentialNumber): The lower bound value.
                upper (ExponentialNumber): The upper bound value.

            Example:
                lower_bound = ExponentialNumber(0.001)
                upper_bound = ExponentialNumber(1000.0)
                spin_box.setBounds(lower_bound, upper_bound)
        """
        self.bounds = Bounds(lower, upper)
        self.update_text(emit=False)

    def setUnits(self, units: str) -> None:
        """
            Set the units to be displayed with the value of the ScientificSpinBox.

            Args:
                units (str): The new units to display with the value.
        """
        self.units = units
        self.update_text(emit=False)

    def keyPressEvent(self, event) -> None:
        """
            Reimplemented key press event handler for the ScientificSpinBox.

            This method handles key press events specific to the ScientificSpinBox.
            It enables interaction with the spin box using arrow keys for navigation,
            as well as incrementing and decrementing the value when the up and down arrow keys are pressed.

            The supported key actions are as follows:
            - Left Arrow: Move the cursor one position to the left. If the current character is a digit, the cursor
                        will be moved to the left of the digit. If it is a decimal point or space, the cursor
                        will be moved to the left of the previous digit.
            - Right Arrow: Move the cursor one position to the right. If the current character is a digit, the cursor
                        will be moved to the right of the digit. If it is a decimal point or space, the cursor
                        will be moved to the right of the next digit.
            - Up Arrow: Increment the value. If a digit is selected, the increment is based on the digit position
                        from the decimal point. If the exponent prefix is selected ('p', 'n', 'u', etc.), the value
                        will be incremented by multiplying it by a factor of 1000. If the selected digit is the
                        leading digit (before the decimal point), the exponent will be increased by 3 to represent
                        a larger order of magnitude.
            - Down Arrow: Decrement the value. Works similarly to the Up Arrow but decrements the value instead.

            The method ensures that the value is clamped within the defined bounds after each operation.
            Additionally, the method emits the `value_changed` signal if the value is modified.

            Args:
                event (QKeyEvent): The key event object.

            Example:
                The following example shows how to interact with the ScientificSpinBox using arrow keys:

                - Pressing the Up Arrow will increment the value by a predefined step.
                - Pressing the Down Arrow will decrement the value by a predefined step.
                - Pressing the Left Arrow will move the cursor left.
                - Pressing the Right Arrow will move the cursor right.

                .. code-block:: python

                    spin_box = ScientificSpinBox()
                    spin_box.setText("123.456 k")
                    spin_box.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier))
                    # Output: The spin box value will be updated to '123.457 k'

            Note:
                - The method also handles selection-based value modifications when a specific part of the value
                is selected before pressing the arrow keys.
                - The method assumes that the spin box's text is formatted as an ExponentialNumber followed by a
                space and an exponent prefix, like '123.456 k' for 123.456 kilo.
                - The exponent prefix is generated by the ExponentialNumber.prefix() method.
        """
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
        """
            Update the text displayed in the ScientificSpinBox.

            This method updates the text displayed in the ScientificSpinBox based on the current value, bounds,
            and units set for the spin box. The updated text includes the absolute value of the significant digits,
            the exponential prefix, and the specified units, if any.

            The method ensures that the value is clamped within the defined bounds before updating the displayed text.
            If the value is negative, a minus sign ('-') is added to the text. If the value is positive, a plus sign
            ('+') is added to the text.

            The emitted signal `value_changed` can be toggled with the `emit` parameter. If `emit` is set to True
            (the default), the `value_changed` signal is emitted after updating the text.

            Args:
                emit (bool, optional): If True, the `value_changed` signal will be emitted after updating the text.
                                    Defaults to True.

            Example:
                The following example shows how to update the displayed text in the ScientificSpinBox:

                .. code-block:: python

                    spin_box = ScientificSpinBox()
                    spin_box.value = ExponentialNumber(123.456, exponent=3)  # 123.456 k
                    spin_box.units = "m/s"
                    spin_box.update_text()

                    print(spin_box.text())
                    # Output: '+123.456 km/s'

            Note:
                - The method assumes that the `value` attribute holds an ExponentialNumber object, which consists of
                the significant digits and exponent of the value.
                - The method uses the `bounds` attribute to clamp the value within the specified range before updating
                the text.
                - The `units` attribute, if specified, is appended to the updated text along with a space separator.
                For instance, if `units` is set to 'm/s', the updated text will include 'm/s' at the end.
                - If the value is not clamped and exceeds the maximum or minimum bounds, it will be adjusted to the
                nearest boundary value and reflected in the updated text.
        """
        self.value = self.bounds.clamp(self.value)
        self._text = f'{abs(self.value.sig):07.3f} {self.value.prefix()}{self.units}'
        if self.value.sig >= 0:
            self._text = f'+{self._text}'
        else:
            self._text = f'-{self._text}'
        self.setText(self._text)
        if emit:
            self.value_changed.emit()