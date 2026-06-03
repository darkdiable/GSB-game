import pygame
import random
import math
from .config import *


class Explosion:
    def __init__(self, x, y, size='medium'):
        self.x = x
        self.y = y
        self.timer = EXPLOSION_DURATION
        self.max_timer = EXPLOSION_DURATION
        self.size = size
        self.active = True
        self.particles = []
        self._create_particles()

    def _create_particles(self):
        count = 15 if self.size == 'small' else 25 if self.size == 'medium' else 40
        radius = 20 if self.size == 'small' else 35 if self.size == 'medium' else 50

        for _ in range(count):
            angle = random.random() * 6.283
            speed = random.uniform(1, 4)
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
                'size': random.randint(3, 8),
                'life': random.randint(self.max_timer // 2, self.max_timer)
            })

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.active = False

        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.1
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)

    def draw(self, screen):
        progress = 1 - (self.timer / self.max_timer)
        alpha = int((1 - progress) * 255)

        radius = 20 if self.size == 'small' else 35 if self.size == 'medium' else 50
        current_radius = radius * (0.5 + progress * 0.5)

        if self.timer > self.max_timer * 0.7:
            color = (min(255, 255), min(255, 200 + int(55 * (1 - progress))), 0)
        elif self.timer > self.max_timer * 0.4:
            color = (255, max(0, int(200 * (self.timer / self.max_timer - 0.4) / 0.3)), 0)
        else:
            color = (max(100, int(255 * (self.timer / self.max_timer) / 0.4)), 0, 0)

        for p in self.particles:
            p_alpha = int((p['life'] / self.max_timer) * 255)
            size = p['size'] * (p['life'] / self.max_timer)
            if size > 0:
                surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*color, p_alpha),
                                 (int(size), int(size)), int(size))
                screen.blit(surf, (int(p['x'] - size), int(p['y'] - size)))


class WaterBubble:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = SCREEN_HEIGHT + random.randint(10, 50)
        self.size = random.randint(2, 6)
        self.speed = random.uniform(0.5, 2)
        self.wobble = random.random() * 6.283
        self.wobble_speed = random.uniform(0.02, 0.05)

    def update(self):
        self.y -= self.speed
        self.wobble += self.wobble_speed
        self.x += math.sin(self.wobble) * 0.3
        return self.y > -10

    def draw(self, screen):
        alpha = 100 + int(math.sin(self.wobble * 2) * 30)
        color = (min(200 + alpha // 3, 255),
                min(220 + alpha // 4, 255),
                min(240 + alpha // 5, 255))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size, 1)
