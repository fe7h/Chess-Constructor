from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Set

# settings
COORD_PATTERN = ['file', 'rank']
FILE_SIZE = 8
RANK_SIZE = 8
# ========

Coord = namedtuple('Coord', COORD_PATTERN)


#ТОЧНО ПЕРЕПИСАТЬ!
class MovesSet:
    def __init__(self):
        self.normal: Set[Coord] = set()
        self.capturing: Set[Coord] = set()
        self.protected: Set[Coord] = set()

    def clear(self):
        self.normal.clear()
        self.capturing.clear()
        self.protected.clear()

    def get(self):
        return self.normal | self.capturing | self.protected


class Figure(ABC):
    def __init__(self, color: str, position: Coord):
        self.color = color
        self.current_position = position
        self.special_move = True
        self.valid_moves = MovesSet()

    @abstractmethod
    def __str__(self):
        pass

# УБРАТЬ СЕТЕРРЫ И ЗАМЕНИТЬ ФУНКЦИЕЙ
    @property
    def position(self):
        return self.current_position

    @position.setter
    def position(self, new_position: Coord):
        if new_position in self.valid_moves.get():
            self.special_move = False
            self.current_position = new_position

    @abstractmethod
    def move_mechanic(self, board, *args, **kwargs):
        """should use valid_move_add"""
        pass

# СДЕЛАТЬ ЧЕРЕЗ ХЕНДЛЕР ВСЕХ ФУНКЦИЙ КОТОРЫЕ НУЖНЫ ПЕРЕД МУВ МЕХАНИК
    def moves_calculated(self, board, *args, **kwargs):
        self.valid_moves.clear()
        self.move_mechanic(board, *args, **kwargs)

    @staticmethod
    def position_check(position: Coord):
        return all(
            0 < getattr(position, atr) <= globals().get(atr.upper() + '_SIZE')
            for atr in COORD_PATTERN
        )

    def temp_valid_if_normal(self, board, position):
        self.valid_moves.normal.add(position)

    def temp_valid_if_normal_and_attack(self, board, position):
        self.valid_moves.normal.add(position)  # сделать как отдельный метод
        self.valid_moves.capturing.add(position)  #

    def temp_valid_if_protected(self, board, position):
        self.valid_moves.protected.add(position)

    # ПЕРЕПИСАТЬ!
    def valid_move_add(self, board, position: Coord) -> bool | None:
        """
        :param position:
        :return:
            True: if position points to empty square
            False: if position points to occupied square
            None: if position out of board size
        """
        if position in board.figures_data:
            if board.check_validation(self, position):
                return False
            if self.color != board.figures_data.get(position).color:
                self.temp_valid_if_normal_and_attack(board, position)       # сделать как отдельный метод
            else:
                self.temp_valid_if_protected(board, position) #не попадает если свзаная фигура ИСПРАВИТЬ! сделать как отдельный метод
            return False
        elif self.position_check(position):
            if board.check_validation(self, position):
                return True
            self.temp_valid_if_normal(board, position)           # сделать как отдельный метод
            return True
        return None

        # if not self.position_check(position):
        #     return None
        # if board.check_validation(self, position):
        #     if position in board.figures_data:
        #         if self.color != board.figures_data.get(position).color:
        #             self.valid_moves.normal.add(position)
        #             self.valid_moves.capturing.add(position)
        #         else:
        #             self.valid_moves.protected.add(position)
        #         return False
        #     elif self.position_check(position):
        #         self.valid_moves.normal.add(position)
        #         return True
        # return True #but pos dont add

        # if position in board.figures_data:
        #     if self.color != board.figures_data.get(position).color:
        #         self.valid_moves.normal.add(position)
        #         self.valid_moves.capturing.add(position)
        #     else:
        #         self.valid_moves.protected.add(position)
        #     return False
        # elif self.position_check(position):
        #     self.valid_moves.normal.add(position)
        #     return True
        # return None

# ===================================classic================================
#     def linear_movement(self, file, rank):
#         for modifier in (-1, 1):
#             for coord in range(1, FILE_SIZE):
#                 file_coord = file + coord * modifier
#                 if not self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank)):
#                     break
#             for coord in range(1, RANK_SIZE):
#                 rank_coord = rank + coord * modifier
#                 if not self.potential_position_add(self.temp_func_for_old_coord_format_set(file, rank_coord)):
#                     break
#
#     def diagonal_movement(self, file, rank):
#         for modifier_1 in (-1, 1):
#             for modifier_2 in (-1, 1):
#                 for coord in range(1, 8):
#                     file_coord = file + coord * modifier_1
#                     rank_coord = rank + coord * modifier_2
#                     if not self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank_coord)):
#                         break
#
#     def one_square_movement(self, file, rank):
#         for modifier_1 in (-1, 1):
#             for modifier_2 in (-1, 1):
#                 file_coord = file + modifier_1
#                 rank_coord = rank + modifier_2
#                 self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank_coord))
#         for coord in (-1, 1):
#             file_coord = file + coord
#             self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank))
#             rank_coord = rank + coord
#             self.potential_position_add(self.temp_func_for_old_coord_format_set(file, rank_coord))
# ==========================================================================


class AbstractKing(Figure, ABC):
    def temp_func_for_minus_attacked_fields(self, board):
        self.valid_moves.normal = self.valid_moves.normal - board.attacked_field_data.get_attacked_squares(self)


class EnPassantCapturingFigure(Figure, ABC):
    def __init__(self, color: str, position: Coord):
        self.en_passant_trail = set() #set[coord]
        super().__init__(color, position)

    @abstractmethod
    def back_trail(self):
        """should return a coords that can be attacked en passant move"""
        pass

    @Figure.position.setter
    def position(self, new_position: Coord):
        Figure.position.fset(self, new_position)
        # super().position = new_position
        self.back_trail()

    def moves_calculated(self, board, *args, **kwargs):
        self.en_passant_trail.clear()
        super().moves_calculated(board, *args, **kwargs)

    def temp_valid_if_normal(self, board, position):
        super().temp_valid_if_normal(board, position)
        if position in board.temp_en_passant_file[self.color]:
            self.valid_moves.capturing.add(position)


class MoveNotEqualAttack(Figure, ABC):
    def for_attack(self, board, position: Coord) -> bool | None:
        pass

    def for_move(self, board, position: Coord) -> bool | None:
        pass

    def valid_move_add(self, board, position: Coord) -> bool | None:
        raise Exception("Not correct method")

    def move_mechanic(self, board, *args, **kwargs):
        """should use for_attack and for_move"""
        return super().move_mechanic(board, *args, **kwargs)


class AbstractPawn(EnPassantCapturingFigure, MoveNotEqualAttack, ABC):
    pass