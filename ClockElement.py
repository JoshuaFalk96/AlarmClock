from random import choice

from PySide6.QtCore import QSize
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget

colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'white',
    'black'
]

class ClockElement(QWidget):
    def __init__(self):
        super().__init__()

        # placeholder
        self.setAutoFillBackground(True)
        self.setMinimumSize(QSize(200, 200))

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(QColor(choice(colors))))
        self.setPalette(palette)
