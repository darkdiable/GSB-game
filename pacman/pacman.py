import pygame
import math
from constants import (
    CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
    PACMAN_SPEED, YELLOW, BLACK,
    UP, DOWN, LEFT, RIGHT, STOP
)


class Pacman:
    def __init__(self):
        self.reset()

    def reset(self):
        self.grid_x = 13
        self.grid_y = 23
        self.x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
        self.y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
        self.direction = STOP
        self.next_direction = STOP
        self.speed = PACMAN_SPEED
        self.mouth_angle = 45
        self.mouth_direction = 1
        self.radius = CELL_SIZE // 2 - 2
        self.alive = True

    def set_direction(self, direction):
        self.next_direction = direction

    def _can_move(self, maze, direction):
        if direction == STOP:
            return True

        dx, dy = direction
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy

        if new_grid_x < 0 or new_grid_x >= GRID_WIDTH:
            return True

        return maze.is_walkable(new_grid_x, new_grid_y)

    def update(self, maze):
        if not self.alive:
            return

        if self.next_direction != STOP and self._can_move(maze, self.next_direction):
            if self._is_centered():
                self.direction = self.next_direction

        if self._is_centered() and not self._can_move(maze, self.direction):
            self.direction = STOP
            return

        dx, dy = self.direction
        self.x += dx * self.speed
        self.y += dy * self.speed

        if self.x < 0:
            self.x = GRID_WIDTH * CELL_SIZE
        elif self.x > GRID_WIDTH * CELL_SIZE:
            self.x = 0

        if self._is_centered():
            self.grid_x = round(self.x / CELL_SIZE - 0.5)
            self.grid_y = round(self.y / CELL_SIZE - 0.5)

        self._animate_mouth()

    def _is_centered(self):
        center_x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
        tolerance = self.speed
        return (abs(self.x - center_x) <= tolerance and
                abs(self.y - center_y) <= tolerance)

    def _animate_mouth(self):
        if self.direction != STOP:
            self.mouth_angle += self.mouth_direction * 3
            if self.mouth_angle >= 45:
                self.mouth_direction = -1
            elif self.mouth_angle <= 0:
                self.mouth_direction = 1

    def get_grid_position(self):
        return self.grid_x, self.grid_y

    def check_collision(self, ghost):
        distance = math.sqrt(
            (self.x - ghost.x) ** 2 +
            (self.y - ghost.y) ** 2
        )
        return distance < (self.radius + ghost.radius - 5)

    def die(self):
        self.alive = False
        self.direction = STOP

    def draw(self, screen):
        if not self.alive:
            return

        center = (int(self.x), int(self.y))

        if self.direction == RIGHT:
            start_angle = math.radians(self.mouth_angle)
            end_angle = math.radians(360 - self.mouth_angle)
        elif self.direction == LEFT:
            start_angle = math.radians(180 + self.mouth_angle)
            end_angle = math.radians(180 - self.mouth_angle)
        elif self.direction == UP:
            start_angle = math.radians(90 + self.mouth_angle)
            end_angle = math.radians(90 - self.mouth_angle)
        elif self.direction == DOWN:
            start_angle = math.radians(270 + self.mouth_angle)
            end_angle = math.radians(270 - self.mouth_angle)
        else:
            start_angle = math.radians(self.mouth_angle)
            end_angle = math.radians(360 - self.mouth_angle)

        pygame.draw.arc(
            screen, YELLOW,
            pygame.Rect(
                self.x - self.radius,
                self.y - self.radius,
                self.radius * 2,
                self.radius * 2
            ),
            start_angle, end_angle, self.radius
        )

        point_list = [center]
        for i in range(int(self.mouth_angle * 2)):
            angle = math.radians(
                math.degrees(start_angle) - i
            ) if self.direction in [RIGHT, DOWN] else math.radians(
                math.degrees(start_angle) + i
            )
            px = self.x + self.radius * math.cos(angle)
            py = self.y - self.radius * math.sin(angle)
            point_list.append((px, py))

        if len(point_list) > 2:
            pygame.draw.polygon(screen, YELLOW, point_list)
