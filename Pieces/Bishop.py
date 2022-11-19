import pygame
from Pieces.Piece import Piece, square_empty


class Bishop(Piece):

    WHITE_IMAGE = pygame.image.load("./Sprites/White_Bishop.png")
    BLACK_IMAGE = pygame.image.load("./Sprites/Black_Bishop.png")
    KINGS_FILE = 6
    QUEENS_FILE = 3

    def __init__(self, board, team, kings_or_queens):
        super().__init__(board, team)
        self.kings_or_queens = kings_or_queens
        if self.kings_or_queens == "kings":
            self.start_square = (Bishop.KINGS_FILE, self.start_rank)
        else:
            self.start_square = (Bishop.QUEENS_FILE, self.start_rank)
        if self.team == 'white':
            self.image = pygame.transform.scale(Bishop.WHITE_IMAGE, self.size)
        else:
            self.image = pygame.transform.scale(Bishop.BLACK_IMAGE, self.size)
        self.pos = self.start_square
        self.value = 3

    def get_legal_moves(self, all_observed=False):
        if self.is_taken:
            return []
        moves = []
        x, y = self.pos
        directions = ['NE', 'SE', 'SW', 'NW']
        for dr in directions:
            blocked = False
            for i in range(1, 8):
                if blocked:
                    continue
                square = None
                if dr == 'NE':
                    square = (x + i, y + i)
                elif dr == 'SE':
                    square = (x + i, y - i)
                elif dr == 'SW':
                    square = (x - i, y - i)
                elif dr == 'NW':
                    square = (x - i, y + i)
                if square not in self.board.squares:
                    continue
                if all_observed:
                    moves.append(square)
                elif (square_empty(square) or self.can_take(square)) and not self.is_king_in_check_after_move(square):
                    moves.append(square)
                if not square_empty(square):
                    blocked = True
        return moves
