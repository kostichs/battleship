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


def create_board() -> list[list[str]]:
    """
    Create a game board with BOARD_SIZE represented as a 11x11 list with number- and letter-coordinates on the edges
    and empty cells inside.

    :return: The created game board as a list[list[str]].
    """
    board = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    return board


def display_board(matrix: list[list[str]]) -> None:
    """
    Print the game board, represented as a matrix of cell states.

    Each cell's state is printed in the middle of a cell_size.
    The 'letters' string is used to fill the left edge of the board.
    Numbers are used to fill the top edge of the board.
    The cell at board[0][0] is intentionally left empty because it doesn't participate in the game.

    :param matrix: A list of lists representing the current state of the game board.
    :return: None
    """
    letters = 'ABCDEFGHIJ'
    for row in range(1, len(matrix)):
        matrix[row][0] = letters[row - 1]

    for col in range(1, len(matrix)):
        matrix[0][col] = str(col)

    cell_size = 3
    flag = True
    matrix[0][0] = ' '
    for row in matrix:
        for col in row:
            if flag:
                flag = False  # avoid changing of the cell 0x0 that has to be empty.
            print(f'{col:^{cell_size}}', end=" ")
        print()


def format_matrix(board) -> str:
    """
    Transform a matrix represented as a list into a formatted string.

    Each cell's state is formatted and aligned in the middle of a cell size.
    The resulting string includes newlines for better readability.

    :param board: A list of lists representing the matrix to be formatted.
    :return: A formatted string representing the matrix.
    """
    formatted_text = ""
    for row in board:
        formatted_row = [f'{col:^{3}}' for col in row]
        formatted_text += " ".join(formatted_row) + "\n\n"
    return formatted_text


def format_matrix_without_points(matrix):
    """
    Transform a matrix represented as a list into a formatted string.

    '.' characters in the matrix will be replaced with spaces (' ') to create a clear battlefield.
    Each cell's state is formatted and aligned in the middle of a cell size.
    The resulting string includes newlines for better readability.

    :param matrix: The game board represented as a list of lists.
    :return: A formatted string representation of the matrix.
    """
    formatted_text = ""
    for row in matrix:
        formatted_row = [f'{col:^{3}}' if col != '.' else '   ' for col in row]
        formatted_text += " ".join(formatted_row) + "\n\n"
    return formatted_text


def generate_warships_list(warships: list[list[int, int]]) -> list[list[int, int]]:
    """
    Moves the key and value from a dictionary to a matrix.

    Parameters:
        warships (list[list[str, int]]): The target matrix to store key-value pairs.

    Returns:
        list[list[str, int]]: The matrix with key-value pairs from the dictionary.
    """
    for warship, value in WARSHIPS.items():
        warships.append([int(warship), value])
    return warships


