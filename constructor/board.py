from abc import ABC, abstractmethod
from typing import Dict
import copy

from constructor.figures import *
from constructor.response import StatusCode, Response


# settings
COLORS = {'white', 'black'}
# ========


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


class Board:

    __slots__ = ('figures_data', 'attacked_field_data', 'kings_list', 'deep')

    def __init__(self):
        self.figures_data: Dict[Coord, Figure] = {}
        # self.attacked_field_data = {'w': set(), 'b': set()}
        self.attacked_field_data = AttackedSquares(COLORS)
        self.kings_list = set()
        self.deep = True

    def all_moves_calculated(self):
        self.attacked_field_data.clear()
        for coord in self.figures_data:
            figure = self.figures_data.get(coord)
            figure.moves_calculated(self)
            self.attacked_field_data.update(figure)

    def check_validation(self, figure: Figure, position: Coord):
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

    def make_a_move(self, old_position: Coord, new_position: Coord):
        if old_position in self.figures_data:
            self.figures_data[old_position].position = new_position
            if self.figures_data[old_position].position == new_position:
                self.figures_data[new_position] = self.figures_data[old_position]
                del self.figures_data[old_position]
            self.all_moves_calculated()
        return Response(StatusCode.WRONG_MOVE)
