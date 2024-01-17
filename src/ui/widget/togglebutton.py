from PySide6.QtWidgets import QPushButton
import qtawesome as fa

class ToggleButton(QPushButton):
    """
        A custom toggle button widget for the STM Automator application.

        This class represents a custom toggle button widget used in the STM Automator application. The button displays an
        icon from the FontAwesome icon set and changes color when toggled. It inherits from QPushButton and overrides
        certain methods to provide custom behavior.

        Parameters:
            objectName (str): The object name for the button.
            unchecked (str, optional): The color of the icon when the button is unchecked. Default is '#fff'.
            checked (str, optional): The color of the icon when the button is checked. Default is "#9badca".

        Attributes:
            _unchecked_color (str): The color of the icon when the button is unchecked.
            _checked_color (str): The color of the icon when the button is checked.
            _icon (QIcon): The icon for the button.
    """

    def __init__(self, objectName, unchecked='#fff', checked="#9badca", toggle=True):
        """
            Initialize the ToggleButton.

            Args:
                objectName (str): The object name for the button.
                unchecked (str, optional): The color of the icon when the button is unchecked. Default is '#fff'.
                checked (str, optional): The color of the icon when the button is checked. Default is "#9badca".
        """
        super().__init__(objectName=objectName)
        
        self._unchecked_color: str = unchecked
        self._checked_color: str = checked

        self._icon = fa.icon(f'fa5s.{self.objectName()}', color=self._unchecked_color)
        self.setIcon(self._icon)
        self.setCheckable(toggle)

        self.clicked.connect(self.toggle)

    def setColor(self, color):
        """
            Set the color of the icon.

            This method sets the color of the icon displayed on the button.

            Args:
                color (str): The color to set for the icon.
        """
        self._icon = fa.icon(f'fa5s.{self.objectName()}', color=color)
        self.setIcon(self._icon)

    def set_checked(self, val: bool):
        self.setChecked(val)
        self.toggle()

    def toggle(self):
        """
            Toggle the button and change the icon color.

            This method is called when the button is clicked. It toggles the button's checked state and changes the icon
            color accordingly.
        """
        if self.isChecked():
            self.setColor(self._checked_color)
        else:
            self.setColor(self._unchecked_color)

    def enterEvent(self, event) -> None:
        """
            Event handler for mouse entering the button area.

            This method is called when the mouse pointer enters the button area. It changes the icon color to the checked
            color if the button is unchecked.

            Args:
                event (QEvent): The event that triggered this method.
        """
        if not self.isChecked():
            self.setColor(self._checked_color)

        return super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        """
            Event handler for mouse leaving the button area.

            This method is called when the mouse pointer leaves the button area. It changes the icon color to the unchecked
            color if the button is unchecked.

            Args:
                event (QEvent): The event that triggered this method.
        """
        if not self.isChecked():
            self.setColor(self._unchecked_color)

        return super().leaveEvent(event)