import pygame
from . import config


class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = config.BOMB_SPEED
        self.active = True
        self.radius = 6
        self.blast_radius = 50
        self.anim = 0

    def update(self):
        self.y += self.speed
        self.anim += 1
        if self.y > config.SCREEN_HEIGHT + 10:
            self.active = False

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def draw(self, surface):
        pygame.draw.circle(surface, config.DARK_GRAY, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, config.GRAY, (int(self.x), int(self.y)), self.radius - 2)
        pygame.draw.circle(surface, config.YELLOW, (int(self.x), int(self.y) - 2), 2)
