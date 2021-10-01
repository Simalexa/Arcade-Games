from PyQt5 import QtCore, QtGui, QtWidgets
from snakeGame import snakeGame
from tetrisGame import tetrisGame
from jumpGame import jumpGame

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setUp(self)
        self.ui.snake.clicked.connect(self.startSnakeGame)
        self.ui.tetris.clicked.connect(self.startTetrisGame)
        self.ui.jump.clicked.connect(self.startColorFrontGame)

    def startSnakeGame(self):
        self.game = snakeGame(self)
        self.game.closed.connect(self.show)
        self.hide()
        self.game.show()

    def startTetrisGame(self):
        self.game = tetrisGame(self)
        self.game.closed.connect(self.show)
        self.hide()
        self.game.show()

    def startColorFrontGame(self):
        self.game = jumpGame(self)
        self.game.closed.connect(self.show)
        self.hide()
        self.game.show()

    def resizeEvent(self, event):
        w = self.size().width()
        h = self.size().height()
        self.ui.snake.setGeometry(QtCore.QRect(w/10, 10, w * 0.8, 50))
        self.ui.tetris.setGeometry(QtCore.QRect(w/10, 70, w * 0.8, 50))
        self.ui.jump.setGeometry(QtCore.QRect(w/10, 130, w * 0.8, 50))

class Ui_MainWindow(object):
    width = 200
    height = 400

    def setUp(self, MainWindow):
        MainWindow.setWindowTitle("Mini Games")
        MainWindow.setGeometry(400, 400, self.width, self.height)
        MainWindow.setMinimumWidth(200)
        MainWindow.setMinimumHeight(200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.snake = QtWidgets.QPushButton(self.centralwidget)
        self.snake.setGeometry(QtCore.QRect(self.width/5, 10, self.width/2, 50))
        self.snake.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black; font-size: 30px; '
                                 'font-family: Helvetica;}')
        self.snake.setText("Snake")

        self.tetris = QtWidgets.QPushButton(self.centralwidget)
        self.tetris.setGeometry(QtCore.QRect(self.width/5, 70, self.width/2, 50))
        self.tetris.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black; font-size: 30px; '
                                 'font-family: Helvetica;}')
        self.tetris.setText("Tetris")

        self.jump = QtWidgets.QPushButton(self.centralwidget)
        self.jump.setGeometry(QtCore.QRect(self.width/5, 130, self.width / 3, 50))
        self.jump.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black; font-size: 30px; '
                                 'font-family: Helvetica;}')
        self.jump.setText("Color Front")


