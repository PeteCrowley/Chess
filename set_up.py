import pygame.sysfont

from Pieces.King import King
from Pieces.Queen import Queen
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn
from Pieces.Piece import Piece


def set_board(board):
    King(board, team='white')
    Queen(board, team='white')
    Bishop(board, team='white', kings_or_queens='kings')
    Bishop(board, team='white', kings_or_queens='queens')
    Knight(board, team='white', kings_or_queens='kings')
    Knight(board, team='white', kings_or_queens='queens')
    Rook(board, team='white', kings_or_queens='kings')
    Rook(board, team='white', kings_or_queens='queens')
    Pawn(board, team='white', start_file='a')
    Pawn(board, team='white', start_file='b')
    Pawn(board, team='white', start_file='c')
    Pawn(board, team='white', start_file='d')
    Pawn(board, team='white', start_file='e')
    Pawn(board, team='white', start_file='f')
    Pawn(board, team='white', start_file='g')
    Pawn(board, team='white', start_file='h')

    King(board, team='black')
    Queen(board, team='black')
    Bishop(board, team='black', kings_or_queens='kings')
    Bishop(board, team='black', kings_or_queens='queens')
    Knight(board, team='black', kings_or_queens='kings')
    Knight(board, team='black', kings_or_queens='queens')
    Rook(board, team='black', kings_or_queens='kings')
    Rook(board, team='black', kings_or_queens='queens')
    Pawn(board, team='black', start_file='a')
    Pawn(board, team='black', start_file='b')
    Pawn(board, team='black', start_file='c')
    Pawn(board, team='black', start_file='d')
    Pawn(board, team='black', start_file='e')
    Pawn(board, team='black', start_file='f')
    Pawn(board, team='black', start_file='g')
    Pawn(board, team='black', start_file='h')


def reset_board():
    for i in range(len(Piece.All_Pieces)):
        piece = Piece.All_Pieces[i]
        if i > 31:
            piece.is_taken = True
            continue
        piece.is_taken = False
        piece.pos = piece.start_square
        piece.has_moved = False
    Piece.All_Pieces = Piece.All_Pieces[:32]
    Piece.White_Piece_List = Piece.White_Piece_List[:16]
    Piece.Black_Piece_List = Piece.Black_Piece_List[:16]


def check_for_result(turn, pos_dict):
    result = None
    for piece in Piece.All_Pieces:
        if type(piece).__name__ == 'King' or type(piece).__name__ == 'MonsterKing':
            if piece.is_in_checkmate():
                if piece.team == 'white':
                    result = 'Black Wins'
                else:
                    result = 'White Wins'
            if piece.is_in_stalemate() and turn == piece.team:
                result = "It's a Draw"
    for pos in pos_dict:
        if pos_dict[pos] >= 3:
            result = "It's a Draw"
    if result is None:
        return None
    return result


def display_result(screen, board, result):
    if result is None:
        return None
    font = pygame.font.SysFont('Arial', 50, bold=True)
    img = font.render(result, True, (200, 50, 50))
    pos = (board.start_pos[0] + board.size//2 - board.square_size*2, board.start_pos[1] + board.size//2 - board.square_size//2)
    screen.blit(img, pos)
    pygame.display.flip()
    return result


def save_position():
    saved_pos = {}
    for piece in Piece.All_Pieces:
        saved_pos[piece] = piece.pos, piece.is_taken, piece.has_moved
    return saved_pos


def restore_position(saved_pos):
    for piece in saved_pos:
        piece.pos = saved_pos[piece][0]
        piece.is_taken = saved_pos[piece][1]
        piece.has_moved = saved_pos[piece][2]
    return


def back_one_move(move_num, pos_history):
    move_num -= 1
    if move_num == -1:
        return 0, True
    pos = pos_history[move_num]
    restore_position(pos)
    return move_num, True


def forward_one_move(move_num, pos_history):
    move_num += 1
    if move_num >= len(pos_history):
        return move_num-1, False
    if move_num == len(pos_history)-1:
        restore_position(pos_history[move_num])
        return move_num, False
    restore_position(pos_history[move_num])
    return move_num, True


def add_pos_to_dictionary(dictionary):
    position = []
    for piece in Piece.All_Pieces:
        position.append((piece, piece.pos))
    clean_pos = tuple(position)
    if clean_pos in dictionary:
        dictionary[clean_pos] += 1
    else:
        dictionary[clean_pos] = 1

