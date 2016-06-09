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


    def won(self):
        return sum(self.remaining_ships.values()) == 0


    def reset(self):
        self.remaining_ships = {1:5, 2:4, 3:3, 4:3, 5:2}
        self.moves = ["".join(move) for move in list(itertools.product(list("ABCDEFGHIJ"), list("0123456789")))]
        self.move_counter = 0

        
    def get_neighbor_moves(self, move):
        col, row = move[0], move[1]        
        moves = []
        moves.append(chr(ord(col)+1) + row)
        moves.append(chr(ord(col)-1) + row)
        moves.append(col + str(int(row)+1))
        moves.append(col + str(int(row)-1))
        valid_moves = []
        for i in moves:
            if '@' not in i and 'K' not in i and '-1' not in i and '10' not in i:
                valid_moves.append(i)
        return valid_moves
    

    def play_random(self):
        self.reset()
        random.shuffle(self.moves)
        for move in self.moves:
            hit, ship = self.board.play(move)
            if hit:
                self.remaining_ships[ship] -= 1   
            if self.won():
                return self.move_counter 
            self.move_counter += 1


    def play_hunt(self):
        self.reset()
        random.shuffle(self.moves)
        moves_played = set()
        while len(self.moves) != 0:
            move = self.moves.pop()
            if move in moves_played:
                continue
            hit, ship = self.board.play(move)
            moves_played.add(move)
            if hit:
                self.remaining_ships[ship] -= 1   
                self.moves.extend(self.get_neighbor_moves(move))   
            if self.won():
                return self.move_counter
            self.move_counter += 1


    def play_diagonal_hunt(self):
        self.reset()
        self.moves = ['A0', 'A2', 'A4', 'A6', 'A8', 'B1', 'B3', 'B5', 'B7', 'B9', 
                      'C0', 'C2', 'C4', 'C6', 'C8', 'D1', 'D3', 'D5', 'D7', 'D9', 
                      'E0', 'E2', 'E4', 'E6', 'E8', 'F1', 'F3', 'F5', 'F7', 'F9', 
                      'G0', 'G2', 'G4', 'G6', 'G8', 'H1', 'H3', 'H5', 'H7', 'H9', 
                      'I0', 'I2', 'I4', 'I6', 'I8', 'J1', 'J3', 'J5', 'J7', 'J9']
        random.shuffle(self.moves)
        moves_played = set()
        while len(self.moves) != 0:
            move = self.moves.pop()
            if move in moves_played:
                continue
            hit, ship = self.board.play(move)
            moves_played.add(move)
            if hit:
                self.remaining_ships[ship] -= 1   
                self.moves.extend(self.get_neighbor_moves(move))   
            if self.won():
                return self.move_counter
            self.move_counter += 1

