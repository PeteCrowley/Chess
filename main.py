import pygame
from Pieces.Piece import Piece
from Pieces.Piece import show_all_pieces
from Board import Board
from set_up import set_board, check_for_result, display_result
from chess_AI import AI_main


pygame.init()

SCREEN_SIZE = WIDTH, HEIGHT, = 700, 700
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)
pygame.display.set_caption("Chess")

CLOCK = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 204)

board = Board(size=600)
set_board(board)


mouse_rect = pygame.rect.Rect(0, 0, 3, 3)
clicked_piece = None
move_count = 0


Piece.White_Piece_List[4].get_legal_moves(board)
running = True
game_over = False
while running:
    CLOCK.tick(FPS)
    if move_count % 2 == 0:
        turn = 'white'
    else:
        turn = 'black'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pos = pygame.mouse.get_pos()
                mouse_rect.center = pos
                if turn == 'white':
                    piece_list = Piece.White_Piece_List
                else:
                    piece_list = Piece.Black_Piece_List
                for piece in piece_list:
                    if mouse_rect.colliderect(piece.hitbox):
                        clicked_piece = piece
                        clicked_piece.is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and clicked_piece is not None:
            if event.button == pygame.BUTTON_LEFT:
                pos = pygame.mouse.get_pos()
                mouse_rect.center = pos
                for square in board.squares:
                    hitbox = board.squares[square]
                    if mouse_rect.colliderect(hitbox):
                        move_count = clicked_piece.move(board, square, move_count)
                clicked_piece.is_clicked = False
                clicked_piece = None
    screen.fill(BLUE)
    board.draw_board(screen)
    show_all_pieces(screen, board)
    if clicked_piece:
        clicked_piece.show_piece(screen, board)

    if not game_over:
        pygame.display.flip()

    result = display_result(screen, check_for_result(board))
    if result is not None:
        game_over = True

    if turn == 'black' and not game_over:
        all_moves = AI_main.get_all_legal_moves(board, 'black')
        move_count = AI_main.random_move(board, all_moves, move_count)

    elif turn == 'white' and not game_over:
        all_moves = AI_main.get_all_legal_moves(board, 'white')
        move_count = AI_main.random_move(board, all_moves, move_count)
