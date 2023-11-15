import sys
from PyQt5.QtWidgets import QApplication
from StartWindow import StartWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.exit((app.exec()))
