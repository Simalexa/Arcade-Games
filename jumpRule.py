import random

class jumpRule:
    def checkRightWall(sel, maxX, coord):
        if coord[0] > maxX:
            return False
        return True

    def checkLeftWall(sel, coord):
        if coord[0] < 0:
            return False
        return True

    def floorCheck(self, maxY, coord):
        if coord[1] >= maxY:
            return True
        return False

    def blockRule(self, front, coord, playerColor):
        for i in range(0, len(front.elementPos) - 1, 1):
            if coord[0] > front.elementPos[i][0] and coord[0] < front.elementPos[i + 1][0]:
                if coord[1] - 1 < front.elementPos[i][1]:
                    if playerColor == front.colorPos[i]:
                        return i
        return -1

    def checkEndGame(self, front, coord):
        for i in range(0, len(front.elementPos) - 1, 1):
            if coord[0] > front.elementPos[i][0] and coord[0] < front.elementPos[i + 1][0]:
                if coord[1] - 1 < front.elementPos[i][1]:
                    if front.colorPos[i] == [0, 0, 0, 0]:
                        return False
                    else:
                        return True

class frontMovement:
    standartColor = []
    colorPos = []
    elementPos = []
    speed = 40
    colorMultiplayer = 0.5
    def generateColor(self, initialColor):
        maxC = initialColor * (1 + self.colorMultiplayer)
        minC = initialColor * (1 - self.colorMultiplayer)
        if maxC >= 255:
            maxC = 255
        if maxC == 0:
            maxC = 50
        return random.randint(int(minC/5), int(maxC/5)) * 5

    def generateFront(self, score, playerColor):
        self.standartColor = [playerColor]
        for i in range(0, 20):
            numberR = self.generateColor(playerColor[0])
            numberG = self.generateColor(playerColor[1])
            numberB = self.generateColor(playerColor[2])
            numberT = self.generateColor(playerColor[3])
            self.standartColor.append([numberR, numberG, numberB, numberT])

    def createFront(self, maxX, score, playerColor):
        self.generateFront(score, playerColor)
        for i in range(0, maxX + 1, 2):
            number = random.randint(0, 20)
            self.colorPos.append(self.standartColor[number])
            self.colorPos.append(self.standartColor[number])
            self.elementPos.append([i, 0])
            self.elementPos.append([i + 1, 0])

    def destroyBlock(self, pos, playerColor):
        toDel = [pos, pos]
        flag = False
        i = pos + 1
        if i < len(self.elementPos):
            while flag == False:
                if self.colorPos[i] == playerColor:
                    toDel[1] = i
                    i += 1
                else:
                    flag = True
                if i == len(self.elementPos):
                    flag = True
        flag = False
        i = pos - 1
        if i > 0:
            while flag == False:
                if self.colorPos[i] == playerColor:
                    toDel[0] = i
                    i -= 1
                else:
                    flag = True
                if i == 0:
                    flag = True
        for i in range(toDel[0], toDel[1] + 1):
            self.colorPos[i] = [0, 0, 0, 0]

    def checkIfWinable(self, playerColor, score):
        for i in range(len(self.colorPos)):
            if self.colorPos[i] == playerColor:
                print(i)
                if score % 50 == 0: #increase dificulty of the game
                    self.colorMultiplayer *= 0.9
                return True
        return False

    def newFront(self, maxX, score, playerColor):
        self.createFront(maxX, score, playerColor)
        del self.elementPos[0:maxX + 1]
        del self.colorPos[0:maxX + 1]
