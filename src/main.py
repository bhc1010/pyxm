import sys
import qdarktheme
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication

from ui.app import Ui_MainWindow

# Set a global attribute to share OpenGL contexts between threads for better performance
QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

# Initialize the Qt application
app = QApplication(sys.argv)

# Load custom CSS style from a file
style = Path('src/ui/style.css').read_text()

# Set up the QDarkTheme with custom colors and additional CSS style
qdarktheme.setup_theme(
    theme="light",  # The theme can be "light" or "dark"
    custom_colors={
        "background": "#fff",  # Set the background color to white (#fff)
    },
    additional_qss=style  # Apply additional CSS styles from the loaded file
)

# Create an instance of the main application window
win = Ui_MainWindow()

# Set the custom style sheet for the main application window
win.setStyleSheet(style)

# Show the main application window
win.show()

# Start the Qt application event loop
app.exec()
