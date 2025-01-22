from chess.console_view import *


def fd(board):
    print('\n\u001b[94mFigures_data:\u001b[0m\n')
    keys = []
    for key in board.figures_data:
        keys += [key]
    keys.sort()
    for key in keys:
        print('%i:%s' % (key, board.figures_data[key].__repr__()), '\n=====', board.figures_data[key].__dict__, '\n')
    print()


def afd(board):
    print('\n\u001b[94mAttacked_field_data:\u001b[0m\n')
    attacked_field_view(board)
    for key in board.attacked_field_data:
        print('%s:%s' % (key, board.attacked_field_data[key]))
    print()


def fd_key(board,key):
    if key in board.figures_data:
        print('\n\u001b[94mFigure.__dict__:\u001b[0m\n')
        print('%i:%s' % (key, board.figures_data[key].__repr__()), '\n=====', board.figures_data[key].__dict__, '\n')
    print()
