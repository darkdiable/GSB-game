import pygame
import random
import math
from .config import *
from . import weapons


class Destroyer:
    def __init__(self):
        self.x = SCREEN_WIDTH + 50
        self.y = WATER_LEVEL - 5
        self.width = 90
        self.height = 25
        self.health = DESTROYER_HEALTH
        self.max_health = DESTROYER_HEALTH
        self.speed = DESTROYER_SPEED
        self.bomb_timer = random.randint(0, DESTROYER_BOMB_RATE // 2)
        self.active = True
        self.wave_offset = random.random() * 3.14 * 2

    def update(self):
        self.x -= self.speed
        self.wave_offset += 0.05
        if self.x < -self.width:
            self.active = False

        self.bomb_timer -= 1

    def drop_depth_charge(self, player_y):
        if self.bomb_timer <= 0 and self.x > 100 and self.x < SCREEN_WIDTH - 100:
            self.bomb_timer = DESTROYER_BOMB_RATE + random.randint(-30, 30)
            return weapons.DepthCharge(self.x, self.y + self.height // 2)
        return None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.active = False
            return True
        return False

    def draw(self, screen):
        wave_y = self.y + int(math.sin(self.wave_offset) * 2)

        hull_rect = pygame.Rect(
            self.x - self.width // 2,
            wave_y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, SHIP_GRAY, hull_rect)
        pygame.draw.rect(screen, (80, 80, 90), hull_rect, 2)

        pygame.draw.polygon(screen, SHIP_GRAY, [
            (self.x - self.width // 2, wave_y + self.height // 2),
            (self.x - self.width // 2 + 15, wave_y + self.height // 2 + 10),
            (self.x + self.width // 2, wave_y + self.height // 2),
        ])

        bridge_rect = pygame.Rect(
            self.x + 10,
            wave_y - self.height // 2 - 20,
            25,
            22
        )
        pygame.draw.rect(screen, DARK_GRAY, bridge_rect)
        pygame.draw.rect(screen, (70, 70, 80), bridge_rect, 2)

        pygame.draw.rect(screen, (150, 150, 160),
                        (self.x + 12, wave_y - self.height // 2 - 28, 3, 10))

        gun_rect = pygame.Rect(
            self.x - 25,
            wave_y - self.height // 2 + 2,
            20,
            6
        )
        pygame.draw.rect(screen, DARK_GRAY, gun_rect)

        depth_charge_rect = pygame.Rect(
            self.x + 15,
            wave_y + self.height // 2 - 8,
            10,
            10
        )
        pygame.draw.ellipse(screen, (60, 60, 70), depth_charge_rect)

        pygame.draw.rect(screen, RED,
                        (self.x - self.width // 2,
                         wave_y - self.height // 2 - 25,
                         self.width,
                         3))

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )


class EnemySubmarine:
    def __init__(self):
        self.x = SCREEN_WIDTH + 40
        self.y = random.randint(WATER_LEVEL + 80, SCREEN_HEIGHT - 60)
        self.width = 60
        self.height = 26
        self.health = ENEMY_SUB_HEALTH
        self.max_health = ENEMY_SUB_HEALTH
        self.speed = ENEMY_SUB_SPEED
        self.torpedo_timer = random.randint(0, ENEMY_SUB_TORPEDO_RATE // 2)
        self.active = True
        self.bubbles = []
        self.bubble_timer = 0

    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.active = False

        self.torpedo_timer -= 1

        self.bubble_timer += 1
        if self.bubble_timer >= 10:
            self.bubble_timer = 0
            self.bubbles.append({
                'x': self.x + self.width // 2,
                'y': self.y,
                'size': 2,
                'speed': 1
            })

        for bubble in self.bubbles[:]:
            bubble['y'] -= bubble['speed']
            if bubble['y'] < WATER_LEVEL:
                self.bubbles.remove(bubble)

    def fire_torpedo(self, player_x):
        if self.torpedo_timer <= 0 and self.x > player_x and self.x < SCREEN_WIDTH:
            self.torpedo_timer = ENEMY_SUB_TORPEDO_RATE + random.randint(-20, 20)
            return weapons.Torpedo(self.x - self.width // 2, self.y, False)
        return None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.active = False
            return True
        return False

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
        pygame.draw.ellipse(screen, (80, 40, 40), body_rect)
        pygame.draw.ellipse(screen, (120, 60, 60), body_rect, 2)

        tower_rect = pygame.Rect(
            self.x - 15,
            self.y - self.height // 2 - 10,
            18,
            13
        )
        pygame.draw.rect(screen, (90, 50, 50), tower_rect)
        pygame.draw.rect(screen, (130, 70, 70), tower_rect, 2)

        propeller_x = self.x + self.width // 2 + 8
        pygame.draw.circle(screen, (100, 60, 60), (propeller_x, self.y), 7)
        for i in range(4):
            angle = (pygame.time.get_ticks() // 40 + i * 90) * 3.14159 / 180
            end_x = propeller_x + 9 * math.cos(angle)
            end_y = self.y + 9 * math.sin(angle)
            pygame.draw.line(screen, (140, 80, 80), (propeller_x, self.y),
                           (int(end_x), int(end_y)), 2)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
