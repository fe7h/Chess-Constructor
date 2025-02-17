import pytest

from constructor import board
from constructor import figures

from utils import Rook, BLACK, PawnOnlyWithMoveNotEqualAttack, WHITE


@pytest.fixture
def board_data():
    board_obj = board.Board()
    b_rook = Rook(BLACK, figures.Coord(3, 4))

    board_obj.figures_data[b_rook.position] = b_rook

    return board_obj


# @pytest.fixture
# def board_data():
#     board = Board()
#     board.figures_data = {
#         34: figures.Dummy('w', 34, board),
#         35: figures.Dummy('w', 35, board),
#         43: figures.Dummy('w', 43, board),
#         44: figures.Dummy('w', 44, board),
#         66: figures.Dummy('b', 66, board),
#         67: figures.Dummy('b', 67, board),
#         75: figures.Dummy('b', 75, board),
#         76: figures.Dummy('b', 76, board),
#     }
#     return board
#
# def test_night(board_data):
#     night = figures.Night('w', 55, board_data)
#     board_data.figures_data[55] = night
#     night.potential_position()
#     assert sorted(night.pp)  == sorted([47, 67, 76, 74, 63, 36])
#
# def test_queen(board_data):
#     queen = figures.Queen('w', 55, board_data)
#     board_data.figures_data[55] = queen
#     queen.potential_position()
#     assert sorted(queen.pp)  == sorted([37, 45, 46, 50, 51, 52, 53, 54, 56, 57, 64, 65, 66, 73, 75])
#
# def test_bishop(board_data):
#     bishop = figures.Bishop('w', 55, board_data)
#     board_data.figures_data[55] = bishop
#     bishop.potential_position()
#     assert sorted(bishop.pp)  == sorted([37, 46, 64, 66, 73])
#
# def test_king(board_data):
#     king = figures.King('w', 55, board_data)
#     board_data.figures_data[55] = king
#     board_data.all_possible_moves()
#     assert sorted(king.pp)  == sorted([45, 46, 54, 56, 64, 65, 66])
#     king.temp_func_for_take_attacked_field_data()
#     assert sorted(king.pp)  == sorted([45, 46, 54])
#
#
# def test_rook(board_data):
#     rook = figures.Rook('w', 55, board_data)
#     board_data.figures_data[55] = rook
#     rook.potential_position()
#     assert sorted(rook.pp)  == sorted([45, 50, 51, 52, 53, 54, 56, 57, 65, 75])
#
# # def test_pawn(board_data):
# #     pawn = figures.Pawn('w', 55, board_data)
# #     board_data.figures_data.add(pawn)
# #     pawn.potential_position()
# #     assert sorted(pawn.pp)  == sorted([])
#
# def test_dummy(board_data):
#     dummy = figures.Dummy('w', 55, board_data)
#     board_data.figures_data[55] = dummy
#     dummy.potential_position()
#     assert sorted(dummy.pp)  == sorted([45, 46, 54, 56, 64, 65, 66])
#
# # for key in module_figures_dict:
# #     if 'chess.figures.' in str(module_figures_dict[key]):
# #         print(f'def test_{key.lower()}(board_data):'
# #               f'\n\t{key.lower()} = figures.{key}(\'w\', 55, board_data)'
# #               f'\n\tboard_data.figures_data.add({key.lower()})'
# #               f'\n\t{key.lower()}.potential_position()'
# #               f'\n\tassert sorted({key.lower()}.pp)  == sorted([])\n')
@pytest.mark.parametrize('coord, blank, attack, capturing',[
    (figures.Coord(2, 4), set(),
     {figures.Coord(3, 3), figures.Coord(3, 5)},
     set()),

    (figures.Coord(2, 3),
     {figures.Coord(3, 3), figures.Coord(4, 3)},
     {figures.Coord(3, 2), figures.Coord(3, 4)},
     {figures.Coord(3, 4)}),

    (figures.Coord(1, 4),
     {figures.Coord(2, 4)},
     {figures.Coord(2, 3), figures.Coord(2, 5)},
     set())
])
def test_MoveNotEqualAttack_figure(coord, blank, attack, board_data, capturing):
    w_pawn = PawnOnlyWithMoveNotEqualAttack(WHITE, coord)

    board_data.figures_data[w_pawn.position] = w_pawn

    board_data.all_moves_calculated()
    assert w_pawn.valid_moves.blank == blank
    assert w_pawn.valid_moves.attack == attack
    assert w_pawn.valid_moves.capturing == capturing
