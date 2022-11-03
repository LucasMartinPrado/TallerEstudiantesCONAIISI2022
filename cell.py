import pygame


class Cell:
    def __init__(self, x, y, width=30, height=30, color=(200, 200, 200)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        return pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def position(self):
        return [self.x, self.y]
