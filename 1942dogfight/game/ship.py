import pygame
import math
import random
from . import config
from .bullet import EnemyBullet


class Ship:
    DESTROYER = 'destroyer'
    CRUISER = 'cruiser'

    def __init__(self, ship_type=None, x=None):
        self.ship_type = ship_type or random.choice([self.DESTROYER, self.CRUISER])
        if self.ship_type == self.DESTROYER:
            self.width = 60
            self.height = 24
            self.health = config.SHIP_HEALTH
            self.score_value = 500
            self.speed = config.SHIP_SPEED
        else:
            self.width = 80
            self.height = 30
            self.health = config.SHIP_HEALTH + 8
            self.speed = config.SHIP_SPEED * 0.7
            self.score_value = 800
        self.x = x if x is not None else random.randint(10, config.SCREEN_WIDTH - self.width - 10)
        self.y = -self.height - random.randint(0, 200)
        self.active = True
        self.shoot_timer = random.randint(20, config.SHIP_SHOOT_RATE)
        self.move_dir = random.choice([-1, 1])
        self.hit_flash = 0

    def update(self):
        self.y += self.speed
        self.x += self.move_dir * self.speed * 0.5
        if self.x < 5:
            self.move_dir = 1
        elif self.x > config.SCREEN_WIDTH - self.width - 5:
            self.move_dir = -1
        if self.y > config.SCREEN_HEIGHT + 50:
            self.active = False
        self.shoot_timer -= 1
        if self.hit_flash > 0:
            self.hit_flash -= 1

    def shoot(self, player_x=None, player_y=None):
        if self.shoot_timer <= 0:
            self.shoot_timer = config.SHIP_SHOOT_RATE
            bullets = []
            cx = self.x + self.width // 2
            if self.ship_type == self.DESTROYER:
                bullets.append(EnemyBullet(cx, self.y + self.height, 0, 1, 3))
                if player_x is not None:
                    dx = player_x - cx
                    dy = player_y - (self.y + self.height)
                    dist = max(1, math.sqrt(dx * dx + dy * dy))
                    bullets.append(EnemyBullet(cx, self.y + self.height,
                                               dx / dist, dy / dist, 3.5, (255, 100, 100)))
            else:
                for offset in [-20, 0, 20]:
                    bx = cx + offset
                    if player_x is not None:
                        dx = player_x - bx
                        dy = player_y - (self.y + self.height)
                        dist = max(1, math.sqrt(dx * dx + dy * dy))
                        bullets.append(EnemyBullet(bx, self.y + self.height,
                                                   dx / dist, dy / dist, 3, (255, 120, 80)))
                    else:
                        bullets.append(EnemyBullet(bx, self.y + self.height, 0, 1, 3))
            return bullets
        return []

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 4
        if self.health <= 0:
            self.active = False
            return True
        return False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        if self.ship_type == self.DESTROYER:
            self._draw_destroyer(surface)
        else:
            self._draw_cruiser(surface)

    def _draw_destroyer(self, surface):
        color = config.WHITE if self.hit_flash > 0 else config.SHIP_GRAY
        deck_color = config.WHITE if self.hit_flash > 0 else config.SHIP_DECK
        cx = self.x + self.width // 2
        pygame.draw.polygon(surface, color, [
            (self.x + 5, self.y + 4),
            (self.x + self.width - 5, self.y + 4),
            (self.x + self.width - 10, self.y + self.height - 4),
            (self.x + 10, self.y + self.height - 4)
        ])
        pygame.draw.polygon(surface, deck_color, [
            (self.x + 8, self.y + 6),
            (self.x + self.width - 8, self.y + 6),
            (self.x + self.width - 12, self.y + self.height - 6),
            (self.x + 12, self.y + self.height - 6)
        ])
        pygame.draw.rect(surface, color, (cx - 6, self.y - 6, 12, 10))
        pygame.draw.rect(surface, deck_color, (cx - 4, self.y - 4, 8, 8))
        pygame.draw.line(surface, color, (cx, self.y - 6), (cx, self.y - 14), 2)
        pygame.draw.rect(surface, (100, 100, 110), (cx - 14, self.y + 8, 6, 6))
        for ex in [self.x + 20, cx + 14]:
            pygame.draw.circle(surface, (140, 140, 150), (ex, self.y + 12), 2)

    def _draw_cruiser(self, surface):
        color = config.WHITE if self.hit_flash > 0 else config.SHIP_GRAY
        deck_color = config.WHITE if self.hit_flash > 0 else config.SHIP_DECK
        cx = self.x + self.width // 2
        pygame.draw.polygon(surface, color, [
            (self.x + 8, self.y + 4),
            (self.x + self.width - 8, self.y + 4),
            (self.x + self.width - 12, self.y + self.height - 4),
            (self.x + 12, self.y + self.height - 4)
        ])
        pygame.draw.polygon(surface, deck_color, [
            (self.x + 11, self.y + 6),
            (self.x + self.width - 11, self.y + 6),
            (self.x + self.width - 14, self.y + self.height - 6),
            (self.x + 14, self.y + self.height - 6)
        ])
        for tower_x in [cx - 20, cx, cx + 20]:
            pygame.draw.rect(surface, color, (tower_x - 5, self.y - 5, 10, 9))
            pygame.draw.rect(surface, deck_color, (tower_x - 3, self.y - 3, 6, 6))
        pygame.draw.line(surface, color, (cx, self.y - 5), (cx, self.y - 16), 2)
        for ex in [self.x + 18, cx + 18, cx - 18]:
            pygame.draw.circle(surface, (140, 140, 150), (ex, self.y + 10), 2)
