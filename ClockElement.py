from random import choice

import qtawesome as qta
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QToolButton, QMenu

from ClockSettings import ClockSettings

colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'white',
    'black'
]


class ClockElement(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._settings = ClockSettings()

        # a container for the layout of the edit and delete buttons
        button_container = QWidget()
        button_container_layout = QHBoxLayout(button_container)
        button_container_layout.setContentsMargins(0, 0, 0, 0)
        button_container_layout.setSpacing(0)
        # setup menu for editing clock settings
        edit_menu = QMenu(self)
        # TODO define settings and create action menu
        edit_menu.addAction('test', lambda: print('tested'))
        # button for opening edit menu
        edit_button = QToolButton()
        edit_button.setIcon(qta.icon('fa6s.pen'))
        edit_button.setPopupMode(edit_button.ToolButtonPopupMode.InstantPopup)
        edit_button.setMenu(self._settings.build_menu(self))
        # button for removing this clock permanently
        delete_button = QToolButton()
        delete_button.setIcon(qta.icon('fa6s.trash'))
        delete_button.clicked.connect(lambda: self.deleteLater())
        # adding buttons to the button layout with flexible spacer between them
        button_container_layout.addWidget(edit_button)
        button_container_layout.addStretch()
        button_container_layout.addWidget(delete_button)
        # TODO actual clock GUI
        clock_container = QWidget()
        clock_container.setContentsMargins(0, 0, 0, 0)
        clock_container.setAutoFillBackground(True)
        clock_container.setMinimumSize(200, 200)
        palette = clock_container.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(QColor(choice(colors))))
        clock_container.setPalette(palette)

        # adding layout container to same grid cell to allow overlap
        top_layout = QGridLayout(self)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(clock_container, 0, 0)
        top_layout.addWidget(button_container, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
