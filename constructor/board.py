from abc import ABC, abstractmethod
from typing import Dict, Type
import copy

from constructor.figures import *
from constructor.response import StatusCode, Response


# settings
COLORS = {'white', 'black'}
PAWN_TRANSFORM_AREA = {'white':{Coord(8, i) for i in range(9)},
                       'black':{Coord(1, i) for i in range(9)}}
# ========

# ОБЕЗЛИЧИТЬ КЛАСС И СДЕЛАТЬ ЕГО БОЛЕЕ ВАРИАТИВНЫМ
class AttackedSquares:
    def __init__(self, colors):
        self.__under_attack = {color: set() for color in colors}

    def update(self, figure: Figure):
        figure_color = figure.color
        for color in self.__under_attack:
            if color != figure_color:
                self.__under_attack[color].update(figure.valid_moves.get())

    def clear(self):
        for color in self.__under_attack:
            self.__under_attack[color].clear()

    def get_attacked_squares(self, color: str | Figure):
        if isinstance(color, Figure):
            color = color.color
        return self.__under_attack.get(color)

    def under_attack(self):
        pass
#     добавить метод для in


class OldBoard:
    # должен включать:
    # данные о разположении фигур (лучше сделать через двойной дикт)
    # метод для смены позиции (make_a_move перенести в MoveMixin и он от туда будет вызвать метод удаления фигуры и метод смены позиции)
    # метод для сменые сразу нескольких позиций
    # метод удаления фигуры
    # метод добавления фигур
    # обработчик конца хода
    # обработчик начала хода
    # метод для расположения фигур в начале партии
    # скорее всего так же должен дублировать с конфига размеры доски и валидировать по ним, а не в методе фигур
    def __init__(self):
        self.figures_data: Dict[Coord, Figure] = {}

    # @abstractmethod
    def figures_arrangement(self):
        # k = {'w': [10, 0], 'b': [60, 70]}
        # for s in ('w', 'b'):
        #     for i in range(8):
        #         self.figures_data[i + k[s][0]] = Pawn(s, i + k[s][0], self)
        #         if i == 0 or i == 7:
        #             self.figures_data[i + k[s][1]] = Rook(s, i + k[s][1], self)
        #         elif i == 1 or i == 6:
        #             self.figures_data[i + k[s][1]] = Bishop(s, i + k[s][1], self)
        #         elif i == 2 or i == 5:
        #             self.figures_data[i + k[s][1]] = Night(s, i + k[s][1], self)
        #         elif i == 3:
        #             self.figures_data[i + k[s][1]] = Queen(s, i + k[s][1], self)
        #         else:
        #             self.figures_data[i + k[s][1]] = King(s, i + k[s][1], self)
        for figure in self.figures_data.values():
            if isinstance(figure, AbstractKing):
                self.kings_list.add(figure)
        self.all_moves_calculated()

    # переписать всю функцию в более явном виде
    def make_a_move(self, old_position: Coord, new_position: Coord):
        if old_position in self.figures_data:
            figure = self.figures_data[old_position]
            figure.position = new_position
            if self.figures_data[old_position].position == new_position:
                self.figures_data[new_position] = self.figures_data[old_position]
                # переписать взятие фигур в явном виде
                del self.figures_data[old_position]
            if isinstance(figure, EnPassantCapturingFigure):
                if new_position in self.temp_en_passant_file[figure.color]:
                    del self.figures_data[self.temp_en_passant_file[figure.color][new_position].position]
            self.all_moves_calculated() #убрать от сюда
        return Response(StatusCode.WRONG_MOVE)

    def end_of_turn(self):
        """must return status codes"""
        # self.pawn_transform()
        # self.get_en_passant_area()
        self.all_moves_calculated()
        # self.is_checkmate()

    # для ракировки сдлетаь функцию которая на вход будет принимать любое количество пар фигур и координат и размешать их по ним
    # и сделать отдельную функцию для размещения и удаления фигуры


# вынести в отдельный файл и довести до ума
class PriorityList:
    def __init__(self):
        self.__data = dict()

    def set(self, priority, obj):
        self.__data[priority] = obj
        self._sort()

    def _sort(self):
        self.__data = {key: self.__data[key] for key in sorted(self.__data)}

    def __iter__(self):
        return iter(tuple(val for val in self.__data.values()))

    def __call__(self, priority):
        def wrapper(func):
            self.set(priority, func)
            return func
        return wrapper


