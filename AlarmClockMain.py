import sys

import qtawesome as qta
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QToolButton

from ClockElement import ClockElement
from FlowLayout import FlowLayout


# setup of main window
class AlarmClockMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # widget to hold layout for main window
        window_widget_container = QWidget()

        # setup layout for individual clock elements
        clock_container = QWidget(window_widget_container)
        clock_layout = FlowLayout(clock_container)

        # button for adding new clock element
        new_clock_button = QToolButton()
        new_clock_button.setIcon(qta.icon('fa6s.plus'))
        new_clock_button.clicked.connect(lambda: clock_layout.addWidget(ClockElement()))

        # add button and clock layout to same grid cell to have button overlap clocks
        widget_container_layout = QGridLayout(window_widget_container)
        widget_container_layout.addWidget(clock_container, 0, 0)
        widget_container_layout.addWidget(new_clock_button, 0, 0,
                                          alignment=Qt.AlignmentFlag.AlignBottom |
                                                    Qt.AlignmentFlag.AlignRight)

        # TODO load clocks from file
        saved_clocks = [ClockElement(), ClockElement()]
        # add loaded clocks to layout
        for clock in saved_clocks:
            clock_layout.addWidget(clock)

        # setup window parameters
        self.setWindowTitle("Alarm Clock")
        self.setCentralWidget(window_widget_container)


# run the application by opening the main window
app = QApplication(sys.argv)
window = AlarmClockMainWindow()
window.show()
app.exec()
