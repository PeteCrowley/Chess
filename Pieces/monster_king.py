import pygame
from Pieces.Piece import Piece, get_piece_on_square, square_empty
from Pieces.monster_piece import MonsterPiece


class MonsterKing(MonsterPiece):
    WHITE_IMAGE = pygame.image.load("./Sprites/White_King.png")
    BLACK_IMAGE = pygame.image.load("./Sprites/Black_King.png")

    def __init__(self, board, team):
        super().__init__(board, team)
        self.start_square = (5, self.start_rank)
        self.pos = self.start_square
        if self.team == 'white':
            self.image = pygame.transform.scale(MonsterKing.WHITE_IMAGE, self.size)
        else:
            self.image = pygame.transform.scale(MonsterKing.BLACK_IMAGE, self.size)
        self.value = 99

    def get_observed(self):
        moves = []
        x, y = self.pos
        for i in [1, 2, -1, -2]:
            for k in [1, 2, -1, -2]:
                square = (x, y + k)
                if square in self.board.squares:
                    moves.append(square)
                square = (x + i, y + k)
                if square in self.board.squares:
                    moves.append(square)
                square = (x + i, y)
                if square in self.board.squares:
                    moves.append(square)
        return moves

    def get_monster_move_1(self):
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
            if not self.legal_moves_after_move_1(square):
                continue
            elif square_empty(square) or get_piece_on_square(square).team != self.team:
                moves.append(square)
        return moves

    def get_monster_move_2(self, all_observed=False):
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
            if not square_empty(square) and not self.can_take(square):
                continue
            if self.is_king_in_check_after_move(square):
                continue
            moves.append(square)
        return moves

    def is_in_check(self):
        return self.is_observed(self.pos)

    def is_in_checkmate(self):
        if not self.is_in_check():
            return False
        for piece in Piece.White_Piece_List:
            if piece.get_monster_move_1() != []:
                return False
        return True

    def move(self, square, move_count):
        if square not in self.get_legal_moves():
            return move_count
        if square_empty(square):
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
        for piece in Piece.White_Piece_List:
            if piece.get_monster_move_1() != []:
                return False
        return True

    def is_king_in_check_after_move(self, square):
        old_pos = self.pos
        self.pos = square
        if self.is_in_check():
            self.pos = old_pos
            return True
        else:
            self.pos = old_pos
            return False


