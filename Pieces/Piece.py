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
        self.board = board

    def show_piece(self, screen):
        if self.is_clicked:
            self.rect.center = pygame.mouse.get_pos()
            self.hitbox.center = pygame.mouse.get_pos()
            self.show_legal_moves(screen)
            screen.blit(self.image, self.rect)
        elif self.is_taken:
            self.pos = (0, 0)
            self.rect.center = (0, 0)
            self.hitbox.center = (0, 0)
        else:
            self.rect.center = self.board.squares[self.pos].center
            self.hitbox.center = self.board.squares[self.pos].center
            screen.blit(self.image, self.rect)

    def can_take(self, square):
        if square_empty(square):
            return False
        piece = get_piece_on_square(square)
        if piece is None:
            return False
        if self.team != piece.team:
            return True
        return False

    def move(self, square, move_count):
        if square not in self.get_legal_moves():
            return move_count
        if square_empty(square):
            self.pos = square
            self.has_moved = True
            move_count += 1
            Piece.En_Passant_Square = None
            Piece.En_Passant_Pawn = None
        else:
            if self.can_take(square):
                self.take(square)
                move_count += 1
                Piece.En_Passant_Square = None
                Piece.En_Passant_Pawn = None
        return move_count

    def take(self, square):
        taken_piece = get_piece_on_square(square)
        self.pos = square
        taken_piece.is_taken = True
        self.has_moved = True

    def show_legal_moves(self, screen):
        legal_moves = self.get_legal_moves()
        if legal_moves is None:
            return
        for square in self.get_legal_moves():
            pygame.draw.circle(screen, self.board.circle_color, self.board.squares[square].center,
                               self.board.circle_radius)

    def get_legal_moves(self, all_observed=False):
        return []

    def is_king_in_check_after_move(self, square):
        old_pos = self.pos
        if self.team == 'white':
            king = Piece.White_Piece_List[0]
        else:
            king = Piece.Black_Piece_List[0]
        needs_to_take = get_piece_on_square(square)
        if needs_to_take:
            taken_piece_old_pos = needs_to_take.pos
            needs_to_take.pos = (0, 0)
            needs_to_take.is_taken = True
        self.pos = square
        check = king.is_in_check()
        if needs_to_take:
            needs_to_take.pos = taken_piece_old_pos
            needs_to_take.is_taken = False
        self.pos = old_pos
        return check





    def is_observed(self, square, return_piece=False):
        if self.team == 'white':
            opp_piece_list = Piece.Black_Piece_List
        else:
            opp_piece_list = Piece.White_Piece_List
        for piece in opp_piece_list:
            observed_squares = piece.get_legal_moves(all_observed=True)
            if square in observed_squares:
                if return_piece:
                    return piece
                return True
        return False

    def is_protected(self, square, return_piece=False):
        if self.team == 'white':
            team_piece_list = Piece.White_Piece_List
        else:
            team_piece_list = Piece.Black_Piece_List
        for piece in team_piece_list:
            if piece is self:
                continue
            observed_squares = piece.get_legal_moves(all_observed=True)
            for sqr in observed_squares:
                if sqr == square:
                    if return_piece:
                        return piece
                    return True
        return False


def square_empty(square):
    for piece in Piece.All_Pieces:
        if piece.pos == square:
            return False
    return True


def get_piece_on_square(square):
    for piece in Piece.All_Pieces:
        if piece.pos == square:
            return piece
    return None


def show_all_pieces(screen):
    for piece in Piece.All_Pieces:
        piece.show_piece(screen)
