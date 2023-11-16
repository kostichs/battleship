from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QFont
from Gamer import Gamer
from Battle import BattleWindow
from Ship import Ship


class ShipGenerationWindow(QMainWindow):
    def __init__(self, name):
        super().__init__()
        self.battle_window = None
        uic.loadUi('ShipGenerationWindow.ui', self)
        self.setWindowTitle("Ship Generation")
        self.name_lbl.setText(f'Hello Admiral {name}!')
        self.up_btn.clicked.connect(self.up)
        self.down_btn.clicked.connect(self.down)
        self.left_btn.clicked.connect(self.left)
        self.right_btn.clicked.connect(self.right)
        self.rotate_btn.clicked.connect(self.rotate)
        self.apply_btn.clicked.connect(self.apply)
        self.reset_btn.clicked.connect(self.reset)
        self.random_btn.clicked.connect(self.random)
        self.confirm_btn.clicked.connect(self.confirm)

        self.bot = Gamer()
        self.bot.set_warships_random(self.bot.board, self.bot.placed_ships)

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
        self.player.display_board()
        if len(self.player.set_warships) > 0:
            self.board_txt.clear()
            self.board_txt.append(self.player.format_matrix())
        else:
            self.board_txt.clear()
            self.board_txt.append(self.player.format_matrix_without_points())
            print('There are no more ships to place.')

    def up(self):
        self.player.motion(-1, 0)
        self.update_window()

    def down(self):
        self.player.motion(1, 0)
        self.update_window()

    def left(self):
        self.player.motion(0, -1)
        self.update_window()

    def right(self):
        self.player.motion(0, 1)
        self.update_window()

    def rotate(self):
        self.player.rotate()
        self.update_window()

    def apply(self):
        if self.player.apply():
            self.player.display_player_ship()
            self.update_window()

    def reset(self):
        self.player.reset()
        self.player.display_player_ship()
        self.board_txt.setPlainText(self.player.get_board())

    def random(self):
        self.player.reset()
        self.player.random()
        self.update_window()

    def confirm(self):
        if self.player.confirm():
            self.bot.display_board()
            self.bot.format_matrix()
            print('bot0')
            print(self.bot.board)
            self.clear_bot_board_from_points()

            self.battle_window = BattleWindow(self.bot, self.player)
            self.battle_window.show()
            self.close()
        else:
            print("There are some ships to place.")

    def clear_bot_board_from_points(self):
        for row in range(len(self.bot.board)):
            for col in range(len(self.bot.board[row])):
                if self.bot.board[row][col] == '.':
                    self.bot.board[row][col] = '   '
