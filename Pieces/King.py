import pygame
from Pieces.Piece import Piece, get_piece_on_square, square_empty


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
        self.value = 99999

    def get_legal_moves(self, all_observed=False):
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
            if square not in self.board.squares:
                continue
            if all_observed:
                moves.append(square)
                continue
            if not square_empty(square) and not self.can_take(square):
                continue
            if self.is_king_in_check_after_move(square):
                continue
            moves.append(square)
        if all_observed:
            moves.append(square)
            return moves
        if self.can_castle_kingside():
            moves.append((7, self.start_rank))
        if self.can_castle_queenside():
            moves.append((3, self.start_rank))
        return moves

    def castle(self, rook):
        if rook.kings_or_queens == 'kings':
            self.pos = (7, self.start_rank)
            rook.pos = (6, self.start_rank)
        else:
            self.pos = (3, self.start_rank)
            rook.pos = (4, self.start_rank)

    def can_castle_kingside(self):
        rook_square = (8, self.start_rank)
        rook = get_piece_on_square(rook_square)
        if self.has_moved:
            return False
        if self.is_in_check():
            return False
        if rook is None or type(rook).__name__ != 'Rook':
            return False
        castle_squares = [(6, self.start_rank), (7, self.start_rank)]
        for piece in Piece.All_Pieces:
            if piece.pos in castle_squares:
                return False
        for square in castle_squares:
            if self.is_observed(square):
                return False
        return True

    def can_castle_queenside(self):
        rook_square = (1, self.start_rank)
        rook = get_piece_on_square(rook_square)
        if self.has_moved:
            return False
        if self.is_in_check():
            return False
        if rook is None or type(rook).__name__ != 'Rook':
            return False
        castle_squares = [(2, self.start_rank), (3, self.start_rank), (4, self.start_rank)]
        for piece in Piece.All_Pieces:
            if piece.pos in castle_squares:
                return False
        for square in castle_squares:
            if self.is_observed(square):
                return False
        return True

    def is_in_check(self):
        return self.is_observed(self.pos)

    def is_in_checkmate(self):
        if self.team == 'white':
            piece_list = Piece.White_Piece_List
        else:
            piece_list = Piece.Black_Piece_List
        if not self.is_in_check():
            return False
        for piece in piece_list:
            if piece.get_legal_moves() != []:
                return False
        return True

    def move(self, square, move_count):
        if square not in self.get_legal_moves():
            return move_count
        if self.team == 'white':
            piece_list = Piece.White_Piece_List
        else:
            piece_list = Piece.Black_Piece_List
        if self.can_castle_kingside() and square == (7, self.start_rank):
            self.castle(piece_list[6])
            self.has_moved = True
            move_count += 1
        elif self.can_castle_queenside() and square == (3, self.start_rank):
            self.castle(piece_list[7])
            self.has_moved = True
            move_count += 1
        elif square_empty(square):
            self.pos = square
            self.has_moved = True
            move_count += 1
        else:
            can_take = self.can_take(square)
            if can_take:
                self.take(square)
                move_count += 1
                return move_count
        return move_count

    def is_in_stalemate(self):
        if self.is_in_checkmate():
            return False
        if self.team == 'white':
            piece_list = Piece.White_Piece_List
        else:
            piece_list = Piece.Black_Piece_List
        for piece in piece_list:
            if piece.get_legal_moves() != []:
                return False
        return True

