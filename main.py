from time import sleep
import colorama
import os
import random
from colorama import Fore, Back, Style, Cursor
import sys
import keyboard

colorama.init(wrap = False)
os.system("cls")

## Contains hexagon with its colour and coordinates


class Hexagon:
    colours = [Back.GREEN, Back.BLUE, Back.CYAN, Back.RED, Back.YELLOW, Back.MAGENTA, Back.LIGHTWHITE_EX, Back.BLACK]
    rst = Style.RESET_ALL

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.initialization()
        self.draw()

    def initialization(self):
        self.type = self.colours[random.randint(0, 6)]

    def draw(self):
        sys.stdout.write("\x1b[%d;%dH" % (self.y, self.x+1))
        sys.stdout.flush()
        sys.stdout.write(self.type + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (self.y+1, self.x))
        sys.stdout.flush()
        sys.stdout.write(self.type + " " + self.rst+self.type + " " + self.rst+self.type + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (self.y+2, self.x))
        sys.stdout.flush()
        sys.stdout.write(self.type + " " + self.rst + self.type + " " + self.rst + self.type + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (self.y+3, self.x+1))
        sys.stdout.flush()
        sys.stdout.write(self.type + " " + self.rst)
        sys.stdout.flush()



## Class that creates list of hexagon, arranged in grid
class Board:
    def __init__(self):
        self.x = 20
        self.y = 15
        self.hexagonslist = []
        self.initialization()

    def initialization(self):
        for j in range(self.x):
            self.hexagonslist.append([])
            for i in range(self.y):
                self.hexagonslist[-1].append(Hexagon(j*3+j+1+(i%2)*2+1, 3*i+1+1))

    def setHexagons(self):
        os.system("cls")
        for i in self.hexagonslist:
            for j in i:
                j.draw()


class Engine:
    def __init__(self):
        self.board = Board()
        self.type = Back.LIGHTGREEN_EX
        self.rst = Style.RESET_ALL
        self.setPx = 0
        self.setPy = 0
        self.isSet = False
        self.drawPlayer(False)
        self.setsetPx = 0
        self.setsetPy = 0
        self.listOfNeighborsPairWise = [[-1,-1],[0,-1],[1,0],[0,1],[-1,1],[-1,0]]
        self.listOfNeighborsOdd = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,0]]
        self.neighborindex = 0
        self.game()

    def drawPlayer(self, isErase):
        x = self.board.hexagonslist[self.setPy][self.setPx].x
        y = self.board.hexagonslist[self.setPy][self.setPx].y
        if self.isSet:
            x = self.board.hexagonslist[self.setsetPy][self.setsetPx].x
            y = self.board.hexagonslist[self.setsetPy][self.setsetPx].y
        h = Back.BLACK if isErase else self.type
        sys.stdout.write("\x1b[%d;%dH" % (y, x))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (y-1, x+1))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (y, x+2))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (y+1, x+3))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (y + 2, x + 3))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (y + 3, x + 2))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (y + 4, x + 1))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (y + 3, x ))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (y + 2, x-1))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sys.stdout.write("\x1b[%d;%dH" % (y + 1, x - 1))
        sys.stdout.flush()
        sys.stdout.write(h + " " + self.rst)
        sys.stdout.flush()
        sleep(0.025)

    def movePlayer(self):
        x = 0
        y = 0
        if not self.isSet:
            if keyboard.is_pressed('Left'):
                y = -1
                if self.setPy > 0:
                    self.drawPlayer(True)
                    self.setPy -=1
                    self.drawPlayer(False)
            if keyboard.is_pressed('Right'):
                y= 1
                if self.setPy < len(self.board.hexagonslist)-1:
                    self.drawPlayer(True)
                    self.setPy += 1
                    self.drawPlayer(False)
            if keyboard.is_pressed('Down'):
                x =1
                if self.setPx < len(self.board.hexagonslist[self.setPy])-1:
                    self.drawPlayer(True)
                    self.setPx += 1
                    self.drawPlayer(False)
            if keyboard.is_pressed('Up'):
                x = -1
                if self.setPx > 0:
                    self.drawPlayer(True)
                    self.setPx -= 1
                    self.drawPlayer(False)
        else:
            if keyboard.is_pressed('Left'):
                self.findNeighbor(True)
            if keyboard.is_pressed("Right"):
                self.findNeighbor(False)
        if keyboard.is_pressed("Space"):
            self.isSet = True
            self.findNeighbor(True)


    def findNeighbor(self,isLeft):
        n = 1
        if isLeft: n = -1
        self.neighborindex += n
        if self.setPx % 2 == 1:
            while True:
                if self.neighborindex <= -1:
                    self.neighborindex = 5
                if self.neighborindex >= 6:
                    self.neighborindex = 0
                if self.setPx+self.listOfNeighborsOdd[self.neighborindex][1] >= 0 and\
                self.setPx + self.listOfNeighborsOdd[self.neighborindex][1] < len(self.board.hexagonslist[self.setPx])\
                and self.setPy + self.listOfNeighborsOdd[self.neighborindex][0]>= 0 and\
                self.setPy + self.listOfNeighborsOdd[self.neighborindex][0] < len(self.board.hexagonslist):
                    self.drawPlayer(True)
                    self.setsetPx =self.setPx+self.listOfNeighborsOdd[self.neighborindex][1]
                    self.setsetPy =self.setPy+self.listOfNeighborsOdd[self.neighborindex][0]
                    self.drawPlayer(False)
                    break
                else:
                    self.neighborindex += n
                    continue
        else:
            while True:
                if self.neighborindex <= -1:
                    self.neighborindex = 5
                if self.neighborindex >= 6:
                    self.neighborindex = 0
                if self.setPx+self.listOfNeighborsPairWise[self.neighborindex][1] >= 0 and\
                self.setPx + self.listOfNeighborsPairWise[self.neighborindex][1] < len(self.board.hexagonslist[self.setPx])\
                and self.setPy + self.listOfNeighborsPairWise[self.neighborindex][0]>= 0 and\
                self.setPy + self.listOfNeighborsPairWise[self.neighborindex][0] < len(self.board.hexagonslist):
                    self.drawPlayer(True)
                    self.setsetPx =self.setPx+self.listOfNeighborsPairWise[self.neighborindex][1]
                    self.setsetPy =self.setPy+self.listOfNeighborsPairWise[self.neighborindex][0]
                    self.drawPlayer(False)
                    break
                else:
                    self.neighborindex += n
                    continue

    def game(self):
        while True:
            self.movePlayer()




start = Engine()
