from Pieces.Piece import Piece
import random
import time
from chess_AI import Taker_AI


def get_all_legal_moves(team):
    all_moves = []
    if team == 'white':
        piece_list = Piece.White_Piece_List
    else:
        piece_list = Piece.Black_Piece_List
    for piece in piece_list:
        legal_moves = piece.get_legal_moves()
        if len(legal_moves) > 0:
            all_moves.append((piece, legal_moves))
    return all_moves


def random_move(move_list, move_count):
    time.sleep(0.1)
    piece, moves = random.choice(move_list)
    move = random.choice(moves)
    move_count = piece.move(move, move_count)
    return move_count


def good_move(legal_move_list, move_count):
    captures = Taker_AI.smart_taker(legal_move_list)
    if captures != []:
        move_list = captures
    else:
        move_list = legal_move_list
    return random_move(move_list, move_count)


def AI_Move(team, move_count):
    moves = get_all_legal_moves(team)
    return good_move(moves, move_count)
