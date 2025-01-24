from abc import ABC, abstractmethod


class Figure(ABC):

    def __init__(self, side, position, board):
        self.side = side  # w,b
        self.__position = position  # Num in pseudo-octal system, where 'decade' is index in y and 'units' is index in x
        self.board = board
        self.pp = []  # pp - potential position

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        if new_position in self.pp:
            self.__position = new_position

    def position_check(self, po):
        return po >= 0 and po // 10 <= 7 and po % 10 <= 7 and po not in self.board.figures_data

    @abstractmethod
    def potential_position(self):
        l = len(self.move_pattern)

        if l == 1 or l == 3:

            for i in (-10, 10):
                for s in range(1, self.move_pattern[0]):
                    po = self.position + s * i
                    if self.position_check(po):# and po % 10 == self.position % 10:
                        self.pp.append(po)
                    elif po in self.board.figures_data:
                        if self.side != self.board.figures_data[po].side:
                            self.pp.append(po)
                            break
                        else:
                            self.board.attacked_field_data[self.side].update([po])
                            break
                    else:
                        break

            for j in (-1, 1):
                for s in range(1, self.move_pattern[0]):
                    po = self.position + s * j
                    if self.position_check(po):# and po // 10 == self.position // 10:
                        self.pp.append(po)
                    elif po in self.board.figures_data:
                        if self.side != self.board.figures_data[po].side:
                            self.pp.append(po)
                            break
                        else:
                            self.board.attacked_field_data[self.side].update([po])
                            break
                    else:
                        break

        if l == 2 or l == 3:

            for i in (-10, 10):
                for j in (-1, 1):
                    for s in range(1, self.move_pattern[0]):
                        po = self.position + s * i + s * j
                        if self.position_check(po):
                            self.pp.append(po)
                        elif po in self.board.figures_data:
                            if self.side != self.board.figures_data[po].side:
                                self.pp.append(po)
                                break
                            else:
                                self.board.attacked_field_data[self.side].update([po])
                                break
                        else:
                            break
        del l

    @abstractmethod
    def __str__(self):
        pass


