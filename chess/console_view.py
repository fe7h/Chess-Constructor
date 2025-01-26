from chess.figures import *
from chess.board import Board

a = [i for i in range(8)]
a.reverse()


def algebraic_convert(position):
    x = ['1', '2', '3', '4', '5', '6', '7', '8']
    y = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    if isinstance(position, int):
        return y[position%10] + x[position//10]
    return y.index(position[0]) + x.index(position[1])*10


def figure_moves_view(figure):
    for i in a:
        print()
        for j in range(8):
            s = algebraic_convert(i*10+j)
            if i*10+j not in figure.pp and i*10+j != figure.position:
                print(s, end=' ')
            elif i*10+j == figure.position:
                print('\u001b[31m' + s + '\u001b[0m', end=' ')
            else:
                print('\u001b[32m' + s + '\u001b[0m', end=' ')
    print('\n\n')


def board_view(board):
    sq = '%s %s%s'
    c2 = '\u001b[0m'
    print('   ', '  '.join('abcdefgh'), end='')
    for i in a:
        print('\n', i+1, end=' ')
        for j in range(8):
            s = i*10+j
            c = '\u001b[48;5;130m'if (s+i) % 2 == 0 else'\u001b[48;5;136m'
            if s in board.figures_data:
                c3 = '\u001b[97m'if board.figures_data[s].side == 'w' else '\u001b[30m'
                print(c3+sq % (c, str(board.figures_data[s]) + ' ', c2), end='')
            else:
                print(sq % (c, '  ', c2), end='')
    print(c2)
    print()


def attacked_field_view(board):
    sq = '%s %s%s'
    c2 = '\u001b[0m'
    print('   ', '  '.join('01234567'), end='')
    for i in a:
        print('\n', i, end=' ')
        for j in range(8):
            s = i*10+j
            if s in board.attacked_field_data['w']:
                c = '\u001b[48;5;231m'
            elif s in board.attacked_field_data['b']:
                c = '\u001b[48;5;232m'
            else:
                c = '\u001b[48;5;130m' if (s+i) % 2 == 0 else '\u001b[48;5;136m'
            if s in board.figures_data:
                c3 = '\u001b[97m'if board.figures_data[s].side == 'w' else '\u001b[30m'
                print(c3 + sq % (c, str(board.figures_data[s]) + ' ', c2), end='')
            else:
                print(sq % (c, '  ', c2), end='')
    print(c2)
    print()


def all_possible_coord_with_moves(figure):
    c = []
    for i in range(8):
        for j in range(8):
            c += [i * 10 + j]
    for i in c:
        figure._Figure__position = i
        figure.potential_position(attack=False)
        figure_moves_view(figure)
        print(i)
        print(figure.__dict__)


# Board = Board()
#
# Pawn = Pawn('w', 0, Board)
# all_possible_coord_with_moves(Pawn)
