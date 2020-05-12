from copy import copy
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
        self.isEmpty = False
        self.type = self.colours[random.randint(0, 6)]
        self.draw()

    def draw(self):
        if self.isEmpty:
            self.type = self.colours[-1]
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
        self.isSpacePressed = False
        self.drawPlayer(False)
        self.setsetPx = 0
        self.setsetPy = 0
        self.listOfNeighborsPairWise = [[-1,-1],[0,-1],[1,0],[0,1],[-1,1],[-1,0]]
        self.listOfNeighborsOdd = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,0]]
        self.neighborindex = 0
        self.game()
        

    def eraseHexagonsbyPlayer(self):
        list = [self.findHexagonsToErase(self.setsetPy, self.setsetPx), self.findHexagonsToErase(self.setPy, self.setPx)]
        for l in list:
            for j in range(0, 3):
                if len(l[j])+len(l[j+3])-2 >= 2:
                    for x in l[j]:
                        self.board.hexagonslist[x[0]][x[1]].isEmpty = True
                        self.board.hexagonslist[x[0]][x[1]].draw()
                    for x in l[j+3]:
                        self.board.hexagonslist[x[0]][x[1]].isEmpty = True
                        self.board.hexagonslist[x[0]][x[1]].draw()

    def eraseHexagons(self):
        for x in range(0,self.board.y):
            for y in range(0,self.board.x):
                f = self.findHexagonsToErase(y,x)
                for j in range(0, 3):
                    if len(f[j]) + len(f[j+3]) - 2 >= 2:
                        for p in f[j]:
                            self.board.hexagonslist[p[0]][p[1]].isEmpty = True
                            self.board.hexagonslist[p[0]][p[1]].draw()
                        for p in f[j + 3]:
                            self.board.hexagonslist[p[0]][p[1]].isEmpty = True
                            self.board.hexagonslist[p[0]][p[1]].draw()


    def findHexagonsToErase(self,y,x):
        listToErase1 = []
        odd = self.listOfNeighborsOdd
        pair = self.listOfNeighborsPairWise
        for i in range(len(self.listOfNeighborsOdd)):
            helperCoords = [y, x]
            listToErase1.append([])
            listToErase1[-1].append(copy(helperCoords))
            while True:
                l = pair
                if helperCoords[1] % 2 == 1:  #for odd rows
                    l = odd
                if helperCoords[1]+l[i][1] >= 0 and\
                helperCoords[1] + l[i][1] < len(self.board.hexagonslist[helperCoords[1]])\
                and helperCoords[0] + l[i][0]>= 0 and\
                helperCoords[0] + l[i][0] < len(self.board.hexagonslist):
                    if self.board.hexagonslist[helperCoords[0]+l[i][0]][helperCoords[1]+l[i][1]].type == self.board.hexagonslist[y][x].type\
                            and not self.board.hexagonslist[helperCoords[0]+l[i][0]][helperCoords[1]+l[i][1]].isEmpty:
                        helperCoords[1] += l[i][1]
                        helperCoords[0] += l[i][0]
                        listToErase1[-1].append(copy(helperCoords))
                    else: break
                else: break
        return listToErase1


    def prepareMap(self):
        self.eraseHexagons()
        while self.gravity():
            sleep(0.3)
            self.eraseHexagons()
            sleep(0.3)
        
        
    def gravity(self):
        isChanged = False
        for y in range(self.board.y-2,-1,-1):
            for x in range(0,self.board.x):
                if self.board.hexagonslist[x][y].isEmpty: continue
                l = self.listOfNeighborsPairWise
                if x % 2 == 1: l = self.listOfNeighborsOdd
                if x != 0 and self.board.hexagonslist[x+l[4][0]][y+l[4][1]].isEmpty:
                    self.board.hexagonslist[x][y].isEmpty = True
                    self.board.hexagonslist[x+l[4][0]][y+l[4][1]].isEmpty = False
                    self.board.hexagonslist[x+l[4][0]][y+l[4][1]].type = self.board.hexagonslist[x][y].type
                    self.board.hexagonslist[x][y].draw()
                    self.board.hexagonslist[x+l[4][0]][y+l[4][1]].draw()
                    isChanged = True
                elif x != self.board.x-1 and self.board.hexagonslist[x+l[3][0]][y+l[3][1]].isEmpty:
                    self.board.hexagonslist[x][y].isEmpty = True
                    self.board.hexagonslist[x+l[3][0]][y+l[3][1]].isEmpty = False
                    self.board.hexagonslist[x+l[3][0]][y+l[3][1]].type = self.board.hexagonslist[x][y].type
                    self.board.hexagonslist[x][y].draw()
                    self.board.hexagonslist[x+l[3][0]][y+l[3][1]].draw()
                    isChanged = True
            if self.infinitMode(): isChanged = True
            sleep(0.005)

        return isChanged

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
        sleep(0.03)

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
            if self.board.hexagonslist[self.setPy][self.setPx].isEmpty: return
            if not self.isSpacePressed and self.isSet:
                if self.board.hexagonslist[self.setsetPy][self.setsetPx].isEmpty: return
                self.swap()
                return
            self.isSpacePressed = True
            self.isSet = True
            self.findNeighbor(True)
        else: self.isSpacePressed = False

    def swap(self):
        self.drawPlayer(True)
        self.isSet = False
        sleep(0.5)
        auto = self.board.hexagonslist[self.setsetPy][self.setsetPx].type
        self.board.hexagonslist[self.setsetPy][self.setsetPx].type = self.board.hexagonslist[self.setPy][self.setPx].type
        self.board.hexagonslist[self.setPy][self.setPx].type = auto
        self.board.hexagonslist[self.setsetPy][self.setsetPx].draw()
        self.board.hexagonslist[self.setPy][self.setPx].draw()
        sleep(0.3)
        self.eraseHexagonsbyPlayer()
        sleep(0.6)
        self.prepareMap()


    def infinitMode(self):
        ischanged = False
        for x in range(0,self.board.x):
            if self.board.hexagonslist[x][0].isEmpty:
                self.board.hexagonslist[x][0].isEmpty = False
                self.board.hexagonslist[x][0].type = self.board.hexagonslist[x][0].colours[random.randint(0,6)]
                self.board.hexagonslist[x][0].draw()
                ischanged = True
        return ischanged


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
        self.prepareMap()
        while True:
            self.movePlayer()

#uncomment to start game in terminal
#start = Engine()
