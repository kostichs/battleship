from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QFont, QPixmap
from Gamer import Gamer
from Ship import Ship


class ShipGenerationWindow(QMainWindow):
    def __init__(self, name):
        super().__init__()
        uic.loadUi('ShipGenerationWindow.ui', self)
        self.setWindowTitle("Ship Generation")
        self.name_lbl.setText(f'Hello {name}')
        self.player = Gamer(name)
        self.board_txt.setFont(QFont("Courier New"))
        self.player.display_player_ship()
        self.board_txt.setPlainText(self.player.get_board())

    def update_window(self) -> None:
        """
        Updates the matrix, clears a text field in the widget, and appends the updated matrix as a string
        to the text field.

        Returns:
            None
        """

        self.player.display_board(self.player.board)
        print(self.player.set_warships)
        if len(self.player.set_warships) > 0:
            self.board_txt.clear()
            self.board_txt.append(self.player.format_matrix(self.player.board))
        else:
            self.board_txt.clear()
            # self.board_txt.append(self.player.format_matrix_without_points(self.player_board))
            self.notify('There are no more ships to place.')
