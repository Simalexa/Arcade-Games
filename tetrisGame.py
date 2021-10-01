from PyQt5 import QtCore, QtGui, QtWidgets
from tetrisRule import figure
from random import randrange
import math
import copy

class tetrisGame(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()
    maxX = 10
    maxY = 20
    blockSize = 20
    speed = 500
    figures = figure()
    allElements = []
    allColors = []
    score = 0
    maxScore = 0
    defeat = False
    pause = False

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(400, 400, 300, 340)
        self.setWindowTitle("Tetris Game")
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        self.createFirstElement()
        self.curr_time = QtCore.QTime(00, 00, 00)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.moveElement)
        self.timer.start(self.speed)

    def resizeEvent(self, event):
        w = self.size().width()
        h = self.size().height()
        if w / (self.maxX + 1) * 0.6 <=  h / (self.maxY + 1):
            self.blockSize = w / (self.maxX + 1) * 0.6
        else:
            self.blockSize = h / (self.maxY + 1)

    def createFirstElement(self):
        self.number = randrange(0, 6)
        self.currentElement = copy.deepcopy(figure().standartFig[self.number])
        self.currentElement = self.figures.move(self.currentElement, self.maxX/2, 0)
        self.allElements = []

    def createNewElement(self):
        self.allElements.append(self.currentElement)
        self.allColors.append(self.figures.standartColor[self.number])
        if self.figures.checkEndGame(self.currentElement):
            self.defeat = True
        else:
            self.number = randrange(0, 6)
            self.currentElement = copy.deepcopy(figure().standartFig[self.number])
            self.currentElement = self.figures.move(self.currentElement, self.maxX / 2, 0)
            layerstoDelete = self.figures.checkAllLayer(self.allElements, self.maxX + 1, self.maxY + 1)
            for i in range(len(layerstoDelete)):
                self.allElements = self.figures.deleteLayer(self.allElements, layerstoDelete[i])
                self.score += 10
            self.speed = self.speed * 0.95

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        self.printScore(qp)
        colorElement = self.figures.standartColor[self.number]
        if self.defeat == False:
            for i in range(len(self.currentElement)):
                qp.fillRect(self.currentElement[i][0] * self.blockSize, self.currentElement[i][1] * self.blockSize,
                            self.blockSize * 1.05, self.blockSize * 1.05, colorElement)
            if len(self.allElements) != 0:
                for j in range(len(self.allElements)):
                    colorElement = self.allColors[j]
                    for i in range(len(self.allElements[j])):
                        qp.fillRect(self.allElements[j][i][0] * self.blockSize, self.allElements[j][i][1] *
                                    self.blockSize, self.blockSize * 1.05, self.blockSize * 1.05, colorElement)
        else:
            self.timer.stop()
            qp.setFont(QtGui.QFont("Times", self.blockSize / 2.5))
            qp.drawText(10, self.maxY * self.blockSize / 2, "Defeat. Press \"1\" to start the new game")
            qp.drawText(10, self.maxY * self.blockSize / 2 + self.blockSize, "Press \"Escape\" to exit")
        self.printBondary(qp)

    def printBondary(self, qp):
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        qp.drawRect(QtCore.QRectF(0, 0, (self.maxX + 1) * self.blockSize, (self.maxY + 1) * self.blockSize))
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 0.1))
        for i in range(1, self.maxX + 1):
            qp.drawLine(i * self.blockSize, 0, i * self.blockSize, (self.maxY + 1) * self.blockSize)
        for i in range(1, self.maxY + 1):
            qp.drawLine(0, i * self.blockSize, (self.maxX + 1) * self.blockSize, i * self.blockSize)

    def printScore(self,qp):
        qp.setFont(QtGui.QFont("Times", self.blockSize / 2.1))
        qp.drawText(self.maxX * self.blockSize * 1.2, self.blockSize, "Score:")
        qp.drawText(self.maxX * self.blockSize * 1.2, 2 * self.blockSize, "{}".format(self.score))
        qp.drawText(self.maxX * self.blockSize * 1.2, 3 * self.blockSize, "Maximum Score:")
        qp.drawText(self.maxX * self.blockSize * 1.2, 4 * self.blockSize, "{}".format(self.maxScore))
        qp.drawText(self.maxX * self.blockSize * 1.2, 6 * self.blockSize, "Press \" Space \" to rotate objects")
        qp.drawText(self.maxX * self.blockSize * 1.2, 7 * self.blockSize, "Press \" ASD \" to move objects")
        qp.drawText(self.maxX * self.blockSize * 1.2, 8 * self.blockSize, "Press \" P \" to pause")
        qp.drawText(self.maxX * self.blockSize * 1.2, 9 * self.blockSize, "Press \" Esc \" to pause")

    def keyPressEvent(self, event):
        key = event.key()
        if self.pause == False:
            if key == QtCore.Qt.Key_D:
                if self.figures.checkRightBounadary(self.currentElement, self.maxX) and \
                        self.figures.checkFloor(self.currentElement, self.maxY):
                    self.currentElement = self.figures.move(self.currentElement, 1, 0)
                    if self.figures.checkAllFigures(self.currentElement, self.allElements) is False:
                        self.currentElement = self.figures.move(self.currentElement, -1, 0)
            if key == QtCore.Qt.Key_A:
                if self.figures.checkLeftBounadary(self.currentElement) and \
                        self.figures.checkFloor(self.currentElement, self.maxY):
                    self.currentElement = self.figures.move(self.currentElement, -1, 0)
                    if self.figures.checkAllFigures(self.currentElement, self.allElements) is False:
                        self.currentElement = self.figures.move(self.currentElement, 1, 0)
            if key == QtCore.Qt.Key_S:
                if self.figures.checkFloor(self.currentElement, self.maxY) and self.figures.checkAllFigures(self.currentElement, self.allElements):
                    self.currentElement = self.figures.move(self.currentElement, 0, 1)
                    if self.figures.checkAllFigures(self.currentElement, self.allElements) is False:
                        self.currentElement = self.figures.move(self.currentElement, 0, -1)
            if key == QtCore.Qt.Key_Space:
                self.currentElement = self.figures.rotate(self.number, self.currentElement, math.pi / 2, self.maxX)
        if key == QtCore.Qt.Key_1:
            self.defeat = False
            self.timer.start(self.speed)
            self.startNewGame()
            if self.score > self.maxScore:
                self.maxScore = self.score
            self.score = 0
        if key == QtCore.Qt.Key_P:
            self.pause = not self.pause
        if key == QtCore.Qt.Key_Escape:
            self.close()
        self.update()

    def startNewGame(self):
        self.speed = 500
        self.allElements = []
        self.allColors = []
        self.currentElement.clear()
        self.createFirstElement()

    def moveElement(self):
        if self.pause == False:
            if self.figures.checkFloor(self.currentElement, self.maxY) and self.figures.checkAllFigures(self.currentElement, self.allElements):
                self.currentElement = self.figures.move(self.currentElement, 0, 1)
                if self.figures.checkAllFigures(self.currentElement, self.allElements) is False:
                    self.currentElement = self.figures.move(self.currentElement, 0, -1)
                    self.createNewElement()
            else:
                self.createNewElement()
            self.score += 1
        self.update()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
