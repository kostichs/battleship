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
    def __init__(self, name='Admiral', size=11):
        self.size = size
        self.name = name
        self.scores = 0
        self.is_horizontal = True
        self.board = [['.' for i in range(self.size)] for j in range(self.size)]
        self.current_coordinates_of_ship = list()
        self.set_warships = list()
        self.placed_ships = list()
        self.generate_ships()

    def get_ship_cell(self):
        return SHIP_CELL  # Constant for displaying the ship on the board.

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
        """
                Confirm the current coordinates of the ship as the final position.

                After confirmation, all lists related to the current ship will be cleared.
                If all ships are already placed, this function will be ignored.

                :return: None
                """
        if len(self.set_warships) > 0:
            if self.apply_placement():
                # every ship has list of its own coordinates and set of cells around it.
                self.placed_ships.append(list(self.current_coordinates_of_ship))
                print(self.placed_ships)
                self.redraw_matrix()
                self.current_coordinates_of_ship.clear()
                # after this type of ship was placed, its amount is reduced.
                self.set_warships[0][1] -= 1
                # self.update_player_window()
                # self.display_player_ship()
                # self.notify(sg.display_player_ship(self.set_warships, self.player_board,
                #                                    self.current_coordinates_of_ship, self.placed_warships))
                self.is_horizontal = True
                return True
            else:
                print('Choose another place.')
                return False
        else:
            print('There are no more ships.')
            return False

    def apply_placement(self) -> bool:
        """
        Checks if the current coordinates of the ship don't conflict with coordinates of other ships.

        If these coordinates are suitable, the cells around the new ship will be marked as empty for a safe zone.

        Returns:
            bool: True if placement is successful, False if there is a conflict with other ships.
        """
        # check whether teh current ship isn't near another one.
        for coordinate in self.current_coordinates_of_ship:
            if self.board[coordinate[0]][coordinate[1]] == COLLISION_CELL:
                return False
        else:
            empty_cells = set()  # set of unrepeatable cells around the ship.
            for c in range(len(self.current_coordinates_of_ship)):
                # make a tuple of coordinates for circling the ship.
                for i in AROUND_SHIP_DIRECTIONS:
                    row, col = self.current_coordinates_of_ship[c][0], self.current_coordinates_of_ship[c][1]
                    if 0 < row + i[0] < len(self.board) \
                            and 0 < col + i[1] < len(self.board) \
                            and self.board[row + i[0]][col + i[1]] != SHIP_CELL:
                        empty_cells.add((row + i[0], col + i[1]))
            self.current_coordinates_of_ship += empty_cells
            return True

    def reset(self):
        """
                Clear the list of already placed warships, the list of ship types and their amounts,
                the list of current coordinates for the current ship, and finally, the player ship matrix.
                The position variable is switched to horizontal.
                Then it calls the function to begin generating from start.

                Returns:
                    None
                """
        self.placed_ships.clear()
        self.set_warships.clear()
        self.board = [['.' for i in range(self.size)] for j in range(self.size)]
        self.current_coordinates_of_ship.clear()
        self.is_horizontal = True
        self.generate_ships()

    def confirm(self) -> bool:
        if len(self.set_warships) == 0:
            return True
        return False

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

    def format_matrix_without_points(self):
        """
        Transform a matrix represented as a list into a formatted string.

        '.' characters in the matrix will be replaced with spaces (' ') to create a clear battlefield.
        Each cell's state is formatted and aligned in the middle of a cell size.
        The resulting string includes newlines for better readability.

        :param matrix: The game board represented as a list of lists.
        :return: A formatted string representation of the matrix.
        """
        formatted_text = ""
        for row in self.board:
            formatted_row = [f'{col:^{3}}' if col != '.' else '   ' for col in row]
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
            for current_coordinate in range(len(self.current_coordinates_of_ship)):
                for ship in self.placed_ships:
                    print('C', current_coordinate)
                    print('S', self.placed_ships)
                    for w in ship:
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

        :return: None
        """
        for coord in range(len(self.current_coordinates_of_ship)):  # clear the symbols on the previous cell in matrix.
            self.board[self.current_coordinates_of_ship[coord][0]][self.current_coordinates_of_ship[coord][1]] = EMPTY_CELL

    def redraw_matrix(self) -> None:
        """
        Redraws the player's game board, updating the positions of previously placed ships.

        This function draws the ship based on its coordinates provided as a list-type,
        along with the safe-zone represented by the neighboring coordinates.

        :return: None
        """
        for p_ship in self.placed_ships:
            for ship in p_ship:
                if type(ship) == list:
                    self.board[ship[0]][ship[1]] = SHIP_CELL
                else:
                    self.board[ship[0]][ship[1]] = ''

    def random(self):
         self.board = self.set_warships_random(self.board, self.placed_ships)

    def set_warships_random(self, matrix: list[list[str]], placed_ships: list) -> list[list[str]]:
        """
            Randomly places warships on the game board matrix.

            Each warship is represented by a specific character (SHIP_CELL) in the matrix,
            and empty cells around the ship are set to ' ' to avoid collision with other ships.

            Parameters:
                matrix (list[list[str]]): The game board represented as a matrix of cell states.
                ships (dict[str, int]): Dictionary of n-cell-long warships as keys with their amounts as values.

            Returns:
                list[list[str]]: The updated game board matrix with randomly placed warships.
            """
        ships: dict[str, int] = WARSHIPS
        def find_empty_cells(coordinates: ()) -> bool:
            """Check if chosen cells are empty to locate a ship on the board."""
            for coordinate in coordinates:  # check if chosen cells are empty to locate a ship on the board.
                if matrix[coordinate[0]][coordinate[1]] != EMPTY_CELL:
                    return False
            else:
                return True

        def is_empty(cell: str) -> bool:
            """This function is part of the calculation for neighboring cells to avoid redundant computations."""
            return cell != SHIP_CELL

        def give_random_coordinates() -> list[tuple]:
            """
                    Generate random coordinates for placing a ship on the game board matrix.

                    The function selects a random coordinate within the range of the matrix length minus the ship length
                    to avoid going beyond the matrix boundaries. It also randomly chooses between vertical and horizontal
                    positions for the ship.

                    The selected coordinates are checked to ensure they are free and not too close to other ships. If any of
                    the coordinates does not meet the check conditions, the randomization process restarts.
                    If the coordinates
                    pass the checks, they are added to the ship's coordinate list.

                    Parameters:
                        matrix (list[list[str]]): The game board represented as a matrix of cell states.
                        ship (str): The size of the ship for which random coordinates are generated.

                    Returns:
                        list[tuple]: A list of tuples representing the generated random coordinates for placing the ship.

                    Raises:
                        ValueError: If the size of the ship is not a positive integer.

                    Example:
                        >>> give_random_coordinates(matrix, "3")
                        [(2, 3), (3, 3), (4, 3)]
                """
            vertical_position, horizontal_position = 0, 1
            rand_position = random.randint(vertical_position, horizontal_position)
            rand_row = random.randint(1, len(matrix) - int(ship))
            if rand_position == vertical_position:
                rand_row = random.randint(1, len(matrix) - int(ship))
                coordinates = [(rand_row + i, rand_row) for i in range(int(ship))]
            else:
                rand_col = random.randint(1, len(matrix[0]) - int(ship))
                coordinates = [(rand_row, rand_col + i) for i in range(int(ship))]
            return coordinates

        for ship, value in ships.items():  # every ship from warships dictionary
            for _ in range(value):  # value = amount of the ships (1, 2, 3, 4)
                while True:
                    ship_coordinates = give_random_coordinates()
                    if find_empty_cells(ship_coordinates):
                        for x in range(len(ship_coordinates)):
                            matrix[ship_coordinates[x][0]][ship_coordinates[x][1]] = SHIP_CELL

                        # warship is placed. Now we need to set empty cells around the ship to avoid collision with
                        # other ships.
                        for c in range(len(ship_coordinates)):
                            '''
                            make a tuple of coordinates for circling the ship.
                            make a unique condition for every single cell around the ship.
                            '''
                            for i in AROUND_SHIP_DIRECTIONS:
                                if 0 < ship_coordinates[c][0] + i[0] < len(matrix) \
                                        and 0 < ship_coordinates[c][1] + i[1] < len(matrix) \
                                        and is_empty(
                                    matrix[ship_coordinates[c][0] + i[0]][ship_coordinates[c][1] + i[1]]):
                                    matrix[ship_coordinates[c][0] + i[0]][ship_coordinates[c][1] + i[1]] = ' '
                                else:
                                    continue
                        placed_ships.append(ship_coordinates)
                        break
                    else:
                        continue
        self.set_warships.clear()
        return matrix