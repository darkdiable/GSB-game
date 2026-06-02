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
AVOID_LANE_CHANGE_COOLDOWN = 800
AVOID_BRAKE_DECELERATION = 0.08
AVOID_MIN_SPEED_FACTOR = 0.3


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
        self.original_speed = random.uniform(*config["speed_range"])
        self.speed = self.original_speed
        self.min_speed = self.original_speed * AVOID_MIN_SPEED_FACTOR
        self.detection_distance = config["detection_distance"]
        self.urgent_distance = config["urgent_distance"]
        self.lane_index = lane_index
        self.x = float(LANE_POSITIONS[lane_index])
        self.y = float(-self.height)
        self.type = "vehicle"
        self.target_x = self.x
        self.is_changing_lane = False
        self.next_lane_change_time = pygame.time.get_ticks() + random.randint(
            LANE_CHANGE_MIN_INTERVAL, LANE_CHANGE_MAX_INTERVAL
        )
        self.avoid_cooldown_until = 0
        self.is_braking = False

    def detect_hazard_ahead(self, all_vehicles, all_obstacles):
        hazards = []
        for v in all_vehicles:
            if v is self:
                continue
            if abs(v.x - self.x) < (self.width // 2 + v.width // 2 + 5):
                ahead_dist = self.y - v.y
                if 0 < ahead_dist < self.detection_distance:
                    if v.speed < self.speed:
                        hazards.append(("vehicle", ahead_dist, v.speed))
        for o in all_obstacles:
            if abs(o.x - self.x) < (self.width // 2 + o.width // 2 + 5):
                ahead_dist = self.y - o.y
                if 0 < ahead_dist < self.detection_distance:
                    hazards.append(("obstacle", ahead_dist, 0))
        hazards.sort(key=lambda h: h[1])
        return hazards

    def try_avoid_hazard(self, current_time, all_vehicles, all_obstacles):
        if self.is_changing_lane:
            return False
        if current_time < self.avoid_cooldown_until:
            self._apply_braking(all_vehicles, all_obstacles)
            return False
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            return False

        hazards = self.detect_hazard_ahead(all_vehicles, all_obstacles)
        if not hazards:
            self._release_brake()
            return False

        closest = hazards[0]
        hazard_type, dist, hazard_speed = closest
        is_urgent = dist < self.urgent_distance

        possible_lanes = []
        if self.lane_index > 0:
            possible_lanes.append(self.lane_index - 1)
        if self.lane_index < len(LANE_POSITIONS) - 1:
            possible_lanes.append(self.lane_index + 1)

        preferred = []
        for target_lane in possible_lanes:
            if not self._is_lane_safe(target_lane, all_vehicles, all_obstacles):
                continue
            if not self._is_target_lane_clear_ahead(target_lane, all_vehicles, all_obstacles):
                continue
            preferred.append(target_lane)

        if preferred:
            if is_urgent:
                best = preferred[0]
            else:
                best = min(preferred, key=lambda l: self._lane_hazard_score(l, all_vehicles, all_obstacles))

            self.lane_index = best
            self.target_x = float(LANE_POSITIONS[best])
            self.is_changing_lane = True
            self.avoid_cooldown_until = current_time + AVOID_LANE_CHANGE_COOLDOWN
            self._release_brake()
            return True
        else:
            safe_lanes = []
            for target_lane in possible_lanes:
                if self._is_lane_safe(target_lane, all_vehicles, all_obstacles):
                    safe_lanes.append(target_lane)

            if safe_lanes and is_urgent:
                best = min(safe_lanes, key=lambda l: self._lane_hazard_score(l, all_vehicles, all_obstacles))
                self.lane_index = best
                self.target_x = float(LANE_POSITIONS[best])
                self.is_changing_lane = True
                self.avoid_cooldown_until = current_time + AVOID_LANE_CHANGE_COOLDOWN
                self._apply_braking(all_vehicles, all_obstacles)
                return True

            self._apply_braking(all_vehicles, all_obstacles)
            return False

    def _apply_braking(self, all_vehicles, all_obstacles):
        hazards = self.detect_hazard_ahead(all_vehicles, all_obstacles)
        if hazards:
            _, dist, hazard_speed = hazards[0]
            target_speed = max(hazard_speed * 0.8, self.min_speed)
            if dist < self.urgent_distance:
                target_speed = max(hazard_speed * 0.5, self.min_speed)
            if self.speed > target_speed:
                self.speed = max(self.speed - AVOID_BRAKE_DECELERATION, target_speed)
            self.is_braking = True
        else:
            self._release_brake()

    def _release_brake(self):
        if self.speed < self.original_speed:
            self.speed = min(self.speed + 0.02, self.original_speed)
        if self.speed >= self.original_speed * 0.95:
            self.speed = self.original_speed
            self.is_braking = False

    def _is_target_lane_clear_ahead(self, target_lane, all_vehicles, all_obstacles):
        target_x = LANE_POSITIONS[target_lane]
        check_distance = self.detection_distance * 0.6
        for v in all_vehicles:
            if v is self:
                continue
            if abs(v.x - target_x) < (self.width // 2 + v.width // 2 + 5):
                ahead_dist = self.y - v.y
                if 0 < ahead_dist < check_distance:
                    return False
        for o in all_obstacles:
            if abs(o.x - target_x) < (self.width // 2 + o.width // 2 + 5):
                ahead_dist = self.y - o.y
                if 0 < ahead_dist < check_distance:
                    return False
        return True

    def _lane_hazard_score(self, target_lane, all_vehicles, all_obstacles):
        target_x = LANE_POSITIONS[target_lane]
        score = 0
        for v in all_vehicles:
            if v is self:
                continue
            if abs(v.x - target_x) < (self.width // 2 + v.width // 2 + 5):
                ahead_dist = self.y - v.y
                if 0 < ahead_dist < self.detection_distance:
                    score += 1000 / max(ahead_dist, 1)
        for o in all_obstacles:
            if abs(o.x - target_x) < (self.width // 2 + o.width // 2 + 5):
                ahead_dist = self.y - o.y
                if 0 < ahead_dist < self.detection_distance:
                    score += 2000 / max(ahead_dist, 1)
        return score

    def try_random_lane_change(self, current_time, all_vehicles, all_obstacles):
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
            if self._is_lane_safe(target_lane, all_vehicles, all_obstacles):
                self.lane_index = target_lane
                self.target_x = float(LANE_POSITIONS[target_lane])
                self.is_changing_lane = True
                break

        self.next_lane_change_time = current_time + random.randint(
            LANE_CHANGE_MIN_INTERVAL, LANE_CHANGE_MAX_INTERVAL
        )

    def _is_lane_safe(self, target_lane, all_vehicles, all_obstacles):
        target_x = LANE_POSITIONS[target_lane]
        for v in all_vehicles:
            if v is self:
                continue
            if abs(v.x - target_x) < (self.width // 2 + v.width // 2 + 8):
                if abs(v.y - self.y) < (self.height // 2 + v.height // 2 + 20):
                    return False
        for o in all_obstacles:
            if abs(o.x - target_x) < (self.width // 2 + o.width // 2 + 8):
                if abs(o.y - self.y) < (self.height // 2 + o.height // 2 + 20):
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
        if self.is_braking:
            self._release_brake()

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

        if self.is_braking:
            pygame.draw.rect(surface, (255, 50, 50), (rect.x + 4, rect.bottom - 6, 8, 4))
            pygame.draw.rect(surface, (255, 50, 50), (rect.right - 12, rect.bottom - 6, 8, 4))

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
            v.try_avoid_hazard(current_time, self.vehicles, self.obstacles)
            if not v.is_changing_lane and not v.is_braking:
                v.try_random_lane_change(current_time, self.vehicles, self.obstacles)
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
