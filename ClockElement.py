from random import choice

import qtawesome as qta
from PySide6.QtCore import Qt, QDateTime, QTimeZone, QTime, QDate, QObject
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QToolButton, QMenu, QWidgetAction, QPushButton, \
    QDateTimeEdit, QVBoxLayout, QLabel, QComboBox, QStackedWidget

colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'black'
]


class EditAction(QWidgetAction):
    # parent class for timezone and alarm time edit menu items
    def _generate_layout(self, input_widget: QWidget):
        # create a dummy widget to hold layout
        edit_layout_container = QWidget()
        edit_layout = QHBoxLayout(edit_layout_container)
        edit_layout.setContentsMargins(25, 0, 20, 0)

        # setup button for confirming edit
        confirm_button = QPushButton('OK')
        confirm_button.setFixedWidth(30)

        # have the button trigger the action
        confirm_button.clicked.connect(lambda: self.trigger())

        # add input field and confirm button to layout of custom widget
        edit_layout.addWidget(input_widget)
        edit_layout.addWidget(confirm_button)

        # set dummy widget with the layout as default of this action
        self.setDefaultWidget(edit_layout_container)


class TimeEditAction(EditAction):
    # menu item for editing alarm time
    def __init__(self, parent: QObject, alarm_time: QTime):
        super().__init__(parent)
        # setup time input field of setting alarm time
        self._alarm_edit_time_input = QDateTimeEdit(alarm_time)
        self._alarm_edit_time_input.setDisplayFormat("HH:mm")

        # use function of parent class to add confirm button and add as default widget of action
        self._generate_layout(self._alarm_edit_time_input)

    def get_time(self) -> QTime:
        # provide time set in input field
        return self._alarm_edit_time_input.time()


class TimezoneEditAction(EditAction):
    # menu item for editing time zone
    def __init__(self, parent: QObject, /):
        super().__init__(parent)
        # setup dropdown field for the different timezones
        self._timezones_combo_box = QComboBox()
        # enable typing in field to search for timezone
        self._timezones_combo_box.setEditable(True)
        self._timezones_combo_box.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self._timezones_combo_box.activated.connect(lambda: self.trigger())

        # add all timezones the OS supports to the list
        for timezone_id in QTimeZone.availableTimeZoneIds():
            # get the timezone object
            timezone = QTimeZone(timezone_id)
            # get the localized name and add timezone id to differentiate same name in different region
            timezone_name = timezone.displayName(QTimeZone.TimeType.GenericTime) + ' (' + str(timezone_id)[2:-1] + ')'
            # add the timezone object represented by the localized name
            self._timezones_combo_box.addItem(timezone_name, timezone)

        # use function of parent class to add confirm button and set as default widget of action
        self._generate_layout(self._timezones_combo_box)

    def get_timezone(self) -> QTimeZone:
        return self._timezones_combo_box.currentData()


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

        clock_representation_widget = QStackedWidget()

        self._time_format_label = QLabel()
        clock_container_layout.addWidget(self._time_format_label)
        self._digital_format_label = QLabel()
        clock_container_layout.addWidget(self._digital_format_label)
        self._alarm_time_label = QLabel()
        clock_container_layout.addWidget(self._alarm_time_label)
        self._alarm_state_label = QLabel()
        clock_container_layout.addWidget(self._alarm_state_label)

        self._timezone_label = QLabel()
        self._timezone_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        clock_container_layout.addWidget(self._timezone_label)

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

        # add options for choosing analog or digital representation
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
        timezone_edit_action = TimezoneEditAction(self._edit_menu)
        timezone_edit_action.triggered.connect(lambda: self._set_timezone(timezone_edit_action.get_timezone()))
        self._edit_menu.addAction(timezone_edit_action)

        # add options for alarm time
        self._edit_menu.addSection('alarm')
        # add custom widget action for choosing alarm time
        time_edit_action = TimeEditAction(self._edit_menu, self._alarm_time)
        time_edit_action.triggered.connect(lambda x: self._set_alarm_time(time_edit_action.get_time()))
        self._edit_menu.addAction(time_edit_action)

        # add option for turning on or off alarm function
        if self._is_alarm_set:
            # if alarm is on display option to turn alarm off
            self._edit_menu.addAction('turn off alarm', self._set_alarm_off)
        else:
            # if alarm is off display option to turn alarm on
            self._edit_menu.addAction('turn on alarm', self._set_alarm_on)

    def _set_digital(self):
        self._is_analog = False
        self._time_format_label.setText('time format: digital')
        self._rebuild_edit_menu()
        print('setting digital')

    def _set_analog(self):
        self._is_analog = True
        self._time_format_label.setText('time format: analog')
        self._rebuild_edit_menu()
        print('setting analog')

    def _set_24h(self):
        self._is_am_pm = False
        self._digital_format_label.setText('digital format: 24h')
        self._rebuild_edit_menu()
        print('setting 24h')

    def _set_am_pm(self):
        self._is_am_pm = True
        self._digital_format_label.setText('digital format: am/pm')
        self._rebuild_edit_menu()
        print('setting am/pm')

    def _set_alarm_on(self):
        self._is_alarm_set = True
        self._alarm_state_label.setText('alarm is on')
        self._rebuild_edit_menu()
        print('turning alarm on')

    def _set_alarm_off(self):
        self._is_alarm_set = False
        self._alarm_state_label.setText('alarm is off')
        self._rebuild_edit_menu()
        print('turning alarm off')

    def _set_alarm_time(self, time: QTime):
        self._alarm_time = time
        set_time = QDateTime(QDate.currentDate(), self._alarm_time, self._timezone)
        set_time = QDateTime(QDate.currentDate(), self._alarm_time, self._timezone)
        self._alarm_time_label.setText('alarm time: ' + set_time.toString("hh:mm"))
        print('setting alarm time ' + set_time.toString("hh:mm"))

    def _set_timezone(self, timezone: QTimeZone):
        self._timezone = timezone
        self._timezone_label.setText(
            '<b>{0} ({1}</b>)'.format(self._timezone.displayName(QTimeZone.TimeType.GenericTime,
                                                                 QTimeZone.NameType.ShortName),
                                      self._timezone.displayName(QTimeZone.TimeType.GenericTime,
                                                                 QTimeZone.NameType.OffsetName)))

        print('setting timezone ' + self._timezone.displayName(QTimeZone.TimeType.GenericTime))
