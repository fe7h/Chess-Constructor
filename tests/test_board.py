import pytest

from constructor import figures
from constructor import board
from constructor.figures import Coord

COLORS = {'white', 'black'}
WHITE = 'white'
BLACK = 'black'

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


@pytest.fixture
def board_obj():
    board_obj = board.Board()

    test_king = King(WHITE, figures.Coord(1,1))
    b_rook = Rook(BLACK, figures.Coord(1,8))

    board_obj.figures_data[test_king.position] = test_king
    board_obj.figures_data[b_rook.position] = b_rook

    board_obj.kings_list.add(test_king)

    return board_obj


@pytest.mark.parametrize('coord, expected',[
    (figures.Coord(1,2), {figures.Coord(1,i) for i in range(3,9)}),
    (figures.Coord(2,1), set())
])
def test_check_validation(coord, expected, board_obj):
    w_rook = Rook(WHITE, coord)
    board_obj.figures_data[w_rook.position] = w_rook

    board_obj.all_moves_calculated()
    assert board_obj.figures_data.get(coord).valid_moves.normal == expected
