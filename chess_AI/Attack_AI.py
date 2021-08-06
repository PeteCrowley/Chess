from Pieces.Piece import get_piece_on_square
from Pieces.Piece import Piece


def is_checkmate_after_move(piece, square):
    old_pos = piece.pos
    if piece.team == 'white':
        king = Piece.Black_Piece_List[0]
    else:
        king = Piece.White_Piece_List[0]
    needs_to_take = get_piece_on_square(square)
    if needs_to_take:
        taken_piece_old_pos = needs_to_take.pos
        needs_to_take.pos = (0, 0)
        needs_to_take.is_taken = True
    piece.pos = square
    if king.is_in_checkmate():
        score = 999999
    else:
        score = 0
    piece.pos = old_pos
    if needs_to_take:
        needs_to_take.pos = taken_piece_old_pos
        needs_to_take.is_taken = False

    return score


def is_check_after_move(piece, square):
    old_pos = piece.pos
    if piece.team == 'white':
        king = Piece.Black_Piece_List[0]
    else:
        king = Piece.White_Piece_List[0]
    needs_to_take = get_piece_on_square(square)
    if needs_to_take:
        taken_piece_old_pos = needs_to_take.pos
        needs_to_take.is_taken = True
    piece.pos = square
    if king.is_in_check():
        score = 1
    else:
        score = 0
    piece.pos = old_pos
    if needs_to_take:
        needs_to_take.pos = taken_piece_old_pos
        needs_to_take.is_taken = False

    return score
