from chess.board import Board
from chess.tech_commands import afd, fd, fd_key
from chess.console_view import board_view, algebraic_convert


def main():
    board = Board()

    # board.figures_data[0] = Night('w', 0, board)
    # board.figures_data[12] = Dummy('w', 12, board)
    # board.figures_data[71] = Dummy('b', 71, board)
    # board.all_possible_moves()
    board.figures_arrangement()

    while True:

        board_view(board)

        command = input()

        if command == 't':
            command = input().split()
            if len(command) == 1:
                if command[0] == 'afd':
                    afd(board)
                elif command[0] == 'fd':
                    fd(board)
                elif command[0] == 'stop':
                    break
            else:
                if command[0] == 'fd':
                    fd_key(board, algebraic_convert(command[1]))

        else:
            try:
                board.move(algebraic_convert(command[0:2]), algebraic_convert(command[2:4]))
            except:
                pass


if __name__ == '__main__':
    # print('lol')
    main()
