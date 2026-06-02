import pygame
from constants import *
from sprites import create_bullet, create_enemy_bullet


class Bullet:
    def __init__(self, x, y, direction_x, direction_y, is_player=True, speed=None):
        self.x = x
        self.y = y
        self.is_player = is_player
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.active = True

        if is_player:
            self.image = create_bullet()
            self.speed = BULLET_SPEED
        else:
            self.image = create_enemy_bullet()
            self.speed = speed if speed else ENEMY_BULLET_SPEED

        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if (self.x < -20 or self.x > LEVEL_WIDTH + 20 or
                self.y < -20 or self.y > SCREEN_HEIGHT + 20):
            self.active = False

    def draw(self, surface, camera_x):
        if self.active:
            draw_x = self.rect.x - camera_x
            if -10 < draw_x < SCREEN_WIDTH + 10:
                surface.blit(self.image, (draw_x, self.rect.y))

    def get_rect(self):
        return self.rect
