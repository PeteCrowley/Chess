from chess_AI.Defense_AI import get_take_score


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
            if get_take_score(piece, move) >= 0:
                piece_captures.append(move)
        if len(piece_captures) > 0:
            captures.append((piece, piece_captures))
    return captures

