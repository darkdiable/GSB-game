import pygame
import random
from constants import *


class Background:
    def __init__(self):
        self.scroll_y = 0
        self.clouds = []
        self.islands = []
        self.wave_pattern = []

        self._generate_clouds()
        self._generate_islands()
        self._generate_waves()

    def _generate_clouds(self):
        for _ in range(8):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT),
                'size': random.randint(30, 60),
                'speed': random.uniform(0.5, 1.5)
            })

    def _generate_islands(self):
        for i in range(4):
            island_type = random.choice(['small', 'medium', 'large'])
            if island_type == 'small':
                width = random.randint(60, 100)
            elif island_type == 'medium':
                width = random.randint(100, 160)
            else:
                width = random.randint(160, 250)

            has_aa = random.choice([True, False]) and island_type != 'small'

            self.islands.append({
                'x': random.randint(30, SCREEN_WIDTH - width - 30),
                'y': -i * 300 - random.randint(100, 300),
                'width': width,
                'height': int(width * 0.6),
                'type': island_type,
                'has_aa': has_aa,
                'aa_spawned': False
            })

    def _generate_waves(self):
        for i in range(20):
            self.wave_pattern.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': i * 50,
                'length': random.randint(20, 50)
            })

    def update(self):
        self.scroll_y += BG_SCROLL_SPEED

        for cloud in self.clouds:
            cloud['y'] += cloud['speed']
            if cloud['y'] > SCREEN_HEIGHT + 50:
                cloud['y'] = -50
                cloud['x'] = random.randint(0, SCREEN_WIDTH)

        for island in self.islands:
            island['y'] += BG_SCROLL_SPEED
            if island['y'] > SCREEN_HEIGHT + 200:
                island['y'] = -300
                island['x'] = random.randint(30, SCREEN_WIDTH - island['width'] - 30)
                island['aa_spawned'] = False

        for wave in self.wave_pattern:
            wave['y'] += BG_SCROLL_SPEED
            if wave['y'] > SCREEN_HEIGHT:
                wave['y'] = -20
                wave['x'] = random.randint(0, SCREEN_WIDTH)

    def check_island_aa_spawn(self, y_threshold=-AA_GUN_HEIGHT):
        aa_positions = []
        for island in self.islands:
            if island['has_aa'] and not island['aa_spawned'] and island['y'] > y_threshold and island['y'] < y_threshold + 80:
                island['aa_spawned'] = True
                aa_x = island['x'] + island['width'] // 2 - AA_GUN_WIDTH // 2
                aa_y = island['y'] + island['height'] // 2 - AA_GUN_HEIGHT // 2
                aa_positions.append((aa_x, aa_y))
        return aa_positions

    def get_ship_spawn_area(self):
        areas = []
        for island in self.islands:
            if island['y'] > 0 and island['y'] < SCREEN_HEIGHT:
                if island['x'] > 120:
                    areas.append((30, island['x'] - 110))
                if island['x'] + island['width'] < SCREEN_WIDTH - 120:
                    areas.append((island['x'] + island['width'] + 10, SCREEN_WIDTH - 110))
        if not areas:
            areas.append((30, SCREEN_WIDTH - 110))
        return areas

    def draw(self, screen):
        self._draw_sky(screen)
        self._draw_clouds(screen)
        self._draw_ocean(screen)
        self._draw_islands(screen)

    def _draw_sky(self, screen):
        for y in range(SCREEN_HEIGHT // 2):
            alpha = int(255 * (1 - y / (SCREEN_HEIGHT // 2)))
            color = (
                int(SKY_BLUE[0] * (1 - y / (SCREEN_HEIGHT // 2)) + OCEAN_BLUE[0] * (y / (SCREEN_HEIGHT // 2))),
                int(SKY_BLUE[1] * (1 - y / (SCREEN_HEIGHT // 2)) + OCEAN_BLUE[1] * (y / (SCREEN_HEIGHT // 2))),
                int(SKY_BLUE[2] * (1 - y / (SCREEN_HEIGHT // 2)) + OCEAN_BLUE[2] * (y / (SCREEN_HEIGHT // 2)))
            )
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

    def _draw_clouds(self, screen):
        for cloud in self.clouds:
            x, y, size = cloud['x'], cloud['y'], cloud['size']
            pygame.draw.ellipse(screen, WHITE, (x, y, size, size // 2))
            pygame.draw.ellipse(screen, WHITE, (x - size // 3, y + 5, size // 1.5, size // 3))
            pygame.draw.ellipse(screen, WHITE, (x + size // 3, y + 5, size // 1.5, size // 3))
            pygame.draw.ellipse(screen, WHITE, (x, y + size // 4, size // 1.2, size // 3))

    def _draw_ocean(self, screen):
        ocean_start = SCREEN_HEIGHT // 2
        pygame.draw.rect(screen, OCEAN_BLUE, (0, ocean_start, SCREEN_WIDTH, SCREEN_HEIGHT // 2))

        for wave in self.wave_pattern:
            y = ocean_start + (wave['y'] % (SCREEN_HEIGHT // 2))
            pygame.draw.arc(screen, OCEAN_LIGHT, (wave['x'], y, wave['length'], 10), 3.14, 6.28, 1)

        for i in range(5):
            y = ocean_start + 30 + i * 80
            pygame.draw.line(screen, OCEAN_LIGHT, (0, y), (SCREEN_WIDTH, y), 1)

    def _draw_islands(self, screen):
        for island in self.islands:
            x, y, width, height = island['x'], island['y'], island['width'], island['height']

            pygame.draw.ellipse(screen, SAND, (x, y, width, height))
            pygame.draw.ellipse(screen, GREEN, (x + 5, y + 5, width - 10, height - 10))
            pygame.draw.ellipse(screen, DARK_GREEN, (x + 15, y + 10, width - 30, height - 20))

            if island['type'] == 'large':
                pygame.draw.polygon(screen, BROWN, [
                    (x + width // 2 - 15, y + 20),
                    (x + width // 2, y + 5),
                    (x + width // 2 + 15, y + 20)
                ])
                pygame.draw.circle(screen, (139, 90, 43), (x + width // 2, y + 18), 8)

            for i in range(random.randint(2, 5)):
                tx = x + random.randint(15, width - 25)
                ty = y + random.randint(10, height - 20)
                pygame.draw.rect(screen, BROWN, (tx, ty + 8, 4, 8))
                pygame.draw.circle(screen, DARK_GREEN, (tx + 2, ty + 5), 6)
