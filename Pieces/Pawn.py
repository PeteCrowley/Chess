import pygame
from Pieces.Piece import Piece, square_empty
from Pieces.Queen import PQueen


class Pawn(Piece):

    WHITE_IMAGE = pygame.image.load("./Sprites/White_Pawn.png")
    BLACK_IMAGE = pygame.image.load("./Sprites/Black_Pawn.png")
    A_START = 1
    B_START = 2
    C_START = 3
    D_START = 4
    E_START = 5
    F_START = 6
    G_START = 7
    H_START = 8

    def __init__(self, board, team, start_file):
        super().__init__(board, team)
        self.start_file = start_file
        self.set_start_pos()
        self.start_square = (self.start_file, self.start_rank)
        self.pos = self.start_square
        if self.team == 'white':
            self.image = pygame.transform.scale(Pawn.WHITE_IMAGE, self.size)
        else:
            self.image = pygame.transform.scale(Pawn.BLACK_IMAGE, self.size)
        self.en_passant_square = None
        self.value = 1

    def set_start_pos(self):
        if self.start_file == "a":
            self.start_file = 1
        elif self.start_file == "b":
            self.start_file = 2
        elif self.start_file == "c":
            self.start_file = 3
        elif self.start_file == "d":
            self.start_file = 4
        elif self.start_file == "e":
            self.start_file = 5
        elif self.start_file == "f":
            self.start_file = 6
        elif self.start_file == "g":
            self.start_file = 7
        elif self.start_file == "h":
            self.start_file = 8
        if self.team == 'white':
            self.start_rank += 1
        else:
            self.start_rank -= 1

    def get_legal_moves(self, all_observed=False):
        if self.is_taken:
            return []
        moves = []
        x = self.pos[0]
        y = self.pos[1]
        if self.team == 'white':
            num = 1
        else:
            num = -1
        if all_observed:
            moves.append((x + 1, y + num))
            moves.append((x - 1, y + num))
            return moves
        square = (x, y + num)
        if square_empty(square) and not self.is_king_in_check_after_move(square):
            moves.append(square)
        square = (x + num, y + num)
        if (self.can_take(square) and not self.is_king_in_check_after_move(square))\
                or square == Piece.En_Passant_Square:
            moves.append(square)
        square = (x - num, y + num)
        if self.can_take(square) and not self.is_king_in_check_after_move(square)\
                or square == Piece.En_Passant_Square:
            moves.append(square)
        square = (x, y + 2 * num)
        if ((num == 1 and y == 2) or (num == -1 and y == 7)) \
                and square_empty(square) and square_empty((square[0], square[1]-num)) \
                and not self.is_king_in_check_after_move(square):
            moves.append(square)
        return moves

    def move(self, square, move_count):
        old_move_count = move_count
        x = self.pos[0]
        y = self.pos[1]
        if square[1] - y == 2:
            move_count = super().move(square, move_count)
            if old_move_count == move_count + 1:
                Piece.En_Passant_Square = (x, y - 1)
                Piece.En_Passant_Pawn = self
        elif square[1] - y == -2:
            move_count = super().move(square, move_count)
            if old_move_count == move_count - 1:
                Piece.En_Passant_Square = (x, y-1)
                Piece.En_Passant_Pawn = self
        elif square == Piece.En_Passant_Square:
            self.pos = square
            self.has_moved = True
            Piece.En_Passant_Pawn.is_taken = True
            move_count += 1
        else:
            move_count = super().move(square, move_count)
        if self.pos[1] == 8 or self.pos[1] == 1:
            self.promote(square)
        return move_count

    def promote(self, square):
        self.is_taken = True
        queen = PQueen(self.board, team=self.team)
        queen.pos = square
