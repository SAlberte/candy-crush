import colorama
import os
import random
from colorama import Fore, Back, Style, Cursor
import sys

colorama.init(wrap = False)
os.system("cls")

## Contains hexagon with its colour and coordinates
class Hexagon:
    colours = [Back.GREEN, Back.BLUE, Back.CYAN, Back.RED, Back.YELLOW, Back.LIGHTMAGENTA_EX, Back.LIGHTWHITE_EX, Back.BLACK]
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
        print(self.type + " " + self.rst)
        sys.stdout.write("\x1b[%d;%dH" % (self.y+1, self.x))
        print(self.type + " " + self.rst+self.type + " " + self.rst+self.type + " " + self.rst)
        sys.stdout.write("\x1b[%d;%dH" % (self.y+2, self.x))
        print(self.type + " " + self.rst + self.type + " " + self.rst + self.type + " " + self.rst)
        sys.stdout.write("\x1b[%d;%dH" % (self.y+3, self.x+1))
        print(self.type + " " + self.rst)



## Class that creates list of hexagon, arranged in grid
class Board:
    def __init__(self):
        self.x = 20
        self.y = 15
        self.hexagonslist = []
        self.initialization()

    def initialization(self):
        self.hexagonslist.append([])
        for j in range(self.x):
            self.hexagonslist.append([])
            for i in range(self.y):
                self.hexagonslist[-1].append(Hexagon(j*3+j+1+(i%2)*2, 3*i+1))

board = Board()