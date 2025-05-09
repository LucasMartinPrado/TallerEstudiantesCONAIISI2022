import pygame


class Individual:
    def __init__(self, position, width, height, moves, speed=3, color=(255, 0, 0)):
        self.start_x = position[0]+10
        self.start_y = position[1]+10
        self.x = position[0]+10
        self.y = position[1]+10
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.moves = moves
        self.currentMove = 0
        self.alive = True
        self.finished = False
        self.is_leader = False
        self.historic_x = []
        self.historic_y = []

    # 0,0,0 up         ##0
    # 0,0,1 up-right   ##1
    # 0,1,0 right      ##2
    # 0,1,1 down-right ##3
    # 1,0,0 down       ##4
    # 1,0,1 down-left  ##5
    # 1,1,0 left       ##6
    # 1,1,1 up-left    ##7

    def move(self, screen, col_list):
        if len(self.moves) > self.currentMove:
            move = self.moves[self.currentMove]
            if move == 0:       # moving up
                self._moveup(screen, col_list)
            elif move == 1:     # moving up-right
                self._moveup(screen, col_list)
                self._moveright(screen, col_list)
            elif move == 2:     # moving right
                self._moveright(screen, col_list)
            elif move == 3:     # moving down-right
                self._movedown(screen, col_list)
                self._moveright(screen, col_list)
            elif move == 4:     # moving down
                self._movedown(screen, col_list)
            elif move == 5:     # moving down-left
                 self._movedown(screen, col_list)
                 self._moveleft(screen, col_list)
            elif move == 6:     # moving left
                self._moveleft(screen, col_list)
            elif move == 7:     # moving up-left
                self._moveup(screen, col_list)
                self._moveleft(screen, col_list)
            self.currentMove += 1
            self.historic_x.append(self.x)
            self.historic_y.append(self.y)

    def draw(self, screen):
        color = self.color
        if self.is_leader:
            color = (0,255,0)
        if self.alive and not self.finished:
            pygame.draw.rect(screen, (0, 0, 0), (self.x-2, self.y-2, self.width+4, self.height+4))
            return pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def collision(self, screen):
        return pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4))

    def reset(self, is_leader):
        self.x = self.start_x
        self.y = self.start_y
        self.currentMove = 0
        self.alive = True
        self.finished = False
        self.is_leader = is_leader
        self.historic_x = []
        self.historic_y = []

    def _moveright(self, screen, col_list):
        self.x += self.speed
        if self.collision(screen).collidelist(col_list) != -1:
            while self.collision(screen).collidelist(col_list) != -1:
                self.x -= 2

    def _moveup(self, screen, col_list):
        self.y -= self.speed
        if self.collision(screen).collidelist(col_list) != -1:
            while self.collision(screen).collidelist(col_list) != -1:
                self.y += 2

    def _movedown(self, screen, col_list):
        self.y += self.speed
        if self.collision(screen).collidelist(col_list) != -1:
            while self.collision(screen).collidelist(col_list) != -1:
                self.y -= 3

    def _moveleft(self, screen, col_list):
        self.x -= self.speed
        if self.collision(screen).collidelist(col_list) != -1:
            while self.collision(screen).collidelist(col_list) != -1:
                self.x += 2

    def die(self):
        self.alive = False

    def finish(self):
        self.finished = True
