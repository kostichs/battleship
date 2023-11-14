import random

rows = 10
columns = 10


def create_board():
    game_board = [["O"] * columns for i in range(rows)]
    return game_board


def create_random_ship():
    return random.randint(1, 5), random.randint(1, 5)


def ship_points(row_col=(3, 3), ship_length=4, count=1, direction=(1, 0), board_size=(10, 10)):
    while count > 0:
        points = []
        for i in range(ship_length):
            points.append((row_col[0]+i*direction[0], row_col[1]+i*direction[1]))
            if points[i][0] >= board_size[0] or points[i][1] >= board_size[1]:
                return None
        count -= 1
        return points


def create_ship_manually():
    x = int(input("Input x coordinate from 1 to 10: "))
    y = int(input("Input y coordinate from 1 to 10: "))
    try:

        if not (0 < x < 10) or not (0 < y < 10):
            print("Value must be between 0 and 10. Try again")
    except ValueError:
        print("Only numbers allowed")
    return tuple((x, y))


def place_ships(coordinates, field):
    print(coordinates)
    for i, k in coordinates:
        field[i][k] = 1
    for i in field:
        print(*i)


def main():
    board = create_board()
    ship = create_random_ship()
    asd = ship_points(row_col = ship )
    place_ships(asd, board)
    create_ship_manually()

if __name__ == '__main__':
    main()
