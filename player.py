import pygame


class Player:
    def __init__(self, position, width, height, speed=5, color=(255, 0, 0)):
        self.start_x = position[0] + 10
        self.start_y = position[1] + 10
        self.x = position[0] + 10
        self.y = position[1] + 10
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.finished = False
        self.alive = True

    def move(self, keys, screen, col_list):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            if self.collision(screen).collidelist(col_list) != -1:
                while self.collision(screen).collidelist(col_list) != -1:
                    self.x += 1
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            if self.collision(screen).collidelist(col_list) != -1:
                while self.collision(screen).collidelist(col_list) != -1:
                    self.x -= 1
        if keys[pygame.K_DOWN]:
            self.y += self.speed
            if self.collision(screen).collidelist(col_list) != -1:
                while self.collision(screen).collidelist(col_list) != -1:
                    self.y -= 1
        if keys[pygame.K_UP]:
            self.y -= self.speed
            if self.collision(screen).collidelist(col_list) != -1:
                while self.collision(screen).collidelist(col_list) != -1:
                    self.y += 1

    def draw(self, screen):
        if self.alive and not self.finished:
            pygame.draw.rect(screen, (0,0,0), (self.x-2, self.y-2, self.width+4, self.height+4))
            return pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collision(self, screen):
        return pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4))

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y

    def die(self):
        self.alive = False

    def finish(self):
        self.finished = True
