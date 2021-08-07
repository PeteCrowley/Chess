import pygame
from Pieces.Piece import square_empty, get_piece_on_square
from Pieces.monster_piece import MonsterPiece


class MonsterQueen(MonsterPiece):

    WHITE_IMAGE = pygame.image.load("./Sprites/White_Queen.png")
    BLACK_IMAGE = pygame.image.load("./Sprites/Black_Queen.png")
    START_SQUARE = (4, 1)

    def __init__(self, board, team):
        super().__init__(board, team)
        self.start_square = (4, self.start_rank)
        self.pos = self.start_square
        if self.team == 'white':
            self.image = pygame.transform.scale(MonsterQueen.WHITE_IMAGE, self.size)
        else:
            self.image = pygame.transform.scale(MonsterQueen.BLACK_IMAGE, self.size)
        self.value = 98

    def get_observed(self):
        if self.is_taken:
            return []
        squares_1 = self.get_monster_move_1()
        moves = []
        directions = ['N', 'NE', 'E', 'SE',
                      'S', 'SW', 'W', 'NW']
        for option in squares_1:
            x = option[0]
            y = option[1]
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
                    elif square_empty(square) or get_piece_on_square(square).team != self.team:
                        moves.append(square)
                    if not square_empty(square):
                        blocked = True
        return moves

    def get_monster_move_1(self):
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
                elif square_empty(square) or get_piece_on_square(square).team != self.team \
                        and self.legal_moves_after_move_1(square):
                    moves.append(square)
                if not square_empty(square):
                    blocked = True
        return moves

    def get_monster_move_2(self):
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
                if square in self.board.squares and (square_empty(square) or self.can_take(square)) \
                        and not self.is_king_in_check_after_move(square):
                    moves.append(square)
                if not square_empty(square):
                    blocked = True
        return moves