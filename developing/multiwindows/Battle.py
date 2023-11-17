from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from Gamer import Gamer
import random

HIT_SIGN = 'X'  # sign when ship is damaged
MISS_SIGN = '*'  # sign when player missed


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
        self.name_txt.setText(f'Admiral {self.player.name}')
        # self.player_shots = list()
        # self.bot_shots = list()
        # print('Player: ', self.player.placed_ships)
        # print('Bot: ', self.bot.placed_ships)

        self.active_player = self.player

        self.draw_player_board()
        self.update_bot_window()
        self.notify(f'Admiral {self.active_player.name} is shooting...')

    def draw_player_board(self):
        formatted_text = ""
        for row in self.active_player.board:
            formatted_row = [f'{col:^{3}}' if col != '.' else '   ' for col in row]
            formatted_text += " ".join(formatted_row) + "\n\n"
        self.player_txt.clear()
        self.player_txt.append(formatted_text)

    def update_player_window(self):
        formatted_text = ""
        for row in self.player.board:
            formatted_row = [f'{col:^{3}}' if col != '.' else '   ' for col in row]
            formatted_text += " ".join(formatted_row) + "\n\n"
        self.player_txt.clear()
        self.player_txt.append(formatted_text)

    def update_bot_window(self):
        formatted_text = ""
        for row in self.bot.board:
            formatted_row = [f'{col:^{3}}' if col != 'o' else '   ' for col in row]
            formatted_text += " ".join(formatted_row) + "\n\n"
        self.bot_txt.clear()
        self.bot_txt.append(formatted_text)

    def change_player(self):
        if self.active_player == self.player:
            self.active_player = self.bot
        else:
            self.active_player = self.player
        self.notify(f' Admiral {self.active_player.name} is shooting...')

    def make_shoot(self):
        if self.active_player == self.player:
            if self.row_line.text() != '' and self.col_line.text() != '':
                row = int(self.row_line.text())
                col = int(self.col_line.text())
                if self.bot.board[row][col] == self.bot.get_ship_cell():
                    self.bot.board[row][col] = HIT_SIGN
                    self.notify('HIT')
                    self.player.scores += 1
                    self.scores_player_lbl.setText(f'Scores: {self.player.scores}')
                    for ship in self.bot.placed_ships:
                        print(ship)
                        for coordinate in ship:
                            if type(coordinate) == list:
                                if [row, col] in ship:
                                    print('true')
                                    flag = True
                                    for s in ship:
                                        if type(s) == list:
                                            print(self.bot.board[s[0]][s[1]])
                                            if self.bot.board[s[0]][s[1]] != HIT_SIGN:
                                                flag = False
                                                break
                                            else:
                                                continue
                                    if flag:
                                        print("Ship is drown")
                                        for empty in ship:
                                            if type(empty) == tuple:
                                                print(self.player.board)
                                                self.bot.board[empty[0]][empty[1]] = '.'
                                                pass
                                else:
                                    print('false')
                else:
                    self.bot.board[row][col] = MISS_SIGN
                    print('MISS')

                self.update_bot_window()
                self.change_player()
                self.make_shoot()
        else:
            self.random_shoot()
            self.change_player()

    def random_shoot(self):
        if self.active_player == self.bot:
            while True:
                random_row = random.randint(1, len(self.active_player.board) - 1)
                random_col = random.randint(1, len(self.active_player.board) - 1)
                if self.player.board[random_row][random_col] == MISS_SIGN \
                        or self.player.board[random_row][random_col] == HIT_SIGN:
                    continue
                else:
                    row = random_row
                    col = random_col

                    if self.player.board[row][col] == self.player.get_ship_cell():
                        self.player.board[row][col] = HIT_SIGN
                        self.bot.scores += 1
                        self.scores_bot_lbl.setText(f'Scores: {self.bot.scores}')
                        print('HIT')
                    else:
                        self.player.board[row][col] = MISS_SIGN
                        print('MISS')
                    break
            self.update_player_window()

    def notify(self, message: str):
        self.message_lbl.setText(message)
