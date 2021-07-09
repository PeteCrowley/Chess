from Pieces.Piece import get_piece_on_square

def taker(legal_move_list):
    captures = []
    for piece, moves in legal_move_list:
        piece_captures = []
        for move in moves:
            if piece.can_take(move)[0]:
                piece_captures.append(move)
        if len(piece_captures) > 0:
            captures.append((piece, piece_captures))
    return captures


def smart_taker(legal_move_list):
    captures = []
    for piece, moves in legal_move_list:
        piece_captures = []
        for move in moves:
            if not piece.can_take(move):
                continue
            if should_take(piece, move):
                piece_captures.append(move)
        if len(piece_captures) > 0:
            captures.append((piece, piece_captures))
    return captures


def should_take(piece, square):
    if not piece.is_observed(square):
        return True
    if piece.value <= get_piece_on_square(square).value:
        return True
    return False
