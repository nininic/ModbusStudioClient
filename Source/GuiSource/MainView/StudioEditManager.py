from PyQt5.QtCore import *
from enum import Enum


class EnumNewAddComType(Enum):
    eDataDisplay = 0
    eTextButton = 1
    eTextLabel = 2

class EnumEditOperation(Enum):
    eAddNewCom = 0
    eResizeCom = 1
    eMoveCom = 2



class StudioEditManager(QObject, object):
    def __init__(self):
        super(StudioEditManager, self).__init__()
        self.new_add_type = None
        self.edit_node_list = []

    def SetNewAddComponent(self, type):
        self.new_add_type = type

    def IsNewAddMode(self):
        return (EnumEditOperation.eAddNewCom == self.new_add_type)


g_Studio_Editing_Mgr = StudioEditManager()
