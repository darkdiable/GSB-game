import pygame
import random
import math
from . import config
from .bullet import EnemyBullet


class Enemy:
    FIGHTER = 'fighter'
    BOMBER = 'bomber'

    def __init__(self, enemy_type=None, x=None):
        self.enemy_type = enemy_type or random.choice([self.FIGHTER, self.BOMBER])
        if self.enemy_type == self.FIGHTER:
            self.width = 30
            self.height = 30
            self.speed = config.ENEMY_FIGHTER_SPEED
            self.health = config.ENEMY_FIGHTER_HEALTH
            self.score_value = 100
        else:
            self.width = 40
            self.height = 36
            self.speed = config.ENEMY_BOMBER_SPEED
            self.health = config.ENEMY_BOMBER_HEALTH
            self.score_value = 200
        self.x = x if x is not None else random.randint(20, config.SCREEN_WIDTH - 20 - self.width)
        self.y = -self.height - random.randint(0, 100)
        self.active = True
        self.shoot_timer = random.randint(30, config.ENEMY_SHOOT_RATE)
        self.move_pattern = random.choice(['straight', 'sine', 'zigzag'])
        self.move_timer = 0
        self.start_x = self.x

    def update(self, player_x=None):
        self.move_timer += 1
        if self.move_pattern == 'straight':
            self.y += self.speed
        elif self.move_pattern == 'sine':
            self.y += self.speed
            self.x = self.start_x + math.sin(self.move_timer * 0.05) * 60
        elif self.move_pattern == 'zigzag':
            self.y += self.speed
            if (self.move_timer // 40) % 2 == 0:
                self.x += self.speed * 0.8
            else:
                self.x -= self.speed * 0.8
        self.x = max(0, min(config.SCREEN_WIDTH - self.width, self.x))
        if self.y > config.SCREEN_HEIGHT + 50:
            self.active = False
        self.shoot_timer -= 1

    def shoot(self, player_x=None, player_y=None):
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(40, config.ENEMY_SHOOT_RATE)
            bullets = []
            cx = self.x + self.width // 2
            cy = self.y + self.height
            if player_x is not None and player_y is not None:
                dx = player_x - cx
                dy = player_y - cy
                dist = max(1, math.sqrt(dx * dx + dy * dy))
                dx /= dist
                dy /= dist
                bullets.append(EnemyBullet(cx, cy, dx, dy, 3.5))
            else:
                bullets.append(EnemyBullet(cx, cy, 0, 1))
            if self.enemy_type == self.BOMBER:
                bullets.append(EnemyBullet(cx - 10, cy, -0.2, 1, 3))
                bullets.append(EnemyBullet(cx + 10, cy, 0.2, 1, 3))
            return bullets
        return []

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.active = False
            return True
        return False

    def get_rect(self):
        return pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)

    def draw(self, surface):
        if self.enemy_type == self.FIGHTER:
            self._draw_fighter(surface)
        else:
            self._draw_bomber(surface)

    def _draw_fighter(self, surface):
        cx = self.x + self.width // 2
        pygame.draw.ellipse(surface, (180, 50, 50),
                            (self.x + 6, self.y + 4, self.width - 12, self.height - 8))
        pygame.draw.polygon(surface, (160, 40, 40), [
            (cx, self.y + self.height),
            (cx - 8, self.y + 6),
            (cx + 8, self.y + 6)
        ])
        pygame.draw.polygon(surface, (140, 30, 30), [
            (self.x, self.y + 14),
            (self.x + 8, self.y + 6),
            (self.x + 10, self.y + 20)
        ])
        pygame.draw.polygon(surface, (140, 30, 30), [
            (self.x + self.width, self.y + 14),
            (self.x + self.width - 8, self.y + 6),
            (self.x + self.width - 10, self.y + 20)
        ])
        pygame.draw.circle(surface, (100, 180, 220),
                           (cx, self.y + 12), 4)

    def _draw_bomber(self, surface):
        cx = self.x + self.width // 2
        pygame.draw.ellipse(surface, (50, 50, 150),
                            (self.x + 4, self.y + 6, self.width - 8, self.height - 12))
        pygame.draw.ellipse(surface, (60, 60, 170),
                            (self.x + 8, self.y + 8, self.width - 16, self.height - 18))
        pygame.draw.polygon(surface, (40, 40, 130), [
            (cx, self.y + self.height),
            (cx - 10, self.y + 10),
            (cx + 10, self.y + 10)
        ])
        pygame.draw.polygon(surface, (40, 40, 130), [
            (self.x - 2, self.y + 18),
            (self.x + 10, self.y + 8),
            (self.x + 12, self.y + 24)
        ])
        pygame.draw.polygon(surface, (40, 40, 130), [
            (self.x + self.width + 2, self.y + 18),
            (self.x + self.width - 10, self.y + 8),
            (self.x + self.width - 12, self.y + 24)
        ])
        pygame.draw.circle(surface, (80, 160, 200),
                           (cx, self.y + 14), 5)
        pygame.draw.circle(surface, (200, 200, 210),
                           (self.x + 8, self.y + self.height - 8), 3)
        pygame.draw.circle(surface, (200, 200, 210),
                           (self.x + self.width - 8, self.y + self.height - 8), 3)
