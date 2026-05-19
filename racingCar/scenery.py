import pygame
import random
from config import *


class SceneryElement:
    def __init__(self, x, y, element_type, scenery_type):
        self.x = x
        self.y = y
        self.type = element_type
        self.scenery_type = scenery_type
        self.width = random.randint(30, 80)
        self.height = random.randint(30, 100)

    def update(self, player_speed):
        self.y += player_speed

    def draw(self, screen):
        if self.scenery_type == 'beach':
            self._draw_beach_element(screen)
        elif self.scenery_type == 'town':
            self._draw_town_element(screen)
        elif self.scenery_type == 'desert':
            self._draw_desert_element(screen)

    def _draw_beach_element(self, screen):
        if self.type == 'palm':
            trunk_rect = pygame.Rect(self.x - 5, self.y - self.height, 10, self.height)
            pygame.draw.rect(screen, (139, 90, 43), trunk_rect)
            for i in range(5):
                angle = (i - 2) * 30
                end_x = self.x + angle * 0.5
                end_y = self.y - self.height + 10 + abs(angle) * 0.3
                pygame.draw.line(screen, (34, 139, 34), (self.x, self.y - self.height + 10), (end_x, end_y), 8)
        elif self.type == 'umbrella':
            pole_rect = pygame.Rect(self.x - 3, self.y - self.height, 6, self.height)
            pygame.draw.rect(screen, (139, 90, 43), pole_rect)
            pygame.draw.circle(screen, (255, 100, 100), (self.x, self.y - self.height), 25)

    def _draw_town_element(self, screen):
        if self.type == 'building':
            building_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height, self.width, self.height)
            pygame.draw.rect(screen, COLORS['town_building'], building_rect)
            roof_rect = pygame.Rect(self.x - self.width // 2 - 5, self.y - self.height - 15, self.width + 10, 15)
            pygame.draw.rect(screen, COLORS['town_roof'], roof_rect)
            for row in range(3):
                for col in range(2):
                    window_rect = pygame.Rect(
                        self.x - self.width // 2 + 10 + col * 25,
                        self.y - self.height + 15 + row * 25,
                        15,
                        18
                    )
                    pygame.draw.rect(screen, (255, 255, 200), window_rect)
        elif self.type == 'lamp':
            pole_rect = pygame.Rect(self.x - 3, self.y - self.height, 6, self.height)
            pygame.draw.rect(screen, (80, 80, 80), pole_rect)
            pygame.draw.circle(screen, (255, 255, 150), (self.x, self.y - self.height), 10)

    def _draw_desert_element(self, screen):
        if self.type == 'cactus':
            trunk_rect = pygame.Rect(self.x - 8, self.y - self.height, 16, self.height)
            pygame.draw.rect(screen, (34, 139, 34), trunk_rect, border_radius=5)
            arm1_rect = pygame.Rect(self.x - 25, self.y - self.height + 15, 20, 8)
            pygame.draw.rect(screen, (34, 139, 34), arm1_rect, border_radius=4)
            arm2_rect = pygame.Rect(self.x + 5, self.y - self.height + 25, 20, 8)
            pygame.draw.rect(screen, (34, 139, 34), arm2_rect, border_radius=4)
        elif self.type == 'rock':
            rock_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height // 2)
            pygame.draw.ellipse(screen, COLORS['desert_rock'], rock_rect)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100


class SceneryManager:
    def __init__(self):
        self.elements = []
        self.current_scenery = 'beach'
        self.distance_traveled = 0
        self.next_change_distance = SCENERY_CHANGE_DISTANCE
        self.spawn_timer = 0
        self.road_offset = 0
        self.scenery_history = []
        self.max_history = 6

    def update(self, player_speed, score):
        self.distance_traveled += player_speed
        self.road_offset = (self.road_offset + player_speed * 3) % 80

        if self.distance_traveled >= self.next_change_distance:
            self._change_scenery()
            self.next_change_distance += SCENERY_CHANGE_DISTANCE

        self.spawn_timer += 1
        if self.spawn_timer >= 30:
            self.spawn_timer = 0
            self._spawn_element()

        for element in self.elements[:]:
            element.update(player_speed)
            if element.is_off_screen():
                self.elements.remove(element)

    def _change_scenery(self):
        scenery_counts = {}
        for s in SCENERY_TYPES:
            scenery_counts[s] = self.scenery_history.count(s)

        min_count = min(scenery_counts.values())
        candidates = [s for s in SCENERY_TYPES if scenery_counts[s] == min_count and s != self.current_scenery]

        if not candidates:
            candidates = [s for s in SCENERY_TYPES if s != self.current_scenery]

        new_scenery = random.choice(candidates)
        self.current_scenery = new_scenery

        self.scenery_history.append(new_scenery)
        if len(self.scenery_history) > self.max_history:
            self.scenery_history.pop(0)

    def _spawn_element(self):
        side = random.choice(['left', 'right'])
        if side == 'left':
            x = random.randint(20, ROAD_LEFT - 40)
        else:
            x = random.randint(ROAD_RIGHT + 40, SCREEN_WIDTH - 20)

        y = -50

        if self.current_scenery == 'beach':
            element_type = random.choice(['palm', 'umbrella'])
        elif self.current_scenery == 'town':
            element_type = random.choice(['building', 'lamp'])
        else:
            element_type = random.choice(['cactus', 'rock'])

        element = SceneryElement(x, y, element_type, self.current_scenery)
        self.elements.append(element)

    def draw(self, screen):
        self._draw_background(screen)
        self._draw_road(screen)

        for element in self.elements:
            element.draw(screen)

    def _draw_background(self, screen):
        if self.current_scenery == 'beach':
            screen.fill(COLORS['beach_sand'])
            water_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 100)
            pygame.draw.rect(screen, COLORS['beach_water'], water_rect)
            for i in range(5):
                wave_y = 80 + i * 5
                pygame.draw.line(screen, (255, 255, 255), (0, wave_y), (SCREEN_WIDTH, wave_y), 2)
        elif self.current_scenery == 'town':
            screen.fill(COLORS['grass'])
            sky_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 80)
            pygame.draw.rect(screen, (135, 206, 235), sky_rect)
        elif self.current_scenery == 'desert':
            screen.fill(COLORS['desert'])
            sky_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 120)
            pygame.draw.rect(screen, (255, 200, 100), sky_rect)

    def _draw_road(self, screen):
        road_rect = pygame.Rect(ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(screen, COLORS['road'], road_rect)

        pygame.draw.rect(screen, (255, 255, 255), (ROAD_LEFT, 0, 5, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (255, 255, 255), (ROAD_RIGHT - 5, 0, 5, SCREEN_HEIGHT))

        for lane in range(1, LANE_COUNT):
            x = ROAD_LEFT + lane * LANE_WIDTH
            for y in range(-80, SCREEN_HEIGHT, 80):
                dash_y = y + self.road_offset
                if dash_y > -40 and dash_y < SCREEN_HEIGHT:
                    pygame.draw.rect(screen, COLORS['road_line'], (x - 2, dash_y, 4, 40))

    def reset(self):
        self.elements = []
        self.current_scenery = 'beach'
        self.distance_traveled = 0
        self.next_change_distance = SCENERY_CHANGE_DISTANCE
        self.spawn_timer = 0
        self.road_offset = 0
        self.scenery_history = []
