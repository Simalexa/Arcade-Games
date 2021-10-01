from PyQt5 import QtCore, QtGui, QtWidgets
from snakeRule import snakeParameters
from random import randrange

class snakeGame(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()
    snake = snakeParameters()
    blockSize = 20
    maxX = 9
    maxY = 9
    dot = [[5, 5]]
    time = 0
    speed = 150
    score = 0
    maxScore = 0
    defeat = False
    pause = False

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(400, 400, 600, 600 * 0.6)
        self.setWindowTitle("Snake Game")
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        self.curr_time = QtCore.QTime(00, 00, 00)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.moveSnake)
        self.timer.start(self.speed)
        self.createDot()

    def resizeEvent(self, event):
        w = self.size().width()
        h = self.size().height()
        if w / (self.maxX + 1) * 0.6 <=  h / (self.maxY + 1):
            self.blockSize = w / (self.maxX + 1) * 0.6
        else:
            self.blockSize = h / (self.maxY + 1)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        self.setBoundary(qp)
        self.printScore(qp)
        if self.defeat == False and self.snake.pos[0][0] < (self.maxX - 1) * self.blockSize and self.snake.pos[0][1] < (self.maxY - 1) * self.blockSize:
            color = QtGui.QColor.fromRgb(0, 255, 0, 100)
            for i in range(len(self.snake.pos)):
                qp.fillRect(self.snake.pos[i][0] * self.blockSize, self.snake.pos[i][1]*self.blockSize, self.blockSize  * 1.05, self.blockSize  * 1.05, color)
            self.printEyes(qp)
            for i in range(len(self.dot)):
                colorDot = QtGui.QColor.fromRgb(255, 0, 0, 200)
                qp.fillRect(self.dot[i][0]*self.blockSize, self.dot[i][1]*self.blockSize, self.blockSize * 1.05, self.blockSize  * 1.05, colorDot)
        if self.defeat == True:
            self.timer.stop()
            qp.setFont(QtGui.QFont("Times", self.blockSize / 2.5))
            qp.drawText(10, self.maxY * self.blockSize / 2, "Defeat. Press \"1\" to start the new game")
            qp.drawText(10, self.maxY * self.blockSize / 2 + self.blockSize, "Press \"Escape\" to exit")

    def printScore(self,qp):
        qp.setFont(QtGui.QFont("Times", self.blockSize / 2.1))
        qp.drawText(self.maxX * self.blockSize * 1.2, self.blockSize, "Score:")
        qp.drawText(self.maxX * self.blockSize * 1.2, 2 * self.blockSize, "{}".format(self.score))
        qp.drawText(self.maxX * self.blockSize * 1.2, 3 * self.blockSize, "Maximum Score:")
        qp.drawText(self.maxX * self.blockSize * 1.2, 4 * self.blockSize, "{}".format(self.maxScore))
        qp.drawText(self.maxX * self.blockSize * 1.2, 6 * self.blockSize, "Press \" P \" to pause")
        qp.drawText(self.maxX * self.blockSize * 1.2, 7 * self.blockSize, "Press \" Esc \" to pause")

    def setBoundary(self,qp):
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        qp.drawRect(QtCore.QRectF(0,0, (self.maxX + 1)*self.blockSize, (self.maxY + 1)*self.blockSize))
        qp.setPen(QtGui.QPen(QtCore.Qt.black,0.1))
        for i in range(1, self.maxX + 1):
            qp.drawLine(i * self.blockSize, 0, i * self.blockSize, (self.maxY + 1) * self.blockSize)
        for i in range(1, self.maxY + 1):
            qp.drawLine(0, i * self.blockSize, (self.maxX + 1) * self.blockSize, i * self.blockSize)

    def printEyes(self, qp):
        color = QtGui.QColor.fromRgb(0, 0, 0, 255)
        pos = self.snake.eyePosition()
        qp.fillRect((pos[0] + self.snake.pos[0][0])*self.blockSize, (pos[1] + self.snake.pos[0][1])*self.blockSize,
                    self.blockSize / 5, self.blockSize /5, color)
        qp.fillRect((pos[2] + self.snake.pos[0][0])*self.blockSize, (pos[3] + self.snake.pos[0][1])*self.blockSize,
                    self.blockSize / 5, self.blockSize / 5, color)

    def keyPressEvent(self, event):
        key = event.key()
        if self.pause == False:
            if key == QtCore.Qt.Key_W:
                self.snake.speed = 0
            if key == QtCore.Qt.Key_D:
                self.snake.speed = 90
            if key == QtCore.Qt.Key_S:
                self.snake.speed = 180
            if key == QtCore.Qt.Key_A:
                self.snake.speed = 270
        if key == QtCore.Qt.Key_1:
            self.defeat = False
            self.timer.start(self.speed)
            self.snake.startNew()
            if self.score > self.maxScore:
                self.maxScore = self.score
            self.score = 0
        if key == QtCore.Qt.Key_Escape:
            self.close()
        if key == QtCore.Qt.Key_P:
            self.pause = not self.pause

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def endGame(self):
        self.defeat = True
        self.snake.startNew()

    def createDot(self):
        del self.dot[0]
        flag = False
        #check if coordiantes of dot not equal one of the coordinate of the snake
        while flag == False:
            dotX = randrange(0, self.maxX)
            dotY = randrange(0, self.maxY)
            if self.snake.creteNewDot(dotX, dotY) == True:
                flag = True
        self.dot.append([dotX, dotY])

    def moveSnake(self):
        if self.pause == False:
            self.curr_time = self.curr_time.addSecs(1)
            self.snake.changePos(1)
            if self.snake.newY != -1:
                self.score +=10
                self.snake.addElement(self.snake.newX, self.snake.newY)
                self.snake.newX = -1
                self.snake.newY = -1
            if self.snake.checkBoundary(self.snake.pos[0][0], self.snake.pos[0][1], self.maxX, self.maxY) is False or self.snake.checkSnake() is False:
                self.endGame()
            else:
                tail = len(self.snake.pos) - 1
                if self.snake.checkDot(self.dot, self.snake.pos[0][0], self.snake.pos[0][1]) is True:
                    self.snake.newX = self.snake.pos[tail][0]
                    self.snake.newY = self.snake.pos[tail][1]
                    self.createDot()
        self.update()