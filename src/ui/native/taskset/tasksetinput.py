from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *


class TaskSetInput(QLineEdit):
    """
    Custom QLineEdit widget with text elision.

    This widget is a custom QLineEdit that elides the text to the right when it exceeds the available width.
    The full text is displayed when the widget gains focus, and the elided text is restored when it loses focus.

    Attributes:
        _text (str): The full text content of the widget.
    """
    def __init__(self, text: str):
        """
        Initialize the TaskSetInput widget.

        Args:
            text (str): The initial text to be displayed in the widget.
        """
        super().__init__(text)
        self._text = text

        self.textChanged.connect(self.updateText)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def updateText(self, text):
        """
        Update the text content of the widget.

        Args:
            text (str): The new text content.

        Returns:
            None
        """
        self._text = text
    
    def elideText(self):
        """
        Elide the text when it exceeds the available width.

        Returns:
            None
        """
        padding = 8
        elidedText = self.fontMetrics().elidedText(self._text, Qt.TextElideMode.ElideRight, self.width() - padding)
        _text = self._text
        self.setText(elidedText)
        self.updateText(_text)
        self.setCursorPosition(0)

    def focusInEvent(self, event) -> None:
        """
        Event handler when the widget gains focus.

        Args:
            event (QFocusEvent): The focus event.

        Returns:
            None
        """
        self.setText(self._text)
        return super().focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        """
        Event handler when the widget loses focus.

        Args:
            event (QFocusEvent): The focus event.

        Returns:
            None
        """
        self.elideText()
        return super().focusOutEvent(event)
