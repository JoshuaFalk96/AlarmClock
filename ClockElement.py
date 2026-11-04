import time
from random import choice
from time import struct_time, localtime

import qtawesome as qta
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QPalette, QColor, QAction
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QToolButton, QMenu, QWidgetAction, QTimeEdit, \
    QVBoxLayout, QPushButton, QDateTimeEdit

colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'white',
    'black'
]


class ClockElement(QWidget):
    def __init__(self, is_analog: bool = True, is_am_pm: bool = False, is_alarm_set: bool = False,
                 alarm_time: struct_time = localtime(), timezone: str = localtime().tm_zone, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # settings for this clock from parameter
        self._is_analog = is_analog  # default True
        self._is_am_pm = is_am_pm  # default False
        self._is_alarm_set = is_alarm_set  # default false
        self._alarm_time = alarm_time  # default local time at creation
        self._timezone = timezone  # default local timezone of machine

        # a container for the layout of the edit and delete buttons
        button_container = QWidget()
        button_container_layout = QHBoxLayout(button_container)
        button_container_layout.setContentsMargins(5, 5, 5, 5)
        button_container_layout.setSpacing(0)

        # edit button for opening settings menu
        edit_button = QToolButton()
        edit_button.setIcon(qta.icon('fa6s.pen'))
        edit_button.setPopupMode(edit_button.ToolButtonPopupMode.InstantPopup)
        self._edit_menu = QMenu(self)
        self._rebuild_edit_menu()
        edit_button.setMenu(self._edit_menu)
        edit_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")

        # delete button for removing this clock permanently
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

        # define the layout for this entire widget
        top_layout = QGridLayout(self)
        top_layout.setContentsMargins(0, 0, 0, 0)
        # add the different layout container to the same cell to allow overlap
        top_layout.addWidget(clock_container, 0, 0)
        top_layout.addWidget(button_container, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)

    def _rebuild_edit_menu(self):
        self._edit_menu.clear()
        if self._is_analog:
            self._edit_menu.addAction('set digital', self._set_digital)
        else:
            self._edit_menu.addAction('set analog', self._set_analog)
            if self._is_am_pm:
                self._edit_menu.addAction('set to 24h', self._set_24h)
            else:
                self._edit_menu.addAction('set to am/pm', self._set_am_pm)
        if self._is_alarm_set:
            self._edit_menu.addAction('turn off alarm', self._set_alarm_off)
        else:
            self._edit_menu.addAction('turn on alarm', self._set_alarm_on)
        alarm_time_action = QWidgetAction(self._edit_menu)
        alarm_edit_layout_container = QWidget()
        alarm_edit_layout = QHBoxLayout(alarm_edit_layout_container)
        self._alarm_edit_time_input = QDateTimeEdit()
        self._alarm_edit_time_input.setDisplayFormat("HH:mm")
        alarm_edit_layout.addWidget(self._alarm_edit_time_input)
        alarm_edit_button = QPushButton('ok')
        alarm_edit_button.clicked.connect(lambda: alarm_time_action.trigger())
        alarm_edit_layout.addWidget(alarm_edit_button)
        alarm_time_action.setDefaultWidget(alarm_edit_layout_container)
        alarm_time_action.triggered.connect(self._set_alarm_time)
        self._edit_menu.addAction(alarm_time_action)
        self._edit_menu.addAction('set timezone placeholder', self._set_timezone)

    def _set_digital(self):
        self._is_analog = False
        self._rebuild_edit_menu()
        print('setting digital')

    def _set_analog(self):
        self._is_analog = True
        self._rebuild_edit_menu()
        print('setting analog')

    def _set_24h(self):
        self._is_am_pm = False
        self._rebuild_edit_menu()
        print('setting 24h')

    def _set_am_pm(self):
        self._is_am_pm = True
        self._rebuild_edit_menu()
        print('setting am/pm')

    def _set_alarm_on(self):
        self._is_alarm_set = True
        self._rebuild_edit_menu()
        print('turning alarm on')

    def _set_alarm_off(self):
        self._is_alarm_set = False
        self._rebuild_edit_menu()
        print('turning alarm off')

    def _set_alarm_time(self):
        self._alarm_edit_time_input.time()
        print('setting alarm time ' + time.strftime("%X", self._alarm_time))

    def _set_timezone(self):
        print('setting timezone ' + self._timezone)
