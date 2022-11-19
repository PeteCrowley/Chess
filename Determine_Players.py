import pygame


def show_player_buttons(screen, board, white_is_AI, black_is_AI, w_butt, b_butt, p_butt):
    if white_is_AI:
        player = "CPU"
    else:
        player = "Human"
    x_pos = board.start_pos[0] + board.size//2 - board.square_size//2
    y_pos = board.start_pos[1] + board.size + 10
    font = pygame.font.SysFont('Arial', 20, bold=True)
    img = font.render(player, True, (200, 200, 200))
    w_butt.topleft = (x_pos, y_pos)
    screen.blit(img, (x_pos, y_pos))

    if black_is_AI:
        player = "CPU"
    else:
        player = "Human"
    y_pos = board.start_pos[1] - 25
    img = font.render(player, True, (200, 200, 200))
    b_butt.topleft = (x_pos, y_pos)
    screen.blit(img, (x_pos, y_pos))

    x_pos = board.start_pos[0] + board.size - board.square_size
    font = pygame.font.SysFont('Arial', 20, bold=True)
    img = font.render("Reset", True, (200, 200, 200))
    p_butt.topleft = (x_pos, y_pos)
    screen.blit(img, (x_pos, y_pos))

    return


