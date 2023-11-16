from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QPixmap
from Gamer import Gamer


HIT_SIGN = 'X'  # sign when ship is damaged
MISS_SIGN = '@'

class BattleWindow(QMainWindow):
    def __init__(self, bot: Gamer, player: Gamer):
        super().__init__()
        uic.loadUi('Battle.ui', self)
        self.setMinimumSize(QSize(320, 140))
        self.setWindowTitle("Battleship")
        self.player_txt.setFont(QFont("Courier New"))
        self.bot_txt.setFont(QFont("Courier New"))
        self.shoot_btn.clicked.connect(self.make_shoot)

        self.bot = bot
        self.player = player
        self.name_txt.setText(f'{self.player.name}')

        self.active_player = self.player

        self.draw_player_board()

        self.notify(f'{self.active_player.name} is shooting...')

    def draw_player_board(self):
        formatted_text = ""
        for row in self.active_player.board:
            formatted_row = [f'{col:^{3}}' if col != '.' else '   ' for col in row]
            formatted_text += " ".join(formatted_row) + "\n\n"
        self.player_txt.clear()
        self.player_txt.append(formatted_text)

    def update_player_window(self):

        pass

    def change_player(self):
        if self.active_player == self.player:
            self.active_player = self.bot
        else:
            self.active_player = self.player
        self.notify(f'{self.active_player.name} is shooting...')

    def make_shoot(self):
        if self.active_player == self.player:
            if self.row_line.text() != '' and self.col_line.text() != '':
                row = int(self.row_line.text())
                col = int(self.col_line.text())
                if self.bot.board[row][col] == self.bot.get_ship_cell():
                    self.bot.board[row][col] = HIT_SIGN
                    print('HIT')
                else:
                    self.bot.board[row][col] = MISS_SIGN
                    print('MISS')

                self.update_bot_window()
                pass
        else:
            print('turn of bot')
            pass

        self.change_player()

    def update_bot_window(self):
        formatted_text = ""
        for row in self.bot.board:
            formatted_row = [f'{col:^{3}}' if col != 'o' else '   ' for col in row]
            formatted_text += " ".join(formatted_row) + "\n\n"
        self.bot_txt.clear()
        self.bot_txt.append(formatted_text)

    def notify(self, message: str):
        self.message_lbl.setText(message)

