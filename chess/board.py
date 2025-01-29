from chess.figures import *


class AttackedSquares:
    def __init__(self, colors):
        self.__under_attack = {color: set() for color in colors}

    def update(self, figure: Figure):
        figure_color = figure.side
        for color in self.__under_attack:
            if color != figure_color:
                self.__under_attack[color].update(figure.pp)

    def clear(self):
        for color in self.__under_attack:
            self.__under_attack[color].clear()

    def get_attacked_squares(self, color: str | Figure):
        if isinstance(color, Figure):
            color = color.side
        return self.__under_attack.get(color)

class Board:

    __slots__ = ('figures_data', 'attacked_field_data')

    def __init__(self):
        self.figures_data = {} # это словарь!
        self.attacked_field_data = {'w': set(), 'b': set()}

    def all_possible_moves(self):#переминовать в all_attacked_field
        self.attacked_field_data = {'w': set(), 'b': set()}
        for key in self.figures_data:
            self.figures_data[key].potential_position()
            self.attacked_field_data[self.figures_data[key].side].update(self.figures_data[key].pp)

    def figures_arrangement(self):
        k = {'w': [10, 0], 'b': [60, 70]}
        for s in ('w', 'b'):
            for i in range(8):
                self.figures_data[i + k[s][0]] = Pawn(s, i + k[s][0], self)
                if i == 0 or i == 7:
                    self.figures_data[i + k[s][1]] = Rook(s, i + k[s][1], self)
                elif i == 1 or i == 6:
                    self.figures_data[i + k[s][1]] = Bishop(s, i + k[s][1], self)
                elif i == 2 or i == 5:
                    self.figures_data[i + k[s][1]] = Night(s, i + k[s][1], self)
                elif i == 3:
                    self.figures_data[i + k[s][1]] = Queen(s, i + k[s][1], self)
                else:
                    self.figures_data[i + k[s][1]] = King(s, i + k[s][1], self)
        self.all_possible_moves()

    def move(self, old_position, new_position):
        self.figures_data[old_position].position = new_position
        if self.figures_data[old_position].position == new_position:
            self.figures_data[new_position] = self.figures_data[old_position]
            del self.figures_data[old_position]
        self.all_possible_moves()
