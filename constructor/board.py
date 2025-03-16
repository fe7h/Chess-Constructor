from abc import ABC, abstractmethod
from typing import Dict, Type
import copy

from constructor.figures import *
from constructor.response import StatusCode, Response
from constructor.utils import AttackedSquares, PriorityList


# settings
COLORS = {'white', 'black'}
PAWN_TRANSFORM_AREA = {'white':{Coord(8, i) for i in range(9)},
                       'black':{Coord(1, i) for i in range(9)}}
# ========


class OldBoard:
    def __init__(self):
        self.figures_data: Dict[Coord, Figure] = {}

    def add(self):
        pass

    def remove(self):
        # как вариант можно хранить сеты с обектмаи определеного класса фигур
        # создавая эти сеты через соотвецтвеные миксины и удалять эти обекты
        # в цикле из всех сетов при вызове этого метода
        # ну тогда подобный метод нужно и для адд релизовать,
        # в таком случаии оба эти метода нужно релизововать подобно all_moves_calculated,
        # только с подобием приритилиста только без приоритета
        pass

    def change(self):
        pass

    def multi_change(self):
        ...
        self.change()

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
    # и вынести её в миксин
    def make_a_move(self, old_position: Coord, new_position: Coord):
        # должен вызывать метод у фигуры который будет проверять
        # возможность хода и кидать ошибку если нельзя походить
        # и эта вот штука должна возрашать статус коды
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
        # !must return status codes
        # релизовать тоже через приорит лист
        # self.pawn_transform()
        # self.get_en_passant_area()
        self.all_moves_calculated()
        # self.is_checkmate()

    # для ракировки сдлетаь функцию которая на вход будет принимать любое количество пар фигур и координат и размешать их по ним
    # и сделать отдельную функцию для размещения и удаления фигуры


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
        # фигуры зависимы от этого метода
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
        # от части temp_en_passant_file работает как AttackedSquares
        # вынести AttackedSquares в более абстрактную реализацию
        # и сделать отдельно наследника от абтрактного класса под этот мексин
        self.temp_en_passant_file = {'black':dict(),'white':dict()}
        for figure in self.figures_data.values():
            if isinstance(figure, EnPassantCapturingFigure):
                color = 'black' if figure.color == 'white' else 'white'
                self.temp_en_passant_file[color].update({coord:figure for coord in figure.en_passant_trail})


# class ClassicMoveMethodsMixin(KingMixin, MoveMixin):
#     pass

class TransformMixin:
    # как то не клеиться методы для трансформации и для пешки вмести
    # надо как то разграничить
    # вообше методы для преврашения пешки как то криво релизованны
    # надо всю эту концепцию именно в рамках игры обдумать ещё раз
    # то пока среди всех методов и абстракций этот именно в лоб работает
    # возможно подобно кингмиксину надо сделать отдельную подкатигорию
    # либо вообше абстрактный класс для миксинов про конкретные фигуры
    # либо просто трансформацию вынести в абстрактный класс(правило) в фигурах
    # как с рокировкой, миксин для которой лишь вызывает метод у всех обектов класса
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
    # добавить make_a_castling
    def all_castling_calculated(self):
        # отправить через декоратор в all_moves_calculated
        # (нужно будет переписать тесты)
        for figure in self.figures_data.values():
            if isinstance(figure, Castling):
                figure.castlings_calculated(self)


class Board(MoveMixin, EnPassantMixin, CastlingMixin, TransformMixin, KingMixin, OldBoard):
    pass
