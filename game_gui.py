from main import Engine, Hexagon, Board
from PySide2.QtWidgets import *
import sys

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Candy Crush")
        self.setGeometry(300,300,600,600)
        self.setMinimumHeight(600)
        self.setMinimumWidth(600)


myApp = QApplication(sys.argv)
window = Window()
window.show()


myApp.exec_()
sys.exit(0)