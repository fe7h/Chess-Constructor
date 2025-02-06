from abc import ABC, abstractmethod
from collections import namedtuple


# settings
COORD_PATTERN = {'file', 'rank'}
FILE_SIZE = 8
RANK_SIZE = 8
# ========

Coord = namedtuple('Coord', COORD_PATTERN)

# class Coord:
#     def __init__(self, file: int, rank: int, **kwargs):
#         self.file = file
#         self.rank = rank
#         for name, value in kwargs.items():
#             setattr(self, name, value)
#
#     def get(self):
#         return tuple(value for name, value in self.__dict__.items())
#
#     def set(self, new_value: tuple):
#         attributes = self.__dict__.keys()
#         self.__dict__ = dict(zip(attributes, new_value))
#
#     def __eq__(self, other: tuple):
#         return self.get() == other

class MovesSet:
    def __init__(self):
        self.normal = set() #valid_moves
        self.capturing = set() #attacked_squares
        self.protected = set() #protected_squares

    def clear(self):
        self.normal.clear()
        self.capturing.clear()
        self.protected.clear()


class Figure(ABC):

    # moves = namedtuple('moves', {'normal', 'capturing', 'protected'})

    def __init__(self, color: str, position: Coord):
        self.color = color
        self.current_position = position
        self.special_move = True
        # self.file, self.rank = self.temp_func_for_new_position_field_get()
        # self.board = board
        # self.valid_moves = set()  # pp - potential position
        # self.protected_squares = set()
        # self.attacked_squares = set()
        self.valid_moves = MovesSet()

    @abstractmethod
    def __str__(self):
        pass
    # def temp_func_for_new_position_field_get(self):
    #     return self.__position // 10, self.__position % 10
    #
    # @staticmethod
    # def temp_func_for_old_coord_format_set(file, rank):
    #     return file * 10 + rank

    @property
    def position(self):
        return self.current_position

    @position.setter
    def position(self, new_position: Coord):
        if new_position in self.valid_moves:
            self.special_move = False
            self.current_position = new_position

    @abstractmethod
    def move_mechanic(self, board, *args, **kwargs):
        pass

    def moves_calculated(self, board, *args, **kwargs):
        self.valid_moves.clear()
        self.move_mechanic(board, *args, **kwargs)

    @staticmethod
    def position_check(position: Coord):
        return all(
            0 < getattr(position, atr) <= globals().get(atr.upper() + '_SIZE')
            for atr in COORD_PATTERN
        )

    # def potential_position_add(self, position):
    def valid_move_add(self, board, position: Coord) -> bool | None:
        """
        :param position:
        :return:
            True: if position points to empty square
            False: if position points to occupied square
            None: if position out of board size
        """

        if position in board.figures_data:
            if self.color != board.figures_data.get(position).color:
                self.valid_moves.normal.add(position)
                self.valid_moves.capturing.add(position)
            else:
                self.valid_moves.protected.add(position)
            return False
        elif self.position_check(position):
            self.valid_moves.normal.add(position)
            return True
        return None

# ===================================classic================================
    def linear_movement(self, file, rank):
        for modifier in (-1, 1):
            for coord in range(1, FILE_SIZE):
                file_coord = file + coord * modifier
                if not self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank)):
                    break
            for coord in range(1, RANK_SIZE):
                rank_coord = rank + coord * modifier
                if not self.potential_position_add(self.temp_func_for_old_coord_format_set(file, rank_coord)):
                    break

    def diagonal_movement(self, file, rank):
        for modifier_1 in (-1, 1):
            for modifier_2 in (-1, 1):
                for coord in range(1, 8):
                    file_coord = file + coord * modifier_1
                    rank_coord = rank + coord * modifier_2
                    if not self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank_coord)):
                        break

    def one_square_movement(self, file, rank):
        for modifier_1 in (-1, 1):
            for modifier_2 in (-1, 1):
                file_coord = file + modifier_1
                rank_coord = rank + modifier_2
                self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank_coord))
        for coord in (-1, 1):
            file_coord = file + coord
            self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank))
            rank_coord = rank + coord
            self.potential_position_add(self.temp_func_for_old_coord_format_set(file, rank_coord))
# ==========================================================================

class Rook(Figure):

    def move_mechanic(self, board):
        # file, rank = self.temp_func_for_new_position_field_get()
        file = self.current_position.file
        rank = self.current_position.rank
        self.linear_movement(file, rank)

    def __str__(self):
        return 'R'