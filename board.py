# board.py
# ====================================================================== 
# Generate random Battleship boards 
# LT 6/7/16

class Board:
    def __init__(self):
        ''' Initialize random board. Using the following pieces:
            Scout(2)         = "1"
            Submarine(3)     = "2"
            Cruiser(3)       = "3"
            Battleship(4)    = "4"
            Carrier(5)       = "5"
        '''

        self.board = ["-"] * 100


    def __str__(self):
        ''' Return printed board in grid fashion '''

        board_string = "  A B C D E F G H I J\n"
        for i in range(0, 100, 10):
            board_string += str(i/10) + " " + " ".join(self.board[i:i+10]) + "\n"

        return board_string


    def play(self, move):
        pass


    def convert_move_to_index(self, move):
        pass


