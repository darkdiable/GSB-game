import pygame
import random
from constants import *


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.active = True
        self.shoot_cooldown = random.randint(60, 120)
        self.hit_flash = 0

        if enemy_type == 'plane':
            self.width = ENEMY_PLANE_WIDTH
            self.height = ENEMY_PLANE_HEIGHT
            self.health = ENEMY_PLANE_HEALTH
            self.max_health = ENEMY_PLANE_HEALTH
            self.speed = ENEMY_PLANE_SPEED
            self.score = 100
            self.dx = random.choice([-1, 0, 1])
            self.can_shoot = True
        elif enemy_type == 'ship':
            self.width = SHIP_WIDTH
            self.height = SHIP_HEIGHT
            self.health = SHIP_HEALTH
            self.max_health = SHIP_HEALTH
            self.speed = SHIP_SPEED
            self.score = 300
            self.dx = random.choice([-1, 1])
            self.can_shoot = True
        else:
            self.width = AA_GUN_WIDTH
            self.height = AA_GUN_HEIGHT
            self.health = AA_GUN_HEALTH
            self.max_health = AA_GUN_HEALTH
            self.speed = 0
            self.score = 200
            self.dx = 0
            self.can_shoot = True

    def update(self, player_x, player_y):
        if self.hit_flash > 0:
            self.hit_flash -= 1

        if self.enemy_type == 'plane':
            self.y += self.speed
            self.x += self.dx * 2
            if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
                self.dx *= -1
        elif self.enemy_type == 'ship':
            self.x += self.dx * self.speed
            if self.x <= 50 or self.x >= SCREEN_WIDTH - self.width - 50:
                self.dx *= -1
            self.y += BG_SCROLL_SPEED

        if self.y > SCREEN_HEIGHT + self.height:
            self.active = False

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self, player_x, player_y):
        if self.can_shoot and self.shoot_cooldown <= 0 and self.y > 0 and self.y < SCREEN_HEIGHT - 100:
            self.shoot_cooldown = random.randint(80, 150)
            bullets = []
            if self.enemy_type == 'plane':
                bullets.append((self.x + self.width // 2 - BULLET_WIDTH // 2, self.y + self.height, False, True))
            else:
                dx = player_x - self.x
                dy = player_y - self.y
                dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
                bullets.append((self.x + self.width // 2 - BULLET_WIDTH // 2, self.y, False, True))
            return bullets
        return None

    def take_damage(self, damage):
        self.health -= damage
        self.hit_flash = 10
        if self.health <= 0:
            self.active = False
            return True
        return False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        if self.hit_flash > 0 and self.hit_flash % 4 < 2:
            return

        x, y = self.x, self.y

        if self.enemy_type == 'plane':
            self._draw_plane(screen, x, y)
        elif self.enemy_type == 'ship':
            self._draw_ship(screen, x, y)
        else:
            self._draw_aa_gun(screen, x, y)

        if self.health < self.max_health:
            bar_width = self.width
            bar_height = 4
            pygame.draw.rect(screen, BLACK, (x, y - 8, bar_width, bar_height))
            pygame.draw.rect(screen, RED, (x, y - 8, int(bar_width * self.health / self.max_health), bar_height))

    def _draw_plane(self, screen, x, y):
        pygame.draw.rect(screen, GRAY, (x + 15, y + 10, 20, 25))
        pygame.draw.polygon(screen, DARK_GRAY, [
            (x + 25, y + 35),
            (x + 15, y + 40),
            (x + 35, y + 40)
        ])

        pygame.draw.rect(screen, DARK_GRAY, (x, y + 15, 50, 6))
        pygame.draw.rect(screen, GRAY, (x + 5, y + 13, 40, 10))

        pygame.draw.rect(screen, DARK_GRAY, (x + 18, y, 14, 10))
        pygame.draw.polygon(screen, GRAY, [
            (x + 20, y),
            (x + 25, y - 5),
            (x + 30, y)
        ])

        pygame.draw.rect(screen, BLACK, (x + 5, y + 20, 8, 8))
        pygame.draw.rect(screen, BLACK, (x + 37, y + 20, 8, 8))

        pygame.draw.ellipse(screen, RED, (x + 22, y + 15, 6, 6))

    def _draw_ship(self, screen, x, y):
        pygame.draw.polygon(screen, GRAY, [
            (x, y + 20),
            (x + 10, y + 40),
            (x + 90, y + 40),
            (x + 100, y + 20),
            (x + 90, y + 15),
            (x + 10, y + 15)
        ])

        pygame.draw.rect(screen, DARK_GRAY, (x + 15, y + 15, 70, 5))

        pygame.draw.rect(screen, GRAY, (x + 35, y - 5, 30, 25))
        pygame.draw.rect(screen, DARK_GRAY, (x + 40, y, 20, 15))

        pygame.draw.rect(screen, (100, 149, 237), (x + 42, y + 3, 8, 6))
        pygame.draw.rect(screen, (100, 149, 237), (x + 52, y + 3, 8, 6))

        pygame.draw.rect(screen, DARK_GRAY, (x + 20, y - 25, 4, 40))
        pygame.draw.polygon(screen, RED, [
            (x + 24, y - 25),
            (x + 40, y - 18),
            (x + 24, y - 10)
        ])

        pygame.draw.rect(screen, BLACK, (x + 70, y + 5, 15, 10))
        pygame.draw.circle(screen, DARK_GRAY, (x + 85, y + 10), 5)

    def _draw_aa_gun(self, screen, x, y):
        pygame.draw.rect(screen, DARK_GREEN, (x, y + 20, 50, 20))
        pygame.draw.rect(screen, GREEN, (x + 5, y + 25, 40, 10))

        pygame.draw.circle(screen, DARK_GRAY, (x + 25, y + 20), 15)
        pygame.draw.circle(screen, GRAY, (x + 25, y + 20), 12)

        pygame.draw.rect(screen, DARK_GRAY, (x + 22, y, 6, 25))
        pygame.draw.rect(screen, BLACK, (x + 20, y - 5, 10, 8))

        for i in range(3):
            pygame.draw.rect(screen, SAND, (x + 5 + i * 15, y + 35, 8, 5))
