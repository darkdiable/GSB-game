import pygame
from constants import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_INITIAL_X, PLAYER_INITIAL_Y,
    PLAYER_MAX_SPEED, PLAYER_ACCELERATION, PLAYER_BRAKE_DECELERATION,
    PLAYER_NATURAL_DECELERATION, PLAYER_LATERAL_SPEED, PLAYER_COLOR,
    ROAD_LEFT, ROAD_RIGHT, WHITE, YELLOW, RED, BLACK,
)


class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = float(PLAYER_INITIAL_X)
        self.y = float(PLAYER_INITIAL_Y)
        self.speed = 0.0
        self.max_speed = PLAYER_MAX_SPEED
        self.acceleration = PLAYER_ACCELERATION
        self.brake_deceleration = PLAYER_BRAKE_DECELERATION
        self.natural_deceleration = PLAYER_NATURAL_DECELERATION
        self.lateral_speed = PLAYER_LATERAL_SPEED
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1500

    def update(self, keys, dt):
        if keys[pygame.K_w]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_s]:
            self.speed = max(self.speed - self.brake_deceleration, 0)
        else:
            if self.speed > 0:
                self.speed = max(self.speed - self.natural_deceleration, 0)

        if keys[pygame.K_a]:
            self.x = max(self.x - self.lateral_speed, ROAD_LEFT + self.width // 2)
        if keys[pygame.K_d]:
            self.x = min(self.x + self.lateral_speed, ROAD_RIGHT - self.width // 2)

        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height,
        )

    def trigger_invincibility(self):
        self.invincible = True
        self.invincible_timer = self.invincible_duration

    def draw(self, surface):
        if self.invincible and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        rect = self.get_rect()
        body_color = PLAYER_COLOR

        pygame.draw.rect(surface, body_color, rect, border_radius=6)

        windshield = pygame.Rect(
            rect.x + 5, rect.y + 8, self.width - 10, 15
        )
        pygame.draw.rect(surface, (180, 220, 255), windshield, border_radius=3)

        rear_window = pygame.Rect(
            rect.x + 8, rect.y + self.height - 20, self.width - 16, 10
        )
        pygame.draw.rect(surface, (150, 200, 240), rear_window, border_radius=2)

        pygame.draw.rect(surface, YELLOW, (rect.x - 3, rect.y + 8, 4, 8))
        pygame.draw.rect(surface, YELLOW, (rect.right - 1, rect.y + 8, 4, 8))

        pygame.draw.rect(surface, RED, (rect.x - 3, rect.y + self.height - 14, 4, 8))
        pygame.draw.rect(surface, RED, (rect.right - 1, rect.y + self.height - 14, 4, 8))

        pygame.draw.circle(surface, BLACK, (rect.x + 8, rect.bottom - 4), 5)
        pygame.draw.circle(surface, BLACK, (rect.right - 8, rect.bottom - 4), 5)
        pygame.draw.circle(surface, BLACK, (rect.x + 8, rect.y + 4), 5)
        pygame.draw.circle(surface, BLACK, (rect.right - 8, rect.y + 4), 5)

    def reset(self):
        self.x = float(PLAYER_INITIAL_X)
        self.y = float(PLAYER_INITIAL_Y)
        self.speed = 0.0
        self.invincible = False
        self.invincible_timer = 0
