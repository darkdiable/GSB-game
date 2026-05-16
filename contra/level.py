import pygame
from constants import *


class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        pygame.draw.rect(screen, (50, 50, 50), (draw_x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (80, 80, 80), (draw_x, self.y, self.width, 4))


class Level:
    def __init__(self):
        self.platforms = []
        self.level_width = 5000
        self.generate_level()

    def generate_level(self):
        self.platforms.append(Platform(400, GROUND_HEIGHT - 100, 150, 20))
        self.platforms.append(Platform(700, GROUND_HEIGHT - 150, 120, 20))
        self.platforms.append(Platform(1000, GROUND_HEIGHT - 100, 180, 20))
        self.platforms.append(Platform(1300, GROUND_HEIGHT - 180, 100, 20))
        self.platforms.append(Platform(1500, GROUND_HEIGHT - 120, 140, 20))
        self.platforms.append(Platform(1800, GROUND_HEIGHT - 160, 160, 20))
        self.platforms.append(Platform(2100, GROUND_HEIGHT - 100, 200, 20))
        self.platforms.append(Platform(2450, GROUND_HEIGHT - 140, 120, 20))
        self.platforms.append(Platform(2700, GROUND_HEIGHT - 180, 150, 20))
        self.platforms.append(Platform(3000, GROUND_HEIGHT - 120, 180, 20))
        self.platforms.append(Platform(3300, GROUND_HEIGHT - 160, 140, 20))
        self.platforms.append(Platform(3600, GROUND_HEIGHT - 100, 200, 20))
        self.platforms.append(Platform(3900, GROUND_HEIGHT - 140, 160, 20))
        self.platforms.append(Platform(4200, GROUND_HEIGHT - 180, 120, 20))
        self.platforms.append(Platform(4500, GROUND_HEIGHT - 120, 180, 20))

    def draw_background(self, screen, camera_x):
        screen.fill(BLUE_SKY)

        for i in range(0, self.level_width, 200):
            cloud_x = i - (camera_x * 0.3) % 200
            pygame.draw.ellipse(screen, WHITE, (cloud_x, 50, 80, 40))
            pygame.draw.ellipse(screen, WHITE, (cloud_x + 40, 40, 60, 35))

        for i in range(0, self.level_width, 300):
            hill_x = i - (camera_x * 0.5) % 300
            pygame.draw.polygon(screen, (34, 139, 34), [
                (hill_x, GROUND_HEIGHT),
                (hill_x + 100, GROUND_HEIGHT - 120),
                (hill_x + 200, GROUND_HEIGHT)
            ])

        for i in range(0, self.level_width, 250):
            tree_x = i - (camera_x * 0.7) % 250
            pygame.draw.rect(screen, BROWN, (tree_x + 20, GROUND_HEIGHT - 80, 10, 80))
            pygame.draw.ellipse(screen, (0, 100, 0), (tree_x, GROUND_HEIGHT - 130, 50, 60))

    def draw_ground(self, screen, camera_x):
        pygame.draw.rect(screen, GREEN_GROUND, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        pygame.draw.rect(screen, DARK_BROWN, (0, GROUND_HEIGHT + 10, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT - 10))

        grass_pattern = pygame.Surface((8, 8))
        grass_pattern.fill(GREEN_GROUND)
        pygame.draw.rect(grass_pattern, (0, 180, 0), (0, 0, 4, 4))

        for x in range(0, SCREEN_WIDTH, 8):
            for y in range(GROUND_HEIGHT, GROUND_HEIGHT + 10, 8):
                if (x + int(camera_x)) % 16 == 0:
                    screen.blit(grass_pattern, (x, y))

    def draw_platforms(self, screen, camera_x):
        for platform in self.platforms:
            if platform.x + platform.width > camera_x and platform.x < camera_x + SCREEN_WIDTH:
                platform.draw(screen, camera_x)

    def get_platforms(self):
        return self.platforms
