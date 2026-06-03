import pygame
from . import config


class Player:
    def __init__(self):
        self.width = 48
        self.height = 56
        self.x = config.SCREEN_WIDTH // 2 - self.width // 2
        self.y = config.SCREEN_HEIGHT - self.height - 40
        self.speed = config.PLAYER_SPEED
        self.health = config.PLAYER_HEALTH
        self.max_health = config.PLAYER_HEALTH
        self.bullet_cooldown = 0
        self.bomb_cooldown = 0
        self.bombs = config.MAX_BOMBS
        self.max_bombs = config.MAX_BOMBS
        self.invincible = 0
        self.engine_anim = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        self.x = max(0, min(config.SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(config.SCREEN_HEIGHT - self.height, self.y))
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1
        self.engine_anim = (self.engine_anim + 1) % 6

    def shoot(self):
        if self.bullet_cooldown <= 0:
            self.bullet_cooldown = config.BULLET_COOLDOWN
            positions = [
                (self.x + 8, self.y),
                (self.x + self.width - 12, self.y),
            ]
            return positions
        return None

    def drop_bomb(self):
        if self.bomb_cooldown <= 0 and self.bombs > 0:
            self.bomb_cooldown = config.BOMB_COOLDOWN
            self.bombs -= 1
            return (self.x + self.width // 2, self.y + self.height)
        return None

    def take_damage(self, amount):
        if self.invincible > 0:
            return False
        self.health -= amount
        self.invincible = 30
        return self.health <= 0

    def get_rect(self):
        margin = 8
        return pygame.Rect(self.x + margin, self.y + margin,
                           self.width - margin * 2, self.height - margin * 2)

    def draw(self, surface):
        if self.invincible > 0 and self.invincible % 4 < 2:
            return
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        pygame.draw.ellipse(surface, (50, 80, 50),
                            (self.x + 8, cy - 4, self.width - 16, self.height - 20))
        pygame.draw.ellipse(surface, (70, 110, 70),
                            (self.x + 12, cy - 2, self.width - 24, self.height - 28))
        pygame.draw.polygon(surface, (80, 80, 90), [
            (cx, self.y + 2),
            (cx - 10, self.y + 18),
            (cx + 10, self.y + 18)
        ])
        pygame.draw.polygon(surface, (60, 60, 70), [
            (cx, self.y + 4),
            (cx - 6, self.y + 16),
            (cx + 6, self.y + 16)
        ])
        pygame.draw.polygon(surface, (80, 80, 90), [
            (self.x + 2, cy + 8),
            (self.x + 10, cy - 8),
            (self.x + 14, cy + 12)
        ])
        pygame.draw.polygon(surface, (80, 80, 90), [
            (self.x + self.width - 2, cy + 8),
            (self.x + self.width - 10, cy - 8),
            (self.x + self.width - 14, cy + 12)
        ])
        pygame.draw.polygon(surface, (90, 90, 100), [
            (cx - 16, cy + 6),
            (cx - 8, cy - 2),
            (cx + 8, cy - 2),
            (cx + 16, cy + 6)
        ])
        pygame.draw.polygon(surface, (70, 70, 80), [
            (cx - 12, cy + 4),
            (cx - 4, cy),
            (cx + 4, cy),
            (cx + 12, cy + 4)
        ])
        for i, ex in enumerate([self.x + 10, self.x + self.width - 14]):
            flame_len = 6 + (3 if self.engine_anim < 3 else 0)
            pygame.draw.polygon(surface, config.ORANGE, [
                (ex, self.y + self.height - 18),
                (ex + 4, self.y + self.height - 18 + flame_len),
                (ex + 8, self.y + self.height - 18)
            ])
            pygame.draw.polygon(surface, config.YELLOW, [
                (ex + 1, self.y + self.height - 18),
                (ex + 4, self.y + self.height - 18 + flame_len - 3),
                (ex + 7, self.y + self.height - 18)
            ])
        for i, ex in enumerate([self.x + 2, self.x + self.width - 6]):
            flame_len = 4 + (2 if self.engine_anim < 3 else 0)
            pygame.draw.polygon(surface, config.ORANGE, [
                (ex, cy + 8),
                (ex + 2, cy + 8 + flame_len),
                (ex + 4, cy + 8)
            ])
        pygame.draw.polygon(surface, (100, 100, 110), [
            (cx, self.y + self.height),
            (cx - 8, self.y + self.height - 12),
            (cx + 8, self.y + self.height - 12)
        ])
