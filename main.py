# main.py
# ====================================================================== 
# Run battleship AI 
# LT 6/7/16

from board import Board
from player import Player
import time

board = Board()
player = Player(board)
print player.play_smart()
