import pygame
from constants import *


class Bullet:
    def __init__(self, x, y, direction, is_enemy=False):
        self.x = x
        self.y = y
        self.direction = direction
        self.is_enemy = is_enemy
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        speed = ENEMY_BULLET_SPEED if is_enemy else BULLET_SPEED
        self.vx = speed * direction
        self.active = True

    def update(self):
        self.x += self.vx
        if self.x < -100 or self.x > SCREEN_WIDTH + 100:
            self.active = False

    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        if self.is_enemy:
            pygame.draw.rect(screen, RED, (draw_x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, YELLOW, (draw_x, self.y, self.width, self.height))
            pygame.draw.rect(screen, ORANGE, (draw_x, self.y + 1, self.width, self.height - 2))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