class MoveMixin:

    move_mixin_priority = PriorityList()

    def __init__(self):
        self.attacked_field_data = AttackedSquares(COLORS)
        super().__init__()

    @move_mixin_priority(0)
    def _attacked_field_data_clear(self):
        self.attacked_field_data.clear()

    @move_mixin_priority(10)
    def _all_moves_calculated_call(self):
        for figure in self.figures_data.values():
            figure.moves_calculated(self)
            self.attacked_field_data.update(figure)

    def all_moves_calculated(self):
        # self._attacked_field_data_clear()
        # self._all_moves_calculated_call()
        # all_accounting_attacked_field()
        for func in self.move_mixin_priority:
            func(self)


class KingMixin:
    def __init__(self):
        self.kings_list = set()
        self.deep = True
        super().__init__()

    def check_validation(self, figure: Figure, position: Coord):
        """проверяет не будет ли шаха королю если передвинуть свою фигуру
        Копирует доску и совершает на ней ход если всё норм то вносит его в
        список доступных ходов
        """
        if self.deep:
            deep_board = copy.deepcopy(self)
            deep_board.deep = False
            deep_figure = deep_board.figures_data.pop(figure.position)
            deep_board.figures_data[position] = deep_figure

            deep_board.all_moves_calculated()
            for king in deep_board.kings_list:
                if king.color == figure.color:
                    if king.position in deep_board.attacked_field_data.get_attacked_squares(king):
                        return True
        return False

    def temp_func_is_checkmate(self):
        """функция конца хода
        провереят есть ли сейчас шах или мат королю"""
        for king in self.kings_list:
            if king.valid_moves.blank == set(): # есть ли ходы у короля
                for figure in self.figures_data.values():
                    if figure.color == king.color and figure.valid_moves.blank != set(): # есть ли ходы у фигур
                        return 'no checkmate'
                    if king.position in self.attacked_field_data.get_attacked_squares(king): # король под атакой
                        return 'checkmate'
                    return 'stalemate'
                return 'no checkmate'

    @MoveMixin.move_mixin_priority(100)
    def all_accounting_attacked_field(self):
        """убирает все атаковные поля с мувсетов всех королей"""
        for king in self.kings_list:
            king.temp_func_for_minus_attacked_fields(self)


class EnPassantMixin:
    def __init__(self):
        self.temp_en_passant_file = {'black':dict(),'white':dict()} #{color: {coord:figure, ...}, ...}
        super().__init__()

    def temp_get_en_passant_area(self):
        self.temp_en_passant_file = {'black':dict(),'white':dict()}
        for figure in self.figures_data.values():
            if isinstance(figure, EnPassantCapturingFigure):
                color = 'black' if figure.color == 'white' else 'white'
                self.temp_en_passant_file[color].update({coord:figure for coord in figure.en_passant_trail})


# class ClassicMoveMethodsMixin(KingMixin, MoveMixin):
#     pass

class TransformMixin:
    def __init__(self):
        self.temp_pawn_transform_area = PAWN_TRANSFORM_AREA
        super().__init__()

    def temp_func_pawn_transform(self):
        for figure in self.figures_data.values():
            if isinstance(figure, AbstractPawn):
                if figure.position in self.temp_pawn_transform_area.get(figure.color):
                    return f'pawn {str(figure.position)} must transform'

    def temp_transform(self, position: Coord, figure: Type[Figure]):
        if position in self.figures_data:
            old_figure = self.figures_data.pop(position)
            new_figure = figure(color=old_figure.color,position=old_figure.position)
            self.figures_data[new_figure.position] = new_figure
            # добавить запрет на фигуры для трансформации
        return 'bad position'


class CastlingMixin:
    def all_castling_calculated(self):
        for figure in self.figures_data.values():
            if isinstance(figure, Castling):
                figure.castlings_calculated(self)


class Board(MoveMixin, EnPassantMixin, CastlingMixin, TransformMixin, KingMixin, OldBoard):
    pass
