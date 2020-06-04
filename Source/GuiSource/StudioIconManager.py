import sys
from pathlib import Path

path_start_up = sys.path[0]
path_resource_root = (Path(path_start_up).parents[0])
msg = '[StudioIconManager] Icon root path is ' + r'"' + str(path_resource_root) + r'"'
print(msg)


TOOL_BAR_BASIC_COMPOMENT_LABLE = str(path_resource_root) + r'\resource' + r'\ToolBar' + '\icon_data_display.png'
TOOL_BAR_BASIC_TEXT_BUTTON = str(path_resource_root) + r'\resource' + r'\ToolBar' + '\icon_text_button.png'
TOOL_BAR_BASIC_TEXT = str(path_resource_root) + r'\resource' + r'\ToolBar' + '\icon_text.png'
class StudioIconManager(object):
    def __init__(self):
        object.__init__()

