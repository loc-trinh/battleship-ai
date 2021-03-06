# board.py
# ====================================================================== 
# Generate random Battleship boards 
# LT 6/7/16

import random
import Tkinter as tk
import time

class Board:
    def __init__(self, visualization=True):
        """ Battleship boards with the following ship pieces:
            '1': Carrier(5)
            '2': Battleship(4)
            '3': Cruiser(3)
            '4': Submarine(3)
            '5': Cuiser(2)
        """

        self.visualization = visualization

        # ===== Board setup ===== #
        self.board = []
        self.ships = (("1",5),("2",4),("3",3), ("4",3), ("5",2)) 
        self.ship_locations = set()

        # ===== Graphics setup ====== #
        if self.visualization:
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
        """ Initialize random board. Pick subset of columns or rows
            based on ship orientation. Check if ships collide with through
            set intersections
        """

        self.board = ['-'] * 100                # Reset board
        self.ship_locations = set()
        placed = False 
        while not placed:
            locations = {}
            for ship_id, ship_length in self.ships:

                orientation = random.randint(0,1) # 1 = column, 0 = row
                if orientation:
                    column = random.randrange(10)
                    indicies = [column+i for i in range(0,100,10)]
                else:
                    row = random.randrange(10)
                    indicies = [row*10 + i for i in range(10)]

                # Randomly draw a ship
                index = random.randrange(10-ship_length)
                for i in indicies[index:index+ship_length]:
                    locations[i] = ship_id 

            if len(set(locations.keys())) == 17:                # Valid layout
                for i in locations:
                    self.board[i] = locations[i]
                    self.ship_locations.add(i)
                break

        if self.visualization:
            self.draw_board()

    def draw_board(self):
        """ Draw the graphical grid """

        # Draw row and column labels and spacers
        tk.Label(self.window, text="A   B   C   D   E   F   G   H   I   J", 
                 font=("Helvetica", 15), 
                 bg="white").grid(row=0, column=1, columnspan=10)
        tk.Label(self.window, text="", bg="white").grid(row=11, column=1, columnspan=10)
        tk.Label(self.window, text="0 1 2 3 4 5 6 7 8 9", wraplength=1, 
                 font=("Helvetica", 18), 
                 bg="white").grid(row=1, column=0, rowspan=10, padx=6)
        tk.Label(self.window, text="", bg="white").grid(row=1, column=11, rowspan=10, padx=5)

        # Draw board
        for i in range(100):
            row, col = i/10, i%10
            color = "white" if self.board[i] == '-' else "gray" + str(int(self.board[i])*5)
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
                ship_id = self.board[index]
                self.board[index] = 'x'
            else:
                self.board[index] = 'o'
                
            if self.visualization:
                if hit:
                    self.canvas.create_rectangle(col*self.GRID_SIZE, row*self.GRID_SIZE,
                                            (col+1)*self.GRID_SIZE, (row+1)*self.GRID_SIZE,
                                            fill="firebrick1")
                self.canvas.create_line(col*self.GRID_SIZE, row*self.GRID_SIZE, 
                                    (col+1)*self.GRID_SIZE, (row+1)*self.GRID_SIZE)
                self.canvas.create_line(col*self.GRID_SIZE, (row+1)*self.GRID_SIZE, 
                                    (col+1)*self.GRID_SIZE, row*self.GRID_SIZE)
                self.window.update()
                time.sleep(.08)
            return (hit, ship_id) if hit else (hit, -1)


    def _convert_move_to_index(self, move):
        """ Helper functions to convert valid moves into board index """

        if len(move) != 2:
            return -1
        column,row = move[0], move[1]
        if column in "ABCDEFGHIJ" and row in "0123456789":
            return int(row)*10 + ord(column)-65
        return -1

