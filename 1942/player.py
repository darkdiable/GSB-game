import pygame
from constants import *


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.score = 0
        self.active = True
        self.invincible = False
        self.invincible_timer = 0
        self.shoot_cooldown = 0
        self.bomb_cooldown = 0
        self.engine_flame = 0

    def handle_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(100, min(SCREEN_HEIGHT - self.height - 50, self.y))

    def update(self):
        self.engine_flame = (self.engine_flame + 1) % 20
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1
        if self.invincible:
            self.invincible_timer -= 16
            if self.invincible_timer <= 0:
                self.invincible = False

    def shoot(self):
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = 10
            bullets = []
            bullets.append((self.x + 15, self.y, False, False))
            bullets.append((self.x + self.width - 21, self.y, False, False))
            return bullets
        return None

    def drop_bomb(self):
        if self.bomb_cooldown <= 0:
            self.bomb_cooldown = 30
            return (self.x + self.width // 2 - BOMB_WIDTH // 2, self.y + self.height, True)
        return None

    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.invincible_timer = PLAYER_INVINCIBLE_TIME
            if self.health <= 0:
                self.active = False

    def is_alive(self):
        return self.active and self.health > 0

    def get_rect(self):
        return pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)

    def draw(self, screen):
        if self.invincible and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        x, y = self.x, self.y

        pygame.draw.rect(screen, DARK_GRAY, (x + 25, y + 10, 30, 40))
        pygame.draw.rect(screen, GRAY, (x + 20, y + 15, 40, 30))

        pygame.draw.polygon(screen, DARK_GRAY, [
            (x + 40, y),
            (x + 30, y + 15),
            (x + 50, y + 15)
        ])

        pygame.draw.rect(screen, GRAY, (x, y + 20, 80, 8))
        pygame.draw.rect(screen, DARK_GRAY, (x + 5, y + 18, 70, 12))

        pygame.draw.rect(screen, GRAY, (x + 20, y + 35, 40, 20))
        pygame.draw.polygon(screen, DARK_GRAY, [
            (x + 25, y + 55),
            (x + 35, y + 60),
            (x + 45, y + 60),
            (x + 55, y + 55)
        ])

        for engine_x in [x + 8, x + 62]:
            pygame.draw.rect(screen, DARK_GRAY, (engine_x, y + 15, 10, 20))
            pygame.draw.circle(screen, BLACK, (engine_x + 5, y + 15), 5)
            if self.engine_flame < 10:
                pygame.draw.polygon(screen, ORANGE, [
                    (engine_x + 2, y + 35),
                    (engine_x + 5, y + 45),
                    (engine_x + 8, y + 35)
                ])
                pygame.draw.polygon(screen, YELLOW, [
                    (engine_x + 3, y + 35),
                    (engine_x + 5, y + 40),
                    (engine_x + 7, y + 35)
                ])

        for engine_x in [x + 8, x + 62]:
            pygame.draw.rect(screen, DARK_GRAY, (engine_x, y + 40, 10, 15))
            pygame.draw.circle(screen, BLACK, (engine_x + 5, y + 40), 5)
            if self.engine_flame < 10:
                pygame.draw.polygon(screen, ORANGE, [
                    (engine_x + 2, y + 55),
                    (engine_x + 5, y + 62),
                    (engine_x + 8, y + 55)
                ])
                pygame.draw.polygon(screen, YELLOW, [
                    (engine_x + 3, y + 55),
                    (engine_x + 5, y + 59),
                    (engine_x + 7, y + 55)
                ])

        pygame.draw.rect(screen, (100, 149, 237), (x + 35, y + 18, 10, 8))
        pygame.draw.rect(screen, (100, 149, 237), (x + 32, y + 28, 16, 6))

        pygame.draw.rect(screen, RED, (x + 38, y + 42, 4, 12))
        pygame.draw.rect(screen, RED, (x + 38, y + 42, 12, 4))
