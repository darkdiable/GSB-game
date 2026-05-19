import pygame
import random
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WATER_SURFACE_Y,
    DESTROYER_SPEED_MIN, DESTROYER_SPEED_MAX,
    DESTROYER_HEALTH, DESTROYER_SCORE,
    DEPTH_CHARGE_COOLDOWN_MIN, DEPTH_CHARGE_COOLDOWN_MAX,
    DEPTH_CHARGE_INITIAL_COOLDOWN_MIN, DEPTH_CHARGE_INITIAL_COOLDOWN_MAX,
    DEPTH_CHARGE_COUNT_PER_DROP,
    ENEMY_SUB_SPEED_MIN, ENEMY_SUB_SPEED_MAX,
    ENEMY_SUB_HEALTH, ENEMY_SUB_SCORE,
    ENEMY_SUB_TORPEDO_COOLDOWN_MIN, ENEMY_SUB_TORPEDO_COOLDOWN_MAX,
    ENEMY_SUB_INITIAL_TORPEDO_COOLDOWN_MIN, ENEMY_SUB_INITIAL_TORPEDO_COOLDOWN_MAX
)
from weapons import DepthCharge, Torpedo

class EnemyDestroyer:
    def __init__(self):
        self.width = 120
        self.height = 50
        self.x = SCREEN_WIDTH + random.randint(50, 200)
        self.y = WATER_SURFACE_Y - self.height + 15
        self.speed = random.uniform(DESTROYER_SPEED_MIN, DESTROYER_SPEED_MAX)
        self.health = DESTROYER_HEALTH
        self.max_health = DESTROYER_HEALTH
        self.depth_charge_cooldown = random.randint(DEPTH_CHARGE_INITIAL_COOLDOWN_MIN, DEPTH_CHARGE_INITIAL_COOLDOWN_MAX)
        self.score_value = DESTROYER_SCORE
        
    def update(self):
        self.x -= self.speed
        if self.depth_charge_cooldown > 0:
            self.depth_charge_cooldown -= 1
        return self.x < -self.width
    
    def fire_depth_charges(self):
        if self.depth_charge_cooldown <= 0:
            self.depth_charge_cooldown = random.randint(DEPTH_CHARGE_COOLDOWN_MIN, DEPTH_CHARGE_COOLDOWN_MAX)
            charges = []
            for i in range(DEPTH_CHARGE_COUNT_PER_DROP):
                offset_x = random.randint(-20, 20)
                charges.append(DepthCharge(self.x + self.width // 2 + offset_x, self.y + self.height))
            return charges
        return []
    
    def draw(self, screen):
        hull_points = [
            (self.x, self.y + self.height - 10),
            (self.x + 10, self.y + self.height),
            (self.x + self.width - 10, self.y + self.height),
            (self.x + self.width, self.y + self.height - 10),
            (self.x + self.width - 5, self.y + 20),
            (self.x + 5, self.y + 20),
        ]
        pygame.draw.polygon(screen, (139, 69, 19), hull_points)
        pygame.draw.polygon(screen, (100, 50, 10), hull_points, 2)
        
        deck_y = self.y + 20
        pygame.draw.rect(screen, (160, 82, 45), 
                        (self.x + 10, deck_y, self.width - 20, 15))
        
        bridge_x = self.x + self.width // 2 - 15
        bridge_y = self.y
        pygame.draw.rect(screen, (128, 128, 128), (bridge_x, bridge_y, 30, 20))
        pygame.draw.rect(screen, (100, 100, 100), (bridge_x + 10, bridge_y - 10, 10, 10))
        
        gun_x = self.x + 20
        pygame.draw.rect(screen, (80, 80, 80), (gun_x, self.y - 5, 8, 15))
        pygame.draw.circle(screen, (60, 60, 60), (gun_x + 4, self.y - 5), 6)
        
        health_bar_width = 60
        health_bar_height = 6
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x + self.width // 2 - health_bar_width // 2, 
                         self.y - 20, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), 
                        (self.x + self.width // 2 - health_bar_width // 2, 
                         self.y - 20, int(health_bar_width * health_ratio), health_bar_height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class EnemySubmarine:
    def __init__(self):
        self.width = 90
        self.height = 35
        self.x = SCREEN_WIDTH + random.randint(50, 200)
        self.y = random.randint(WATER_SURFACE_Y + 80, SCREEN_HEIGHT - 100)
        self.speed = random.uniform(ENEMY_SUB_SPEED_MIN, ENEMY_SUB_SPEED_MAX)
        self.health = ENEMY_SUB_HEALTH
        self.max_health = ENEMY_SUB_HEALTH
        self.torpedo_cooldown = random.randint(ENEMY_SUB_INITIAL_TORPEDO_COOLDOWN_MIN, ENEMY_SUB_INITIAL_TORPEDO_COOLDOWN_MAX)
        self.score_value = ENEMY_SUB_SCORE
        self.vertical_direction = random.choice([-1, 1])
        self.vertical_timer = 0
        
    def update(self):
        self.x -= self.speed
        
        self.vertical_timer += 1
        if self.vertical_timer > 60:
            self.vertical_timer = 0
            if random.random() < 0.3:
                self.vertical_direction *= -1
        
        self.y += self.vertical_direction * 0.5
        self.y = max(WATER_SURFACE_Y + 50, min(SCREEN_HEIGHT - self.height - 20, self.y))
        
        if self.torpedo_cooldown > 0:
            self.torpedo_cooldown -= 1
        
        return self.x < -self.width
    
    def fire_torpedo(self):
        if self.torpedo_cooldown <= 0:
            self.torpedo_cooldown = random.randint(ENEMY_SUB_TORPEDO_COOLDOWN_MIN, ENEMY_SUB_TORPEDO_COOLDOWN_MAX)
            return Torpedo(self.x - 10, self.y + self.height // 2, is_player=False)
        return None
    
    def take_damage(self, damage, is_torpedo=False):
        if is_torpedo:
            self.health = 0
        else:
            self.health -= damage
        return self.health <= 0
    
    def draw(self, screen):
        points = [
            (self.x, self.y + self.height // 2),
            (self.x + 15, self.y),
            (self.x + self.width - 10, self.y),
            (self.x + self.width, self.y + self.height // 2),
            (self.x + self.width - 10, self.y + self.height),
            (self.x + 15, self.y + self.height),
        ]
        pygame.draw.polygon(screen, (180, 50, 50), points)
        pygame.draw.polygon(screen, (140, 30, 30), points, 2)
        
        conning_x = self.x + self.width - 30
        conning_y = self.y - 10
        pygame.draw.rect(screen, (160, 40, 40), (conning_x, conning_y, 15, 15))
        
        propeller_x = self.x - 5
        pygame.draw.ellipse(screen, (200, 60, 60), 
                          (propeller_x, self.y + self.height // 2 - 6, 8, 12))
        
        health_bar_width = 50
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x + 20, self.y - 15, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), 
                        (self.x + 20, self.y - 15, int(health_bar_width * health_ratio), health_bar_height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
