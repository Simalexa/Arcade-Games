
class snakeParameters:
    pos = [[5, 5]]
    speed = 0
    newX = -1
    newY = -1

    def addElement(self, X, Y):
        self.pos.append([X, Y])

    def changePos(self, step):
        for i in range(1, len(self.pos)):
            self.pos[len(self.pos) - i][0] = self.pos[len(self.pos) - i - 1][0]
            self.pos[len(self.pos) - i][1] = self.pos[len(self.pos) - i - 1][1]
        if self.speed == 0:
            self.pos[0][1] -= step
        if self.speed == 90:
            self.pos[0][0] += step
        if self.speed == 180:
            self.pos[0][1] += step
        if self.speed == 270:
            self.pos[0][0] -= step

    def eyePosition(self):
        if self.speed == 0:
            return [1 / 5, 1 / 5, 3 * 1 / 5, 1 / 5]
        if self.speed == 90:
            return [3 * 1/5, 1/5, 3 * 1/5, 3 * 1/5]
        if self.speed == 180:
            return [1 / 5, 3 * 1 / 5, 3 * 1 / 5, 3 * 1 / 5]
        if self.speed == 270:
            return [1/5, 1/5,  1/5, 3 * 1/5]

    def startNew(self):
        self.pos = [[5, 5]]
        self.speed = 0

    def checkBoundary(self, posX, posY, maxX, maxY):
        if posX > maxX or posX < 0 or posY > maxY or posY < 0:
            return False
        else:
            return True

    def checkSnake(self):
        for i in range(len(self.pos)):
            for j in range(len(self.pos)):
                if self.pos[i] == self.pos[j] and i != j:
                    return False
        return True

    def checkDot(self, dot, newX, newY):
        for j in range(len(dot)):
            if newX == dot[j][0] and newY == dot[j][1]:
                return True
        return False

    def creteNewDot(self, X, Y):
        for i in range(len(self.pos)):
            if self.pos[i][0] == X and self.pos[i][1] == Y:
                return False
        return True