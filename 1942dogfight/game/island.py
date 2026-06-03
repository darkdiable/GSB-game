import pygame
import math
import random
from . import config
from .bullet import EnemyBullet


class Island:
    def __init__(self, x=None):
        self.width = random.randint(100, 160)
        self.height = random.randint(80, 120)
        self.x = x if x is not None else random.randint(10, config.SCREEN_WIDTH - self.width - 10)
        self.y = -self.height - random.randint(0, 200)
        self.active = True
        self.health = config.ISLAND_AA_HEALTH
        self.max_health = config.ISLAND_AA_HEALTH
        self.score_value = 1000
        self.shoot_timer = random.randint(10, config.ISLAND_SHOOT_RATE)
        self.hit_flash = 0
        self.aa_positions = []
        margin = 20
        num_aa = random.randint(2, 4)
        for i in range(num_aa):
            ax = self.x + margin + (self.width - margin * 2) * (i / max(1, num_aa - 1))
            ay = self.y + self.height // 2 + random.randint(-10, 10)
            self.aa_positions.append([ax, ay])
        self.tree_positions = []
        for _ in range(random.randint(5, 12)):
            tx = random.randint(self.x + 8, self.x + self.width - 8)
            ty = random.randint(self.y + 8, self.y + self.height - 8)
            tr = random.randint(4, 8)
            self.tree_positions.append((tx, ty, tr))

    def update(self):
        self.y += config.SCROLL_SPEED
        for aa in self.aa_positions:
            aa[1] += config.SCROLL_SPEED
        for i in range(len(self.tree_positions)):
            tx, ty, tr = self.tree_positions[i]
            self.tree_positions[i] = (tx, ty + config.SCROLL_SPEED, tr)
        if self.y > config.SCREEN_HEIGHT + 50:
            self.active = False
        self.shoot_timer -= 1
        if self.hit_flash > 0:
            self.hit_flash -= 1

    def shoot(self, player_x=None, player_y=None):
        if self.shoot_timer <= 0 and self.health > 0:
            self.shoot_timer = config.ISLAND_SHOOT_RATE
            bullets = []
            if player_x is not None:
                for aa in self.aa_positions:
                    dx = player_x - aa[0]
                    dy = player_y - aa[1]
                    dist = max(1, math.sqrt(dx * dx + dy * dy))
                    bullets.append(EnemyBullet(aa[0], aa[1],
                                               dx / dist, dy / dist, 3.5, (255, 150, 50)))
            return bullets
        return []

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 4
        if self.health <= 0:
            self.health = 0
            return True
        return False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_aa_rects(self):
        rects = []
        for aa in self.aa_positions:
            rects.append(pygame.Rect(aa[0] - 8, aa[1] - 8, 16, 16))
        return rects

    def draw(self, surface):
        color = config.WHITE if self.hit_flash > 0 else config.ISLAND_SAND
        points = []
        cx = self.x + self.width // 2
        cy = self.y + self.height // 2
        for angle in range(0, 360, 20):
            rad = math.radians(angle)
            rx = self.width // 2 * (0.7 + 0.3 * math.sin(rad * 3))
            ry = self.height // 2 * (0.7 + 0.3 * math.cos(rad * 2))
            px = cx + rx * math.cos(rad)
            py = cy + ry * math.sin(rad)
            points.append((px, py))
        if len(points) >= 3:
            pygame.draw.polygon(surface, color, points)
            inner_color = config.ISLAND_GREEN if self.hit_flash == 0 else (200, 230, 200)
            inner_points = []
            for angle in range(0, 360, 20):
                rad = math.radians(angle)
                rx = self.width // 2 * 0.6 * (0.7 + 0.3 * math.sin(rad * 3))
                ry = self.height // 2 * 0.6 * (0.7 + 0.3 * math.cos(rad * 2))
                px = cx + rx * math.cos(rad)
                py = cy + ry * math.sin(rad)
                inner_points.append((px, py))
            if len(inner_points) >= 3:
                pygame.draw.polygon(surface, inner_color, inner_points)
        for tx, ty, tr in self.tree_positions:
            pygame.draw.circle(surface, (40, 110, 40), (int(tx), int(ty)), tr)
            pygame.draw.circle(surface, (50, 130, 50), (int(tx), int(ty)), tr - 2)
        if self.health > 0:
            for aa in self.aa_positions:
                pygame.draw.rect(surface, (80, 80, 80), (aa[0] - 4, aa[1] - 4, 8, 8))
                pygame.draw.rect(surface, (100, 100, 100), (aa[0] - 2, aa[1] - 2, 4, 4))
                pygame.draw.circle(surface, (50, 50, 50), (int(aa[0]), int(aa[1]) - 5), 3)
        bar_w = self.width - 20
        bar_h = 4
        bar_x = self.x + 10
        bar_y = self.y - 10
        pygame.draw.rect(surface, config.DARK_GRAY, (bar_x, bar_y, bar_w, bar_h))
        fill = int(bar_w * self.health / self.max_health)
        bar_color = config.RED if self.health < self.max_health * 0.3 else config.YELLOW
        pygame.draw.rect(surface, bar_color, (bar_x, bar_y, fill, bar_h))
