from constructor.figures import Coord, AbstractPawn, EnPassantCapturingFigure
from constructor import figures


COLORS = {'white', 'black'}
WHITE = 'white'
BLACK = 'black'


class King(figures.AbstractKing):
    def move_mechanic(self, board, *args, **kwargs):
            for modifier_1 in (-1, 1):
                for modifier_2 in (-1, 1):
                    file_coord = self.position.file + modifier_1
                    rank_coord = self.position.rank + modifier_2
                    self.valid_move_add(board, figures.Coord(file_coord, rank_coord))
            for coord in (-1, 1):
                file_coord = self.position.file + coord
                self.valid_move_add(board, figures.Coord(file_coord, self.position.rank))
                rank_coord = self.position.rank + coord
                self.valid_move_add(board, figures.Coord(self.position.file, rank_coord))

    def __str__(self):
        return 'K'


class Rook(figures.Figure):
    def __str__(self):
        return 'R'

    def move_mechanic(self, board, *args, **kwargs):
        for modifier in (-1, 1):
            for i in range(1, 8):
                new_file = self.position.file + i * modifier
                if not self.valid_move_add(board, figures.Coord(new_file, self.position.rank)):
                    break
            for i in range(1, 8):
                new_rank = self.position.rank + i * modifier
                if not self.valid_move_add(board, figures.Coord(self.position.file, new_rank)):
                    break


class EnPassantRook(Rook, EnPassantCapturingFigure):
    def back_trail(self):
        pass


class Pawn(AbstractPawn):
    def __str__(self):
        return 'P'

    def back_trail(self):
        pass

    def move_mechanic(self, board, *args, **kwargs):
        pass
        # if self.valid_move_add(board, figures.Coord(self.position.file + 1, self.position.rank)):
        #     self.valid_move_add(board, figures.Coord(self.position.file + 2, self.position.rank))
        #
        # self.valid_move_add(board, figures.Coord(self.position.file + 1, self.position.rank))


class PawnOnlyWithMoveNotEqualAttack(figures.MoveNotEqualAttack):
    def __str__(self):
        return 'P'

    def move_mechanic(self, board, *args, **kwargs):
        for modifier in range(1,3):
            file_coord = self.position.file + modifier
            rank_coord = self.position.rank
            new_position = figures.Coord(file=file_coord, rank=rank_coord)

            if not self.for_move(board, new_position):
                break

        for modifier in (-1,1):
            file_coord = self.position.file + 1
            rank_coord = self.position.rank + modifier
            new_position = figures.Coord(file=file_coord, rank=rank_coord)

            self.for_attack(board, new_position)


class CastlingKing(King, figures.Castling):
    def castling_mechanic(self, figure, board, *args, **kwargs):
        target_coord = figure.position
        modifier_direction = -1 if target_coord.rank == 1 else 1

        if figure.special_move:
            if all(map(lambda coord: not coord in board.attacked_field_data.get_attacked_squares(self),
                       (figures.Coord(file=self.position.file,
                                      rank=self.position.rank + rank * modifier_direction) for rank in range(3)))):

                self_old_coord = self.position
                self_new_coord = Coord(file=self.position.file,
                                       rank=self.position.rank + 2 * modifier_direction)

                figure_old_coord = figure.position
                figure_new_coord = Coord(file=figure.position.file,
                                         rank=figure.position.rank + 2 * modifier_direction * -1 + (1 if modifier_direction == -1 else 0))

                self.valid_castling[target_coord] = {
                    (self_old_coord, self_new_coord),
                    (figure_old_coord, figure_new_coord)
                }

    def castling_target_type_set(self):
        return Rook
