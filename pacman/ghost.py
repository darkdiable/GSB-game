import pygame
import random
import math
from constants import *


class Ghost:
    def __init__(self, x, y, color, name):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.radius = CELL_SIZE // 2 - 2
        self.edible = False
        self.edible_timer = 0
        self.respawning = False
        self.respawn_timer = 0
        self.in_house = True
        self.exit_timer = random.randint(0, 3000)
        self.move_counter = 0
        self.eye_offset = 2

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.edible = False
        self.edible_timer = 0
        self.respawning = False
        self.respawn_timer = 0
        self.in_house = True
        self.exit_timer = random.randint(0, 3000)
        self.move_counter = 0

    def make_edible(self):
        if not self.respawning:
            self.edible = True
            self.edible_timer = GHOST_EDIBLE_TIME

    def start_respawn(self):
        self.edible = False
        self.respawning = True
        self.respawn_timer = GHOST_RESPAWN_TIME
        self.x = self.start_x
        self.y = self.start_y
        self.in_house = True
        self.exit_timer = 2000

    def update(self, maze, pacman, dt):
        if self.respawning:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.respawning = False
                self.in_house = False
            return

        if self.edible:
            self.edible_timer -= dt
            if self.edible_timer <= 0:
                self.edible = False

        if self.in_house:
            self.exit_timer -= dt
            if self.exit_timer <= 0:
                self.in_house = False
            else:
                self.y -= 0.5
                return

        self.move_counter += 1
        if self.move_counter < 3:
            self.x += self.direction[0] * GHOST_SPEED
            self.y += self.direction[1] * GHOST_SPEED
            return
        self.move_counter = 0

        current_col = int(self.x // CELL_SIZE)
        current_row = int(self.y // CELL_SIZE)

        center_x = current_col * CELL_SIZE + CELL_SIZE // 2
        center_y = current_row * CELL_SIZE + CELL_SIZE // 2

        if abs(self.x - center_x) < 3 and abs(self.y - center_y) < 3:
            self.x = center_x
            self.y = center_y
            self.choose_direction(maze, pacman)

        self.x += self.direction[0] * GHOST_SPEED
        self.y += self.direction[1] * GHOST_SPEED

        if self.x < 0:
            self.x = WIDTH - CELL_SIZE // 2
        elif self.x > WIDTH:
            self.x = CELL_SIZE // 2

    def choose_direction(self, maze, pacman):
        directions = [UP, DOWN, LEFT, RIGHT]
        opposite = (-self.direction[0], -self.direction[1])
        valid_dirs = []

        for d in directions:
            if d == opposite:
                continue
            new_col = int(self.x // CELL_SIZE) + d[0]
            new_row = int(self.y // CELL_SIZE) + d[1]

            if not maze.is_wall(new_col, new_row):
                valid_dirs.append(d)

        if not valid_dirs:
            valid_dirs.append(opposite)

        if self.edible:
            self.direction = random.choice(valid_dirs)
        else:
            best_dir = valid_dirs[0]
            best_dist = float('inf')

            for d in valid_dirs:
                new_x = self.x + d[0] * CELL_SIZE
                new_y = self.y + d[1] * CELL_SIZE
                dist = math.sqrt((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2)

                if self.name == "blinky":
                    if dist < best_dist:
                        best_dist = dist
                        best_dir = d
                elif self.name == "pinky":
                    target_x = pacman.x + pacman.direction[0] * CELL_SIZE * 4
                    target_y = pacman.y + pacman.direction[1] * CELL_SIZE * 4
                    dist = math.sqrt((new_x - target_x) ** 2 + (new_y - target_y) ** 2)
                    if dist < best_dist:
                        best_dist = dist
                        best_dir = d
                elif self.name == "inky":
                    target_x = pacman.x - pacman.direction[0] * CELL_SIZE * 2
                    target_y = pacman.y - pacman.direction[1] * CELL_SIZE * 2
                    dist = math.sqrt((new_x - target_x) ** 2 + (new_y - target_y) ** 2)
                    if dist < best_dist:
                        best_dist = dist
                        best_dir = d
                else:
                    if random.random() < 0.3:
                        best_dir = random.choice(valid_dirs)
                        break
                    if dist < best_dist:
                        best_dist = dist
                        best_dir = d

            self.direction = best_dir

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def draw(self, screen):
        if self.respawning:
            color = BLUE_GHOST
        elif self.edible:
            if self.edible_timer < 1000 and int(self.edible_timer / 200) % 2 == 0:
                color = WHITE
            else:
                color = BLUE_GHOST
        else:
            color = self.color

        pygame.draw.circle(screen, color,
                         (int(self.x), int(self.y - 2)),
                         self.radius)

        bottom_pts = [
            (self.x - self.radius, self.y + self.radius - 2),
            (self.x - self.radius + 4, self.y + self.radius + 4),
            (self.x, self.y + self.radius - 2),
            (self.x + self.radius - 4, self.y + self.radius + 4),
            (self.x + self.radius, self.y + self.radius - 2),
        ]
        pygame.draw.polygon(screen, color, bottom_pts)

        eye_x1 = self.x - self.radius * 0.4
        eye_x2 = self.x + self.radius * 0.4
        eye_y = self.y - self.radius * 0.2
        eye_r = self.radius * 0.3

        pygame.draw.circle(screen, WHITE, (int(eye_x1), int(eye_y)), int(eye_r))
        pygame.draw.circle(screen, WHITE, (int(eye_x2), int(eye_y)), int(eye_r))

        if not self.edible and not self.respawning:
            pupil_offset_x = self.direction[0] * self.eye_offset
            pupil_offset_y = self.direction[1] * self.eye_offset
            pygame.draw.circle(screen, BLUE,
                             (int(eye_x1 + pupil_offset_x),
                              int(eye_y + pupil_offset_y)),
                             int(eye_r * 0.5))
            pygame.draw.circle(screen, BLUE,
                             (int(eye_x2 + pupil_offset_x),
                              int(eye_y + pupil_offset_y)),
                             int(eye_r * 0.5))
        else:
            pygame.draw.circle(screen, WHITE,
                             (int(eye_x1), int(eye_y)), int(eye_r * 0.3))
            pygame.draw.circle(screen, WHITE,
                             (int(eye_x2), int(eye_y)), int(eye_r * 0.3))
