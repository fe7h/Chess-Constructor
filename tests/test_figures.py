import pytest

from chess.board import Board
import chess.figures as figures


@pytest.fixture
def board_data():
    board = Board()
    board.figures_data = {
        figures.Dummy('w', 34, board),
        figures.Dummy('w', 35, board),
        figures.Dummy('w', 43, board),
        figures.Dummy('w', 44, board),
        figures.Dummy('b', 66, board),
        figures.Dummy('b', 67, board),
        figures.Dummy('b', 75, board),
        figures.Dummy('b', 76, board),
    }
    return board

def test_night(board_data):
    night = figures.Night('w', 55, board_data)
    board_data.figures_data.add(night)
    night.potential_position()
    assert sorted(night.pp)  == sorted([])

def test_queen(board_data):
    queen = figures.Queen('w', 55, board_data)
    board_data.figures_data.add(queen)
    queen.potential_position()
    assert sorted(queen.pp)  == sorted([])

def test_bishop(board_data):
    bishop = figures.Bishop('w', 55, board_data)
    board_data.figures_data.add(bishop)
    bishop.potential_position()
    assert sorted(bishop.pp)  == sorted([])

def test_king(board_data):
    king = figures.King('w', 55, board_data)
    board_data.figures_data.add(king)
    king.potential_position()
    assert sorted(king.pp)  == sorted([])

def test_rook(board_data):
    rook = figures.Rook('w', 55, board_data)
    board_data.figures_data.add(rook)
    rook.potential_position()
    assert sorted(rook.pp)  == sorted([])

def test_pawn(board_data):
    pawn = figures.Pawn('w', 55, board_data)
    board_data.figures_data.add(pawn)
    pawn.potential_position()
    assert sorted(pawn.pp)  == sorted([])

# def test_dummy(board_data):
#     dummy = figures.Dummy('w', 55, board_data)
#     board_data.figures_data.add(dummy)
#     dummy.potential_position()
#     assert dummy.pp  == []

# for key in module_figures_dict:
#     if 'chess.figures.' in str(module_figures_dict[key]):
#         print(f'def test_{key.lower()}(board_data):'
#               f'\n\t{key.lower()} = figures.{key}(\'w\', 55, board_data)'
#               f'\n\tboard_data.figures_data.add({key.lower()})'
#               f'\n\t{key.lower()}.potential_position()'
#               f'\n\tassert sorted({key.lower()}.pp)  == sorted([])\n')
