from cell import Cell
from enemy import Enemy
import math


class Level:
    def __init__(self, maze_arrangement, start, finish, enemies):
        self.M = 27
        self.N = 20
        self.maze = maze_arrangement
        self.walls = []
        self.enemies = []
        self.start = Cell(start[0], start[1], 30, 30, (20, 230, 20))
        self.finish = Cell(finish[0], finish[1], 30, 30, (20, 200, 20))
        self.fillWalls()
        self.init_enemies(enemies)

    def init_enemies(self, enemies):
        for enemy in enemies:
            self.enemies.append(Enemy(enemy["position"], enemy["size"], enemy["vertical"], enemy["bounds"], enemy["speed"]))

    def start_position(self):
        return self.start.position()  # Returns the position of the start cell as [x, y]

    def finish_position(self):
        return self.finish.position()  # Returns the position of the finish cell as [x, y]

    def fillWalls(self):
        bx = 0
        by = 0
        for i in range(0, self.M * self.N):
            if self.maze[bx + (by * self.M)] == 1:
                self.walls.append(Cell(bx * 30, by * 30))
            bx = bx + 1
            if bx > self.M - 1:
                bx = 0
                by = by + 1

    def draw(self, screen):
        self.start.draw(screen)
        self.finish.draw(screen)
        for cell in self.walls:
            cell.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)

    def collisions(self, screen, x, y):
        col_list = []
        for cell in self.walls:
            if math.dist([cell.x, cell.y], [x, y]) < 60.0:
                col_list.append(cell.draw(screen))
        return col_list

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()

    def enemy_collision(self, screen):
        col_list = []
        for enemy in self.enemies:
            col_list.append(enemy.draw(screen))
        return col_list

    def reset(self):
        for enemy in self.enemies:
            enemy.reset()


