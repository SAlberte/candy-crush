from game_engine import Engine, Hexagon, Board
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import xml.etree.ElementTree as ET
from xml.dom import minidom
import codecs
import threading
import json
import socket
import pickle
import os
import sys

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Candy Crush")
        self.setGeometry(300, 300, 900, 600)
        self.canIMove = True
        self.setMinimumHeight(600)
        self.setMinimumWidth(600)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene,self)
        self.view.setGeometry(130, 10, 700, 400)
        self.isGame = False
        self.isGameOnline = False
        self.isSettlingStart = False
        self.shouldcreateRoom = False
        self.is2PlayerMode = False
        self.wasFirstSettling = False
        self.replayN = 0
        self.replayActualN = 0
        self.shouldCloseSocket = False
        self.player1score = 0
        self.player2score = 0
        self.IteratorTimer = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.gameLoop)
        self.timer.setInterval(50)
        self.replayTimer = QTimer(self)
        self.replayTimer.timeout.connect(self.replayLoop)
        self.replayTimer.setInterval(350)
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

    def createXML(self):
        # create the file structure
        if self.replayN == 0:
            data = ET.Element('data')
            item0 = ET.SubElement(data, 'data')
            item1 = ET.SubElement(data, 'item')
            item1.set('object', str(self.replayN))
            item1.text = codecs.encode(pickle.dumps(self.engine.board.hexagonslist), "base64").decode()

            item2 = ET.SubElement(data, 'item1')
            item2.set('score1', str(self.replayN))
            item2.text = codecs.encode(pickle.dumps(self.player1score), "base64").decode()

            item3 = ET.SubElement(data, 'item2')
            item3.set('score2', str(self.replayN))
            item3.text = codecs.encode(pickle.dumps(self.player2score), "base64").decode()

            # create a new XML file with the results
            mydata = ET.tostring(item0)
            myfile = open("history.xml", "wb")
            myfile.write(mydata)
            self.replayN += 1
        else:
            tree = ET.parse('history.xml')
            root = tree.getroot()

            data = ET.Element('data')

            item1 = ET.SubElement(data, 'item')
            item1.set('object', str(self.replayN))
            item1.text = codecs.encode(pickle.dumps(self.engine.board.hexagonslist), "base64").decode()

            item2 = ET.SubElement(data, 'item1')
            item2.set('score1', str(self.replayN))
            item2.text = codecs.encode(pickle.dumps(self.player1score), "base64").decode()

            item3 = ET.SubElement(data, 'item2')
            item3.set('score2', str(self.replayN))
            item3.text = codecs.encode(pickle.dumps(self.player2score), "base64").decode()

            root.append(data)

            tree.write('history.xml')
            self.replayN += 1

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

        # button to get last ip addres
        self.btnjoin = QPushButton("GET LAST IP ADDRESS", self)
        self.btnjoin.setAutoDefault(False)
        self.btnjoin.setStyleSheet("background-color: #66ffff")
        self.btnjoin.move(20, 250)
        self.btnjoin.clicked.connect(self.getIPaddr)

        #button to join online player
        self.btnjoin = QPushButton("JOIN PLAYER", self)
        self.btnjoin.setAutoDefault(False)
        self.btnjoin.setStyleSheet("background-color: #66ffff")
        self.btnjoin.move(20, 300)
        self.btnjoin.clicked.connect(self.createEngineandJoin)

        # button to create room for online player
        self.btnjoin = QPushButton("CREATE ROOM", self)
        self.btnjoin.setAutoDefault(False)
        self.btnjoin.setStyleSheet("background-color: #66ffff")
        self.btnjoin.move(20, 350)
        self.btnjoin.clicked.connect(self.createEngineAndMap)

        # button to play replay
        self.btnjoin = QPushButton("PLAY REPLAY", self)
        self.btnjoin.setAutoDefault(False)
        self.btnjoin.setStyleSheet("background-color: #66ffff")
        self.btnjoin.move(20, 400)
        self.btnjoin.clicked.connect(self.playReplay)


    def getIPaddr(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as read_file:
                json_object = json.load(read_file)
                self.textbox.setText(json_object["ip"])
                return


    def playReplay(self):
        if os.path.exists("history.xml"):
            self.isGameOnline = False
            self.timer.stop()
            self.engine = Engine()
            self.replayActualN = 0
            self.isGame = True
            self.replayTimer.start()


    def replayLoop(self):
        if self.replayActualN == self.replayN-1:
            print("koniec")
            self.replayTimer.stop()
            return
        else:
            #self.engine.board.hexagonlist = XXX
            tree = ET.parse('history.xml')
            root = tree.getroot()
            n = root[self.replayActualN][0].text
            score1 = root[self.replayActualN][1].text
            score2 = root[self.replayActualN][2].text
            n = pickle.loads(codecs.decode(n.encode(), "base64"))
            score1 = pickle.loads(codecs.decode(score1.encode(),"base64"))
            score2 = pickle.loads(codecs.decode(score2.encode(),"base64"))
            print("pokazuje klatke nr"+ str(self.replayActualN))
            self.engine.board.hexagonslist = n
            self.replayActualN += 1
            self.labelplayer1.setText(f"PLAYER 1 SCORE : {score1}   ")
            self.labelplayer2.setText(f"PlAYER 2 SCORE : {score2}    ")
            self.paint()

    def createRoom(self):
        self.isEnemyTurn = True
        self.t = threading.Thread(target=self.recieveBoard,args=(self.isEnemyTurn, self.engine.board.hexagonslist,))
        self.t.start()
        #t.join()

    def joinRoom(self):
        self.sendBoard()

    def sendBoard(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.textbox.text(), 10061)
        x = {
            "ip": server_address[0],
            "port": server_address[1],
        }
        with open('data.json', 'w') as outfile:
            outfile.write(json.dumps(x))

        sock.connect(server_address)

        try:
            n = self.engine.board.hexagonslist
            message = pickle.dumps([n, self.player1score])
            # print('sending {!r}'.format(message))
            sock.send(message)
            self.canIMove = False

        finally:
            print('closing socket')
            sock.close()

    def recieveBoard(self, isEnemy, board):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ("0.0.0.0", 10061)

        sock.settimeout(0.5)
        sock.bind(server_address)
        print("waiting for connection")
        while True:

            sock.listen(1)
            if self.shouldCloseSocket:
                self.shouldCloseSocket = False
                self.isEnemyTurn = False
                self.canIMove = True
                break
            try:
                connection, client_address = sock.accept()
            except:
                pass
            else: break

        try:
            print("connection from", client_address)

            while True:

                data = connection.recv(100000)

                if data:
                    self.engine.board.hexagonslist, self.player2score = pickle.loads(data)
                    print("odebrano mape")
                else:
                    print("skonczono odbierac mape", client_address)
                    self.isEnemyTurn = False
                    break

        finally:

            print("Closing current connectoin")
            connection.close()
            self.isEnemyTurn = False
            self.canIMove = True


    def quitApp(self):
        self.shouldCloseSocket = True
        with open('data.json', 'w') as outfile:
            outfile.write(json.dumps([ob.__dict__ for ob in self.engine.board.hexagonslist]))
        myApp.quit()

    def StartGame(self):
        self.canIMove = True
        self.shouldCloseSocket = True
        self.replayTimer.stop()

        self.replayN = 0
        self.labelplayer1.setText("PLAYER 1 SCORE : ")
        self.labelplayer2.setText("PLAYER 2 SCORE : ")
        self.isSettlingStart = False
        self.is2PlayerMode = False
        self.wasFirstSettling = False
        self.shouldcreateRoom = False
        self.player1score = 0
        self.player2score = 0
        #self.repaint()
        #self.show()
        self.btnstart.setText("NEW GAME")
        self.isGame = True
        self.isGameOnline = False
        self.engine = Engine()
        self.timer.start()

    def player2StartGame(self):
        self.labelplayer1.setText("PLAYER 1 SCORE : ")
        self.labelplayer2.setText("PLAYER 2 SCORE : ")
        self.shouldCloseSocket = True
        self.replayTimer.stop()
        self.isSettlingStart = False
        self.replayN = 0
        self.shouldcreateRoom = False
        self.isGameOnline = False
        self.canIMove = True
        self.is2PlayerMode = True
        self.wasFirstSettling = False
        self.player1score = 0
        self.player2score = 0
        self.repaint()
        self.btnstart.setText("NEW GAME")
        self.isGame = True
        self.engine = Engine()
        self.timer.start()

    def createEngineAndMap(self):
        self.labelplayer1.setText("PLAYER 1 SCORE : ")
        self.labelplayer2.setText("PLAYER 2 SCORE : ")
        self.is2PlayerMode = False
        self.replayTimer.stop()
        self.replayN = 0
        self.shouldcreateRoom = False
        self.wasFirstSettling = False
        self.isSettlingStart = False
        self.player1score = 0
        self.player2score = 0
        self.btnstart.setText("NEW GAME")
        self.isGame = True
        self.engine = Engine()
        while not self.wasFirstSettling:
            isSettling, isPlayer1, score = self.engine.game()
            if not isSettling:
                self.wasFirstSettling = True
        self.isGameOnline = True
        self.createRoom()
        self.timer.start()

    def createEngineandJoin(self):
        self.labelplayer1.setText("PLAYER 1 SCORE : ")
        self.labelplayer2.setText("PLAYER 2 SCORE : ")
        self.isSettlingStart = False
        self.replayN = 0
        self.shouldcreateRoom = False
        self.is2PlayerMode = False
        self.wasFirstSettling = False
        self.replayTimer.stop()
        self.player1score = 0
        self.player2score = 0
        self.btnstart.setText("NEW GAME")
        self.isGame = True
        self.engine = Engine()
        while (not self.wasFirstSettling):
            isSettling, isPlayer1, score = self.engine.game()
            if not isSettling:
                self.wasFirstSettling = True
        self.joinRoom()
        self.isEnemyTurn = False
        self.paint()
        self.canIMove = False
        self.createRoom()
        self.isGameOnline = True
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

        if self.IteratorTimer >= 5 and (not self.isGameOnline and not self.isEnemyTurn):
            self.createXML()
            self.IteratorTimer = 0
        else:
            self.IteratorTimer += 1
        if self.isGameOnline and self.shouldcreateRoom:
            self.shouldcreateRoom = False
            self.createRoom()
        if not self.isEnemyTurn and self.canIMove:
            isSettling, isPlayer1, score = self.engine.game()

            if isSettling:
                self.timer.setInterval(600)
                if self.isGameOnline:
                    self.isSettlingStart = True
            else:
                if self.isSettlingStart and self.isGameOnline:
                    self.isSettlingStart = False
                    self.joinRoom()
                    self.shouldcreateRoom = True
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
os._exit(0)