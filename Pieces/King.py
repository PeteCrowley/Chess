import pygame
from Pieces.Piece import Piece


class King(Piece):

    WHITE_IMAGE = pygame.image.load("./Sprites/White_King.png")
    BLACK_IMAGE = pygame.image.load("./Sprites/Black_King.png")

    def __init__(self, board, team):
        super().__init__(board, team)
        self.start_square = (5, self.start_rank)
        self.pos = self.start_square
        if self.team == 'white':
            self.image = pygame.transform.scale(King.WHITE_IMAGE, self.size)
        else:
            self.image = pygame.transform.scale(King.BLACK_IMAGE, self.size)

    def get_legal_moves(self, board, all_observed=False):
        square = None
        if self.is_taken:
            return []
        moves = []
        x, y = self.pos
        directions = ['N', 'NE', 'E', 'SE',
                      'S', 'SW', 'W', 'NW']
        for dr in directions:
            square = None
            if dr == 'N':
                square = (x, y + 1)
            elif dr == 'NE':
                square = (x + 1, y + 1)
            elif dr == 'E':
                square = (x + 1, y)
            elif dr == 'SE':
                square = (x + 1, y - 1)
            elif dr == 'S':
                square = (x, y - 1)
            elif dr == 'SW':
                square = (x - 1, y - 1)
            elif dr == 'W':
                square = (x - 1, y)
            elif dr == 'NW':
                square = (x - 1, y + 1)
            if square not in board.squares:
                continue
            if all_observed:
                moves.append(square)
                continue
            if not self.can_move(square) and not self.can_take(square)[0]:
                continue
            if self.is_king_in_check_after_move(board, square):
                continue
            moves.append(square)
        if all_observed:
            moves.append(square)
            return moves
        if self.can_castle_kingside(board):
            moves.append((7, self.start_rank))
        if self.can_castle_queenside(board):
            moves.append((3, self.start_rank))
        return moves

    def castle(self, rook):
        if rook.kings_or_queens == 'kings':
            self.pos = (7, self.start_rank)
            rook.pos = (6, self.start_rank)
        else:
            self.pos = (3, self.start_rank)
            rook.pos = (4, self.start_rank)

    def can_castle_kingside(self, board):
        if self.has_moved:
            return False
        if self.is_in_check(board):
            return False
        castle_squares = [(6, self.start_rank), (7, self.start_rank)]
        for piece in Piece.All_Pieces:
            if piece.pos in castle_squares:
                return False
        for square in castle_squares:
            if self.is_observed(board, square):
                return False
        return True

    def can_castle_queenside(self, board):
        if self.has_moved:
            return False
        if self.is_in_check(board):
            return False
        castle_squares = [(2, self.start_rank), (3, self.start_rank), (4, self.start_rank)]
        for piece in Piece.All_Pieces:
            if piece.pos in castle_squares:
                return False
        for square in castle_squares:
            if self.is_observed(board, square):
                return False
        return True

    def is_in_check(self, board):
        return self.is_observed(board, self.pos)

    def is_in_checkmate(self, board):
        if self.team == 'white':
            piece_list = Piece.White_Piece_List
        else:
            piece_list = Piece.Black_Piece_List
        if not self.is_in_check(board):
            return False
        for piece in piece_list:
            if piece.get_legal_moves(board) != []:
                return False
        return True

    def move(self, board, square, move_count):
        if square not in self.get_legal_moves(board):
            return move_count
        if self.team == 'white':
            piece_list = Piece.White_Piece_List
        else:
            piece_list = Piece.Black_Piece_List
        if self.can_castle_kingside(board) and square == (7, self.start_rank):
            self.castle(piece_list[6])
            self.has_moved = True
            move_count += 1
        elif self.can_castle_queenside(board) and square == (3, self.start_rank):
            self.castle(piece_list[7])
            self.has_moved = True
            move_count += 1
        elif self.can_move(square):
            self.pos = square
            self.has_moved = True
            move_count += 1
        else:
            can_take, piece = self.can_take(square)
            if can_take:
                self.take(piece)
                move_count += 1
                return move_count
        return move_count

    def is_observed(self, board, square):
        if self.team == 'white':
            opp_piece_list = Piece.Black_Piece_List
        else:
            opp_piece_list = Piece.White_Piece_List
        for piece in opp_piece_list:
            observed_squares = piece.get_legal_moves(board, all_observed=True)
            for sqr in observed_squares:
                if sqr == square:
                    return True
        return False

    def is_in_stalemate(self, board):
        if self.is_in_checkmate(board):
            return False
        if self.team == 'white':
            piece_list = Piece.White_Piece_List
        else:
            piece_list = Piece.Black_Piece_List
        for piece in piece_list:
            if piece.get_legal_moves(board) != []:
                return False
        return True

    def is_king_in_check_after_move(self, board, square):
        old_pos = self.pos
        self.pos = square
        if self.is_in_check(board):
            self.pos = old_pos
            return True
        else:
            self.pos = old_pos
            return False
