import random
import pygame
from constants import (
    OBSTACLE_WIDTH, OBSTACLE_HEIGHT, OBSTACLE_COLOR,
    VEHICLE_CONFIGS, VEHICLE_TYPES, LANE_POSITIONS,
    SCREEN_HEIGHT, ROAD_LEFT, ROAD_RIGHT, BLACK, WHITE, YELLOW, RED,
)

LANE_CHANGE_MIN_INTERVAL = 2000
LANE_CHANGE_MAX_INTERVAL = 5000
LANE_CHANGE_SPEED = 2.0


class Obstacle:
    def __init__(self, x, y):
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.x = float(x)
        self.y = float(y)
        self.color = OBSTACLE_COLOR
        self.type = "obstacle"
        self.speed = 0

    def update(self, player_speed):
        self.y += player_speed

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height,
        )

    def is_off_screen(self):
        return self.y - self.height // 2 > SCREEN_HEIGHT + 50

    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.rect(surface, self.color, rect, border_radius=4)
        pygame.draw.line(surface, BLACK, rect.topleft, rect.bottomright, 2)
        pygame.draw.line(surface, BLACK, rect.topright, rect.bottomleft, 2)
        pygame.draw.rect(surface, (50, 50, 50), rect, 2, border_radius=4)


class Vehicle:
    def __init__(self, vehicle_type, lane_index):
        config = VEHICLE_CONFIGS[vehicle_type]
        self.vehicle_type = vehicle_type
        self.width = config["width"]
        self.height = config["height"]
        self.color = config["color"]
        self.speed = random.uniform(*config["speed_range"])
        self.lane_index = lane_index
        self.x = float(LANE_POSITIONS[lane_index])
        self.y = float(-self.height)
        self.type = "vehicle"
        self.target_x = self.x
        self.is_changing_lane = False
        self.next_lane_change_time = pygame.time.get_ticks() + random.randint(
            LANE_CHANGE_MIN_INTERVAL, LANE_CHANGE_MAX_INTERVAL
        )

    def try_lane_change(self, current_time, all_vehicles):
        if self.is_changing_lane:
            return
        if current_time < self.next_lane_change_time:
            return
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            return

        possible_lanes = []
        if self.lane_index > 0:
            possible_lanes.append(self.lane_index - 1)
        if self.lane_index < len(LANE_POSITIONS) - 1:
            possible_lanes.append(self.lane_index + 1)

        random.shuffle(possible_lanes)
        for target_lane in possible_lanes:
            if self._is_lane_safe(target_lane, all_vehicles):
                self.lane_index = target_lane
                self.target_x = float(LANE_POSITIONS[target_lane])
                self.is_changing_lane = True
                break

        self.next_lane_change_time = current_time + random.randint(
            LANE_CHANGE_MIN_INTERVAL, LANE_CHANGE_MAX_INTERVAL
        )

    def _is_lane_safe(self, target_lane, all_vehicles):
        target_x = LANE_POSITIONS[target_lane]
        for v in all_vehicles:
            if v is self:
                continue
            if abs(v.x - target_x) < 30 and abs(v.y - self.y) < 120:
                return False
        return True

    def update(self, player_speed):
        self.y += player_speed - self.speed
        if self.is_changing_lane:
            diff = self.target_x - self.x
            if abs(diff) < LANE_CHANGE_SPEED:
                self.x = self.target_x
                self.is_changing_lane = False
            else:
                self.x += LANE_CHANGE_SPEED if diff > 0 else -LANE_CHANGE_SPEED

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height,
        )

    def is_off_screen(self):
        return self.y - self.height // 2 > SCREEN_HEIGHT + 50 or self.y + self.height // 2 < -200

    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.rect(surface, self.color, rect, border_radius=5)

        if self.vehicle_type == "truck":
            cab = pygame.Rect(rect.x + 4, rect.y + 5, self.width - 8, 20)
            pygame.draw.rect(surface, (140, 60, 10), cab, border_radius=3)
            cargo = pygame.Rect(rect.x + 2, rect.y + 28, self.width - 4, self.height - 38)
            pygame.draw.rect(surface, (200, 160, 60), cargo, border_radius=2)
            pygame.draw.rect(surface, RED, (rect.x - 2, rect.bottom - 10, 4, 6))
            pygame.draw.rect(surface, RED, (rect.right - 2, rect.bottom - 10, 4, 6))
        elif self.vehicle_type == "sports_car":
            hood = pygame.Rect(rect.x + 5, rect.y + 6, self.width - 10, 14)
            pygame.draw.rect(surface, (180, 20, 20), hood, border_radius=3)
            windshield = pygame.Rect(rect.x + 8, rect.y + 22, self.width - 16, 12)
            pygame.draw.rect(surface, (150, 210, 255), windshield, border_radius=2)
            stripe_y = rect.centery + 5
            pygame.draw.line(surface, WHITE, (rect.x + 6, stripe_y), (rect.right - 6, stripe_y), 2)
        elif self.vehicle_type == "suv":
            roof = pygame.Rect(rect.x + 4, rect.y + 8, self.width - 8, 20)
            pygame.draw.rect(surface, (40, 40, 130), roof, border_radius=3)
            window = pygame.Rect(rect.x + 7, rect.y + 12, self.width - 14, 12)
            pygame.draw.rect(surface, (150, 200, 240), window, border_radius=2)

        pygame.draw.circle(surface, BLACK, (rect.x + 7, rect.bottom - 3), 4)
        pygame.draw.circle(surface, BLACK, (rect.right - 7, rect.bottom - 3), 4)
        pygame.draw.circle(surface, BLACK, (rect.x + 7, rect.y + 3), 4)
        pygame.draw.circle(surface, BLACK, (rect.right - 7, rect.y + 3), 4)


