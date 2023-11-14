# Homework: NAVY BATTLE

# Kostichev Sergey
# Start date: 09.11.2023
# End date: 11.11.2023

import random
import sys

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


def start() -> None:
    """
    Initialize and start the battleship game.

    This function sets up the game boards for both the player and the bot,
    randomly places warships on the bot's board, and allows the player to place their warships.
    The game boards are then displayed to start the game.

    Returns:
        None
    """
    board_size = 11  # 11x11 = 100 cell + 20 cell for coordinates + 1 for empty cell 0x0.
    warships = {  # Set of n-cell-long warships as a key and with their amounts on the game board as a value.
        "4": 1,
        "3": 2,
        "2": 3,
        "1": 4,
    }

    board_bot = [[EMPTY_CELL for _ in range(board_size)] for _ in range(board_size)]
    board_bot = set_warships_random(board_bot, warships)
    display_board(board_bot)

    board_player = [[EMPTY_CELL for _ in range(board_size)] for _ in range(board_size)]
    board_player = set_player_warships(board_player, warships)

    return


def display_board(matrix: list[list[str]]) -> None:
    """
    Print the game board, represented as a matrix of cell states.

    Each cell's state is printed in the middle of a cell_size.
    The 'letters' string is used to fill the right edge of the board.
    The cell at board[0][0] is intentionally left empty because it doesn't participate in the game.

    Parameters:
        matrix (list[list[str]]): A list of lists representing the current state of the game board.

    Returns:
        None
    """
    letters = 'ABCDEFGHIJ'
    for row in range(1, len(matrix)):
        matrix[row][0] = letters[row - 1]

    for col in range(1, len(matrix)):
        matrix[0][col] = str(col)

    cell_size = 3
    flag = True  # avoids changing of the cell 0x0 that has to be empty.
    matrix[0][0] = ' '
    for row in matrix:
        for col in row:
            if flag:
                flag = False
            print(f'{col:^{cell_size}}', end=" ")
        print()


def set_warships_random(matrix: list[list[str]], ships: dict[str, int]) -> list[list[str]]:
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
        the coordinates does not meet the check conditions, the randomization process restarts. If the coordinates
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
        position = (0, 1)
        rand_position = random.randint(*position)
        rand_row = random.randint(1, len(matrix) - int(ship))
        if rand_position == position[0]:  # vertical
            rand_row = random.randint(1, len(matrix) - int(ship))
            coordinates = [(rand_row + i, rand_row) for i in range(int(ship))]
        else:  # horizontal
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
                        # Write a tuple of coordinates around the current ship.
                        # Put a unique symbol for every single cell around the ship.
                        for i in AROUND_SHIP_DIRECTIONS:
                            if 0 < ship_coordinates[c][0] + i[0] < len(matrix) \
                                    and 0 < ship_coordinates[c][1] + i[1] < len(matrix) \
                                    and is_empty(matrix[ship_coordinates[c][0] + i[0]][ship_coordinates[c][1] + i[1]]):
                                matrix[ship_coordinates[c][0] + i[0]][ship_coordinates[c][1] + i[1]] = ' '
                            else:
                                continue
                    break
                else:
                    continue

    return matrix


