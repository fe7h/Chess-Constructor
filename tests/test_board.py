import pytest

from constructor import figures
from constructor import board
from constructor.figures import Coord, AbstractPawn, EnPassantCapturingFigure

COLORS = {'white', 'black'}
WHITE = 'white'
BLACK = 'black'

class King(figures.AbstractKing):
    def move_mechanic(self, board, *args, **kwargs):
            for modifier_1 in (-1, 1):
                for modifier_2 in (-1, 1):
                    file_coord = self.position.file + modifier_1
                    rank_coord = self.position.rank + modifier_2
                    self.valid_move_add(board, figures.Coord(file_coord, rank_coord))
            for coord in (-1, 1):
                file_coord = self.position.file + coord
                self.valid_move_add(board, figures.Coord(file_coord, self.position.rank))
                rank_coord = self.position.rank + coord
                self.valid_move_add(board, figures.Coord(self.position.file, rank_coord))

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


class EnPassantRook(Rook, EnPassantCapturingFigure):
    def back_trail(self):
        pass


class Pawn(AbstractPawn):
    def __str__(self):
        return 'P'

    def move_mechanic(self, board, *args, **kwargs):
        if self.valid_move_add(board, figures.Coord(self.position.file + 1, self.position.rank)):
            self.valid_move_add(board, figures.Coord(self.position.file + 2, self.position.rank))

        self.valid_move_add(board, figures.Coord(self.position.file + 1, self.position.rank))

@pytest.fixture
def board_obj():
    board_obj = board.Board()

    test_king = King(WHITE, figures.Coord(1, 1))
    b_rook = Rook(BLACK, figures.Coord(1, 8))

    board_obj.figures_data[test_king.position] = test_king
    board_obj.figures_data[b_rook.position] = b_rook

    board_obj.kings_list.add(test_king)

    return board_obj

@pytest.fixture
def board_obj_2():
    board_obj = board.Board()

    test_king = King(WHITE, figures.Coord(1, 1))
    b_rook = Rook(BLACK, figures.Coord(2, 8))

    board_obj.figures_data[test_king.position] = test_king
    board_obj.figures_data[b_rook.position] = b_rook

    board_obj.kings_list.add(test_king)

    return board_obj

# @pytest.fixture
# def board_obj_en_passant():
#     board_obj = board.Board()
#
#     b_rook = EnPassantRook(BLACK, figures.Coord(8, 1))
#     b_rook.en_passant_trail = {figures.Coord(i, 1) for i in range(2, 8)}
#     board_obj.figures_data[b_rook.position] = b_rook
#
#     board_obj.temp_get_en_passant_area()
#
#     return board_obj


@pytest.mark.parametrize('coord, expected',[
    (figures.Coord(1, 2), {figures.Coord(1, i) for i in range(3, 9)}),
    (figures.Coord(2, 1), set())
])
def test_check_validation(coord, expected, board_obj):
    w_rook = Rook(WHITE, coord)
    board_obj.figures_data[w_rook.position] = w_rook

    board_obj.all_moves_calculated()
    assert board_obj.figures_data.get(coord).valid_moves.normal == expected

@pytest.mark.parametrize('coord, expected',[
    (figures.Coord(8, 2), 'stalemate'),
    (figures.Coord(1, 8), 'checkmate')
])
def test_is_checkmate(coord, expected, board_obj_2):
    b_rook = Rook(BLACK, coord)
    board_obj_2.figures_data[b_rook.position] = b_rook

    board_obj_2.all_moves_calculated()
    board_obj_2.all_moves_calculated()
    assert board_obj_2.temp_func_is_checkmate() == expected

def test_en_passant():
    board_obj = board.Board()

    b_rook = EnPassantRook(BLACK, figures.Coord(8, 1))
    w_rook = EnPassantRook(WHITE, figures.Coord(2,8))

    board_obj.figures_data[b_rook.position] = b_rook
    board_obj.figures_data[w_rook.position] = w_rook

    b_rook.en_passant_trail = {figures.Coord(i, 1) for i in range(2, 8)}
    board_obj.temp_get_en_passant_area()

    board_obj.all_moves_calculated()

    board_obj.make_a_move(figures.Coord(2,8), figures.Coord(2,1))
    assert b_rook not in board_obj.figures_data.values()