class VehicleSpawner:
    def __init__(self):
        self.vehicles = []
        self.obstacles = []
        self.last_vehicle_time = 0
        self.last_obstacle_time = 0

    def try_spawn_vehicle(self, current_time, vehicle_interval, obstacle_interval):
        if current_time - self.last_vehicle_time > vehicle_interval:
            lane = random.randint(0, len(LANE_POSITIONS) - 1)
            v_type = random.choice(VEHICLE_TYPES)
            if not self._lane_blocked(lane, -100):
                self.vehicles.append(Vehicle(v_type, lane))
            self.last_vehicle_time = current_time

        if current_time - self.last_obstacle_time > obstacle_interval:
            lane = random.randint(0, len(LANE_POSITIONS) - 1)
            if not self._lane_blocked(lane, -60):
                self.obstacles.append(Obstacle(LANE_POSITIONS[lane], -OBSTACLE_HEIGHT))
            self.last_obstacle_time = current_time

    def _lane_blocked(self, lane, y_threshold):
        for v in self.vehicles:
            if abs(v.x - LANE_POSITIONS[lane]) < 10 and v.y < y_threshold + 80:
                return True
        for o in self.obstacles:
            if abs(o.x - LANE_POSITIONS[lane]) < 10 and o.y < y_threshold + 80:
                return True
        return False

    def update(self, player_speed):
        current_time = pygame.time.get_ticks()
        for v in self.vehicles:
            v.try_lane_change(current_time, self.vehicles)
            v.update(player_speed)
        for o in self.obstacles:
            o.update(player_speed)

        self.vehicles = [v for v in self.vehicles if not v.is_off_screen()]
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

    def check_collision(self, player_rect):
        for v in self.vehicles:
            if player_rect.colliderect(v.get_rect()):
                return v
        for o in self.obstacles:
            if player_rect.colliderect(o.get_rect()):
                return o
        return None

    def draw(self, surface):
        for v in self.vehicles:
            v.draw(surface)
        for o in self.obstacles:
            o.draw(surface)

    def reset(self):
        self.vehicles.clear()
        self.obstacles.clear()
        self.last_vehicle_time = 0
        self.last_obstacle_time = 0
