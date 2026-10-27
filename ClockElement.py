from random import choice

from PySide6.QtCore import QSize
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem

colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'white',
    'black'
]

class ClockElement(QWidget):
    def __init__(self, index=0):
        super().__init__()
        self.index = index

        button_container = QWidget()
        button_container_layout = QHBoxLayout(button_container)
        edit_button = QPushButton()
        edit_button.clicked.connect()
        button_container_layout.addWidget(edit_button)
        button_container_layout.addStretch()
        delete_button = QPushButton()
        delete_button.clicked.connect()
        button_container_layout.addWidget(delete_button)
        top_layout = QGridLayout()
        top_layout.addWidget(button_container, 0, 0)


        self.setLayout(top_layout)
        # placeholder
        self.setText(str(index))
        self.setAutoFillBackground(True)
        self.setMinimumSize(QSize(200, 200))

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(QColor(choice(colors))))
        self.setPalette(palette)