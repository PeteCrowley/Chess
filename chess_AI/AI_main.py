from Pieces.Piece import Piece
import random
import time


def get_all_legal_moves(board, team):
    all_moves = []
    if team == 'white':
        piece_list = Piece.White_Piece_List
    else:
        piece_list = Piece.Black_Piece_List
    for piece in piece_list:
        legal_moves = piece.get_legal_moves(board)
        if len(legal_moves) > 0:
            all_moves.append((piece, legal_moves))
    return all_moves


def random_move(board, move_list, move_count):
    time.sleep(0.1)
    piece, moves = random.choice(move_list)
    move = random.choice(moves)
    move_count = piece.move(board, move, move_count)
    return move_count
