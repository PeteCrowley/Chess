import pygame


class Board:
    STARTING_POS = 50, 50
    BLACK = (64, 64, 64)
    WHITE = (200, 200, 200)

    def __init__(self, size=400):
        self.width = size
        self.height = size
        self.square_size = size//8
        self.hitbox_size = self.square_size * 8 /10
        self.squares = {}
        self.create_virtual_board()
        self.circle_color = (0, 100, 150)
        self.circle_radius = self.square_size//4

    def draw_board(self, screen):
        x_pos, y_pos = Board.STARTING_POS
        color = Board.WHITE
        for i in range(1, 9):
            for x in range(1, 9):
                square = pygame.Rect((x_pos, y_pos), (self.square_size, self.square_size))
                screen.fill(color, square)
                x_pos += self.square_size
                color = self.switch_color(color)
            y_pos += self.square_size
            x_pos -= self.width
            color = self.switch_color(color)

    def create_virtual_board(self):
        x_pos, y_pos = Board.STARTING_POS
        x_pos += (self.square_size-self.hitbox_size)/2
        y_pos += (self.square_size - self.hitbox_size) / 2
        for i in range(1, 9).__reversed__():
            for x in range(1, 9):
                square = pygame.Rect((x_pos, y_pos), (self.hitbox_size, self.hitbox_size))
                self.squares[(x, i)] = square
                x_pos += self.square_size
            y_pos += self.square_size
            x_pos -= self.width

    def switch_color(self, color):
        if color == Board.BLACK:
            color = Board.WHITE
        else:
            color = Board.BLACK
        return color
