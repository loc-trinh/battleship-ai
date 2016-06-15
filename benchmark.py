# benchmark.py
# ====================================================================== 
# Benchmarking various AI's performance over 1000 games
# LT 6/8/16

from board import Board
from player import Player
import numpy as np
from matplotlib import pyplot as plt

board = Board(visualization=False)
player = Player(board)
results = {i:0 for i in range(101)} 
trials = 10000
for i in range(trials):
    print i
    results[player.play_smart()] += 1
    player.board.generate_board()

print "Average: %f" % (sum([i*results[i] for i in results.keys()])/float(trials)) 
plt.plot(results.keys(), results.values(), 'bo')
plt.show()
