import pygame
from constants import *
from sprites import (
    create_ground_tile, create_platform_tile, create_bridge_tile,
    create_water_tile, create_bush, create_tree,
    create_wall_tile, create_fortress,
)


class Level:
    def __init__(self):
        self.platforms = []
        self.decorations = []
        self.ground_tiles = []
        self.water_zones = []
        self.camera_x = 0
        self.tile_cache = {}
        self.decoration_cache = []

        self._build_level()
        self._build_decorations()

    def _get_tile(self, tile_type):
        if tile_type not in self.tile_cache:
            if tile_type == "ground":
                self.tile_cache[tile_type] = create_ground_tile()
            elif tile_type == "platform":
                self.tile_cache[tile_type] = create_platform_tile()
            elif tile_type == "bridge":
                self.tile_cache[tile_type] = create_bridge_tile()
            elif tile_type == "wall":
                self.tile_cache[tile_type] = create_wall_tile()
        return self.tile_cache[tile_type]

    def _build_level(self):
        self.platforms = []

        self._add_ground(0, 960)

        self._add_platform(300, GROUND_Y - 80, 128)
        self._add_platform(500, GROUND_Y - 160, 96)
        self._add_platform(700, GROUND_Y - 120, 64)

        self._add_bridge(960, GROUND_Y, 320)

        self._add_ground(1280, 2560)

        self._add_platform(1400, GROUND_Y - 100, 160)
        self._add_platform(1650, GROUND_Y - 180, 128)
        self._add_platform(1900, GROUND_Y - 120, 96)
        self._add_platform(2100, GROUND_Y - 200, 128)
        self._add_platform(2350, GROUND_Y - 140, 96)

        self._add_water_zone(2560, 640)

        self._add_floating_platforms(2600, GROUND_Y - 60, 96)
        self._add_floating_platforms(2800, GROUND_Y - 140, 96)
        self._add_floating_platforms(3000, GROUND_Y - 80, 96)

        self._add_ground(3200, 4480)

        self._add_wall(3600, GROUND_Y - 160, 96, 160)

        self._add_platform(3800, GROUND_Y - 100, 128)
        self._add_platform(4000, GROUND_Y - 180, 160)
        self._add_platform(4250, GROUND_Y - 120, 96)

        self._add_bridge(4480, GROUND_Y, 320)

        self._add_ground(4800, LEVEL_WIDTH)

        self._add_wall(5200, GROUND_Y - 200, 128, 200)
        self._add_platform(5400, GROUND_Y - 100, 128)
        self._add_platform(5600, GROUND_Y - 160, 96)
        self._add_platform(5800, GROUND_Y - 120, 160)
        self._add_platform(6050, GROUND_Y - 80, 128)

        self._add_fortress(6100, GROUND_Y - 160)

    def _add_ground(self, start_x, end_x):
        for x in range(start_x, end_x, 32):
            plat = pygame.Rect(x, GROUND_Y, 32, 60)
            self.platforms.append(plat)
            self.ground_tiles.append(("ground", x, GROUND_Y))
            for gy in range(GROUND_Y + 32, GROUND_Y + 60, 32):
                self.ground_tiles.append(("ground", x, gy))

    def _add_platform(self, x, y, width):
        plat = pygame.Rect(x, y, width, 16)
        self.platforms.append(plat)
        for px in range(x, x + width, 32):
            self.ground_tiles.append(("platform", px, y))

    def _add_bridge(self, x, y, width):
        plat = pygame.Rect(x, y, width, 16)
        self.platforms.append(plat)
        for px in range(x, x + width, 32):
            self.ground_tiles.append(("bridge", px, y))

    def _add_water_zone(self, x, width):
        self.water_zones.append(pygame.Rect(x, GROUND_Y + 16, width, 60))
        for wx in range(x, x + width, 32):
            self.ground_tiles.append(("water", wx, GROUND_Y + 16))

    def _add_floating_platforms(self, x, y, width):
        plat = pygame.Rect(x, y, width, 16)
        self.platforms.append(plat)
        for px in range(x, x + width, 32):
            self.ground_tiles.append(("platform", px, y))

    def _add_wall(self, x, y, width, height):
        plat = pygame.Rect(x, y, width, height)
        self.platforms.append(plat)
        for wx in range(x, x + width, 32):
            for wy in range(y, y + height, 32):
                self.ground_tiles.append(("wall", wx, wy))

    def _add_fortress(self, x, y):
        plat = pygame.Rect(x, y, 128, 160)
        self.platforms.append(plat)

    def _build_decorations(self):
        self.decoration_cache = []

        self.decoration_cache.append(("bush", 100, GROUND_Y - 16))
        self.decoration_cache.append(("bush", 250, GROUND_Y - 16))
        self.decoration_cache.append(("tree", 150, GROUND_Y - 80))

        self.decoration_cache.append(("bush", 800, GROUND_Y - 16))
        self.decoration_cache.append(("tree", 850, GROUND_Y - 80))

        self.decoration_cache.append(("bush", 1350, GROUND_Y - 16))
        self.decoration_cache.append(("tree", 1450, GROUND_Y - 80))
        self.decoration_cache.append(("bush", 1700, GROUND_Y - 16))
        self.decoration_cache.append(("bush", 2000, GROUND_Y - 16))
        self.decoration_cache.append(("tree", 2200, GROUND_Y - 80))

        self.decoration_cache.append(("bush", 3300, GROUND_Y - 16))
        self.decoration_cache.append(("tree", 3500, GROUND_Y - 80))
        self.decoration_cache.append(("bush", 3900, GROUND_Y - 16))
        self.decoration_cache.append(("tree", 4100, GROUND_Y - 80))

        self.decoration_cache.append(("bush", 4900, GROUND_Y - 16))
        self.decoration_cache.append(("tree", 5000, GROUND_Y - 80))
        self.decoration_cache.append(("bush", 5300, GROUND_Y - 16))
        self.decoration_cache.append(("tree", 5500, GROUND_Y - 80))
        self.decoration_cache.append(("bush", 5700, GROUND_Y - 16))

    def update(self, player):
        target_x = player.rect.x - SCREEN_WIDTH // 3
        self.camera_x += (target_x - self.camera_x) * 0.1

        if self.camera_x < 0:
            self.camera_x = 0
        max_camera = LEVEL_WIDTH - SCREEN_WIDTH
        if self.camera_x > max_camera:
            self.camera_x = max_camera

    def draw(self, surface):
        self._draw_sky(surface)
        self._draw_mountains(surface)
        self._draw_tiles(surface)
        self._draw_decorations(surface)
        self._draw_fortress_decoration(surface)

    def _draw_sky(self, surface):
        for y in range(0, SCREEN_HEIGHT, 4):
            ratio = y / SCREEN_HEIGHT
            r = int(SKY_BLUE[0] * (1 - ratio * 0.3))
            g = int(SKY_BLUE[1] * (1 - ratio * 0.2))
            b = int(SKY_BLUE[2] * (1 - ratio * 0.1))
            pygame.draw.rect(surface, (r, g, b), (0, y, SCREEN_WIDTH, 4))

    def _draw_mountains(self, surface):
        parallax = self.camera_x * 0.3
        color1 = (60, 100, 60)
        color2 = (80, 130, 80)

        points1 = []
        for x in range(0, SCREEN_WIDTH + 100, 100):
            real_x = x + parallax
            h = 150 + 80 * ((real_x % 400) / 400)
            if (int(real_x / 200)) % 2 == 0:
                h += 60
            points1.append((x, GROUND_Y - h))
        points1.append((SCREEN_WIDTH, GROUND_Y))
        points1.append((0, GROUND_Y))
        if len(points1) >= 3:
            pygame.draw.polygon(surface, color1, points1)

        points2 = []
        for x in range(0, SCREEN_WIDTH + 100, 80):
            real_x = x + parallax * 1.3
            h = 80 + 50 * ((real_x % 300) / 300)
            if (int(real_x / 150)) % 2 == 0:
                h += 40
            points2.append((x, GROUND_Y - h))
        points2.append((SCREEN_WIDTH, GROUND_Y))
        points2.append((0, GROUND_Y))
        if len(points2) >= 3:
            pygame.draw.polygon(surface, color2, points2)

    def _draw_tiles(self, surface):
        for tile_type, tx, ty in self.ground_tiles:
            draw_x = tx - self.camera_x
            if -32 < draw_x < SCREEN_WIDTH + 32:
                tile = self._get_tile(tile_type)
                if tile:
                    surface.blit(tile, (draw_x, ty))

        for wz in self.water_zones:
            draw_x = wz.x - self.camera_x
            if -wz.width < draw_x < SCREEN_WIDTH + wz.width:
                water_tile = self._get_tile("ground") if "ground" in self.tile_cache else None
                if water_tile is None:
                    water_tile = create_water_tile()
                    self.tile_cache["water_tile"] = water_tile
                for wx in range(wz.x, wz.x + wz.width, 32):
                    dx = wx - self.camera_x
                    if -32 < dx < SCREEN_WIDTH + 32:
                        surface.blit(self.tile_cache.get("water_tile", water_tile),
                                     (dx, wz.y))

    def _draw_decorations(self, surface):
        for dec_type, dx, dy in self.decoration_cache:
            draw_x = dx - self.camera_x
            if -64 < draw_x < SCREEN_WIDTH + 64:
                if dec_type == "bush":
                    img = create_bush()
                    surface.blit(img, (draw_x, dy))
                elif dec_type == "tree":
                    img = create_tree()
                    surface.blit(img, (draw_x, dy))

    def _draw_fortress_decoration(self, surface):
        fortress_x = 6100 - self.camera_x
        if -128 < fortress_x < SCREEN_WIDTH + 128:
            fortress = create_fortress()
            surface.blit(fortress, (fortress_x, GROUND_Y - 160))

    def get_platforms(self):
        return self.platforms

    def is_in_water(self, rect):
        for wz in self.water_zones:
            if rect.colliderect(wz):
                return True
        return False

    def get_camera_x(self):
        return self.camera_x

    def is_level_end(self, player_x):
        return player_x >= LEVEL_WIDTH - 200
