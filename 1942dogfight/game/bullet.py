import pygame
from . import config


class Bullet:
    def __init__(self, x, y, dx=0, dy=-1, speed=None, color=None, owner='player'):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed or config.BULLET_SPEED
        self.color = color or config.YELLOW
        self.owner = owner
        self.width = 4
        self.height = 10 if owner == 'player' else 8
        self.active = True

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        if (self.y < -20 or self.y > config.SCREEN_HEIGHT + 20 or
                self.x < -20 or self.x > config.SCREEN_WIDTH + 20):
            self.active = False

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                           self.width, self.height)

    def draw(self, surface):
        if self.owner == 'player':
            pygame.draw.rect(surface, config.YELLOW,
                             (self.x - 1, self.y - 5, 3, 10))
            pygame.draw.rect(surface, config.WHITE,
                             (self.x, self.y - 3, 1, 6))
        else:
            pygame.draw.circle(surface, self.color,
                               (int(self.x), int(self.y)), 4)
            pygame.draw.circle(surface, config.WHITE,
                               (int(self.x), int(self.y)), 2)


class EnemyBullet(Bullet):
    def __init__(self, x, y, dx=0, dy=1, speed=None, color=None):
        super().__init__(x, y, dx, dy, speed or 4, color or config.RED, 'enemy')
        self.width = 6
        self.height = 6
