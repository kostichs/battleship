import random

BOARD_SIZE = 11  # 11x11 = 100 cell + 20 cell for coordinates + 1 for empty cell 0x0.
EMPTY_CELL = '.'  # This constant string is used to fill the inside part of the board for easy navigation.
SHIP_CELL = 'o'  # Constant for displaying the ship on the board.
AROUND_CELL = '-'  # Constant for displaying cells around the placed ship.
COLLISION_CELL = '?'  # Constant for displaying that the current ship can't be placed here.
AROUND_SHIP_DIRECTIONS = (  # set of 8 directions around any cell like top, down, left, right and diagonal.
    (0, -1),  # y-1
    (-1, -1),  # x-1, y-1
    (-1, 0),  # x-1
    (-1, 1),  # x-1, y+1
    (0, 1),  # y+1
    (1, 1),  # x+1, y+1
    (1, 0),  # x+1
    (1, -1)  # x+1, y-1
)
WARSHIPS = {  # Set of n-cell-long warships as a key and with their amounts on the game board as a value.
    "4": 1,
    "3": 2,
    "2": 3,
    "1": 4,
}


class Gamer:
    """
    Class gamer has name, scores, its own board and list of ships of class Ship.
    Object Gamer can give commands to manipulate its ships on the board, like move, rotate, apply, reset etc.
    This class gives notifications for every action of its object.
    """
    def __init__(self, name='bot', size=11):
        self.name = name
        self.scores = 0
        self.is_horizontal = True
        self.board = [['.' for i in range(size)] for j in range(size)]
        self.current_coordinates_of_ship = list()
        self.set_warships = list()
        self.placed_ships = list()
        self.generate_ships()

    def generate_ships(self) -> None:
        """
        Moves the key and value from a dictionary to a matrix to realize a step-by-step placement of ships.
        """
        for warship, value in WARSHIPS.items():
            self.set_warships.append([int(warship), value])

    def get_board(self):
        self.board = self.display_board()
        return self.format_matrix()

    def command(self, order=''):
        dir_row, dir_col = 0, 0
        match order:
            case 'UP':
                dir_row = -1
            case 'DOWN':
                dir_row = 1
            case 'LEFT':
                dir_col = -1
            case 'RIGHT':
                dir_col = 1
            case 'ROTATE':
                self.rotate()
            case 'APPLY':
                self.apply()
            case 'RESET':
                self.reset()
            case _:
                pass
        pass

    def rotate(self):
        if len(self.set_warships) > 0:
            self.is_horizontal = self.rotate_ship()
            self.motion(0, 0)
        else:
            print('There are no more ships.')

    def rotate_ship(self) -> bool:
        """
        Rotate the ship from a horizontal to a vertical position or vice versa.

        The function checks the current position of the ship and, based on whether it is in a horizontal or vertical
        position, calculates new coordinates to rotate the ship. It also checks whether the new position goes beyond the
        matrix boundaries. If rotation is not possible due to going out of the matrix range, the ship's position remains
        unchanged, and no modifications occur.

        Parameters:
            horizontal (bool): The current orientation of the ship. True for horizontal, False for vertical.
            warships (list): List of ships and their quantities.
            coordinates (list): List of coordinates of the current ship.
            board (list[list[str]]): The game board represented as a list of lists.
            placed_warships (list): List of coordinates of previously placed ships.

        Returns:
            bool: The new orientation of the ship after attempting to rotate. True for horizontal, False for vertical.
        """
        ship_type = int(self.set_warships[0][0])
        print('j')
        if self.is_horizontal:  # horizontal position
            for i in range(len(self.current_coordinates_of_ship)):
                current_cell = self.current_coordinates_of_ship[i]  # reduce the length of next expressions.
                if current_cell[0] - ship_type // 2 + i < 1 \
                        or current_cell[0] - ship_type // 2 + i > len(self.board) - 1 \
                        or current_cell[1] + ship_type // 2 - i < 1 \
                        or current_cell[1] + ship_type // 2 - i > len(self.board) - 1:
                    return self.is_horizontal
            else:
                self.is_horizontal = not self.is_horizontal
                self.clear_previous_step()
                for i in range(len(self.current_coordinates_of_ship)):
                    current_cell = self.current_coordinates_of_ship[i]
                    current_cell[0] = current_cell[0] - ship_type // 2 + i
                    current_cell[1] = current_cell[1] + ship_type // 2 - i
                self.redraw_matrix()
                self.draw_current_ship()
        else:  # vertical position
            for i in range(len(self.current_coordinates_of_ship)):
                current_cell = self.current_coordinates_of_ship[i]
                if self.current_coordinates_of_ship[i][1] - ship_type // 2 + i < 1 \
                        or current_cell[1] - ship_type // 2 + i > len(self.board) - 1 \
                        or current_cell[0] + ship_type // 2 - i < 1 \
                        or current_cell[0] + ship_type // 2 - i > len(self.board) - 1:
                    return self.is_horizontal
            else:
                self.is_horizontal = True
                self.clear_previous_step()
                for i in range(len(self.current_coordinates_of_ship) - 1, -1, -1):
                    current_cell = self.current_coordinates_of_ship[i]
                    current_cell[0] = current_cell[0] + ship_type // 2 - i
                    current_cell[1] = current_cell[1] - ship_type // 2 + i
                self.redraw_matrix()
                self.draw_current_ship()
                return self.is_horizontal

    def apply(self):
        pass

    def reset(self):
        pass

    def check_board(self):
        pass

    def display_board(self) -> list[list[str]]:
        """
        Print the game board, represented as a matrix of cell states.

        Each cell's state is printed in the middle of a cell_size.
        The 'letters' string is used to fill the left edge of the board.
        Numbers are used to fill the top edge of the board.
        The cell at board[0][0] is intentionally left empty because it doesn't participate in the game.

        """
        letters = 'ABCDEFGHIJ'
        for row in range(1, len(self.board)):
            self.board[row][0] = letters[row - 1]

        for col in range(1, len(self.board)):
            self.board[0][col] = str(col)

        cell_size = 3
        flag = True
        self.board[0][0] = ' '
        for row in self.board:
            for col in row:
                if flag:
                    flag = False  # avoid changing of the cell 0x0 that has to be empty.
                print(f'{col:^{cell_size}}', end=" ")
            print()
        return self.board

    def format_matrix(self) -> str:
        """
        Transform a matrix represented as a list into a formatted string.

        Each cell's state is formatted and aligned in the middle of a cell size.
        The resulting string includes newlines for better readability.

        """
        formatted_text = ""
        for row in self.board:
            formatted_row = [f'{col:^{3}}' for col in row]
            formatted_text += " ".join(formatted_row) + "\n\n"
        return formatted_text

    def display_player_ship(self) -> None:
        """
        If the count of the ship type reaches zero, exclude that ship type from the list, and move to the next type.
        If the list of ship types is empty, initiate the final matrix cleanup before its rendering.
        If the count of the current ship type is still greater than zero, the function places the ship in the middle
        of the matrix,
        and updates the current coordinates of the new ship in the list.

        """
        if self.set_warships[0][1] <= 0:
            self.set_warships.pop(0)
            # the first location is in the middle of the board, depending on its length.
        if len(self.set_warships) > 0:

            ship_type = int(self.set_warships[0][0])
            for i in range(ship_type):
                self.board[len(self.board) // 2][len(self.board) // 2 - ship_type // 2 + i + 1] = SHIP_CELL
                self.current_coordinates_of_ship.append([len(self.board) // 2, len(self.board) // 2 - ship_type // 2 + i + 1])
                self.draw_current_ship()
            # return 'Place the ship on the board.'
            print('Place the ship on the board.')
        else:  # if there are no more ships to place on the board.
            # return 'There are no more ships to place.'
            print('There are no more ships to place.')

    def draw_current_ship(self) -> None:
        """
        Draws the current ship on the matrix based on its position, considering collisions with other ships or lack thereof.

        """
        is_collided = False
        if len(self.placed_ships) > 0:  # The first time the list of placed ships is empty

            for current_coordinate in range(len(self.current_coordinates_of_ship)):  # clear the matrix

                for w in self.placed_ships:
                    if self.current_coordinates_of_ship[current_coordinate][0] == w[0] \
                            and self.current_coordinates_of_ship[current_coordinate][1] == w[1]:
                        self.board[self.current_coordinates_of_ship[current_coordinate][0]][
                            self.current_coordinates_of_ship[current_coordinate][1]] = COLLISION_CELL
                        is_collided = True
                        break
                if not is_collided:
                    self.board[self.current_coordinates_of_ship[current_coordinate][0]][
                        self.current_coordinates_of_ship[current_coordinate][1]] = SHIP_CELL
        else:
            for current_coordinate in range(len(self.current_coordinates_of_ship)):  # place a ship on the matrix.
                self.board[self.current_coordinates_of_ship[current_coordinate][0]][
                    self.current_coordinates_of_ship[current_coordinate][1]] = SHIP_CELL

    def motion(self, row, col) -> None:
        """
        Move the ship based on user input for row and column directions.

        Check whether the ship will stay within the boundaries of the matrix after the move.
        If the ship is beyond the matrix edges, the motion won't be confirmed,
        and the ship remains in its current position.

        :param row: The row direction for the ship's motion.
        :param col: The column direction for the ship's motion.
        :param coordinates: The current coordinates of the ship.
        :param board: The game board represented as a list of lists.
        :param warships: List of coordinates of previously placed ships.
        :return: None
        """
        if len(self.set_warships) > 0:
            # Moving the ship depending on the input of user with checking the valid coordinates.
            for i in range(len(self.current_coordinates_of_ship)):
                if self.current_coordinates_of_ship[i][0] + row < 1 \
                        or self.current_coordinates_of_ship[i][0] + row > len(self.board) - 1 \
                        or self.current_coordinates_of_ship[i][1] + col < 1 \
                        or self.current_coordinates_of_ship[i][1] + col > len(self.board) - 1:
                    break
            else:
                self.clear_previous_step()
                for i in range(len(self.current_coordinates_of_ship)):  # move the ship
                    self.board[self.current_coordinates_of_ship[i][0] + row][
                        self.current_coordinates_of_ship[i][1] + col] = SHIP_CELL
                    self.current_coordinates_of_ship[i][0] = self.current_coordinates_of_ship[i][0] + row
                    self.current_coordinates_of_ship[i][1] = self.current_coordinates_of_ship[i][1] + col
                self.redraw_matrix()
                self.draw_current_ship()
        else:
            print('There are no more ships to place')

    def clear_previous_step(self) -> None:
        """
        Clear the symbols on the previous cell in the matrix after changing the position of the ship.

        This function updates the game board matrix by setting the cells specified by the given coordinates
        to the default empty cell value.

        :param board: The game board represented as a list of lists.
        :param coordinates: List of coordinates to clear on the game board.
        :return: None
        """
        for coord in range(len(self.current_coordinates_of_ship)):  # clear the symbols on the previous cell in matrix.
            self.board[self.current_coordinates_of_ship[coord][0]][self.current_coordinates_of_ship[coord][1]] = EMPTY_CELL

    def redraw_matrix(self) -> None:
        """
        Redraws the player's game board, updating the positions of previously placed ships.

        This function draws the ship based on its coordinates provided as a list-type,
        along with the safe-zone represented by the neighboring coordinates.

        :param board: The game board represented as a list of lists.
        :param warships: List of coordinates of previously placed ships.
        :return: None
        """
        for ship in self.placed_ships:
            if type(ship) == list:
                self.board[ship[0]][ship[1]] = SHIP_CELL
            else:
                self.board[ship[0]][ship[1]] = ''
