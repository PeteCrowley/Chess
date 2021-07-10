from Pieces.Piece import get_piece_on_square


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
    if piece.can_take(square):
        return 0
    observing_piece = piece.is_observed(square, return_piece=True)
    if not observing_piece:
        return 0
    if piece.is_protected(square) and piece.value <= observing_piece.value:
        return 0
    return -piece.value


def get_take_score(piece, square):
    if not piece.can_take(square):
        return 0
    taken_piece = get_piece_on_square(square)
    observing_piece = piece.is_observed(square, return_piece=True)
    is_protected = piece.is_protected(square)
    if not observing_piece:
        return taken_piece.value
    if is_protected and type(observing_piece).__name__ == "King":
        return observing_piece.value + taken_piece.value - piece.value
    return taken_piece.value - piece.value
