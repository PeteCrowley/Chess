import pygame
from Pieces.Piece import Piece, square_empty


class Queen(Piece):

    WHITE_IMAGE = pygame.image.load("./Sprites/White_Queen.png")
    BLACK_IMAGE = pygame.image.load("./Sprites/Black_Queen.png")
    START_SQUARE = (4, 1)

    def __init__(self, board, team):
        super().__init__(board, team)
        self.start_square = (4, self.start_rank)
        self.pos = self.start_square
        if self.team == 'white':
            self.image = pygame.transform.scale(Queen.WHITE_IMAGE, self.size)
        else:
            self.image = pygame.transform.scale(Queen.BLACK_IMAGE, self.size)
        self.value = 9

    def get_legal_moves(self, all_observed=False):
        if self.is_taken:
            return []
        moves = []
        x, y = self.pos
        directions = ['N', 'NE', 'E', 'SE',
                      'S', 'SW', 'W', 'NW']
        for dr in directions:
            blocked = False
            for i in range(1, 8):
                if blocked:
                    continue
                square = None
                if dr == 'N':
                    square = (x, y + i)
                elif dr == 'NE':
                    square = (x + i, y + i)
                elif dr == 'E':
                    square = (x + i, y)
                elif dr == 'SE':
                    square = (x + i, y - i)
                elif dr == 'S':
                    square = (x, y - i)
                elif dr == 'SW':
                    square = (x - i, y - i)
                elif dr == 'W':
                    square = (x - i, y)
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


class PQueen(Queen):
    def __init__(self, board, team):
        super().__init__(board, team)
