# main.py
# ====================================================================== 
# Run battleship AI 
# LT 6/7/16

from board import Board
from player import Player
import time

board = Board()
player = Player(board)
for i in range(10):
    player.play_random()
    player.board.generate_board()
player.board.display()
