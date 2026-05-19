import pygame
from config import *


class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = 0
        self.max_speed = MAX_SPEED
        self.min_speed = MIN_SPEED
        self.acceleration = ACCELERATION
        self.brake_deceleration = BRAKE_DECELERATION
        self.friction = FRICTION
        self.turn_speed = TURN_SPEED
        self.collisions = 0
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 120

    def update(self, keys):
        if keys[pygame.K_w]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_s]:
            self.speed = max(self.speed - self.brake_deceleration, self.min_speed)
        else:
            if self.speed > 0:
                self.speed = max(self.speed - self.friction, 0)

        if keys[pygame.K_a]:
            self.x -= self.turn_speed
        if keys[pygame.K_d]:
            self.x += self.turn_speed

        self.x = max(ROAD_LEFT + self.width // 2, min(self.x, ROAD_RIGHT - self.width // 2))

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def draw(self, screen):
        if self.invincible and self.invincible_timer % 10 < 5:
            return

        car_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, COLORS['player_car'], car_rect, border_radius=8)

        window_rect = pygame.Rect(
            self.x - self.width // 2 + 8,
            self.y - self.height // 2 + 15,
            self.width - 16,
            25
        )
        pygame.draw.rect(screen, (200, 230, 255), window_rect, border_radius=4)

        pygame.draw.circle(screen, (255, 255, 0), (self.x - 12, self.y + self.height // 2 - 8), 5)
        pygame.draw.circle(screen, (255, 255, 0), (self.x + 12, self.y + self.height // 2 - 8), 5)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2 + 5,
            self.y - self.height // 2 + 5,
            self.width - 10,
            self.height - 10
        )

    def take_damage(self):
        if not self.invincible:
            self.collisions += 1
            self.invincible = True
            self.invincible_timer = self.invincible_duration
            self.speed = max(self.speed - 2, 0)
            return True
        return False

    def is_game_over(self):
        return self.collisions >= MAX_COLLISIONS

    def reset(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = 0
        self.collisions = 0
        self.invincible = False
        self.invincible_timer = 0
