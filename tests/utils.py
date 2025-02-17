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
