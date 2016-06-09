# board.py
# ====================================================================== 
# Generate random Battleship boards 
# LT 6/7/16

import random
import Tkinter as tk

class Board:
    def __init__(self):
        # ===== Board setup ===== #
        self.board = []
        self.ships = [5,4,3,3,2]  
        self.ship_locations = set()

        # ===== Graphics setup ====== #
        self.window = tk.Tk()
        self.window.title("Battleship")
        self.window.configure(background="white")
        self.canvas = tk.Canvas(self.window, width=300, height=300)
        self.GRID_SIZE = 30
        self.canvas.grid(row=1, column=1, columnspan=10, rowspan=10)

        self.generate_board()


    def __str__(self):
        """ Return printed board in grid fashion """ 

        board_string = "  A B C D E F G H I J"
        for i in range(0, 100, 10):
            board_string += "\n" + str(i/10) + " " + " ".join(self.board[i:i+10]) 

        return board_string


    def display(self):
        """ Display Tkinter graphical board """

        self.window.mainloop()


    def generate_board(self):
        """ Initialize random board. Using the following pieces:
            Scout(2), Submarine(3), Cruiser(3), Battleship(4), Carrier(5)
        """

        self.board = ['-'] * 100                #reset board
        while True:
            ship_locations = {}
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
                for i in indicies[index:index+ship]:
                    ship_locations[i] = self.ships.index(ship)+1

            if len(set(ship_locations.keys())) == 17:
                self.ship_locations = set(ship_locations.keys())
                for i in self.ship_locations:
                    self.board[i] = ship_locations[i] 
                break
        self.draw_board()

    def draw_board(self):
        """ Draw the graphical grid """

        #Row and column labels and spacers
        tk.Label(self.window, text="A   B   C   D   E   F   G   H   I   J", 
                 font=("Helvetica", 15), 
                 bg="white").grid(row=0, column=1, columnspan=10)
        tk.Label(self.window, text="", bg="white").grid(row=11, column=1, columnspan=10)
        tk.Label(self.window, text="0 1 2 3 4 5 6 7 8 9", wraplength=1, 
                 font=("Helvetica", 18), 
                 bg="white").grid(row=1, column=0, rowspan=10, padx=6)
        tk.Label(self.window, text="", bg="white").grid(row=1, column=11, rowspan=10, padx=5)

        #Board
        for i in range(100):
            row, col = i/10, i%10
            if self.board[i] == '-':
                color = "white"
            else: 
                color = "gray" + str(self.board[i]*5)
            self.canvas.create_rectangle(col*self.GRID_SIZE, row*self.GRID_SIZE, 
                                         (col+1)*self.GRID_SIZE, (row+1)*self.GRID_SIZE,
                                         fill=color)


    def play(self, move):
        """ Play a move. Return (True, ship) or (False, -1) if there's a ship at location
        """

        index = self._convert_move_to_index(move)
        if index == -1:
            return "Invalid move!"
        else:
            row, col = index/10, index%10
            hit = not self.board[index] == '-'
            if hit:
                self.canvas.create_rectangle(col*self.GRID_SIZE, row*self.GRID_SIZE,
                                            (col+1)*self.GRID_SIZE, (row+1)*self.GRID_SIZE,
                                            fill="firebrick1")
                ship = self.board[index]
                self.board[index] = 'X'
            else:
                self.board[index] = 'x'
                
            self.canvas.create_line(col*self.GRID_SIZE, row*self.GRID_SIZE, 
                                    (col+1)*self.GRID_SIZE, (row+1)*self.GRID_SIZE)
            self.canvas.create_line(col*self.GRID_SIZE, (row+1)*self.GRID_SIZE, 
                                    (col+1)*self.GRID_SIZE, row*self.GRID_SIZE)
            self.window.update()
            if hit:
                return (hit, ship)
            else:
                return (hit, -1)


    def _convert_move_to_index(self, move):
        """ Helper functions to convert valid moves into board index """

        if len(move) != 2:
            return -1
        column,row = move[0], move[1]
        if column in "ABCDEFGHIJ" and row in "0123456789":
            return int(row)*10 + ord(column)-65
        return -1

