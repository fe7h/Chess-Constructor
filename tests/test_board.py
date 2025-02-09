import pytest

from constructor import figures
from constructor import board
from constructor.figures import Coord

#ПОДПРАВИТЬ ЭТОТ ТЕСТ!
@pytest.fixture
def board_data():
    COLORS = {'white', 'black'}


    class King(figures.AbstractKing):
        def move_mechanic(self, board, *args, **kwargs):
            pass
        def __str__(self):
            return 'K'


    class Rook(figures.Figure):
        def __str__(self):
            return 'R'
        def move_mechanic(self, board, *args, **kwargs):
            for modifier in (-1, 1):
                for i in range(1, 8):
                    new_file = self.position.file + i * modifier
                    if not self.valid_move_add(board, figures.Coord(new_file, self.position.rank)):
                        break
                for i in range(1, 8):
                    new_rank = self.position.rank + i * modifier
                    if not self.valid_move_add(board, figures.Coord(self.position.file, new_rank)):
                        break


    test_board = board.Board()

    test_king = King('white', figures.Coord(1,1))
    w_rook = Rook('white', figures.Coord(1,2))
    b_rook = Rook('black', figures.Coord(1,8))

    test_board.figures_data[test_king.position] = test_king
    test_board.figures_data[w_rook.position] = w_rook
    test_board.figures_data[b_rook.position] = b_rook

    test_board.kings_list.add(test_king)

    return test_board


def test_check_validation(board_data):
    board_data.all_moves_calculated()
    assert board_data.figures_data.get(figures.Coord(1,2)).valid_moves.normal == {figures.Coord(1,3),
                                                                                  figures.Coord(1,4),
                                                                                  figures.Coord(1,5),
                                                                                  figures.Coord(1,6),
                                                                                  figures.Coord(1,7),
                                                                                  figures.Coord(1,8)}
