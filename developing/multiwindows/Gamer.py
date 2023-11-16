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
        print(self.set_warships)

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

    def move(self):
        pass

    def rotate(self):
        pass

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
        if len(self.set_warships) > 0:  # The first time the list of placed ships is empty

            for current_coordinate in range(len(self.current_coordinates_of_ship)):  # clear the matrix

                for w in self.set_warships:
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
