from Pieces.Piece import get_piece_on_square, Piece
import time


def safe_mover(legal_move_list):
    safe_moves = []
    for piece, moves in legal_move_list:
        piece_safe_moves = []
        for move in moves:
            if safe_move_score(piece, move) == 0:
                piece_safe_moves.append(move)
        if len(piece_safe_moves) > 0:
            safe_moves.append((piece, piece_safe_moves))
    return safe_moves


def safe_move_score(piece, square):
    if piece.team == 'white':
        piece_list = Piece.White_Piece_List
    else:
        piece_list = Piece.Black_Piece_List
    score = 0
    old_pos = piece.pos
    piece.pos = square
    for hanging_piece in piece_list:
        move_score = 0
        if type(hanging_piece).__name__ == "King":
            continue
        observing_piece = hanging_piece.is_observed(hanging_piece.pos, return_piece=True)
        if not observing_piece:
            continue
        elif hanging_piece.is_protected(square) and hanging_piece.value <= observing_piece.value:
            continue
        elif hanging_piece.is_protected(square):
            score -= hanging_piece.value - observing_piece.value
            continue
        move_score -= hanging_piece.value
        if move_score < score:
            score = move_score
    piece.pos = old_pos
    return score * 10


def get_take_score(piece, square):
    if not piece.can_take(square):
        return 0
    taken_piece = get_piece_on_square(square)
    observing_piece = piece.is_observed(square, return_piece=True)
    is_protected = piece.is_protected(square)
    if not observing_piece or (is_protected and type(observing_piece).__name__ == "King"):
        take_score = taken_piece.value
    elif is_protected:
        take_score = observing_piece.value + taken_piece.value - piece.value
    else:
        take_score = taken_piece.value - piece.value
    return take_score * 10
