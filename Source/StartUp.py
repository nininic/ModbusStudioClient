import os
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QWindow


from Source.GuiSource.MainView.StudioClientWindow import StudioClientWindow
'''
app = QApplication([])
windowMain = QWindow()
windowMain.resize(300, 400)
windowMain.show()
app.exec()
print(os.name)
'''

def main_loop():
    qt_app = QApplication([])
    window_studio_client =  StudioClientWindow()
    window_studio_client.show()
    qt_app.exec()


main_loop()
