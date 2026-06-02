import random
import pygame
from constants import (
    SCENERY_WIDTH, SCREEN_HEIGHT, SCENERY_TYPES, SCENERY_SEGMENT_HEIGHT,
    SCENERY_CHANGE_DISTANCE, ROAD_LEFT, SCREEN_WIDTH,
    SEASIDE_COLORS, TOWN_COLORS, DESERT_COLORS, GRASS_COLOR,
)


class ScenerySegment:
    def __init__(self, scenery_type, y_offset):
        self.scenery_type = scenery_type
        self.y_offset = y_offset
        self.random_seed = random.randint(0, 999999)

    def draw(self, surface, scroll_y):
        rng = random.Random(self.random_seed)
        y = int(self.y_offset - scroll_y)

        if self.scenery_type == "seaside":
            self._draw_seaside(surface, y, rng)
        elif self.scenery_type == "town":
            self._draw_town(surface, y, rng)
        elif self.scenery_type == "desert":
            self._draw_desert(surface, y, rng)

    def _draw_seaside(self, surface, y, rng):
        colors = SEASIDE_COLORS
        h = SCENERY_SEGMENT_HEIGHT

        for side in ("left", "right"):
            x_start = 0 if side == "left" else ROAD_LEFT + 300
            w = SCENERY_WIDTH

            pygame.draw.rect(surface, colors["ground"], (x_start, y, w, h))

            water_w = w // 3
            water_x = x_start + (w // 3 if side == "left" else w // 6)
            pygame.draw.rect(surface, colors["water"], (water_x, y, water_w, h))

            wave_y = y + rng.randint(20, h - 40)
            for wx in range(water_x, water_x + water_w, 12):
                pygame.draw.arc(
                    surface, colors["accent"],
                    (wx, wave_y, 12, 6), 0, 3.14, 1,
                )

            for _ in range(rng.randint(2, 4)):
                px = x_start + rng.randint(10, w - 30)
                py = y + rng.randint(10, h - 30)
                if not (water_x <= px <= water_x + water_w):
                    pygame.draw.circle(surface, (255, 255, 255), (px, py), 3)

    def _draw_town(self, surface, y, rng):
        colors = TOWN_COLORS
        h = SCENERY_SEGMENT_HEIGHT

        for side in ("left", "right"):
            x_start = 0 if side == "left" else ROAD_LEFT + 300
            w = SCENERY_WIDTH

            pygame.draw.rect(surface, colors["ground"], (x_start, y, w, h))

            building_count = rng.randint(2, 4)
            bx = x_start + 10
            for _ in range(building_count):
                bw = rng.randint(30, 50)
                bh = rng.randint(60, h - 20)
                by = y + h - bh
                if bx + bw > x_start + w:
                    break
                pygame.draw.rect(surface, colors["building"], (bx, by, bw, bh))
                pygame.draw.rect(surface, colors["accent"], (bx, by, bw, bh), 2)
                for wy in range(by + 8, by + bh - 10, 16):
                    for wx in range(bx + 6, bx + bw - 6, 12):
                        pygame.draw.rect(surface, (255, 255, 180), (wx, wy, 6, 8))
                bx += bw + rng.randint(5, 15)

    def _draw_desert(self, surface, y, rng):
        colors = DESERT_COLORS
        h = SCENERY_SEGMENT_HEIGHT

        for side in ("left", "right"):
            x_start = 0 if side == "left" else ROAD_LEFT + 300
            w = SCENERY_WIDTH

            pygame.draw.rect(surface, colors["ground"], (x_start, y, w, h))

            for _ in range(rng.randint(3, 6)):
                dx = x_start + rng.randint(10, w - 30)
                dy = y + rng.randint(10, h - 30)
                pygame.draw.ellipse(surface, colors["sand"], (dx, dy, 30, 10))

            for _ in range(rng.randint(1, 3)):
                cx = x_start + rng.randint(20, w - 20)
                cy = y + rng.randint(30, h - 30)
                pygame.draw.rect(surface, (0, 140, 0), (cx, cy, 4, 20))
                pygame.draw.ellipse(surface, (0, 160, 0), (cx - 8, cy - 4, 20, 12))
                pygame.draw.ellipse(surface, (0, 160, 0), (cx - 6, cy + 6, 16, 10))


class SceneryManager:
    def __init__(self):
        self.scroll_y = 0.0
        self.distance = 0.0
        self.segments = []
        self.current_type_index = 0
        self._init_segments()

    def _init_segments(self):
        needed = (SCREEN_HEIGHT // SCENERY_SEGMENT_HEIGHT) + 3
        for i in range(needed):
            stype = SCENERY_TYPES[self.current_type_index]
            self.segments.append(ScenerySegment(stype, i * SCENERY_SEGMENT_HEIGHT))

    def update(self, player_speed, dt):
        scroll_delta = player_speed
        self.scroll_y += scroll_delta
        self.distance += player_speed

        if self.distance >= SCENERY_CHANGE_DISTANCE:
            self.distance = 0
            self.current_type_index = (self.current_type_index + 1) % len(SCENERY_TYPES)

        self._recycle_segments()

    def _recycle_segments(self):
        while self.segments and self.segments[0].y_offset - self.scroll_y < -SCENERY_SEGMENT_HEIGHT:
            old = self.segments.pop(0)
            new_y = self.segments[-1].y_offset + SCENERY_SEGMENT_HEIGHT
            stype = SCENERY_TYPES[self.current_type_index]
            self.segments.append(ScenerySegment(stype, new_y))

    def draw(self, surface):
        for seg in self.segments:
            seg.draw(surface, self.scroll_y)

    def reset(self):
        self.scroll_y = 0.0
        self.distance = 0.0
        self.segments.clear()
        self.current_type_index = 0
        self._init_segments()
