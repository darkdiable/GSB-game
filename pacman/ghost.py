import pygame
import math
import random
from constants import (
    CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
    GHOST_SPEED, GHOST_HOUSE,
    UP, DOWN, LEFT, RIGHT, STOP,
    RED, PINK, CYAN, ORANGE, GREEN, PURPLE, BLUE, WHITE,
    POWER_DURATION
)


class Ghost:
    def __init__(self, ghost_type, start_x, start_y):
        self.ghost_type = ghost_type
        self.start_x = start_x
        self.start_y = start_y
        self.colors = {
            'blinky': RED,
            'pinky': PINK,
            'inky': CYAN,
            'clyde': ORANGE,
            'slimy': GREEN,
            'spooky': PURPLE
        }
        self.reset()

    def reset(self):
        self.grid_x = self.start_x
        self.grid_y = self.start_y
        self.x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
        self.y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
        self.direction = self._get_random_direction()
        self.speed = GHOST_SPEED
        self.radius = CELL_SIZE // 2 - 2
        self.vulnerable = False
        self.vulnerable_timer = 0
        self.eaten = False
        self.eye_direction = self.direction

        delay_map = {
            'blinky': 0,
            'pinky': 500,
            'inky': 1500,
            'clyde': 2500,
            'slimy': 3500,
            'spooky': 4500
        }
        self.house_timer = -delay_map.get(self.ghost_type, 0)
        self.in_house = (self.house_timer < 0)

    def _get_random_direction(self):
        directions = [UP, DOWN, LEFT, RIGHT]
        return random.choice(directions)

    def _get_possible_directions(self, maze):
        directions = [UP, DOWN, LEFT, RIGHT]
        opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        possible = []

        for d in directions:
            if d == opposite.get(self.direction, None):
                continue
            dx, dy = d
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy

            if new_x < 0 or new_x >= GRID_WIDTH:
                possible.append(d)
                continue

            if self.in_house:
                if maze.is_walkable(new_x, new_y) or maze.get_cell(new_x, new_y) == GHOST_HOUSE:
                    possible.append(d)
            else:
                if maze.is_walkable(new_x, new_y):
                    possible.append(d)

        if not possible:
            for d in directions:
                dx, dy = d
                new_x = self.grid_x + dx
                new_y = self.grid_y + dy
                if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                    if maze.is_walkable(new_x, new_y):
                        possible.append(d)

        return possible if possible else [self.direction]

    def _choose_direction(self, maze, pacman):
        possible = self._get_possible_directions(maze)

        if self.eaten:
            target_x, target_y = 13, 14
            return self._get_best_direction(possible, target_x, target_y)

        if self.vulnerable:
            return random.choice(possible)

        if self.ghost_type == 'blinky':
            target_x, target_y = pacman.grid_x, pacman.grid_y
        elif self.ghost_type == 'pinky':
            px, py = pacman.direction
            target_x = pacman.grid_x + px * 4
            target_y = pacman.grid_y + py * 4
        elif self.ghost_type == 'inky':
            px, py = pacman.direction
            target_x = pacman.grid_x + px * 2
            target_y = pacman.grid_y + py * 2
        else:
            dist = math.sqrt(
                (self.grid_x - pacman.grid_x) ** 2 +
                (self.grid_y - pacman.grid_y) ** 2
            )
            if dist > 8:
                target_x, target_y = pacman.grid_x, pacman.grid_y
            else:
                target_x, target_y = 1, GRID_HEIGHT - 2

        return self._get_best_direction(possible, target_x, target_y)

    def _get_best_direction(self, possible, target_x, target_y):
        best_dir = possible[0]
        min_dist = float('inf')

        for d in possible:
            dx, dy = d
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            dist = math.sqrt(
                (new_x - target_x) ** 2 +
                (new_y - target_y) ** 2
            )
            if dist < min_dist:
                min_dist = dist
                best_dir = d

        return best_dir

    def make_vulnerable(self):
        if not self.eaten:
            self.vulnerable = True
            self.vulnerable_timer = POWER_DURATION

    def update(self, maze, pacman, delta_time):
        if self.vulnerable and not self.eaten:
            self.vulnerable_timer -= delta_time
            if self.vulnerable_timer <= 0:
                self.vulnerable = False

        if self.eaten:
            if self.grid_x == 13 and self.grid_y == 14:
                self.eaten = False
                self.vulnerable = False
                self.in_house = True
                self.house_timer = -2000
                self.x = self.start_x * CELL_SIZE + CELL_SIZE // 2
                self.y = self.start_y * CELL_SIZE + CELL_SIZE // 2
                self.grid_x = self.start_x
                self.grid_y = self.start_y

        if self.in_house:
            self.house_timer += delta_time
            if self.house_timer < 0:
                self.direction = STOP
            elif self.grid_y > 12:
                self.direction = UP
            else:
                self.in_house = False
                self.direction = self._choose_direction(maze, pacman)

        if self._is_centered():
            if not self.in_house:
                self.direction = self._choose_direction(maze, pacman)
            self.eye_direction = self.direction
            self.grid_x = int(self.x // CELL_SIZE)
            self.grid_y = int(self.y // CELL_SIZE)

        if self.house_timer >= 0 or not self.in_house:
            dx, dy = self.direction
            speed = self.speed if not self.eaten else self.speed * 2
            self.x += dx * speed
            self.y += dy * speed

        if self.x < -CELL_SIZE // 2:
            self.x = GRID_WIDTH * CELL_SIZE + CELL_SIZE // 2
        elif self.x > GRID_WIDTH * CELL_SIZE + CELL_SIZE // 2:
            self.x = -CELL_SIZE // 2

    def _is_centered(self):
        grid_x = int(self.x // CELL_SIZE)
        grid_y = int(self.y // CELL_SIZE)
        center_x = grid_x * CELL_SIZE + CELL_SIZE // 2
        center_y = grid_y * CELL_SIZE + CELL_SIZE // 2
        tolerance = self.speed
        return (abs(self.x - center_x) <= tolerance and
                abs(self.y - center_y) <= tolerance)

    def get_eaten(self):
        self.eaten = True
        self.vulnerable = False

    def draw(self, screen):
        center = (int(self.x), int(self.y))

        if self.eaten:
            self._draw_eyes(screen)
            return

        color = self.colors[self.ghost_type]
        if self.vulnerable:
            if self.vulnerable_timer < 1500:
                if int(pygame.time.get_ticks() / 200) % 2 == 0:
                    color = WHITE
                else:
                    color = BLUE
            else:
                color = BLUE

        pygame.draw.circle(screen, color, center, self.radius)

        bottom_y = self.y + self.radius
        wave_points = [(int(self.x - self.radius), int(bottom_y))]
        for i in range(-self.radius, self.radius + 1, 6):
            wave_y = bottom_y + (4 if (i // 6) % 2 == 0 else -2)
            wave_points.append((int(self.x + i), int(wave_y)))
        wave_points.append((int(self.x + self.radius), int(bottom_y)))
        wave_points.append((int(self.x + self.radius), int(self.y)))
        wave_points.append((int(self.x - self.radius), int(self.y)))

        pygame.draw.polygon(screen, color, wave_points)

        if not self.vulnerable:
            self._draw_eyes(screen)
        else:
            self._draw_scared_eyes(screen)

    def _draw_eyes(self, screen):
        eye_offset_x = 5
        eye_offset_y = -3
        eye_radius = 5
        pupil_radius = 3

        left_eye_x = self.x - eye_offset_x
        right_eye_x = self.x + eye_offset_x
        eye_y = self.y + eye_offset_y

        dx, dy = self.eye_direction
        pupil_offset = 2

        pygame.draw.circle(screen, WHITE, (int(left_eye_x), int(eye_y)), eye_radius)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x), int(eye_y)), eye_radius)

        pygame.draw.circle(
            screen, BLUE,
            (int(left_eye_x + dx * pupil_offset), int(eye_y + dy * pupil_offset)),
            pupil_radius
        )
        pygame.draw.circle(
            screen, BLUE,
            (int(right_eye_x + dx * pupil_offset), int(eye_y + dy * pupil_offset)),
            pupil_radius
        )

    def _draw_scared_eyes(self, screen):
        eye_offset_x = 5
        eye_offset_y = -3
        eye_size = 4

        left_eye_x = self.x - eye_offset_x
        right_eye_x = self.x + eye_offset_x
        eye_y = self.y + eye_offset_y

        pygame.draw.rect(
            screen, WHITE,
            pygame.Rect(left_eye_x - eye_size, eye_y - eye_size, eye_size * 2, eye_size * 2)
        )
        pygame.draw.rect(
            screen, WHITE,
            pygame.Rect(right_eye_x - eye_size, eye_y - eye_size, eye_size * 2, eye_size * 2)
        )
