import pygame
import random
from config import *


class Vehicle:
    def __init__(self, vehicle_type, x, y):
        self.type = vehicle_type
        self.x = x
        self.y = y
        self.width, self.height = VEHICLE_SIZES[vehicle_type]
        self.base_speed = VEHICLE_SPEEDS[vehicle_type]
        self.speed = self.base_speed

        if vehicle_type == 'sports':
            self.color = COLORS['sports_car']
        elif vehicle_type == 'suv':
            self.color = COLORS['suv_car']
        elif vehicle_type == 'truck':
            self.color = COLORS['truck_car']
        else:
            self.color = COLORS['obstacle']

    def update(self, player_speed):
        self.y += player_speed - self.speed

    def draw(self, screen):
        if self.type == 'obstacle':
            self._draw_obstacle(screen)
        else:
            self._draw_car(screen)

    def _draw_car(self, screen):
        car_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, self.color, car_rect, border_radius=6)

        window_rect = pygame.Rect(
            self.x - self.width // 2 + 6,
            self.y - self.height // 2 + 12,
            self.width - 12,
            20
        )
        pygame.draw.rect(screen, (200, 230, 255), window_rect, border_radius=3)

        if self.type == 'truck':
            cargo_rect = pygame.Rect(
                self.x - self.width // 2 + 5,
                self.y - self.height // 2 + 40,
                self.width - 10,
                self.height - 60
            )
            pygame.draw.rect(screen, (200, 140, 0), cargo_rect, border_radius=3)

        pygame.draw.circle(screen, (255, 0, 0), (self.x - 10, self.y - self.height // 2 + 8), 4)
        pygame.draw.circle(screen, (255, 0, 0), (self.x + 10, self.y - self.height // 2 + 8), 4)

    def _draw_obstacle(self, screen):
        obstacle_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, self.color, obstacle_rect, border_radius=4)

        for i in range(3):
            stripe_rect = pygame.Rect(
                self.x - self.width // 2 + 5,
                self.y - self.height // 2 + 8 + i * 12,
                self.width - 10,
                6
            )
            stripe_color = (255, 100, 0) if i % 2 == 0 else (255, 255, 255)
            pygame.draw.rect(screen, stripe_color, stripe_rect)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + 100 or self.y < -200


class VehicleManager:
    def __init__(self):
        self.vehicles = []
        self.spawn_timer = 0
        self.spawn_interval = 60
        self.min_spawn_interval = 25

    def update(self, player_speed, score):
        self.spawn_timer += 1

        difficulty = min(score / 5000, 1)
        current_interval = max(
            self.min_spawn_interval,
            self.spawn_interval - int(difficulty * 35)
        )

        if self.spawn_timer >= current_interval:
            self.spawn_timer = 0
            self._spawn_vehicle()

        for vehicle in self.vehicles[:]:
            vehicle.update(player_speed)
            if vehicle.is_off_screen():
                self.vehicles.remove(vehicle)

    def _spawn_vehicle(self):
        vehicle_type = random.choice(VEHICLE_TYPES)
        lane = random.randint(0, LANE_COUNT - 1)
        x = ROAD_LEFT + LANE_WIDTH // 2 + lane * LANE_WIDTH

        for existing in self.vehicles:
            if abs(existing.x - x) < 60 and existing.y < 150:
                return

        y = -100
        vehicle = Vehicle(vehicle_type, x, y)
        self.vehicles.append(vehicle)

    def draw(self, screen):
        for vehicle in self.vehicles:
            vehicle.draw(screen)

    def check_collision(self, player_rect):
        for vehicle in self.vehicles:
            if player_rect.colliderect(vehicle.get_rect()):
                return vehicle
        return None

    def reset(self):
        self.vehicles = []
        self.spawn_timer = 0
