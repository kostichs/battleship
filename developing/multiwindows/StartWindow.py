import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize
from ShipGenerationWindow import ShipGenerationWindow


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.second_window = None
        uic.loadUi('mainWindow.ui', self)
        self.setMinimumSize(QSize(320, 140))
        self.setWindowTitle("Battleship")
        self.start_btn.clicked.connect(self.ship_generation)

    def ship_generation(self):
        name = self.name_line.text()
        self.second_window = ShipGenerationWindow(name)
        self.second_window.show()
        self.close()
