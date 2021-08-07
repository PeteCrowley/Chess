from Pieces.King import King
from Pieces.Queen import Queen
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn
from Pieces.monster_king import MonsterKing
from Pieces.monster_pawn import MonsterPawn
from Pieces.monster_piece import MonsterPiece
from Pieces.Piece import Piece
from set_up import save_position


def monster_set_up(board):
    MonsterKing(board, team='white')
    MonsterPawn(board, team='white', start_file='c')
    MonsterPawn(board, team='white', start_file='d')
    MonsterPawn(board, team='white', start_file='e')
    MonsterPawn(board, team='white', start_file='f')
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


def monster_reset():
    for i in range(len(Piece.All_Pieces)):
        piece = Piece.All_Pieces[i]
        if i > 20:
            piece.is_taken = True
            continue
        piece.is_taken = False
        piece.pos = piece.start_square
    Piece.All_Pieces = Piece.All_Pieces[:32]
    Piece.White_Piece_List = Piece.White_Piece_List[:16]
    Piece.Black_Piece_List = Piece.Black_Piece_List[:16]
