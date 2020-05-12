from game_engine import Engine, Hexagon, Board
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Candy Crush")
        self.setGeometry(300, 300, 900, 600)
        self.setMinimumHeight(600)
        self.setMinimumWidth(600)
        self.isGame = False
        self.is2PlayerMode = False
        self.wasFirstSettling = False
        self.player1score = 0
        self.player2score = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.gameLoop)
        self.timer.setInterval(50)
        self.setLabel()
        self.setButtons()




    def setLabel(self):
        self.label = QLabel(self)
        self.label.setFont("TimesNewRoman")
        self.label.move(20, 300)
        self.label.setText("STEERING WITH ARROW KEYS \n SELECT WITH ENTER KEY")
        self.labelplayer1 = QLabel(self)
        self.labelplayer1.setFont("TimesNewRoman")
        self.labelplayer1.move(300,400)
        self.labelplayer1.setText("PLAYER 1 SCORE : ")
        self.labelplayer2 = QLabel(self)
        self.labelplayer2.setFont("TimesNewRoman")
        self.labelplayer2.move(500, 400)
        self.labelplayer2.setText("PLAYER 2 SCORE : ")



    def setButtons(self):
        self.btn2player = QPushButton("2 PLAYER MODE", self)
        self.btnstart = QPushButton("START", self)
        self.btnstart.move(50, 50)
        self.btnstop = QPushButton("EXIT", self)
        self.btnstop.move(50, 150)
        self.btnstop.clicked.connect(self.quitApp)
        self.btnstart.clicked.connect(self.StartGame)
        self.btnstart.setAutoDefault(False)
        self.btnstop.setAutoDefault(False)
        self.btn2player.setAutoDefault(False)
        self.btnstart.setStyleSheet("background-color: #66ffff")
        self.btnstop.setStyleSheet("background-color: #66ffff")
        self.btn2player.setStyleSheet("background-color: #66ffff")
        self.btn2player.move(50, 100)
        self.btn2player.clicked.connect(self.player2StartGame)
        


    def quitApp(self):
        myApp.quit()

    def StartGame(self):
        self.labelplayer1.setText("PLAYER 1 SCORE : ")
        self.labelplayer2.setText("PLAYER 2 SCORE : ")
        self.is2PlayerMode = False
        self.wasFirstSettling = False
        self.player1score = 0
        self.player2score = 0
        self.repaint()
        self.btnstart.setText("NEW GAME")
        self.isGame = True
        self.engine = Engine()
        self.timer.start()

    def player2StartGame(self):
        self.labelplayer1.setText("PLAYER 1 SCORE : ")
        self.labelplayer2.setText("PLAYER 2 SCORE : ")
        self.is2PlayerMode = True
        self.wasFirstSettling = False
        self.player1score = 0
        self.player2score = 0
        self.repaint()
        self.btnstart.setText("NEW GAME")
        self.isGame = True
        self.engine = Engine()
        self.timer.start()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.white, 3, Qt.SolidLine))

        #point = QPolygon([QPoint(10,10), QPoint(20, 10),QPoint(20, 20),QPoint(10, 20)])
        #painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        #painter.drawPolygon(points)
        #Draw board with hexagons
        if self.isGame:
            for indi,i in enumerate(self.engine.board.hexagonslist):
                for ind,j in enumerate(i):
                    painter.setBrush(QBrush(self.getColour(j), Qt.SolidPattern))
                    xpom = j.x*8+200
                    ypom = j.y*8
                    points = QPolygon([QPoint(xpom+16,ypom), QPoint(xpom+32,ypom+10),QPoint(xpom+32,ypom+22),QPoint(xpom+16,ypom+32),QPoint(xpom,ypom+22), QPoint(xpom,ypom+10)])
                    painter.drawPolygon(points)
        #Draw player handles on board
            painter2 = QPainter(self)
            painter2.setPen(QPen(Qt.black,4,Qt.SolidLine))

            x = self.engine.board.hexagonslist[self.engine.setPy][self.engine.setPx].x
            y = self.engine.board.hexagonslist[self.engine.setPy][self.engine.setPx].y
            xpom = x * 8 + 200
            ypom = y * 8
            points = QPolygon([QPoint(xpom + 16, ypom), QPoint(xpom + 32, ypom + 10), QPoint(xpom + 32, ypom + 22),
                               QPoint(xpom + 16, ypom + 32), QPoint(xpom, ypom + 22), QPoint(xpom, ypom + 10)])
            painter2.drawPolygon(points)
            if self.engine.isSet:
                x = self.engine.board.hexagonslist[self.engine.setsetPy][self.engine.setsetPx].x
                y = self.engine.board.hexagonslist[self.engine.setsetPy][self.engine.setsetPx].y
                xpom = x * 8 + 200
                ypom = y * 8
                points = QPolygon([QPoint(xpom + 16, ypom), QPoint(xpom + 32, ypom + 10), QPoint(xpom + 32, ypom + 22),
                                   QPoint(xpom + 16, ypom + 32), QPoint(xpom, ypom + 22), QPoint(xpom, ypom + 10)])
                painter2.drawPolygon(points)




    def getColour(self,j):
        if j.type == Hexagon.colours[0]:
            return Qt.green
        if j.type == Hexagon.colours[1]:
            return Qt.blue
        if j.type == Hexagon.colours[2]:
            return Qt.cyan
        if j.type == Hexagon.colours[3]:
            return Qt.red
        if j.type == Hexagon.colours[4]:
            return Qt.yellow
        if j.type == Hexagon.colours[5]:
            return Qt.magenta
        if j.type == Hexagon.colours[6]:
            return Qt.lightGray
        if j.type == Hexagon.colours[7]:
            return Qt.black

    def gameLoop(self):
        isSettling, isPlayer1, score = self.engine.game()
        if isSettling:
            self.timer.setInterval(600)
        else:
            self.timer.setInterval(50)
            self.wasFirstSettling = True
        if self.wasFirstSettling:
            if self.is2PlayerMode:
                if isPlayer1:   self.player1score+=score
                else: self.player2score += score
            else: self.player1score += score
            self.labelplayer1.setText("PLAYER 1 SCORE : %d" % self.player1score)
            self.labelplayer2.setText("PLAYER 2 SCORE : %d" % self.player2score)
        self.repaint()
        



myApp = QApplication(sys.argv)
window = Window()
window.show()


myApp.exec_()
sys.exit(0)