import pygame
import math
from constants import *


class Pacman:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.direction = STOP
        self.next_direction = STOP
        self.radius = CELL_SIZE // 2 - 2
        self.mouth_angle = 0
        self.mouth_opening = True
        self.mouth_speed = 0.3

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = STOP
        self.next_direction = STOP

    def set_direction(self, direction, maze):
        if self.can_move(direction, maze):
            self.direction = direction
            self.next_direction = STOP
        else:
            self.next_direction = direction

    def can_move(self, direction, maze):
        dx, dy = direction
        new_x = self.x + dx * CELL_SIZE
        new_y = self.y + dy * CELL_SIZE
        col = int(new_x // CELL_SIZE)
        row = int(new_y // CELL_SIZE)

        if dx != 0:
            center_row = int(self.y // CELL_SIZE)
            if abs(self.y - (center_row * CELL_SIZE + CELL_SIZE // 2)) > 2:
                return False

        if dy != 0:
            center_col = int(self.x // CELL_SIZE)
            if abs(self.x - (center_col * CELL_SIZE + CELL_SIZE // 2)) > 2:
                return False

        if col < 0 or col >= COLS or row < 0 or row >= ROWS:
            if row == 14 and (col < 0 or col >= COLS):
                return True
            return False

        return not maze.is_wall(col, row)

    def update(self, maze):
        if self.next_direction != STOP and self.can_move(self.next_direction, maze):
            self.direction = self.next_direction
            self.next_direction = STOP

        if self.can_move(self.direction, maze):
            self.x += self.direction[0] * PACMAN_SPEED
            self.y += self.direction[1] * PACMAN_SPEED

            if self.x < 0:
                self.x = WIDTH - CELL_SIZE // 2
            elif self.x > WIDTH:
                self.x = CELL_SIZE // 2

        if self.direction != STOP:
            if self.mouth_opening:
                self.mouth_angle += self.mouth_speed
                if self.mouth_angle >= math.pi / 4:
                    self.mouth_opening = False
            else:
                self.mouth_angle -= self.mouth_speed
                if self.mouth_angle <= 0:
                    self.mouth_opening = True

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def draw(self, screen):
        if self.direction == RIGHT or self.direction == STOP:
            start_angle = self.mouth_angle
            end_angle = 2 * math.pi - self.mouth_angle
        elif self.direction == LEFT:
            start_angle = math.pi + self.mouth_angle
            end_angle = math.pi - self.mouth_angle
        elif self.direction == UP:
            start_angle = math.pi * 1.5 + self.mouth_angle
            end_angle = math.pi * 1.5 - self.mouth_angle
        else:
            start_angle = math.pi * 0.5 + self.mouth_angle
            end_angle = math.pi * 0.5 - self.mouth_angle

        pygame.draw.arc(screen, YELLOW,
                        (self.x - self.radius, self.y - self.radius,
                         self.radius * 2, self.radius * 2),
                        start_angle, end_angle, self.radius)

        point_list = [(self.x, self.y)]
        if start_angle < end_angle:
            point_list.append((self.x + self.radius * math.cos(start_angle),
                              self.y + self.radius * math.sin(start_angle)))
            point_list.append((self.x + self.radius * math.cos(end_angle),
                              self.y + self.radius * math.sin(end_angle)))
        else:
            point_list.append((self.x + self.radius * math.cos(end_angle),
                              self.y + self.radius * math.sin(end_angle)))
            point_list.append((self.x + self.radius * math.cos(start_angle),
                              self.y + self.radius * math.sin(start_angle)))

        if len(point_list) == 3:
            pygame.draw.polygon(screen, YELLOW, point_list)
