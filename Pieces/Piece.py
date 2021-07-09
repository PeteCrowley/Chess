import pygame


class Piece(pygame.sprite.Sprite):
    All_Pieces = []
    White_Piece_List = []
    Black_Piece_List = []
    BLACK_RANK = 8
    WHITE_RANK = 1
    En_Passant_Square = None
    En_Passant_Pawn = None

    def __init__(self, board, team):
        super().__init__()
        self.__class__.All_Pieces.append(self)
        self.team = team
        if self.team == 'white':
            self.__class__.White_Piece_List.append(self)
            self.start_rank = Piece.WHITE_RANK
        else:
            self.__class__.Black_Piece_List.append(self)
            self.start_rank = Piece.BLACK_RANK
        self.pos = None
        self.size = board.square_size, board.square_size
        self.rect = pygame.Rect((0, 0), self.size)
        self.hitbox = pygame.Rect((0, 0), (board.square_size*8//10, board.square_size*8//10,))
        self.is_clicked = False
        self.is_taken = False
        self.has_moved = False

    def show_piece(self, screen, board):
        if self.is_clicked:
            self.rect.center = pygame.mouse.get_pos()
            self.hitbox.center = pygame.mouse.get_pos()
            self.show_legal_moves(screen, board)
            screen.blit(self.image, self.rect)
        elif self.is_taken:
            self.pos = (0, 0)
            self.rect.center = (0, 0)
            self.hitbox.center = (0, 0)
        else:
            self.rect.center = board.squares[self.pos].center
            self.hitbox.center = board.squares[self.pos].center
            screen.blit(self.image, self.rect)

    def can_move(self, square):
        filled = False
        for piece in Piece.All_Pieces:
            if piece.pos == square:
                filled = True
        return not filled

    def can_take(self, square):
        can_take = (False, self)
        for piece in Piece.All_Pieces:
            if piece.pos == square:
                if self.team != piece.team:
                    can_take = (True, piece)
        return can_take

    def move(self, board, square, move_count):
        if square not in self.get_legal_moves(board):
            return move_count
        if self.can_move(square):
            self.pos = square
            self.has_moved = True
            move_count += 1
            Piece.En_Passant_Square = None
            Piece.En_Passant_Pawn = None
        else:
            can_take, piece = self.can_take(square)
            if can_take:
                self.take(piece)
                move_count += 1
                Piece.En_Passant_Square = None
                Piece.En_Passant_Pawn = None
        return move_count

    def take(self, piece):
        self.pos = piece.pos
        piece.is_taken = True
        self.has_moved = True

    def show_legal_moves(self, screen, board):
        legal_moves = self.get_legal_moves(board)
        if legal_moves is None:
            return
        for square in self.get_legal_moves(board):
            pygame.draw.circle(screen, board.circle_color, board.squares[square].center, board.circle_radius)

    def get_legal_moves(self, board, all_observed=False):
        return []

    def is_king_in_check_after_move(self, board, square):
        old_pos = self.pos
        if self.team == 'white':
            king = Piece.White_Piece_List[0]
        else:
            king = Piece.Black_Piece_List[0]
        can_take, piece = self.can_take(square)
        if can_take:
            piece.is_taken = True
            if king.is_in_check(board):
                piece.is_taken = False
                return True
            else:
                piece.is_taken = False
                return False
        else:
            self.pos = square
            if king.is_in_check(board):
                self.pos = old_pos
                return True
            else:
                self.pos = old_pos
                return False


def show_all_pieces(screen, board):
    for piece in Piece.All_Pieces:
        piece.show_piece(screen, board)
