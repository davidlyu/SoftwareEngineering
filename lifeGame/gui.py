# encoding = utf-8

import random
from PyQt4 import QtGui


class Window(QtGui.QWidget):
    def __init__(self, matrix, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.cell_size = 5
        width = len(matrix[0]) * self.cell_size
        height = len(matrix) * self.cell_size
        self.resize(width, height)
        self.width = width
        self.height = height
        self.matrix = matrix
        self.update()
        self.red = 0
        self.green = 0
        self.blue = 0


    def draw(self, matrix):
        self.matrix = matrix
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == 1:
                    # self.red += 1
                    # self.red %= 255
                    # self.green += 1
                    # self.green %= 255
                    # self.blue += 1
                    # self.blue %= 255
                    self.red = 100
                    self.green = 100
                    self.blue = 100
                    qp.fillRect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size,
                                QtGui.QColor(self.red, self.green, self.blue, 255))
