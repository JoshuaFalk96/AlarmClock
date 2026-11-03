import time
from enum import Enum
from time import struct_time

from PySide6.QtWidgets import QMenu, QWidget

class ClockFormat(Enum):
    ANALOG = object()
    DIGITAL24 = object()
    DIGITAL12 = object()
    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self._name_)


class ClockSettings:
    def __init__(self, clock_format:ClockFormat = ClockFormat.ANALOG, timezone = ..., alarm_time: struct_time = time.localtime(), set_alarm: bool = False):
        self._clock_format = clock_format
        self._timezone = timezone
        self._alarm_time = alarm_time
        self._is_alarm_set = set_alarm

    def build_menu(self, parent: QWidget) -> QMenu:
        menu = QMenu(parent)
        return menu
