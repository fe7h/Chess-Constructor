from abc import ABC, abstractmethod


class Figure(ABC):

    def __init__(self, side, position, board):
        self.side = side  # w,b
        self.__position = position  # Num in pseudo-octal system, where 'decade' is index in y and 'units' is index in x (0-7)
        self.file, self.rank = self.temp_func_for_new_position_field_get()
        self.board = board
        self.pp = []  # pp - potential position
        self.special_move = True

    def temp_func_for_new_position_field_get(self):
        return self.__position // 10, self.__position % 10

    @staticmethod
    def temp_func_for_old_coord_format_set(file, rank):
        return file * 10 + rank

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        if new_position in self.pp:
            self.special_move = False
            self.__position = new_position

    def position_check(self, position):
        return position >= 0 and position // 10 <= 7 and position % 10 <= 7 and position not in self.board.figures_data

    def potential_position_add(self, position):
        if self.position_check(position):
            self.pp.append(position)
            return True
        elif position in self.board.figures_data:
            if self.side != self.board.figures_data.get(position).side:
                self.pp.append(position)
            else:
                self.board.attacked_field_data[self.side].add(position)
            return False
        return None

    @abstractmethod
    def position_calculated(self, *args, **kwargs):
        pass

    def potential_position(self, *args, **kwargs):
        self.pp.clear()
        self.position_calculated(*args, **kwargs)

    def linear_movement(self, file, rank):
        for modifier in (-1, 1):
            for coord in range(1, 8):
                file_coord = file + coord * modifier
                if not self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank)):
                    break
            for coord in range(1, 8):
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

    @abstractmethod
    def __str__(self):
        pass


class Night(Figure):

    def position_calculated(self):
        file, rank = self.temp_func_for_new_position_field_get()

        for i in (0, 1):
            for modifier_1 in (-2+i, 2-i):
                for modifier_2 in (-1-i, 1+i):
                    file_coord = file + modifier_1
                    rank_coord = rank + modifier_2
                    self.potential_position_add(self.temp_func_for_old_coord_format_set(file_coord, rank_coord))

    def __str__(self):
        return 'N'


class Queen(Figure):

    def position_calculated(self):
        file, rank = self.temp_func_for_new_position_field_get()
        self.diagonal_movement(file, rank)
        self.linear_movement(file, rank)

    def __str__(self):
        return 'Q'


class Bishop(Figure):

    def position_calculated(self):
        file, rank = self.temp_func_for_new_position_field_get()
        self.diagonal_movement(file, rank)

    def __str__(self):
        return 'B'


# class SpecialMoveFigure(Figure):
#
#     def __init__(self, side, position, board):
#         super().__init__(side, position, board)
#         self.special_move = True
#
#     @Figure.position.setter
#     def position(self, new_position):
#         if new_position in self.pp:
#             #сюда впихнуть проверку для взятия на подходе
#             self.special_move = False
#             Figure.position.fset(self, new_position)


class King(Figure):

    # def position_check(self, position):
    #     return super().position_check(position) and not all(
    #         position in self.board.attacked_field_data[side]
    #         for side in self.board.attacked_field_data if side != self.side)

    def position_calculated(self):
        file, rank = self.temp_func_for_new_position_field_get()
        self.one_square_movement(file, rank)

    def temp_func_for_take_attacked_field_data(self):
        side = 'b' if self.side == 'w' else 'w'
        self.pp = list(set(self.pp) - self.board.attacked_field_data[side])

    def __str__(self):
        return 'K'


class Rook(Figure):

    def position_calculated(self):
        file, rank = self.temp_func_for_new_position_field_get()
        self.linear_movement(file, rank)

    def __str__(self):
        return 'R'


class Pawn(Figure):

    @Figure.position.setter #переписать в более вменяемом виде, то некотріе проверки пару раз проходит
    def position(self, new_position):
        self.potential_position(attack=False)
        if new_position in self.pp:
            if self.special_move:
                if abs(new_position - self.position) >= 20:
                    for i in (-1, 1):
                        if new_position + i in self.board.figures_data and isinstance(self.board.figures_data[new_position + i], Pawn) and self.board.figures_data[new_position+i].side != self.side:
                            self.board.figures_data[new_position + i].en_passant = [new_position, self.pp[-2], 0]
                self.special_move = False
            elif 'en_passant' in self.__dict__ and new_position == self.en_passant[1]:
                del self.board.figures_data[self.en_passant[0]]
                del self.en_passant
            Figure.position.fset(self, new_position)

    def position_calculated(self, attack=True):

        self.pp = []

        if attack:

            if 'en_passant' in self.__dict__:
                self.en_passant[2] += 1
                if self.en_passant[2] == 2:
                    del self.en_passant

            s = 1 if self.side == 'w' else -1

            for i in (-1, 1):
                po = self.position + 10 * s + i
                if po % 10 <= 7:
                    self.pp.append(po)
        else:

            if 'en_passant' in self.__dict__:
                self.pp.append(self.en_passant[1])

            s = 1 if self.side == 'w' else -1

            po = self.position + 10*s

            for i in (-1, 1):
                if po + i in self.board.figures_data and self.board.figures_data[po + i].side != self.side:
                    self.pp.append(po + i)

            if po not in self.board.figures_data:
                self.pp.append(po)
                if self.special_move:
                    po = self.position + 20 * s
                    if po not in self.board.figures_data:
                        self.pp.append(po)

    def __str__(self):
        return 'P'


class Dummy(Figure):

    def position_calculated(self):
        file, rank = self.temp_func_for_new_position_field_get()
        self.one_square_movement(file, rank)

    def __str__(self):
        return 'D'
