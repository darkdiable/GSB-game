import pygame
from .config import *


class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 6
        self.height = 15
        self.speed = MISSILE_SPEED
        self.damage = 20
        self.active = True

    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW,
                        (self.x - self.width // 2, self.y - self.height // 2,
                         self.width, self.height))
        pygame.draw.polygon(screen, ORANGE, [
            (self.x, self.y - self.height // 2),
            (self.x - self.width // 2, self.y - self.height // 2 + 5),
            (self.x + self.width // 2, self.y - self.height // 2 + 5)
        ])
        pygame.draw.rect(screen, RED,
                        (self.x - self.width // 2, self.y + self.height // 2 - 5,
                         self.width, 8))

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )


class Torpedo:
    def __init__(self, x, y, from_player=True):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 8
        self.speed = TORPEDO_SPEED if from_player else ENEMY_TORPEDO_SPEED
        self.direction = 1 if from_player else -1
        self.damage = 25
        self.active = True
        self.bubbles = []
        self.bubble_timer = 0

    def update(self):
        self.x += self.speed * self.direction
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.active = False

        self.bubble_timer += 1
        if self.bubble_timer >= 3:
            self.bubble_timer = 0
            self.bubbles.append({
                'x': self.x - self.width // 2 * self.direction,
                'y': self.y,
                'size': 2,
                'life': 15
            })

        for bubble in self.bubbles[:]:
            bubble['life'] -= 1
            bubble['y'] -= 0.5
            if bubble['life'] <= 0:
                self.bubbles.remove(bubble)

    def draw(self, screen):
        for bubble in self.bubbles:
            alpha = int((bubble['life'] / 15) * 255)
            color = (min(200 + alpha // 3, 255),
                    min(220 + alpha // 4, 255),
                    min(240 + alpha // 5, 255))
            pygame.draw.circle(screen, color,
                             (int(bubble['x']), int(bubble['y'])), bubble['size'])

        body_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.ellipse(screen, (100, 100, 120), body_rect)
        pygame.draw.ellipse(screen, (140, 140, 160), body_rect, 1)

        tail_x = self.x - self.width // 2 * self.direction
        pygame.draw.polygon(screen, (80, 80, 100), [
            (tail_x, self.y),
            (tail_x - 5 * self.direction, self.y - self.height // 2 - 2),
            (tail_x - 5 * self.direction, self.y + self.height // 2 + 2)
        ])

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )


class DepthCharge:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 12
        self.height = 16
        self.speed = DEPTH_CHARGE_SPEED
        self.damage = 30
        self.active = True
        self.bubbles = []
        self.bubble_timer = 0

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.active = False

        if self.y > WATER_LEVEL:
            self.bubble_timer += 1
            if self.bubble_timer >= 5:
                self.bubble_timer = 0
                self.bubbles.append({
                    'x': self.x,
                    'y': self.y - self.height // 2,
                    'size': 2,
                    'life': 10
                })

        for bubble in self.bubbles[:]:
            bubble['life'] -= 1
            if bubble['life'] <= 0:
                self.bubbles.remove(bubble)

    def draw(self, screen):
        for bubble in self.bubbles:
            pygame.draw.circle(screen, BUBBLE_COLOR,
                             (int(bubble['x']), int(bubble['y'])), bubble['size'])

        body_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.ellipse(screen, (70, 70, 90), body_rect)
        pygame.draw.ellipse(screen, (100, 100, 120), body_rect, 1)

        pygame.draw.line(screen, (90, 90, 110),
                        (self.x, self.y - self.height // 2),
                        (self.x, self.y - self.height // 2 - 8), 2)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