def set_player_warships(matrix: list[list[str]], ships: dict[str, int]) -> list[list[str]]:
    """
    Place player's warships on the game board matrix.

    The function allows the player to interactively place their warships using input-method. It provides
    the ability to move WASD, rotate Q or E, and apply the placement of each ship X, while ensuring valid positions
    and avoiding collisions with other ships.

    Parameters:
        matrix (list[list[str]]): The game board represented as a matrix of cell states.
        ships (dict[str, int]): Dictionary of n-cell-long warships as keys with their amounts as values.

    Returns:
        list[list[str]]: The updated game board matrix with player-placed warships.
    """

    def clear_previous_step(coordinates: list[list]) -> None:
        """Clear the symbols on the previous coordinates of a ship in matrix"""
        for coord in range(len(coordinates)):
            matrix[coordinates[coord][0]][coordinates[coord][1]] = EMPTY_CELL

    def draw_current_ship(warships: list[list[list[int]]], current_coordinates: list[list[int]]) -> None:
        """
        Redraw the matrix considering the coordinates of already placed ships and the current ship.

        The function updates the game board matrix by redrawing the coordinates of both already placed ships and
        the current ship. Depending on the state, the cell of the current ship may be drawn as a ship or as
        a question mark if it intersects with the coordinates of already placed ships.

        Parameters:
            warships (list[list[list[int]]]): List of coordinates of already placed ships on the game board.
            current_coordinates (list[list[int]]): List of coordinates of the current ship.

        Returns:
            None
        """
        is_collided = False
        # First, the list of placed ships is empty.
        if len(warships) > 0:
            """Compares every coordinate of current ship with every coordinate of every single placed ship
            to ensure there are no collisions."""
            for current_coordinate in range(len(current_coordinates)):
                for war in warships:
                    for w in war:
                        if current_coordinates[current_coordinate][0] == w[0] \
                                and current_coordinates[current_coordinate][1] == w[1]:
                            matrix[current_coordinates[current_coordinate][0]][
                                current_coordinates[current_coordinate][1]] = COLLISION_CELL
                            is_collided = True
                            break
                if not is_collided:
                    matrix[current_coordinates[current_coordinate][0]][
                        current_coordinates[current_coordinate][1]] = SHIP_CELL
        else:
            for current_coordinate in range(len(current_coordinates)):  # place a ship on the matrix.
                matrix[current_coordinates[current_coordinate][0]][
                    current_coordinates[current_coordinate][1]] = SHIP_CELL

    def redraw_matrix(warships: list[list[list[int]]]) -> None:
        """
        Redraws all previously placed ships before drawing a new ship.

        Parameters:
            warships (list[list[list[int]]]): List of coordinates of already placed ships on the game board.

        Returns:
            None
        """
        for warship in warships:
            for w in warship:
                if type(w) == list:
                    matrix[w[0]][w[1]] = SHIP_CELL
                else:
                    matrix[w[0]][w[1]] = ''

    def rotate_ship(horizontal: bool) -> bool:
        """
        Rotate the ship either from a horizontal to a vertical position or vice versa.

        The function checks the current position of the ship, and depending on whether it is in a horizontal or vertical
        position, calculates new coordinates to rotate the ship. It also checks whether the new position goes beyond the
        matrix boundaries. If rotation is not possible due to going out of the matrix range, the ship's position remains
        unchanged, and no modifications occur.

        Parameters:
            horizontal (bool): The current orientation of the ship. True for horizontal, False for vertical.

        Returns:
            bool: The new orientation of the ship after attempting to rotate. True for horizontal, False for vertical.
        """
        _horizontal = horizontal
        if _horizontal:  # horizontal position
            for i in range(len(current_coordinates_of_ship)):
                current_cell = current_coordinates_of_ship[i]  # reduce the length of next expressions.
                if current_cell[0] - int(ship) // 2 + i < 1 \
                        or current_cell[0] - int(ship) // 2 + i > len(matrix) - 1 \
                        or current_cell[1] + int(ship) // 2 - i < 1 \
                        or current_cell[1] + int(ship) // 2 - i > len(matrix) - 1:
                    break
            else:
                _horizontal = not _horizontal
                clear_previous_step(current_coordinates_of_ship)
                for i in range(len(current_coordinates_of_ship)):
                    current_cell = current_coordinates_of_ship[i]
                    current_cell[0] = current_cell[0] - int(ship) // 2 + i
                    current_cell[1] = current_cell[1] + int(ship) // 2 - i
                redraw_matrix(placed_warships)
                draw_current_ship(placed_warships, current_coordinates_of_ship)
        else:  # vertical position
            for i in range(len(current_coordinates_of_ship)):
                current_cell = current_coordinates_of_ship[i]
                if current_coordinates_of_ship[i][1] - int(ship) // 2 + i < 1 \
                        or current_cell[1] - int(ship) // 2 + i > len(matrix) - 1 \
                        or current_cell[0] + int(ship) // 2 - i < 1 \
                        or current_cell[0] + int(ship) // 2 - i > len(matrix) - 1:
                    break
            else:
                _horizontal = True
                clear_previous_step(current_coordinates_of_ship)
                for i in range(len(current_coordinates_of_ship) - 1, -1, -1):
                    current_cell = current_coordinates_of_ship[i]
                    current_cell[0] = current_cell[0] + int(ship) // 2 - i
                    current_cell[1] = current_cell[1] - int(ship) // 2 + i
                redraw_matrix(placed_warships)
                draw_current_ship(placed_warships, current_coordinates_of_ship)
        return _horizontal

    # Start function
    placed_warships = list()  # list of located ships on the board.
    for ship, amount in ships.items():  # every ship from warships dictionary.
        for _ in range(amount):  # value = amount of the ships (1, 2, 3, 4).
            current_coordinates_of_ship = list()  # list of coordinates of the current ship.
            is_horizontal = True  # Switcher for rotation statement. Horizontal position is by default.
            for i in range(int(ship)):  # the first location is in the middle of the board, depending on its length.
                matrix[len(matrix) // 2][len(matrix) // 2 - int(ship) // 2 + i + 1] = SHIP_CELL
                current_coordinates_of_ship.append([len(matrix) // 2, len(matrix) // 2 - int(ship) // 2 + i + 1])
                draw_current_ship(placed_warships, current_coordinates_of_ship)

            while True:  # Loop with the same ship until it is placed onto the valid cells.
                display_board(matrix)
                # update the previous ships on the board that was cleared by current ship.
                redraw_matrix(placed_warships)
                # draw current ship above all previously placed ships.
                draw_current_ship(placed_warships, current_coordinates_of_ship)
                direction_row, direction_col = 0, 0  # direction variables

                direction = input('Move: W A S D, Rotate: Q or E , Apply: X, Exit: 0 ').upper()  # User's control
                match direction:
                    case 'W':  # up
                        direction_row = -1
                    case 'S':  # down
                        direction_row = 1
                    case 'A':  # left
                        direction_col = -1
                    case 'D':  # right
                        direction_col = 1
                    case 'Q' | 'E':  # rotation
                        # check whether the rotation is safe because of the edge of matrix and rotate it.
                        is_horizontal = rotate_ship(is_horizontal)
                    case 'X':  # apply
                        # check whether teh current ship isn't near another one.
                        for coordinate in current_coordinates_of_ship:
                            if matrix[coordinate[0]][coordinate[1]] == COLLISION_CELL:
                                break
                        else:
                            empty_cells = set()  # set of unrepeatable cells around the ship.
                            for c in range(len(current_coordinates_of_ship)):
                                # make a tuple of coordinates for circling the ship.
                                for i in AROUND_SHIP_DIRECTIONS:
                                    row, col = current_coordinates_of_ship[c][0], current_coordinates_of_ship[c][1]
                                    if 0 < row + i[0] < len(matrix) \
                                            and 0 < col + i[1] < len(matrix) \
                                            and matrix[row + i[0]][col + i[1]] != SHIP_CELL:
                                        empty_cells.add((row + i[0], col + i[1]))

                            # every ship has list of its own coordinates and set of tuples of cells around it.
                            current_coordinates_of_ship += empty_cells
                            placed_warships.append(list(current_coordinates_of_ship))
                            redraw_matrix(placed_warships)
                            current_coordinates_of_ship.clear()
                            break
                    case '0':  # Close program
                        sys.exit()
                    case _:  # in case of the invalid input.
                        pass
                # Moving the ship depending on the input of user with checking the valid coordinates.
                for i in range(len(current_coordinates_of_ship)):
                    if current_coordinates_of_ship[i][0] + direction_row < 1 \
                            or current_coordinates_of_ship[i][0] + direction_row > len(matrix) - 1 \
                            or current_coordinates_of_ship[i][1] + direction_col < 1 \
                            or current_coordinates_of_ship[i][1] + direction_col > len(matrix) - 1:
                        break
                else:
                    clear_previous_step(current_coordinates_of_ship)
                    for i in range(len(current_coordinates_of_ship)):  # move the ship
                        matrix[current_coordinates_of_ship[i][0] + direction_row][
                            current_coordinates_of_ship[i][1] + direction_col] = SHIP_CELL
                        current_coordinates_of_ship[i][0] = current_coordinates_of_ship[i][0] + direction_row
                        current_coordinates_of_ship[i][1] = current_coordinates_of_ship[i][1] + direction_col
                    redraw_matrix(placed_warships)
                    draw_current_ship(placed_warships, current_coordinates_of_ship)

    return matrix


if __name__ == "__main__":
    start()
