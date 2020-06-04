import sys
from ..StudioIconManager import TOOL_BAR_BASIC_COMPOMENT_LABLE, TOOL_BAR_BASIC_TEXT_BUTTON, TOOL_BAR_BASIC_TEXT
from .StudioEditManager import g_Studio_Editing_Mgr, EnumNewAddComType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QIcon, QBrush, QPainter, QColor, QPen
from PyQt5.QtCore import QSize


class StudioClientWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.mouse_presed = None

        # Window dimensions
        self.screen_ = QDesktopWidget().screenGeometry()
        self.setGeometry(int(self.screen_.width()* 0.2/2), int(self.screen_.height()*0.2/2), int(self.screen_.width()*0.8), int(self.screen_.height()*0.8))
        self.setMinimumSize(QSize(int(self.screen_.width()*0.1), int(self.screen_.height()*0.1)))

        self.edit_area_ = None
        self.toolbar_action_map = {}





        self.InitMenuBar()
        self.InitMainArea()
        self.InitToolBarArea()

        # Toolbar
        self.toolbar_basic_component = None

        ms_status_hide = 3000
        self.statusBar().showMessage("This is status bar", ms_status_hide);
        print("MainWindow")


    def InitMenuBar(self):
        # Menubar
        menubar  = self.menuBar()
        menuFile = menubar.addMenu("File")
        menubar.addMenu("Setting")

        action_open = QAction(QIcon('exit.png'), '&Open', self)
        action_open.setShortcut('Ctrl+O')
        action_open.setStatusTip('Open File')

        action_exit = QAction(QIcon('exit.png'), '&Exit', self)
        action_exit.setShortcut('Ctrl+Q')
        action_exit.setStatusTip('Exit application')

        menuFile.addAction(action_open)
        menuFile.addSeparator()
        menuFile.addAction(action_exit)
        menuFile.addAction(QIcon(TOOL_BAR_BASIC_COMPOMENT_LABLE), 'aaa')

    def InitToolBarArea(self):
        self.toolbar_basic_component = QToolBar(self)
        # self.toolbar_basic_component.setIconSize(QSize(16, 16))

        # it will not show when action has no parent
        action_data_display = QAction(QIcon(TOOL_BAR_BASIC_COMPOMENT_LABLE), 'Data Display', self)
        action_data_display.setCheckable(True)
        self.toolbar_basic_component.addAction(action_data_display)
        self.toolbar_action_map['action_data_display'] = action_data_display

        action_text_button = QAction(QIcon(TOOL_BAR_BASIC_TEXT_BUTTON), 'Text Button', self)
        action_text_button.setCheckable(True)
        self.toolbar_basic_component.addAction(action_text_button)
        self.toolbar_action_map['action_text_button'] = action_text_button

        action_text_label = QAction(QIcon(TOOL_BAR_BASIC_TEXT), 'Label', self)
        action_text_label.setCheckable(True)
        self.toolbar_basic_component.addAction(action_text_label)
        self.toolbar_action_map['action_text_label'] = action_text_label

        for key, action_item in self.toolbar_action_map.items():
            action_item.triggered.connect(self.SlotToolBarActionTrigger)


        self.addToolBar( self.toolbar_basic_component)

    def InitMainArea(self):
        hlayout = QHBoxLayout()
        self.dock = QDockWidget("Page View", self)
        # self.bt = QPushButton("点我")
        # self.dock.setWidget(self.bt)
        self.tt = QTextEdit()
        self.setCentralWidget(self.tt)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.setLayout(hlayout)
        self.setWindowTitle("Studio For Modbus")
        #self.bt.clicked.connect(self.game)

        self.edit_area_ = StudioClientEditArea(self)
        self.setCentralWidget(self.edit_area_)

    def SlotToolBarActionTrigger(self, checked):
        if checked:
            for key, action in self.toolbar_action_map.items():
                if action != self.sender() and action.isChecked():
                    action.setChecked(False)

            if self.sender() == self.toolbar_action_map['action_data_display']:
                g_Studio_Editing_Mgr.SetNewAddComponent(EnumNewAddComType.eDataDisplay)
            elif self.sender() == self.toolbar_action_map['action_text_button']:
                g_Studio_Editing_Mgr.SetNewAddComponent(EnumNewAddComType.eTextButton)
            elif self.sender() == self.toolbar_action_map['action_text_label']:
                g_Studio_Editing_Mgr.SetNewAddComponent(EnumNewAddComType.eTextLabel)


class StudioClientEditArea(QWidget):

    def __init__(self, parent = None):

        super(StudioClientEditArea, self).__init__(parent)
        self.pos_press_start_pos = None

        self.setMouseTracking(True)
        self.new_component_rect = None
        self.dic_rect_point = {}
        self.list_components = []
        #
        # current_palette = self.palette()
        # current_palette.setColor(self.backgroundRole(), Qt.red)
        # self.setPalette(current_palette)
        # self.setAutoFillBackground(True)

    def paintEvent(self, event):
        # Draw background

        draw_transparent_brush = QBrush(QColor(0, 0, 0, 0))
        draw_edit_area_bg_brush = QBrush(QColor(100, 10, 10, 60))

        painter = QPainter(self)
        painter.setBrush(draw_edit_area_bg_brush)
        margin_size = 40
        painter.drawRect(margin_size, margin_size, self.width()-margin_size*2, self.height()-margin_size*2)

        draw_dot_line_pen = QPen(Qt.black, 1, Qt.DotLine)
        painter.setPen(draw_dot_line_pen)
        painter.setBrush(draw_transparent_brush)

        #margin_size = 80
        print("paint" , self.new_component_rect)
        if self.new_component_rect:

            painter.drawRect(self.new_component_rect)
        # margin_size = 100
        # painter.drawRect(margin_size, margin_size, self.width() - margin_size * 2, self.height() - margin_size * 2)

    def mouseMoveEvent(self, mouse_event):
        """ mouseMoveEvent(self, QMouseEvent) """
        if mouse_event.buttons() == Qt.NoButton:
            # normal mouse move
            pass
        elif mouse_event.buttons() == Qt.LeftButton:
            self.dic_rect_point['end_point'] = mouse_event.pos()
            self.updateSelectedRect()
            self.update()
        elif mouse_event.buttons() == Qt.RightButton:
            # print("Right click drag")
            pass

    def mousePressEvent(self, mouse_event):
        """ mousePressEvent(self, QMouseEvent) """
        self.dic_rect_point = {"start_point": mouse_event.pos(), "end_point": mouse_event.pos()}
        self.updateSelectedRect()
        pass

    def mouseReleaseEvent(self, mouse_event):
        """ mouseReleaseEvent(self, QMouseEvent) """
        self.dic_rect_point = {}

        #self.new_component_rect = None
        pass

    def updateSelectedRect(self):
        if self.dic_rect_point:
            start_point = self.dic_rect_point['start_point']
            end_point = self.dic_rect_point['end_point']
            if not self.new_component_rect:
                self.new_component_rect = QRect()
            point_top_left = QPoint(min(start_point.x(), end_point.x()), min(start_point.y(), end_point.y()))
            point_bottom_right = QPoint(max(start_point.x(), end_point.x()), max(start_point.y(), end_point.y()))
            self.new_component_rect.setTopLeft(point_top_left)
            self.new_component_rect.setBottomRight(point_bottom_right)




