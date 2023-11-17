class Ship:
    """
    Class has type, length and list of tuples for coordinates that indicate where it is located.
    Ship has list of marks for displaying on the board of Gamer.
    """
    '''        self.safe_zone = ' '
            self.ship_zone = 'o'
            self.collision_zone = '?'
            self.damage_zone = '+'
            '''
    def __init__(self, length):
        self.length = length
        self.is_placed = False
        self.coordinates = list()
        self.safe_coordinates = list()
        # self.generate_coordinates(self.coordinates)

    def set_coordinates(self, row, col):
        pass

    def get_coordinates(self):
        pass

    def generate_coordinates(self, coordinates):
        pass
