from Pieces.Piece import get_piece_on_square


def safe_mover(legal_move_list):
    safe_moves = []
    for piece, moves in legal_move_list:
        piece_safe_moves = []
        for move in moves:
            if should_move(piece, move):
                piece_safe_moves.append(move)
        if len(piece_safe_moves) > 0:
            safe_moves.append((piece, piece_safe_moves))
    return safe_moves


def should_move(piece, square):
    observing_piece = piece.is_observed(square, return_piece=True)
    if not observing_piece:
        return True
    if piece.is_protected(square) and piece.value <= observing_piece.value:
        return True
    return False


def should_take(piece, square):
    observing_piece = piece.is_observed(square, return_piece=True)
    if not observing_piece:
        return True
    if piece.value <= get_piece_on_square(square).value:
        return True
    if piece.is_protected(square) and piece.value <= observing_piece.value:
        return True
    return False