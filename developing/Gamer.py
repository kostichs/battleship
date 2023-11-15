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
        self.ships = list()
        self.generate_ships()

    def generate_ships(self):
        pass

    def command(self, order=str(input().upper())):
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

