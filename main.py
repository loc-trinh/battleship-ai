# main.py
# ====================================================================== 
# Run battleship AI 
# LT 6/7/16

from board import Board
import time

board = Board()
for i in list("ABCDEFGHIJ"):
    for j in list("0123456789"):
        print board.play(i+j)
        time.sleep(.3)
board.display()
