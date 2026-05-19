import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WATER_SURFACE_Y,
    PLAYER_SPEED, PLAYER_MAX_HEALTH,
    MISSILE_COOLDOWN, TORPEDO_COOLDOWN
)
from weapons import Missile, Torpedo

class PlayerSubmarine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 40
        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.missile_cooldown = 0
        self.torpedo_cooldown = 0
        self.missile_cooldown_time = MISSILE_COOLDOWN
        self.torpedo_cooldown_time = TORPEDO_COOLDOWN
        
    def update(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y = max(WATER_SURFACE_Y + 20, self.y - self.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y = min(SCREEN_HEIGHT - self.height - 10, self.y + self.speed)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(10, self.x - self.speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = min(SCREEN_WIDTH - self.width - 10, self.x + self.speed)
        
        if self.missile_cooldown > 0:
            self.missile_cooldown -= 1
        if self.torpedo_cooldown > 0:
            self.torpedo_cooldown -= 1
    
    def fire_missile(self):
        if self.missile_cooldown <= 0:
            self.missile_cooldown = self.missile_cooldown_time
            return Missile(self.x + self.width, self.y + self.height // 2)
        return None
    
    def fire_torpedo(self):
        if self.torpedo_cooldown <= 0:
            self.torpedo_cooldown = self.torpedo_cooldown_time
            return Torpedo(self.x + self.width, self.y + self.height // 2, is_player=True)
        return None
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    
    def draw(self, screen):
        points = [
            (self.x, self.y + self.height // 2),
            (self.x + 20, self.y),
            (self.x + self.width - 10, self.y),
            (self.x + self.width, self.y + self.height // 2),
            (self.x + self.width - 10, self.y + self.height),
            (self.x + 20, self.y + self.height),
        ]
        pygame.draw.polygon(screen, (128, 128, 128), points)
        pygame.draw.polygon(screen, (100, 100, 100), points, 2)
        
        periscope_x = self.x + 30
        periscope_y = self.y - 15
        pygame.draw.rect(screen, (80, 80, 80), (periscope_x, periscope_y, 8, 20))
        pygame.draw.circle(screen, (60, 60, 60), (periscope_x + 4, periscope_y), 5)
        
        propeller_x = self.x - 5
        pygame.draw.ellipse(screen, (150, 150, 150), 
                          (propeller_x, self.y + self.height // 2 - 8, 10, 16))
        
        health_bar_width = 80
        health_bar_height = 8
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x + 10, self.y - 25, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), 
                        (self.x + 10, self.y - 25, int(health_bar_width * health_ratio), health_bar_height))
        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.x + 10, self.y - 25, health_bar_width, health_bar_height), 1)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
