import pygame
import math
import random
from constants import *


class CollapseEffect:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.particles = []
        self.rings = []
        self.start_time = pygame.time.get_ticks()
        self.duration = 1000
        self.active = True
        
        for _ in range(30):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'size': random.randint(3, 8)
            })
        
        for i in range(3):
            self.rings.append({
                'radius': 10,
                'max_radius': 80 + i * 30,
                'alpha': 255,
                'width': 3
            })

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        if elapsed > self.duration:
            self.active = False
            return
        
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.1
            p['life'] -= 0.02
        
        for ring in self.rings:
            if ring['radius'] < ring['max_radius']:
                ring['radius'] += 4
            ring['alpha'] = max(0, int(255 * (1 - ring['radius'] / ring['max_radius'])))

    def draw(self, surface):
        for ring in self.rings:
            if ring['alpha'] > 0:
                temp_surface = pygame.Surface((ring['radius'] * 2, ring['radius'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, (*self.color, ring['alpha']),
                                 (ring['radius'], ring['radius']), ring['radius'], ring['width'])
                surface.blit(temp_surface, (self.x - ring['radius'], self.y - ring['radius']))
        
        for p in self.particles:
            if p['life'] > 0:
                alpha = int(255 * p['life'])
                pygame.draw.circle(surface, (*self.color, alpha),
                                 (int(p['x']), int(p['y'])), int(p['size'] * p['life']))


class ScorePopup:
    def __init__(self, x, y, score, combo):
        self.x = x
        self.y = y
        self.score = score
        self.combo = combo
        self.start_time = pygame.time.get_ticks()
        self.duration = 800
        self.active = True

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        if elapsed > self.duration:
            self.active = False
        self.y -= 0.5

    def draw(self, surface):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        alpha = int(255 * (1 - elapsed / self.duration))
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"+{self.score}", True, (255, 255, 100))
        text.set_alpha(alpha)
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)
        
        if self.combo > 1:
            combo_font = pygame.font.Font(None, 24)
            combo_text = combo_font.render(f"{self.combo}x COMBO!", True, (255, 100, 100))
            combo_text.set_alpha(alpha)
            combo_rect = combo_text.get_rect(center=(self.x, self.y + 25))
            surface.blit(combo_text, combo_rect)


class BackgroundParticle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.1, 0.5)
        self.alpha = random.randint(30, 100)
        self.phase = random.uniform(0, math.pi * 2)

    def update(self):
        self.y -= self.speed
        self.phase += 0.02
        self.alpha = 30 + int(70 * (0.5 + 0.5 * math.sin(self.phase)))
        
        if self.y < -10:
            self.reset()

    def draw(self, surface):
        pygame.draw.circle(surface, (100, 150, 255, self.alpha),
                         (int(self.x), int(self.y)), self.size)


class DynamicBackground:
    def __init__(self):
        self.particles = [BackgroundParticle() for _ in range(80)]
        self.grid_lines = []
        self.time = 0
        
        for i in range(0, SCREEN_WIDTH, 80):
            self.grid_lines.append(('v', i))
        for i in range(0, SCREEN_HEIGHT, 80):
            self.grid_lines.append(('h', i))

    def update(self):
        self.time += 0.01
        for p in self.particles:
            p.update()

    def draw(self, surface):
        gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            r = int(10 + 5 * math.sin(self.time + y * 0.01))
            g = int(10 + 5 * math.cos(self.time + y * 0.01))
            b = int(30 + 10 * math.sin(self.time * 0.5 + y * 0.005))
            pygame.draw.line(gradient, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        surface.blit(gradient, (0, 0))
        
        for line_type, pos in self.grid_lines:
            alpha = int(30 + 20 * math.sin(self.time + pos * 0.01))
            color = (50, 80, 150, alpha)
            if line_type == 'v':
                pygame.draw.line(surface, color, (pos, 0), (pos, SCREEN_HEIGHT), 1)
            else:
                pygame.draw.line(surface, color, (0, pos), (SCREEN_WIDTH, pos), 1)
        
        for p in self.particles:
            p.draw(surface)
