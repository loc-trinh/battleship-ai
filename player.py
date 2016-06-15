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
        self.remaining_ships = {"1":5, "2":4, "3":3, "4":3, "5":2}
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
        while not self.won():
            hit, ship_id = self.board.play(self.moves.pop())
            if hit:
                self.remaining_ships[ship_id] -= 1   
            self.move_counter += 1
        return self.move_counter


    def play_hunt(self):
        self.reset()
        self.moves = ['A0', 'A2', 'A4', 'A6', 'A8', 'B1', 'B3', 'B5', 'B7', 'B9', 
                      'C0', 'C2', 'C4', 'C6', 'C8', 'D1', 'D3', 'D5', 'D7', 'D9', 
                      'E0', 'E2', 'E4', 'E6', 'E8', 'F1', 'F3', 'F5', 'F7', 'F9', 
                      'G0', 'G2', 'G4', 'G6', 'G8', 'H1', 'H3', 'H5', 'H7', 'H9', 
                      'I0', 'I2', 'I4', 'I6', 'I8', 'J1', 'J3', 'J5', 'J7', 'J9']
        random.shuffle(self.moves)
        moves_played = set()
        while not self.won():
            move = self.moves.pop()
            if move in moves_played:
                continue
            hit, ship_id = self.board.play(move)
            moves_played.add(move)
            if hit:
                self.remaining_ships[ship_id] -= 1   
                self.moves.extend(self.get_neighbor_moves(move))   
            self.move_counter += 1 
        return self.move_counter


    def play_smart(self):
        self.reset()
        observations = ['-']*100
        ships_hit = []
        moves_played = set()
        while not self.won():
            belief = [0]*100
            self.update(belief, observations, ships_hit, self.remaining_ships)
            max_hits = max(belief)
            moves = [i for i in range(100) if belief[i] == max_hits]
            move_index = random.choice(moves)
            move = self._convert_index_to_move(move_index)
            if move in moves_played:
                continue
            hit, ship_id = self.board.play(move)
            moves_played.add(move)
            if hit:
                observations[move_index] = ship_id
                self.remaining_ships[ship_id] -= 1
                ships_hit.append(ship_id)
            else:
                observations[move_index] = 'o'
            self.move_counter += 1
        return self.move_counter

    def update(self, belief, obs, ships_hit, remaining_ships):
        for i in range(100):
            if obs[i] != '-':
                belief[i] = -float("inf")
        for ship_id in remaining_ships:
            parts = remaining_ships[ship_id]
            if parts == 0:
                continue
            if ship_id in ships_hit:
                indicies = [i for i, x in enumerate(obs) if x == ship_id]
                if len(indicies) > 1:
                    if abs(indicies[1]-indicies[0]) == 1:           #horizontal
                        min_ship = min(indicies)
                        max_ship = max(indicies)
                        for i in range(parts+1):
                            row = min_ship / 10
                            for j in range(min_ship-1, min_ship-1-i, -1):
                                if j / 10 != row:
                                    continue
                                if obs[j] != "-":
                                    break
                                belief[j] += 100
                            for j in range(max_ship+1, max_ship+i+1):
                                if j / 10 != row:
                                    continue
                                if obs[j] != "-":
                                    break
                                belief[j] += 100
                    else:                                           #vertical
                        min_ship = min(indicies)
                        max_ship = max(indicies)
                        for i in range(parts+1):
                            col = min_ship % 10
                            for j in range(min_ship-10, min_ship-i*11, -10):
                                if j % 10 != col or j < 0 or j > 99:
                                    continue
                                belief[j] += 100
                            for j in range(max_ship+10, max_ship+i*11, 10):
                                if j % 10 != col or j < 0 or j > 99:
                                    continue
                                if obs[j] != "-":
                                    break
                                belief[j] += 100
                else:
                    min_ship = max_ship = indicies[0] 
                    for i in range(parts+1):
                        row = min_ship / 10
                        for j in range(min_ship-1, min_ship-1-i, -1):
                            if j / 10 != row:
                                continue
                            if obs[j] != "-":
                                break
                            belief[j] += 100
                        for j in range(max_ship+1, max_ship+i+1):
                            if j / 10 != row:
                                continue
                            if obs[j] != "-":
                                break
                            belief[j] += 100
                    for i in range(parts+1):
                        col = min_ship % 10
                        for j in range(min_ship-10, min_ship-i*11, -10):
                            if j % 10 != col or j < 0 or j > 99:
                                continue
                            belief[j] += 100
                        for j in range(max_ship+10, max_ship+i*11, 10):
                            if j % 10 != col or j < 0 or j > 99:
                                continue
                            if obs[j] != "-":
                                break
                            belief[j] += 100
            else:
                for k in range(100):
                    if obs[k] != "-":
                        continue
                    min_ship = max_ship = k 
                    for i in range(parts+1):
                        row = min_ship / 10
                        for j in range(min_ship, min_ship-i, -1):
                            if j / 10 != row:
                                continue
                            if obs[j] != "-":
                                break
                            belief[j] += 1
                        for j in range(max_ship, max_ship+i):
                            if j / 10 != row:
                                continue
                            if obs[j] != "-":
                                break
                            belief[j] += 1
                    for i in range(parts+1):
                        col = min_ship % 10
                        for j in range(min_ship, min_ship-i*10, -10):
                            if j % 10 != col or j < 0 or j > 99:
                                continue
                            belief[j] += 1
                        for j in range(max_ship, max_ship+i*10, 10):
                            if j % 10 != col or j < 0 or j > 99:
                                continue
                            if obs[j] != "-":
                                break
                            belief[j] += 1
                


    def _convert_index_to_move(self, index):
        cols = list("ABCDEFGHIJ")
        rows = list("0123456789")
        return cols[index%10] + rows[index/10]









