import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout

from ClockElement import ClockElement
from CustomQtClasses import FlowLayout


# setup of main window
class AlarmClockMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # setup layout for individual clock elements
        clock_container = QWidget()
        self._clock_layout = FlowLayout(clock_container)

        # button for adding new clock element
        new_clock_button = QPushButton('new')
        new_clock_button.clicked.connect(self.add_clock)

        # widget to hold layout for main window
        window_widget_container = QWidget()
        # add button and clock layout to same grid cell to have button overlap clocks
        widget_container_layout = QGridLayout(window_widget_container)
        widget_container_layout.addWidget(clock_container, 0, 0)
        widget_container_layout.addWidget(new_clock_button, 0, 0,
                                          alignment=Qt.AlignmentFlag.AlignBottom |
                                                    Qt.AlignmentFlag.AlignRight)

        # setup window parameters
        self.setWindowTitle("My App")
        self.setCentralWidget(window_widget_container)

    # add new clock element to window
    def add_clock(self):
        clock = ClockElement()
        self._clock_layout.addWidget(clock)

    # remove a clock from the window
    def remove_clock(self, index):
        self._clock_layout.takeAt(index)



# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = AlarmClockMainWindow()
window.show()# IMPORTANT!!!!! Windows are hidden by default.

window.add_clock()
window.add_clock()
window.add_clock()

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.