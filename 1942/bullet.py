import pygame
from constants import *


class Bullet:
    def __init__(self, x, y, is_bomb=False, is_enemy=False):
        self.x = x
        self.y = y
        self.is_bomb = is_bomb
        self.is_enemy = is_enemy
        self.active = True

        if is_bomb:
            self.width = BOMB_WIDTH
            self.height = BOMB_HEIGHT
            self.speed = BOMB_SPEED
            self.damage = 3
        elif is_enemy:
            self.width = BULLET_WIDTH
            self.height = BULLET_HEIGHT
            self.speed = ENEMY_BULLET_SPEED
            self.damage = 1
        else:
            self.width = BULLET_WIDTH
            self.height = BULLET_HEIGHT
            self.speed = BULLET_SPEED
            self.damage = 1

    def update(self):
        if self.is_enemy:
            self.y += self.speed
        elif self.is_bomb:
            self.y += self.speed
        else:
            self.y -= self.speed

        if self.y < -self.height or self.y > SCREEN_HEIGHT + self.height:
            self.active = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        if self.is_bomb:
            pygame.draw.ellipse(screen, DARK_GRAY, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, GRAY, (self.x + 2, self.y + 2, self.width - 4, self.height - 4))
            pygame.draw.circle(screen, RED, (self.x + self.width // 2, self.y + self.height - 3), 4)
            pygame.draw.line(screen, YELLOW, (self.x + self.width // 2, self.y + self.height),
                             (self.x + self.width // 2, self.y + self.height + 8), 2)
        elif self.is_enemy:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, ORANGE, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))
        else:
            pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x + 1, self.y + 2, self.width - 2, self.height - 4))
