from PyQt5 import QtCore, QtGui, QtWidgets
from jumpRule import jumpRule, frontMovement


class jumpGame(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()
    blockSize = 20
    maxX = 9
    maxY = 20
    playerCoordinate = []
    rule = jumpRule()
    front = frontMovement()
    playerColor = [100, 100, 100, 200]
    frontCoordinate = []
    speedBody = 10
    moveForce = 0.005
    force = [0, 0]
    mass = 5
    curTime = 0
    moveTime = 15
    score = 0
    maxScore = 0
    jump = False
    kick = False
    pause = False
    endGame = False

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(400, 400, 230, 430)
        self.setWindowTitle("Jump Game")
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.changeLevel()
        self.playerCoordinate = [self.maxX/2, self.maxY]
        self.moveTimer = QtCore.QTimer()
        self.moveTimer.timeout.connect(self.moveBody)
        self.gravityTimer = QtCore.QTimer()
        self.gravityTimer.timeout.connect(self.gravity)
        self.jumpTimer = QtCore.QTimer()
        self.jumpTimer.timeout.connect(self.jumpBody)
        self.createFront()
        self.frontTimer = QtCore.QTimer()
        self.frontTimer.timeout.connect(self.frontMovement)
        self.frontTimer.start(self.front.speed)

    def resizeEvent(self, event):
        w = self.size().width()
        h = self.size().height()
        if w / (self.maxX + 1) * 0.6 <=  h / (self.maxY + 1):
            self.blockSize = w / (self.maxX + 1) * 0.6
        else:
            self.blockSize = h / (self.maxY + 1)

    def changeLevel(self):
        if self.score == 0:
            self.playerColor = [0, 100, 100, 150]
        if self.score == 100:
            self.playerColor = [100, 100, 0, 200]
        if self.score == 200:
            self.playerColor = [0, 50, 200, 200]
        if self.score == 300:
            self.playerColor = [0, 0, 255, 200]
        if self.score == 400:
            self.playerColor = [255, 0, 0, 200]
        if self.score == 500:
            self.playerColor = [0, 255, 0, 200]

    def createFront(self):
        self.front.createFront(self.maxX, self.score, self.playerColor)
        while self.front.checkIfWinable(self.playerColor, self.score) == False:
            self.front.newFront(self.maxX, self.score, self.playerColor)

    def frontMovement(self):
        if self.pause == False:
            for i in range(len(self.front.elementPos)):
                self.front.elementPos[i][1] += 0.2
            if self.front.elementPos[0][1] >= self.maxY + 1:
                self.front.newFront(self.maxX, self.score, self.playerColor)
                while self.front.checkIfWinable(self.playerColor, self.score) == False:
                    self.front.newFront(self.maxX, self.score, self.playerColor)
            if self.rule.checkEndGame(self.front, self.playerCoordinate) is True:
                self.endGame = True
            self.update()

    def moveBody(self):
        if self.pause == False:
            self.curTime += 1;
            if self.rule.checkRightWall(self.maxX, self.playerCoordinate) is False:
                self.playerCoordinate[0] = self.maxX
                self.force[0] = -0.5 * self.force[0]
            if self.rule.checkLeftWall(self.playerCoordinate) is False:
                self.playerCoordinate[0] = 0
                self.force[0] = -0.5 * self.force[0]
            if self.kick is True:
                self.playerCoordinate[0] += self.force[0] / self.mass * (self.curTime - self.moveTime) ** 2
            if self.curTime == self.moveTime:
                self.kick = False
                self.moveTimer.stop()
            self.update()

    def startNewGame(self):
        self.jumpTime = 0
        self.curTime = 0
        self.front.newFront(self.maxX, self.score, self.playerColor)
        while self.front.checkIfWinable(self.playerColor, self.score) == False:
            self.front.newFront(self.maxX, self.score, self.playerColor)

    def jumpBody(self):
        if self.pause == False:
            self.jumpTime += 1;
            if self.jump is True:
                self.playerCoordinate[1] += self.force[1] / self.mass * (self.jumpTime - self.moveTime) ** 2
            if self.jumpTime == self.moveTime:
                self.jump = False
                self.jumpTimer.stop()
            self.update()

    def applyForce(self, forceX, forceY):
        self.force = [forceX, forceY]
        if forceX != 0:
            self.curTime = 0
            self.kick = True
            self.moveTimer.start(self.speedBody)
        if forceY != 0:
            self.jumpTime = 0
            self.jump = True
            self.jumpTimer.start(self.speedBody)

    def gravity(self):
        if self.pause == False:
            self.fallTime +=1
            if self.rule.floorCheck(self.maxY, self.playerCoordinate) is False:
                self.playerCoordinate[1] += 0.0001 * self.fallTime**2
                posToDesytoy = self.rule.blockRule(self.front, self.playerCoordinate, self.playerColor)
                if posToDesytoy != -1:
                    self.front.destroyBlock(posToDesytoy, self.playerColor)
                    self.front.speed *= 0.95
                    self.score += 10
                    self.changeLevel()
            if self.playerCoordinate[1] > self.maxY:
                self.playerCoordinate[1] = self.maxY
                self.gravityTimer.stop()
            self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_D:
            if self.rule.checkRightWall(self.maxX, self.playerCoordinate):
                self.applyForce(self.moveForce, 0)
        if key == QtCore.Qt.Key_A:
            if self.rule.checkLeftWall(self.playerCoordinate):
                self.applyForce(-self.moveForce, 0)
        if key == QtCore.Qt.Key_Space:
            if self.rule.floorCheck(self.maxY, self.playerCoordinate) is True:
                self.fallTime = 0
                self.gravityTimer.start(self.speedBody)
                self.applyForce(0, -self.moveForce * 3)
        if key == QtCore.Qt.Key_1:
            self.frontTimer.start()
            self.endGame = False
            self.changeLevel()
            self.startNewGame()
            if self.score > self.maxScore:
                self.maxScore = self.score
            self.score = 0
        if key ==QtCore.Qt.Key_P:
            self.pause = not self.pause
        if key == QtCore.Qt.Key_Escape:
            self.close()
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        self.setBoundary(qp)
        self.printScore(qp)
        if self.endGame == False:
            color = QtGui.QColor.fromRgb(self.playerColor[0], self.playerColor[1], self.playerColor[2], self.playerColor[3])
            qp.fillRect(self.playerCoordinate[0] * self.blockSize, self.playerCoordinate[1] *
                        self.blockSize, self.blockSize * 1.05, self.blockSize * 1.05, color)
            self.printFront(qp)
        else:
            self.frontTimer.stop()
            qp.setFont(QtGui.QFont("Times", self.blockSize / 2.5))
            qp.drawText(self.maxX * self.blockSize / 2, self.maxY * self.blockSize / 2, "Defeat!")
            qp.drawText(30, self.maxY * self.blockSize / 2 + self.blockSize, "Press \"1\" to start the new game")

    def printFront(self, qp):
        for i in range(0, len(self.front.elementPos)):
            color = QtGui.QColor.fromRgb(self.front.colorPos[i][0], self.front.colorPos[i][1], self.front.colorPos[i][2], self.front.colorPos[i][3])
            qp.fillRect(self.front.elementPos[i][0] * self.blockSize, self.front.elementPos[i][1] *
                        self.blockSize, self.blockSize * 1.05, self.blockSize * 1.05, color)

    def setBoundary(self, qp):
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
        qp.drawText(self.maxX * self.blockSize * 1.2, 6 * self.blockSize, "Jump to destroy objects with the same color")
        qp.drawText(self.maxX * self.blockSize * 1.2, 7 * self.blockSize, "Press \" Space \" to jump")
        qp.drawText(self.maxX * self.blockSize * 1.2, 8 * self.blockSize, "Press \" P \" to pause")
        qp.drawText(self.maxX * self.blockSize * 1.2, 9 * self.blockSize, "Press \" Escape \" to exit")
