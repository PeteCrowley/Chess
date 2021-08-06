import pygame


class Board:
    BLACK = (64, 64, 64)
    WHITE = (200, 200, 200)

    def __init__(self, width, height):
        if width <= height:
            self.size = width * 5//6
        else:
            self.size = height * 5//6
        while self.size % 8 != 0:
            self.size += 1
        self.start_pos = ((width - self.size)/2, (height - self.size)/2)
        self.square_size = self.size//8
        self.hitbox_size = self.square_size * 8 / 10
        self.squares = {}
        self.create_virtual_board()
        self.circle_color = (0, 100, 150)
        self.circle_radius = self.square_size//4

    def draw_board(self, screen):
        x_pos, y_pos = self.start_pos
        color = Board.WHITE
        for i in range(1, 9):
            for x in range(1, 9):
                square = pygame.Rect((x_pos, y_pos), (self.square_size, self.square_size))
                screen.fill(color, square)
                x_pos += self.square_size
                color = self.switch_color(color)
            y_pos += self.square_size
            x_pos -= self.size
            color = self.switch_color(color)

    def create_virtual_board(self):
        x_pos, y_pos = self.start_pos
        x_pos += (self.square_size-self.hitbox_size)/2
        y_pos += (self.square_size - self.hitbox_size) / 2
        for i in range(1, 9).__reversed__():
            for x in range(1, 9):
                square = pygame.Rect((x_pos, y_pos), (self.hitbox_size, self.hitbox_size))
                self.squares[(x, i)] = square
                x_pos += self.square_size
            y_pos += self.square_size
            x_pos -= self.size

    def switch_color(self, color):
        if color == Board.BLACK:
            color = Board.WHITE
        else:
            color = Board.BLACK
        return color
