from PyQt5.QtCore import *
from enum import Enum

class EnumSettingType(Enum):
    ePos = 1
    eSize = 2
    eRegister = 101

class StudioSettingData(QObject, object):
    def __init__(self):
        self.map_setting_value = {}
