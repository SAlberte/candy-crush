from game_engine import Engine, Hexagon, Board
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import threading
import socket
import pickle
import sys

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Candy Crush")
        self.setGeometry(300, 300, 900, 600)
        self.setMinimumHeight(600)
        self.setMinimumWidth(600)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene,self)
        self.view.setGeometry(130, 10, 700, 400)
        self.isGame = False
        self.is2PlayerMode = False
        self.wasFirstSettling = False
        self.player1score = 0
        self.player2score = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.gameLoop)
        self.timer.setInterval(50)
        self.setTextBox()
        self.setLabel()
        self.setButtons()
        self.isEnemyTurn = False
        self.enemyIP = 0

    def setLabel(self):
        self.label = QLabel(self)
        self.label.move(20, 450)
        self.label.setText("STEERING WITH ARROW KEYS \n SELECT WITH ENTER KEY")
        self.labelplayer1 = QLabel(self)
        self.labelplayer1.move(300,450)
        self.labelplayer1.setText("PLAYER 1 SCORE :              ")
        self.labelplayer2 = QLabel(self)
        self.labelplayer2.move(500, 450)
        self.labelplayer2.setText("PLAYER 2 SCORE :              ")

    def setTextBox(self):
        self.textbox = QLineEdit(self)
        self.textbox.move(20,200)
        self.textbox.resize(100,40)
        self.textbox.setPlaceholderText(" IP ADDRESS")

    def setButtons(self):
        #button for 2 player mode
        self.btn2player = QPushButton("2 PLAYER MODE", self)
        self.btn2player.setAutoDefault(False)
        self.btn2player.setStyleSheet("background-color: #66ffff")
        self.btn2player.move(20, 100)
        self.btn2player.clicked.connect(self.player2StartGame)
        
        #button for one player mode
        self.btnstart = QPushButton("START", self)
        self.btnstart.move(20, 50)
        self.btnstart.setAutoDefault(False)
        self.btnstart.setStyleSheet("background-color: #66ffff")
        self.btnstart.clicked.connect(self.StartGame)
        
        #button to exit program
        self.btnstop = QPushButton("EXIT", self)
        self.btnstop.setAutoDefault(False)
        self.btnstop.setStyleSheet("background-color: #66ffff")        
        self.btnstop.move(20, 150)
        self.btnstop.clicked.connect(self.quitApp)
        
        #button to join online player
        self.btnjoin = QPushButton("JOIN PLAYER", self)
        self.btnjoin.setAutoDefault(False)
        self.btnjoin.setStyleSheet("background-color: #66ffff")
        self.btnjoin.move(20, 250)
        self.btnjoin.clicked.connect(self.joinRoom)

        # button to create room for online player
        self.btnjoin = QPushButton("CREATE ROOM", self)
        self.btnjoin.setAutoDefault(False)
        self.btnjoin.setStyleSheet("background-color: #66ffff")
        self.btnjoin.move(20, 300)
        self.btnjoin.clicked.connect(self.createRoom)
       
    def createRoom(self):
        self.isEnemyTurn = True
        t = threading.Thread(target=self.recieveBoard,args=(self.isEnemyTurn, self.engine.board.hexagonslist,))
        t.start()
        #t.join()

    def joinRoom(self):
        self.sendBoard()

    def sendBoard(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.textbox.text(), 10061)

        sock.connect(server_address)

        try:

            # Send data
            # message = b"This is our message. It is very long but will only be transmitted in chunks of 16 at a time"
            n = self.engine.board.hexagonslist
            message = pickle.dumps(n)
            # print('sending {!r}'.format(message))
            sock.send(message)

        finally:
            print('closing socket')
            sock.close()

    def recieveBoard(self, isEnemy, board):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 10061)
        sock.bind(server_address)
        sock.listen(1)


        print("waiting for connection")
        connection, client_address = sock.accept()
        try:
            print("connection from", client_address)

            while True:
                data = connection.recv(100000)

                if data:
                    self.engine.board.hexagonslist = pickle.loads(data)
                    print("odebrano mape")
                else:
                    print("skonczono odbierac mape", client_address)
                    self.isEnemyTurn = False
                    break

        finally:

            print("Closing current connectoin")
            connection.close()
            self.isEnemyTurn = False

    def quitApp(self):
        myApp.quit()

    def StartGame(self):
        self.labelplayer1.setText("PLAYER 1 SCORE : ")
        self.labelplayer2.setText("PLAYER 2 SCORE : ")
        self.is2PlayerMode = False
        self.wasFirstSettling = False
        self.player1score = 0
        self.player2score = 0
        #self.repaint()
        #self.show()
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


    def paint(self):
        if not self.isEnemyTurn:
            self.scene.clear()
            if self.isGame:
                for indi,i in enumerate(self.engine.board.hexagonslist):
                    for ind,j in enumerate(i):
                        xpom = j.x*8
                        ypom = j.y*8
                        points = QPolygonF([QPoint(xpom+16,ypom), QPoint(xpom+32,ypom+10),QPoint(xpom+32,ypom+22),QPoint(xpom+16,ypom+32),QPoint(xpom,ypom+22), QPoint(xpom,ypom+10)])
                        self.scene.addPolygon(points,QPen(Qt.white, 3, Qt.SolidLine),QBrush(self.getColour(j), Qt.SolidPattern))
            #Draw player handles on board
                x = self.engine.board.hexagonslist[self.engine.setPy][self.engine.setPx].x
                y = self.engine.board.hexagonslist[self.engine.setPy][self.engine.setPx].y
                xpom = x * 8
                ypom = y * 8
                points = QPolygonF([QPoint(xpom + 16, ypom), QPoint(xpom + 32, ypom + 10), QPoint(xpom + 32, ypom + 22),
                                   QPoint(xpom + 16, ypom + 32), QPoint(xpom, ypom + 22), QPoint(xpom, ypom + 10)])
                self.scene.addPolygon(points,QPen(Qt.black,4,Qt.SolidLine), QBrush())
                if self.engine.isSet:
                    x = self.engine.board.hexagonslist[self.engine.setsetPy][self.engine.setsetPx].x
                    y = self.engine.board.hexagonslist[self.engine.setsetPy][self.engine.setsetPx].y
                    xpom = x * 8
                    ypom = y * 8
                    points = QPolygonF([QPoint(xpom + 16, ypom), QPoint(xpom + 32, ypom + 10), QPoint(xpom + 32, ypom + 22),
                                       QPoint(xpom + 16, ypom + 32), QPoint(xpom, ypom + 22), QPoint(xpom, ypom + 10)])
                    self.scene.addPolygon(points,
                                          QPen(Qt.black, 4, Qt.SolidLine), QBrush())


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
        print(self.isEnemyTurn)
        if not self.isEnemyTurn:
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
                self.labelplayer1.setText(f"PLAYER 1 SCORE : {self.player1score}   ")
                self.labelplayer2.setText(f"PlAYER 2 SCORE : {self.player2score}    ")
                if self.is2PlayerMode:
                    if isPlayer1:
                        self.labelplayer2.setStyleSheet('color: red')
                        self.labelplayer1.setStyleSheet('color: black')
                    else :
                        self.labelplayer1.setStyleSheet('color: red')
                        self.labelplayer2.setStyleSheet('color: black')
                self.labelplayer1.update()
                self.labelplayer2.update()

        self.paint()
        



myApp = QApplication(sys.argv)
window = Window()
window.show()


myApp.exec_()
sys.exit(0)