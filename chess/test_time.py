from chess.Board import Board as board
import time


_startTime = time.time()

for i in range(3000):

    Board = board()

    Board.figures_arrangement()


print('\ntime =', time.time() - _startTime)
#0.56 полная логика пешек
#0.43 вроде полная логика ходов и атак
