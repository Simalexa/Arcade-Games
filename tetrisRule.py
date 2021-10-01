from PyQt5 import QtGui
import math
import copy

class figure:
    standartFig = [[[0, 0], [0, 1], [0, 2], [0, 3]],
           [[0, 0], [0, 1], [1, 0], [1, 1]],
           [[0, 0], [1, 0], [2, 0], [1, 1]],
           [[0, 0], [1, 0], [0, 1], [0, 2]],
           [[0, 0], [1, 0], [1, 1], [1, 2]],
           [[0, 0], [1, 0], [1, 1], [2, 1]],
           [[1, 0], [2, 0], [0, 1], [1, 1]]]
    pivot = [1, -1, 2, 2, 2, 2, 3]
    standartColor = [QtGui.QColor.fromRgb(0, 255, 0, 150), QtGui.QColor.fromRgb(255, 0, 0, 150),
                     QtGui.QColor.fromRgb(0, 0, 255, 150), QtGui.QColor.fromRgb(0, 255, 255, 150),
                     QtGui.QColor.fromRgb(255, 0, 255, 150),QtGui.QColor.fromRgb(100, 100, 255, 150),
                     QtGui.QColor.fromRgb(250, 100, 100, 150)]

    def checkRightBounadary(self, element, maxX):
        for i in range(len(element)):
            if element[i][0] > maxX - 1:
                return False
        return True

    def checkOneBlock(self, elements, X, Y):
        for j in range(len(elements)):
            for k in range(len(elements[j])):
                if elements[j][k][0] == X and elements[j][k][1] == Y:
                    return True
        return False

    def checkOneLayer(self, elements, maxX, Y):
        for i in range(maxX):
            if self.checkOneBlock(elements, i, Y) is False:
                return False
        return True

    def checkAllLayer(self, elements, maxX, maxY):
        layer = []
        for i in range(maxY):
            if self.checkOneLayer(elements, maxX, i):
                layer.append(i)
        return layer

    def deleteLayer(self, elements, number):
        for i in reversed(elements):
            for element in reversed(i):
                if element[1] == number:
                    i.remove(element)
        for i in range(len(elements)):
            for j in range(len(elements[i])):
                if elements[i][j][1] < number:
                    elements[i][j][1] += 1
        return elements

    def checkEndGame(self, element):
        for i in range(len(element)):
            if element[i][1] == 1:
                return True
        return False

    def checkLeftBounadary(self, element):
        for i in range(len(element)):
            if element[i][0] < 1:
                return False
        return True

    def checkFloor(self, element, maxY):
        for i in range(len(element)):
            if element[i][1] > maxY - 1:
                return False
        return True

    def checkTwoFigures(self, element1, element2):
        for i in range(len(element1)):
            for j in range(len(element2)):
                if element1[i][0] == element2[j][0] and element1[i][1] == element2[j][1]:
                    return False
        return True

    def checkAllFigures(self, element, allElements):
        if len(allElements) == 0:
            return True
        for i in range(len(allElements)):
            if self.checkTwoFigures(element, allElements[i]) is False:
                return False
        return True

    def move(self, element, X, Y):
        for i in range(len(element)):
                element[i][0] += X
                element[i][1] += Y
        return element

    def rotate(self, number, element, angle, maxX):
        X0 = element[self.pivot[number]][0]
        Y0 = element[self.pivot[number]][1]
        newElement = copy.deepcopy(element)
        if self.pivot[number] != -1:
            for i in range(len(element)):
                newElement[i][0] = (element[i][0] - X0) * math.cos(angle) \
                                - (element[i][1] - Y0) * math.sin(angle) + X0
                newElement[i][1] = (element[i][0] - X0) * math.sin(angle) \
                                + (element[i][1] - Y0) * math.cos(angle) + Y0
        while self.checkRightBounadary(newElement, maxX) == False:
            self.move(newElement, -1, 0)
        self.move(newElement, 1, 0)
        
        while self.checkLeftBounadary(newElement) == False:
            self.move(newElement, 1, 0)
        self.move(newElement, -1, 0)
        return newElement
