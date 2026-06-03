import pygame
import random
from . import config


class Explosion:
    def __init__(self, x, y, size='small'):
        self.x = x
        self.y = y
        self.size = size
        if size == 'small':
            self.max_radius = 15
            self.duration = 20
        elif size == 'medium':
            self.max_radius = 30
            self.duration = config.EXPLOSION_DURATION
        else:
            self.max_radius = 50
            self.duration = 40
        self.timer = self.duration
        self.active = True
        self.particles = []
        num_particles = 8 if size == 'small' else (14 if size == 'medium' else 20)
        for _ in range(num_particles):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(1, 4 if size == 'small' else 6)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.randint(10, self.duration),
                'size': random.uniform(2, 5 if size == 'small' else 8)
            })

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.active = False
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.05
            p['life'] -= 1
            p['size'] *= 0.97

    def draw(self, surface):
        progress = 1 - self.timer / self.duration
        if progress < 0.3:
            color = config.WHITE
        elif progress < 0.6:
            color = config.YELLOW
        elif progress < 0.8:
            color = config.ORANGE
        else:
            color = config.RED
        radius = int(self.max_radius * min(1, progress * 2) * (1 - progress * 0.5))
        if radius > 0:
            exp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            alpha = int(200 * (1 - progress))
            pygame.draw.circle(exp_surf, (*color, alpha), (radius, radius), radius)
            inner_r = max(1, radius // 2)
            inner_alpha = min(255, alpha + 50)
            pygame.draw.circle(exp_surf, (255, 255, 200, inner_alpha),
                               (radius, radius), inner_r)
            surface.blit(exp_surf, (self.x - radius, self.y - radius))
        for p in self.particles:
            if p['life'] > 0 and p['size'] > 0.5:
                p_alpha = int(200 * (p['life'] / self.duration))
                p_color = config.ORANGE if random.random() > 0.5 else config.YELLOW
                ps = max(1, int(p['size']))
                p_surf = pygame.Surface((ps * 2, ps * 2), pygame.SRCALPHA)
                pygame.draw.circle(p_surf, (*p_color, p_alpha), (ps, ps), ps)
                surface.blit(p_surf, (int(p['x']) - ps, int(p['y']) - ps))


class BombSplash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 25
        self.duration = 25
        self.active = True

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.active = False

    def draw(self, surface):
        progress = 1 - self.timer / self.duration
        radius = int(35 * progress)
        if radius > 0:
            alpha = int(180 * (1 - progress))
            splash_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(splash_surf, (200, 220, 255, alpha),
                               (radius, radius), radius)
            inner_r = max(1, int(radius * 0.4))
            pygame.draw.circle(splash_surf, (255, 255, 255, min(255, alpha + 40)),
                               (radius, radius), inner_r)
            surface.blit(splash_surf, (self.x - radius, self.y - radius))


class ScorePopup:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.timer = 40
        self.active = True

    def update(self):
        self.timer -= 1
        self.y -= 1
        if self.timer <= 0:
            self.active = False

    def draw(self, surface, font):
        alpha = min(255, int(255 * self.timer / 20))
        text = font.render(str(self.score), True, config.YELLOW)
        text.set_alpha(alpha)
        surface.blit(text, (self.x, self.y))


import math