def display_player_ship(warships: list[list[int, int]], board: list[list[str]],
                        current_coordinates_of_ship: list, placed_warships: list) -> str:
    """
    If the count of the ship type reaches zero, exclude that ship type from the list, and move to the next type.
    If the list of ship types is empty, initiate the final matrix cleanup before its rendering.
    If the count of the current ship type is still greater than zero, the function places the ship in the middle
    of the matrix,
    and updates the current coordinates of the new ship in the list.

    Parameters:
        warships (list[list[int, int]]): List of ship types with their counts.
        board (list[list[str]]): The game board matrix.
        current_coordinates_of_ship (list): List of coordinates for the current ship.
        placed_warships (list): List of placed ships on the board.

    Returns:
        string to notify about the current statement of the game.
    """
    if warships[0][1] <= 0:
        warships.pop(0)
        # the first location is in the middle of the board, depending on its length.
    if len(warships) > 0:
        ship_type = int(warships[0][0])
        for i in range(ship_type):
            board[len(board) // 2][len(board) // 2 - ship_type // 2 + i + 1] = SHIP_CELL
            current_coordinates_of_ship.append([len(board) // 2, len(board) // 2 - ship_type // 2 + i + 1])
            draw_current_ship(placed_warships, current_coordinates_of_ship, board)
        return 'Place the ship on the board.'
    else:  # if there are no more ships to place on the board.
        return 'There are no more ships to place.'


def clear_previous_step(board: list[list[str]], coordinates: list) -> None:
    """
    Clear the symbols on the previous cell in the matrix after changing the position of the ship.

    This function updates the game board matrix by setting the cells specified by the given coordinates
    to the default empty cell value.

    :param board: The game board represented as a list of lists.
    :param coordinates: List of coordinates to clear on the game board.
    :return: None
    """
    for coord in range(len(coordinates)):  # clear the symbols on the previous cell in matrix.
        board[coordinates[coord][0]][coordinates[coord][1]] = EMPTY_CELL


def draw_current_ship(warships: list[list[int, int]], current_coordinates: list[list], board: list[list[str]]) -> None:
    """
    Draws the current ship on the matrix based on its position, considering collisions with other ships or lack thereof.

    Parameters:
        warships (list[list[int, int]]): List of ship types with their counts.
        current_coordinates (list): List of coordinates for the current ship.
        board (list[list[str]]): The game board matrix.

    Returns:
        None
    """
    is_collided = False
    if len(warships) > 0:  # The first time the list of placed ships is empty
        for current_coordinate in range(len(current_coordinates)):  # clear the matrix
            for war in warships:
                for w in war:
                    if current_coordinates[current_coordinate][0] == w[0] \
                            and current_coordinates[current_coordinate][1] == w[1]:
                        board[current_coordinates[current_coordinate][0]][
                            current_coordinates[current_coordinate][1]] = COLLISION_CELL
                        is_collided = True
                        break
            if not is_collided:
                board[current_coordinates[current_coordinate][0]][
                    current_coordinates[current_coordinate][1]] = SHIP_CELL
    else:
        for current_coordinate in range(len(current_coordinates)):  # place a ship on the matrix.
            board[current_coordinates[current_coordinate][0]][
                current_coordinates[current_coordinate][1]] = SHIP_CELL


def redraw_matrix(board: list[list[str]], warships: list) -> None:
    """
    Redraws the player's game board, updating the positions of previously placed ships.

    This function draws the ship based on its coordinates provided as a list-type,
    along with the safe-zone represented by the neighboring coordinates.

    :param board: The game board represented as a list of lists.
    :param warships: List of coordinates of previously placed ships.
    :return: None
    """
    for warship in warships:
        for w in warship:
            if type(w) == list:
                board[w[0]][w[1]] = SHIP_CELL
            else:
                board[w[0]][w[1]] = ''


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
                                    and is_empty(matrix[ship_coordinates[c][0] + i[0]][ship_coordinates[c][1] + i[1]]):
                                matrix[ship_coordinates[c][0] + i[0]][ship_coordinates[c][1] + i[1]] = ' '
                            else:
                                continue
                    break
                else:
                    continue

    return matrix


def motion(row, col, coordinates: list, board: list[list[str]], warships: list) -> None:
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
    direction_row, direction_col = row, col
    # Moving the ship depending on the input of user with checking the valid coordinates.
    for i in range(len(coordinates)):
        if coordinates[i][0] + direction_row < 1 \
                or coordinates[i][0] + direction_row > len(board) - 1 \
                or coordinates[i][1] + direction_col < 1 \
                or coordinates[i][1] + direction_col > len(board) - 1:
            break
    else:
        clear_previous_step(board, coordinates)
        for i in range(len(coordinates)):  # move the ship
            board[coordinates[i][0] + direction_row][
                coordinates[i][1] + direction_col] = SHIP_CELL
            coordinates[i][0] = coordinates[i][0] + direction_row
            coordinates[i][1] = coordinates[i][1] + direction_col
        redraw_matrix(board, warships)
        draw_current_ship(warships, coordinates, board)


def rotate_ship(horizontal: bool, warships: list, coordinates: list,
                board: list[list[str]], placed_warships: list) -> bool:
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
    _horizontal = horizontal
    ship_type = int(warships[0][0])

    if _horizontal:  # horizontal position
        for i in range(len(coordinates)):
            current_cell = coordinates[i]  # reduce the length of next expressions.
            if current_cell[0] - ship_type // 2 + i < 1 \
                    or current_cell[0] - ship_type // 2 + i > len(board) - 1 \
                    or current_cell[1] + ship_type // 2 - i < 1 \
                    or current_cell[1] + ship_type // 2 - i > len(board) - 1:
                return _horizontal
        else:
            _horizontal = not _horizontal
            clear_previous_step(board, coordinates)
            for i in range(len(coordinates)):
                current_cell = coordinates[i]
                current_cell[0] = current_cell[0] - ship_type // 2 + i
                current_cell[1] = current_cell[1] + ship_type // 2 - i
            redraw_matrix(board, placed_warships)
            draw_current_ship(placed_warships, coordinates, board)
    else:  # vertical position
        for i in range(len(coordinates)):
            current_cell = coordinates[i]
            if coordinates[i][1] - ship_type // 2 + i < 1 \
                    or current_cell[1] - ship_type // 2 + i > len(board) - 1 \
                    or current_cell[0] + ship_type // 2 - i < 1 \
                    or current_cell[0] + ship_type // 2 - i > len(board) - 1:
                return horizontal
        else:
            _horizontal = True
            clear_previous_step(board, coordinates)
            for i in range(len(coordinates) - 1, -1, -1):
                current_cell = coordinates[i]
                current_cell[0] = current_cell[0] + ship_type // 2 - i
                current_cell[1] = current_cell[1] - ship_type // 2 + i
            redraw_matrix(board, placed_warships)
            draw_current_ship(placed_warships, coordinates, board)
            return _horizontal


def apply_placement(board: list[list[str]], coordinates: list) -> bool:
    """
    Checks if the current coordinates of the ship don't conflict with coordinates of other ships.

    If these coordinates are suitable, the cells around the new ship will be marked as empty for a safe zone.

    Parameters:
        board (list[list[str]]): The game board represented as a list of lists.
        coordinates (list): List of coordinates of the current ship.

    Returns:
        bool: True if placement is successful, False if there is a conflict with other ships.
    """
    # check whether teh current ship isn't near another one.
    for coordinate in coordinates:
        if board[coordinate[0]][coordinate[1]] == COLLISION_CELL:
            return False
    else:
        empty_cells = set()  # set of unrepeatable cells around the ship.
        for c in range(len(coordinates)):
            # make a tuple of coordinates for circling the ship.
            for i in AROUND_SHIP_DIRECTIONS:
                row, col = coordinates[c][0], coordinates[c][1]
                if 0 < row + i[0] < len(board) \
                        and 0 < col + i[1] < len(board) \
                        and board[row + i[0]][col + i[1]] != SHIP_CELL:
                    empty_cells.add((row + i[0], col + i[1]))
        coordinates += empty_cells
        return True