class Night(Figure):

    @staticmethod
    def position_check(po):
        return po >= 0 and po // 10 <= 7 and po % 10 <= 7

    def potential_position(self):
        # можно переписать удобнее
        for i in (-10, 10):
            for j in (-1, 1):
                for s in range(1, 2):
                    po = self.position + s * i + s * j
                    if self.position_check(po):
                        self.pp.append(po)
                    elif po in self.board.figures_data:
                        if self.side != self.board.figures_data[po].side:
                            self.pp.append(po)
                            break
                        else:
                            self.board.attacked_field_data[self.side].update([po])
                            break
                    else:
                        break
        self.pp = list(map(lambda x: x%10 - self.position%10 + x, self.pp)) + list(map(lambda x: (x//10-self.position//10)*10 + x, self.pp))
        t = self.pp * 1
        for i in t:
            if i in self.board.figures_data and self.side == self.board.figures_data[i].side:
                self.board.attacked_field_data[self.side].update([i])
                self.pp.remove(i)
        del t

    def __str__(self):
        return 'N'


class Queen(Figure):

    def potential_position(self):
        for i in (-10, 10):
            for s in range(1, 8):
                po = self.position + s * i
                if self.position_check(po):  # and po % 10 == self.position % 10:
                    self.pp.append(po)
                elif po in self.board.figures_data:
                    if self.side != self.board.figures_data[po].side:
                        self.pp.append(po)
                        break
                    else:
                        self.board.attacked_field_data[self.side].update([po])
                        break
                else:
                    break

        for j in (-1, 1):
            for s in range(1, 8):
                po = self.position + s * j
                if self.position_check(po):  # and po // 10 == self.position // 10:
                    self.pp.append(po)
                elif po in self.board.figures_data:
                    if self.side != self.board.figures_data[po].side:
                        self.pp.append(po)
                        break
                    else:
                        self.board.attacked_field_data[self.side].update([po])
                        break
                else:
                    break

        for i in (-10, 10):
            for j in (-1, 1):
                for s in range(1, 8):
                    po = self.position + s * i + s * j
                    if self.position_check(po):
                        self.pp.append(po)
                    elif po in self.board.figures_data:
                        if self.side != self.board.figures_data[po].side:
                            self.pp.append(po)
                            break
                        else:
                            self.board.attacked_field_data[self.side].update([po])
                            break
                    else:
                        break


    def __str__(self):
        return 'Q'


class Bishop(Figure):

    def potential_position(self):
        for i in (-10, 10):
            for j in (-1, 1):
                for s in range(1, 8):
                    po = self.position + s * i + s * j
                    if self.position_check(po):
                        self.pp.append(po)
                    elif po in self.board.figures_data:
                        if self.side != self.board.figures_data[po].side:
                            self.pp.append(po)
                            break
                        else:
                            self.board.attacked_field_data[self.side].update([po])
                            break
                    else:
                        break

    def __str__(self):
        return 'B'


class SpecialMoveFigure(Figure):

    def __init__(self, side, position, board):
        super().__init__(side, position, board)
        self.special_move = True

    @Figure.position.setter
    def position(self, new_position):
        if new_position in self.pp:
            #сюда впихнуть проверку для взятия на подходе
            self.special_move = False
            Figure.position.fset(self, new_position)


class King(SpecialMoveFigure):

    def potential_position(self):
        for i in (-10, 10):
            for s in range(1, 2):
                po = self.position + s * i
                if self.position_check(po):# and po % 10 == self.position % 10:
                    self.pp.append(po)
                elif po in self.board.figures_data:
                    if self.side != self.board.figures_data[po].side:
                        self.pp.append(po)
                        break
                    else:
                        self.board.attacked_field_data[self.side].update([po])
                        break
                else:
                    break

        for j in (-1, 1):
            for s in range(1, 2):
                po = self.position + s * j
                if self.position_check(po):# and po // 10 == self.position // 10:
                    self.pp.append(po)
                elif po in self.board.figures_data:
                    if self.side != self.board.figures_data[po].side:
                        self.pp.append(po)
                        break
                    else:
                        self.board.attacked_field_data[self.side].update([po])
                        break
                else:
                    break

        for i in (-10, 10):
            for j in (-1, 1):
                for s in range(1, 2):
                    po = self.position + s * i + s * j
                    if self.position_check(po):
                        self.pp.append(po)
                    elif po in self.board.figures_data:
                        if self.side != self.board.figures_data[po].side:
                            self.pp.append(po)
                            break
                        else:
                            self.board.attacked_field_data[self.side].update([po])
                            break
                    else:
                        break

    def __str__(self):
        return 'K'


class Rook(SpecialMoveFigure):

    def potential_position(self):
        for i in (-10, 10):
            for s in range(1, 8):
                po = self.position + s * i
                if self.position_check(po):# and po % 10 == self.position % 10:
                    self.pp.append(po)
                elif po in self.board.figures_data:
                    if self.side != self.board.figures_data[po].side:
                        self.pp.append(po)
                        break
                    else:
                        self.board.attacked_field_data[self.side].update([po])
                        break
                else:
                    break

        for j in (-1, 1):
            for s in range(1, 8):
                po = self.position + s * j
                if self.position_check(po):# and po // 10 == self.position // 10:
                    self.pp.append(po)
                elif po in self.board.figures_data:
                    if self.side != self.board.figures_data[po].side:
                        self.pp.append(po)
                        break
                    else:
                        self.board.attacked_field_data[self.side].update([po])
                        break
                else:
                    break

    def __str__(self):
        return 'R'


class Pawn(SpecialMoveFigure):

    @SpecialMoveFigure.position.setter #переписать в более вменяемом виде, то некотріе проверки пару раз проходит
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

    def potential_position(self, attack=True):

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

    def potential_position(self):
        for i in (-10, 10):
            for s in range(1, 1):
                po = self.position + s * i
                if self.position_check(po):# and po % 10 == self.position % 10:
                    self.pp.append(po)
                elif po in self.board.figures_data:
                    if self.side != self.board.figures_data[po].side:
                        self.pp.append(po)
                        break
                    else:
                        self.board.attacked_field_data[self.side].update([po])
                        break
                else:
                    break

        for j in (-1, 1):
            for s in range(1, 1):
                po = self.position + s * j
                if self.position_check(po):# and po // 10 == self.position // 10:
                    self.pp.append(po)
                elif po in self.board.figures_data:
                    if self.side != self.board.figures_data[po].side:
                        self.pp.append(po)
                        break
                    else:
                        self.board.attacked_field_data[self.side].update([po])
                        break
                else:
                    break

        for i in (-10, 10):
            for j in (-1, 1):
                for s in range(1, 1):
                    po = self.position + s * i + s * j
                    if self.position_check(po):
                        self.pp.append(po)
                    elif po in self.board.figures_data:
                        if self.side != self.board.figures_data[po].side:
                            self.pp.append(po)
                            break
                        else:
                            self.board.attacked_field_data[self.side].update([po])
                            break
                    else:
                        break

    def __str__(self):
        return 'D'

    # def position_check(self,pp):
    #     return super().position_check(pp) and pp < 50
