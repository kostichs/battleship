
import sys
import ship_generation as sg
from PyQt5 import uic
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ship_generating_form.ui', self)
        self.logo_lbl.setPixmap(QPixmap('logo3.png'))
        self.random_btn.clicked.connect(self.update_bot_window)
        self.apply_btn.clicked.connect(self.apply)
        self.up_btn.clicked.connect(self.up)
        self.down_btn.clicked.connect(self.down)
        self.left_btn.clicked.connect(self.left)
        self.right_btn.clicked.connect(self.right)
        self.rotate_btn.clicked.connect(self.rotate)
        self.reset_btn.clicked.connect(self.reset)

        # List of coordinates for the already placed ships.
        # It includes a list of its own coordinates and tuples of the neighboring cells around the ship.
        self.placed_warships = list()

        self.set_warships = list()  # List to store the remaining ship types and their quantities.

        self.bot_board = list()  # List representing the game board for the computer opponent.

        self.player_board = list()  # List representing the game board for the player.

        self.current_coordinates_of_ship = list()  # List to store the current coordinates of the player's ship.

        self.is_horizontal = True  # Boolean flag indicating the orientation of the current ship(horizontal by default).
        # Set a fixed-width font for QTextEdit
        font = QFont("Courier New")
        self.bot_window.setFont(font)
        self.player_window.setFont(font)

        self.start_player()

    def update_bot_window(self) -> None:
        """
        Updates the display for the bot game board.

        This function creates a new list and generates random placements of ships. The generated matrix is displayed
        on the console and in the text field of the widget.

        Returns:
            None
        """
        self.bot_board = sg.create_board()
        self.bot_board = sg.set_warships_random(self.bot_board, sg.WARSHIPS)
        self.bot_window.clear()
        sg.display_board(self.bot_board)
        self.bot_window.append(sg.format_matrix_without_points(self.bot_board))

    def up(self) -> None:
        """
        Move the current ship upward on the player's game board.

        This method checks if there are ships left to place on the board and updates the player window accordingly.
        If there are no more ships, the user is notified with a relevant message.

        Returns:
            None
        """
        if len(self.set_warships) > 0:
            sg.motion(-1, 0, self.current_coordinates_of_ship, self.player_board, self.placed_warships)
            self.update_player_window()
        else:
            self.notify('There are no more ships.')

    def down(self) -> None:
        """
        Move the current ship downward on the player's game board.

        This method checks if there are ships left to place on the board and updates the player window accordingly.
        If there are no more ships, the user is notified with a relevant message.

        Returns:
            None
        """
        if len(self.set_warships) > 0:
            sg.motion(1, 0, self.current_coordinates_of_ship, self.player_board, self.placed_warships)
            self.update_player_window()
        else:
            self.notify('There are no more ships.')

    def left(self) -> None:
        """
        Move the current ship to the left side on the player's game board.

        This method checks if there are ships left to place on the board and updates the player window accordingly.
        If there are no more ships, the user is notified with a relevant message.

        Returns:
            None
        """
        if len(self.set_warships) > 0:
            sg.motion(0, -1, self.current_coordinates_of_ship, self.player_board, self.placed_warships)
            self.update_player_window()
        else:
            self.notify('There are no more ships.')

    def right(self) -> None:
        """
        Move the current ship to the right side on the player's game board.

        This method checks if there are ships left to place on the board and updates the player window accordingly.
        If there are no more ships, the user is notified with a relevant message.

        Returns:
            None
        """
        if len(self.set_warships) > 0:
            sg.motion(0, 1, self.current_coordinates_of_ship, self.player_board, self.placed_warships)
            self.update_player_window()
        else:
            self.notify('There are no more ships.')

    def rotate(self) -> None:
        """
        Rotate the current ship depending on its current position on the player's game board.

        This method checks if there are ships left to place on the board and updates the player window accordingly.
        If there are no more ships, the user is notified with a relevant message.

        Returns:
            None
    """
        if len(self.set_warships) > 0:
            self.is_horizontal = sg.rotate_ship(self.is_horizontal, self.set_warships,
                                                self.current_coordinates_of_ship, self.player_board,
                                                self.placed_warships)
            sg.motion(0, 0, self.current_coordinates_of_ship, self.player_board, self.placed_warships)
            self.update_player_window()
        else:
            self.notify('There are no more ships.')

    def apply(self) -> None:
        """
        Confirm the current coordinates of the ship as the final position.

        After confirmation, all lists related to the current ship will be cleared.
        If all ships are already placed, this function will be ignored.

        :return: None
        """
        if len(self.set_warships) > 0:
            if sg.apply_placement(self.player_board, self.current_coordinates_of_ship):
                # every ship has list of its own coordinates and set of cells around it.
                self.placed_warships.append(list(self.current_coordinates_of_ship))
                # self.redraw_matrix(self.placed_warships)
                sg.redraw_matrix(self.player_board, self.placed_warships)
                self.current_coordinates_of_ship.clear()
                # after this type of ship was placed, its amount is reduced.
                self.set_warships[0][1] -= 1
                self.update_player_window()
                # self.display_player_ship()
                self.notify(sg.display_player_ship(self.set_warships, self.player_board,
                            self.current_coordinates_of_ship, self.placed_warships))
                self.update_player_window()
                self.is_horizontal = True
            else:
                self.notify('Choose another place.')
                return
        else:
            self.notify('There are no more ships.')

    def reset(self) -> None:
        """
        Clear the list of already placed warships, the list of ship types and their amounts,
        the list of current coordinates for the current ship, and finally, the player ship matrix.
        The position variable is switched to horizontal.
        Then it calls the function to begin generating from start.

        Returns:
            None
        """
        self.placed_warships.clear()
        self.set_warships.clear()
        self.player_board.clear()
        self.current_coordinates_of_ship.clear()
        self.is_horizontal = True
        self.start_player()

    def start_player(self) -> None:
        """

        :return:
        """
        self.notify('Place your fleet on the board.')
        self.player_board = sg.create_board()
        self.set_warships = sg.generate_warships_list(self.set_warships)  # fill the list with warships.
        self.notify(sg.display_player_ship(self.set_warships, self.player_board, self.current_coordinates_of_ship,
                                           self.placed_warships))
        self.update_player_window()

    def update_player_window(self) -> None:
        """
        Updates the matrix, clears a text field in the widget, and appends the updated matrix as a string
        to the text field.

        Returns:
            None
        """
        sg.display_board(self.player_board)
        if len(self.set_warships) > 0:
            self.player_window.clear()
            self.player_window.append(sg.format_matrix(self.player_board))
        else:
            self.player_window.clear()
            self.player_window.append(sg.format_matrix_without_points(self.player_board))
            self.notify('There are no more ships to place.')

    def notify(self, text: str) -> None:
        """
        Takes a string to place it into the label as notification text.

        Parameters:
            text (str): The text to display as a notification.

        Returns:
            None
        """
        self.notify_lbl.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
