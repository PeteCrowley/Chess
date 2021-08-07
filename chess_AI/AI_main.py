from Pieces.Piece import Piece
import random
import time
from chess_AI import Taker_AI
from chess_AI.Defense_AI import safe_mover, safe_move_score, get_take_score
from chess_AI.Attack_AI import is_checkmate_after_move, is_check_after_move


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
    piece, moves = random.choice(move_list)
    move = random.choice(moves)
    time.sleep(1)
    move_count = piece.move(move, move_count)
    return move_count


def good_move(legal_move_list, move_count):
    if move_count >= 3:
        for piece, moves in legal_move_list:
            for move in moves:
                if is_checkmate_after_move(piece, move):
                    return piece.move(move, move_count)
    good_captures = Taker_AI.smart_taker(legal_move_list)
    good_moves = safe_mover(legal_move_list)
    if good_captures != []:
        move_list = good_captures
    elif good_moves != []:
        move_list = good_moves
    else:
        move_list = legal_move_list
    return random_move(move_list, move_count)


def get_move_score(piece, move):
    score = 0
    score += safe_move_score(piece, move)
    score += get_take_score(piece, move)
    score += is_check_after_move(piece, move)
    score += is_checkmate_after_move(piece, move)
    return score


def move_by_score(legal_move_list, move_count):
    scored_move_list = []
    for piece, moves in legal_move_list:
        for move in moves:
            score = get_move_score(piece, move)
            scored_move_list.append((score, (piece, move)))
    random.shuffle(scored_move_list)
    scored_move_list.sort(key=lambda x: x[0], reverse=True)
    piece, best_move = scored_move_list[0][1]
    move_count = piece.move(best_move, move_count)
    return move_count


def AI_Move(team, move_count):
    time.sleep(0.02)
    moves = get_all_legal_moves(team)
    return move_by_score(moves, move_count)
