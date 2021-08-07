import pygame
from Pieces.Piece import Piece
from Pieces.Piece import show_all_pieces
from Board import Board
from set_up import set_board, check_for_result, display_result, reset_board, save_position, back_one_move, forward_one_move, add_pos_to_dictionary
from chess_AI.AI_main import AI_Move
from Determine_Players import show_player_buttons
import time

pygame.init()

SCREEN_SIZE = WIDTH, HEIGHT, = 700, 700
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)
pygame.display.set_caption("Chess")

CLOCK = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 204)

board = Board(WIDTH, HEIGHT)
set_board(board)


mouse_rect = pygame.rect.Rect(0, 0, 3, 3)

play_again_button = pygame.rect.Rect((620, 10), (60, 20))
white_player_rect = pygame.rect.Rect((330, 670), (60, 20))
black_player_rect = pygame.rect.Rect((330, 10), (60, 20))

white_is_AI = False
black_is_AI = True

clicked_piece = None
move_count = 0
position_history = [save_position()]
position_dictionary = {}
add_pos_to_dictionary(position_dictionary)


running = True
game_over = False
frozen = False
while running:
    CLOCK.tick(FPS)
    if game_over:
        frozen = True
    elif move_count % 2 == 0:
        turn = 'white'
    else:
        turn = 'black'

    result = check_for_result(turn, position_dictionary)
    if result is not None:
        game_over = True
        frozen = True

    if turn == 'black' and black_is_AI and not frozen:
        move_count = AI_Move(turn, move_count)
        position_history.append(save_position())
        add_pos_to_dictionary(position_dictionary)

    elif turn == 'white' and white_is_AI and not frozen:
        move_count = AI_Move(turn, move_count)
        position_history.append(save_position())
        add_pos_to_dictionary(position_dictionary)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pos = pygame.mouse.get_pos()
                mouse_rect.center = pos
                if mouse_rect.colliderect(white_player_rect):
                    white_is_AI = not white_is_AI
                elif mouse_rect.colliderect(black_player_rect):
                    black_is_AI = not black_is_AI
                elif mouse_rect.colliderect(play_again_button):
                    game_over = False
                    frozen = False
                    reset_board()
                    move_count = 0
                    position_history = [save_position()]
                    position_dictionary = {}
                    add_pos_to_dictionary(position_dictionary)
                if not frozen:
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
                        old_move_count = move_count
                        move_count = clicked_piece.move(square, move_count)
                        time.sleep(0.0001)
                        if move_count > old_move_count:
                            position_history.append(save_position())
                            add_pos_to_dictionary(position_dictionary)
                clicked_piece.is_clicked = False
                clicked_piece = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_count, frozen = back_one_move(move_count, position_history)
            elif event.key == pygame.K_RIGHT:
                move_count, frozen = forward_one_move(move_count, position_history)
    screen.fill(BLUE)
    board.draw_board(screen)
    show_all_pieces(screen)
    show_player_buttons(screen, board, white_is_AI, black_is_AI, white_player_rect, black_player_rect, play_again_button)
    if clicked_piece:
        clicked_piece.show_piece(screen)
    display_result(screen, board, result)



    pygame.display.flip()





