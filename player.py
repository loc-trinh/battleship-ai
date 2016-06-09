# player.py
# ====================================================================== 
# AI bot for various strategy to play Battleship 
# LT 6/8/16
import itertools
import random
import time
import copy

class Player:
    def __init__(self, board):
        self.board = board
        self.remaining_ships = {}
        self.moves = []
        self.move_counter = 0


    def reset(self):
        self.remaining_ships = {1:5, 2:4, 3:3, 4:3, 5:2}
        self.moves = ["".join(move) for move in list(itertools.product(list("ABCDEFGHIJ"), list("0123456789")))]
        self.move_counter = 0


    def won(self):
        return sum(self.remaining_ships.values()) == 0
        
    
    def play_random(self):
        self.reset()
        random.shuffle(self.moves)
        for move in self.moves:
            hit, ship = self.board.play(move)
            if hit:
                self.remaining_ships[ship] -= 1   
            if self.won():
                print "Total moves: %d" % self.move_counter
                break
            self.move_counter += 1
            time.sleep(.1)

