from chess.Board import Board as board
from guppy import hpy

h = hpy()

Board = board()

Board.figures_arrangement()

print(h.heap()) #3992893 - 4003118
print(4003118 - 3992893) # ещё не реализована логика с трушными ходами куда можно ходить
print(4006653 - 3992893) # полная логика пешек
