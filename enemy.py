import pygame


class Enemy:
    def __init__(self, position, size, vertical_movement, bounds, speed=5, color=(0, 100, 255)):
        self.x = position[0]
        self.y = position[1]
        self.start_x = position[0]
        self.start_y = position[1]
        self.width = size[0]
        self.height = size[1]
        self.vertical_movement = vertical_movement
        self.bound1 = bounds[0]
        self.bound2 = bounds[1]
        self.speed = speed
        self.color = color
        self.orientation = True

    def move(self):
        if self.vertical_movement:
            if self.y < self.bound1 or self.y > self.bound2:
                self.orientation = not self.orientation
            if self.orientation:
                self.y += self.speed
            else:
                self.y -= self.speed
        else:
            if self.x < self.bound1 or self.x > self.bound2:
                self.orientation = not self.orientation
            if self.orientation:
                self.x += self.speed
            else:
                self.x -= self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.width+2, self.height+2)
        return pygame.draw.circle(screen, self.color, (self.x, self.y), self.width, self.height)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.orientation = True