import pygame
import math
from .config import *
from . import weapons


class PlayerSubmarine:
    def __init__(self):
        self.x = PLAYER_X
        self.y = SCREEN_HEIGHT // 2
        self.width = 70
        self.height = 30
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED
        self.missile_cooldown = 0
        self.torpedo_cooldown = 0
        self.bubbles = []
        self.bubble_timer = 0

    def move(self, dy):
        self.y += dy * self.speed
        water_bottom = WATER_LEVEL + 30
        if self.y < water_bottom + self.height // 2:
            self.y = water_bottom + self.height // 2
        if self.y > SCREEN_HEIGHT - self.height // 2:
            self.y = SCREEN_HEIGHT - self.height // 2

    def update(self):
        if self.missile_cooldown > 0:
            self.missile_cooldown -= 1
        if self.torpedo_cooldown > 0:
            self.torpedo_cooldown -= 1

        self.bubble_timer += 1
        if self.bubble_timer >= 8:
            self.bubble_timer = 0
            self.bubbles.append({
                'x': self.x - self.width // 2,
                'y': self.y,
                'size': 3,
                'speed': 1.5
            })

        for bubble in self.bubbles[:]:
            bubble['y'] -= bubble['speed']
            bubble['x'] += 0.3
            if bubble['y'] < WATER_LEVEL:
                self.bubbles.remove(bubble)

    def fire_missile(self):
        if self.missile_cooldown <= 0:
            self.missile_cooldown = MISSILE_COOLDOWN
            return weapons.Missile(self.x, self.y - self.height // 2)
        return None

    def fire_torpedo(self):
        if self.torpedo_cooldown <= 0:
            self.torpedo_cooldown = TORPEDO_COOLDOWN
            return weapons.Torpedo(self.x + self.width // 2, self.y, True)
        return None

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

    def draw(self, screen):
        for bubble in self.bubbles:
            pygame.draw.circle(screen, BUBBLE_COLOR,
                             (int(bubble['x']), int(bubble['y'])), bubble['size'])

        body_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.ellipse(screen, (50, 100, 150), body_rect)
        pygame.draw.ellipse(screen, (70, 130, 180), body_rect, 2)

        tower_rect = pygame.Rect(
            self.x - 5,
            self.y - self.height // 2 - 12,
            20,
            15
        )
        pygame.draw.rect(screen, (60, 110, 160), tower_rect)
        pygame.draw.rect(screen, (80, 140, 190), tower_rect, 2)

        periscope_rect = pygame.Rect(
            self.x + 2,
            self.y - self.height // 2 - 20,
            4,
            10
        )
        pygame.draw.rect(screen, (70, 120, 170), periscope_rect)

        propeller_x = self.x - self.width // 2 - 8
        pygame.draw.circle(screen, (80, 130, 180), (propeller_x, self.y), 8)
        for i in range(4):
            angle = (pygame.time.get_ticks() // 30 + i * 90) * 3.14159 / 180
            end_x = propeller_x + 10 * math.cos(angle)
            end_y = self.y + 10 * math.sin(angle)
            pygame.draw.line(screen, (100, 150, 200), (propeller_x, self.y),
                           (int(end_x), int(end_y)), 2)

        pygame.draw.line(screen, (100, 150, 200),
                        (self.x - 10, self.y - self.height // 2 + 5),
                        (self.x + 10, self.y - self.height // 2 + 5), 2)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
