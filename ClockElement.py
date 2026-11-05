from random import choice

import qtawesome as qta
from PySide6.QtCore import Qt, QDateTime, QTimeZone, QTime, QDate
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QToolButton, QMenu, QWidgetAction, QPushButton, \
    QDateTimeEdit, QVBoxLayout, QLabel

colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'black'
]


class ClockElement(QWidget):
    def __init__(self, is_analog: bool = True, is_am_pm: bool = False, is_alarm_set: bool = False,
                 alarm_time: QTime = QTime.currentTime(),
                 timezone: QTimeZone = QTimeZone.systemTimeZone(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        # settings for this clock from parameter
        self._is_analog = is_analog  # default True
        self._is_am_pm = is_am_pm  # default False
        self._is_alarm_set = is_alarm_set  # default false
        self._alarm_time = alarm_time  # default local time at creation
        self._timezone = timezone  # default local timezone of machine

        # TODO actual clock GUI
        clock_container = QWidget()
        clock_container_layout = QVBoxLayout(clock_container)
        clock_container_layout.setContentsMargins(0, 0, 0, 0)
        self._time_format_label = QLabel()
        clock_container_layout.addWidget(self._time_format_label)
        self._digital_format_label = QLabel()
        clock_container_layout.addWidget(self._digital_format_label)
        self._timezone_label = QLabel()
        clock_container_layout.addWidget(self._timezone_label)
        self._alarm_time_label = QLabel()
        clock_container_layout.addWidget(self._alarm_time_label)
        self._alarm_state_label = QLabel()
        clock_container_layout.addWidget(self._alarm_state_label)
        clock_container.setAutoFillBackground(True)
        clock_container.setMinimumSize(200, 200)
        palette = clock_container.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(QColor(choice(colors))))
        clock_container.setPalette(palette)

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

        # define the layout for this entire widget
        top_layout = QGridLayout(self)
        top_layout.setContentsMargins(0, 0, 0, 0)
        # add the different layout container to the same cell to allow overlap
        top_layout.addWidget(clock_container, 0, 0)
        top_layout.addWidget(button_container, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)

        self._update_ui()

    def _rebuild_edit_menu(self):
        # clear the edit menu
        self._edit_menu.clear()
        self._update_ui()

        # add option for choosing analog or digital representation
        self._edit_menu.addSection('display')
        if self._is_analog:
            # if the clock is analog, display option to turn digital
            self._edit_menu.addAction('set digital', self._set_digital)
        else:
            # if the clock is digital display option to turn analog
            self._edit_menu.addAction('set analog', self._set_analog)

            # only display am/pm or 24h choice when clock is digital
            if self._is_am_pm:
                # if clock is am/pm display option for 24h format
                self._edit_menu.addAction('set to 24h', self._set_24h)
            else:
                # if clock is 24h display option for am/pm format
                self._edit_menu.addAction('set to am/pm', self._set_am_pm)

        # add option for choosing the timezone
        self._edit_menu.addSection('timezone')
        self._edit_menu.addAction('set timezone placeholder', self._set_timezone)

        # add option for choosing alarm time
        self._edit_menu.addSection('alarm')
        # create action to hold custom widget
        alarm_time_action = QWidgetAction(self._edit_menu)
        # create a dummy widget to hold layout of custom alarm time input
        alarm_edit_layout_container = QWidget()
        alarm_edit_layout = QHBoxLayout(alarm_edit_layout_container)
        alarm_edit_layout.setContentsMargins(25, 0, 20, 0)
        # setup time input field of setting alarm time
        # time input needs to be accessed from different function -> saved as field instead of local
        self._alarm_edit_time_input = QDateTimeEdit(self._alarm_time)
        self._alarm_edit_time_input.setDisplayFormat("HH:mm")
        # setup button for confirming alarm time choice
        alarm_edit_button = QPushButton('OK')
        alarm_edit_button.setFixedWidth(30)
        # have the button trigger the alarm time action
        alarm_edit_button.clicked.connect(lambda: alarm_time_action.trigger())
        # add time field and confirm button to layout of custom widget
        alarm_edit_layout.addWidget(self._alarm_edit_time_input)
        alarm_edit_layout.addWidget(alarm_edit_button)
        # set the custom widget as the widget of the action
        alarm_time_action.setDefaultWidget(alarm_edit_layout_container)
        alarm_time_action.triggered.connect(self._set_alarm_time)
        # add the custom alarm time chooser to the menu
        self._edit_menu.addAction(alarm_time_action)

        # add option for turning on or off alarm function
        if self._is_alarm_set:
            # if alarm is on display option to turn alarm off
            self._edit_menu.addAction('turn off alarm', self._set_alarm_off)
        else:
            # if alarm is off display option to turn alarm on
            self._edit_menu.addAction('turn on alarm', self._set_alarm_on)

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
        self._alarm_time = self._alarm_edit_time_input.time()
        set_time = QDateTime(QDate.currentDate(), self._alarm_time, self._timezone)
        self._update_ui()
        print('setting alarm time ' + set_time.toString("hh:mm"))

    def _set_timezone(self):
        self._update_ui()
        print('setting timezone ' + self._timezone.displayName(QTimeZone.TimeType.GenericTime))

    def _update_ui(self):
        self._time_format_label.setText('time format: ' + ('analog' if self._is_analog else 'digital'))
        self._digital_format_label.setText('digital format: ' + ('am/pm' if self._is_am_pm else '24h'))
        set_time = QDateTime(QDate.currentDate(), self._alarm_time, self._timezone)
        self._timezone_label.setText('timezone: ' + self._timezone.displayName(QTimeZone.TimeType.GenericTime))
        self._alarm_time_label.setText('alarm time: ' + set_time.toString("hh:mm"))
        self._alarm_state_label.setText('alarm is ' + ('on' if self._is_alarm_set else 'off'))
