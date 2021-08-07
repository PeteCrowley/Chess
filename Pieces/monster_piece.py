from Pieces.Piece import Piece
from Pieces.Piece import get_piece_on_square


class MonsterPiece(Piece):

    move_num = 0

    def __init__(self, board, team):
        super().__init__(board, team)

    def get_legal_moves(self, all_observed=False):
        if all_observed:
            return self.get_observed()
        elif MonsterPiece.move_num == 0:
            return self.get_monster_move_1()
        elif MonsterPiece.move_num == 1:
            return self.get_monster_move_2()

    def get_monster_move_1(self):
        return 'movelist'

    def get_monster_move_2(self):
        return 'movelist'

    def get_observed(self):
        return 'movelist'

    def legal_moves_after_move_1(self, square):
        old_pos = self.pos
        needs_to_take = get_piece_on_square(square)
        if needs_to_take:
            taken_piece_old_pos = needs_to_take.pos
            needs_to_take.pos = (0, 0)
            needs_to_take.is_taken = True
        self.pos = square
        for piece in Piece.White_Piece_List:
            if piece.get_monster_move_2():
                self.pos = old_pos
                if needs_to_take:
                    needs_to_take.pos = taken_piece_old_pos
                    needs_to_take.is_taken = False
                return True
        self.pos = old_pos
        if needs_to_take:
            needs_to_take.pos = taken_piece_old_pos
            needs_to_take.is_taken = False
        return False

