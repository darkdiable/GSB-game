import pygame
import random
import math
from . import config


class Background:
    def __init__(self):
        self.scroll_y = 0
        self.wave_offset = 0
        self.cloud_positions = []
        for _ in range(8):
            self.cloud_positions.append({
                'x': random.randint(0, config.SCREEN_WIDTH),
                'y': random.randint(0, config.SCREEN_HEIGHT * 3),
                'w': random.randint(60, 150),
                'h': random.randint(20, 40),
                'alpha': random.randint(30, 70)
            })

    def update(self):
        self.scroll_y += config.SCROLL_SPEED
        if self.scroll_y >= config.SCREEN_HEIGHT:
            self.scroll_y -= config.SCREEN_HEIGHT
        self.wave_offset += 0.02
        for cloud in self.cloud_positions:
            cloud['y'] += config.SCROLL_SPEED * 0.3
            if cloud['y'] > config.SCREEN_HEIGHT + 50:
                cloud['y'] = -50
                cloud['x'] = random.randint(0, config.SCREEN_WIDTH)

    def draw(self, surface):
        surface.fill(config.OCEAN_COLOR)
        for y in range(0, config.SCREEN_HEIGHT, 4):
            wave = math.sin(self.wave_offset + y * 0.03) * 5
            shifted_y = (y + int(self.scroll_y)) % config.SCREEN_HEIGHT
            r = config.OCEAN_COLOR[0] + int(wave)
            g = config.OCEAN_COLOR[1] + int(wave * 2)
            b = config.OCEAN_COLOR[2] + int(wave)
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            pygame.draw.line(surface, (r, g, b), (0, shifted_y), (config.SCREEN_WIDTH, shifted_y))
        for cloud in self.cloud_positions:
            cloud_surf = pygame.Surface((cloud['w'], cloud['h']), pygame.SRCALPHA)
            pygame.draw.ellipse(cloud_surf, (255, 255, 255, cloud['alpha']),
                                (0, 0, cloud['w'], cloud['h']))
            surface.blit(cloud_surf, (cloud['x'], int(cloud['y'])))
