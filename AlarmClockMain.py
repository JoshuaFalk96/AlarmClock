import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout
import qtawesome as qta

from ClockElement import ClockElement
from FlowLayout import FlowLayout


# setup of main window
class AlarmClockMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # setup layout for individual clock elements
        clock_container = QWidget()
        self._clock_layout = FlowLayout(clock_container)

        # button for adding new clock element
        new_clock_button = QPushButton(qta.icon('fa6s.plus'), '')
        new_clock_button.setMinimumSize(QSize(30,30))
        new_clock_button.clicked.connect(self.add_new_clock)

        # widget to hold layout for main window
        window_widget_container = QWidget()
        # add button and clock layout to same grid cell to have button overlap clocks
        widget_container_layout = QGridLayout(window_widget_container)
        widget_container_layout.addWidget(clock_container, 0, 0)
        widget_container_layout.addWidget(new_clock_button, 0, 0,
                                          alignment=Qt.AlignmentFlag.AlignBottom |
                                                    Qt.AlignmentFlag.AlignRight)



        # TODO load clocks from file
        self._saved_clocks = [ClockElement(),ClockElement()]
        # add loaded clocks to layout
        for index in range(len(self._saved_clocks)-1):
            clock = self._saved_clocks[index]
            clock.index = index
            self._clock_layout.addWidget(clock)

        # setup window parameters
        self.setWindowTitle("Alarm Clock")
        self.setCentralWidget(window_widget_container)

    # add new clock element to window
    def add_new_clock(self):
        index = self._clock_layout.count()
        clock = ClockElement(index)
        self._clock_layout.addWidget(clock)

    # remove a clock from the window
    def remove_clock(self, index):
        self._clock_layout.takeAt(index)





app = QApplication(sys.argv)
window = AlarmClockMainWindow()
window.show()

window.add_new_clock()
window.add_new_clock()
window.add_new_clock()

app.exec()
