import pygame
from Pieces.Piece import Piece, square_empty


class Knight(Piece):

    WHITE_IMAGE = pygame.image.load("./Sprites/White_Knight.png")
    BLACK_IMAGE = pygame.image.load("./Sprites/Black_Knight.png")
    KINGS_FILE = 7
    QUEENS_FILE = 2

    def __init__(self, board, team, kings_or_queens):
        super().__init__(board, team)
        self.kings_or_queens = kings_or_queens
        if self.kings_or_queens == "kings":
            self.start_square = (Knight.KINGS_FILE, self.start_rank)
        else:
            self.start_square = (Knight.QUEENS_FILE, self.start_rank)
        if self.team == 'white':
            self.image = pygame.transform.scale(Knight.WHITE_IMAGE, self.size)
        else:
            self.image = pygame.transform.scale(Knight.BLACK_IMAGE, self.size)
        self.pos = self.start_square
        self.value = 3

    def get_legal_moves(self, all_observed=False):
        if self.is_taken:
            return []
        moves = []
        move_list = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                     (1, -2), (1, 2), (2, -1), (2, 1)]
        for x, y in move_list:
            square = (self.pos[0] + x, self.pos[1] + y)
            if square not in self.board.squares:
                continue
            if all_observed:
                moves.append(square)
            elif (square_empty(square) or self.can_take(square)) and not self.is_king_in_check_after_move(square):
                moves.append(square)
        return moves
