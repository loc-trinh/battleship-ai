# board.py
# ====================================================================== 
# Generate random Battleship boards 
# LT 6/7/16

import random

class Board:
    def __init__(self):
        self.board = []
        self.ships = [2,3,3,4,5] 
        self.ship_locations = set()
        self.generate_board()
       

    def __str__(self):
        """ Return printed board in grid fashion """ 

        board_string = "  A B C D E F G H I J"
        for i in range(0, 100, 10):
            board_string += "\n" + str(i/10) + " " + " ".join(self.board[i:i+10]) 

        return board_string


    def generate_board(self):
        """ Initialize random board. Using the following pieces:
            Scout(2), Submarine(3), Cruiser(3), Battleship(4), Carrier(5)
        """

        self.board = ['-'] * 100                #reset board
        while True:
            ship_locations = []
            for ship in self.ships:
                # pick a row or column
                if random.randint(0,1):
                    column = random.randrange(10)
                    indicies = [column+i for i in range(0,100,10)]
                else:
                    row = random.randrange(10)
                    indicies = [row*10 + i for i in range(10)]

                # randomly draw a ship
                index = random.randrange(10-ship)
                ship_locations += indicies[index:index+ship]

            if len(set(ship_locations)) == 17:
                self.ship_locations = set(ship_locations)
                for i in self.ship_locations:
                    self.board[i] = 'o'
                break

    def play(self, move):
        """ Play a move. Return "HIT" or "MISS" if there's a ship at location
        """

        index = self.convert_move_to_index(move)
        if index == -1:
            return "Invalid move!"
        else:
            self.board[index] = 'X' if self.board[index] == 'o' else 'x'
            print self.__str__()
            return "HIT" if self.board[index] == 'X' else "MISS"


    def convert_move_to_index(self, move):
        """ Helper functions to convert moves into board index """

        if len(move) != 2:
            return -1
        column = move[0]
        row = move[1]
        if column in "ABCDEFGHIJ" and row in "0123456789":
            return int(row)*10 + ord(column)-65
        return -1

