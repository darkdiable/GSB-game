import pygame
import random
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    MISSILE_SPEED, MISSILE_VERTICAL_SPEED, MISSILE_DAMAGE,
    TORPEDO_SPEED_PLAYER, TORPEDO_SPEED_ENEMY, TORPEDO_DAMAGE,
    DEPTH_CHARGE_FALL_SPEED, DEPTH_CHARGE_DAMAGE, DEPTH_CHARGE_EXPLOSION_DAMAGE
)

class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 8
        self.speed = MISSILE_SPEED
        self.vertical_speed = MISSILE_VERTICAL_SPEED
        self.damage = MISSILE_DAMAGE
        
    def update(self):
        self.x += self.speed * 0.3
        self.y += self.vertical_speed
        return self.y < 0
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 200, 0), 
                          (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, (255, 100, 0), 
                          (self.x - 8, self.y + 1, 10, 6))
        
        for i in range(3):
            trail_y = self.y + self.height // 2 + random.randint(-2, 2)
            pygame.draw.circle(screen, (255, 150, 0), 
                             (int(self.x - 5 - i * 4), int(trail_y)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Torpedo:
    def __init__(self, x, y, is_player=True):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 8
        self.speed = TORPEDO_SPEED_PLAYER if is_player else TORPEDO_SPEED_ENEMY
        self.is_player = is_player
        self.damage = TORPEDO_DAMAGE
        
    def update(self):
        self.x += self.speed
        if self.is_player:
            return self.x > SCREEN_WIDTH
        else:
            return self.x < -self.width
    
    def draw(self, screen):
        color = (0, 255, 255) if self.is_player else (255, 100, 100)
        pygame.draw.ellipse(screen, color, 
                          (self.x, self.y, self.width, self.height))
        
        if self.is_player:
            trail_x = self.x - 10
        else:
            trail_x = self.x + self.width
        pygame.draw.circle(screen, (200, 200, 200), (int(trail_x), int(self.y + 4)), 3)
        
        for i in range(5):
            bubble_x = trail_x + random.randint(-5, 5)
            bubble_y = self.y + random.randint(-3, self.height + 3)
            pygame.draw.circle(screen, (150, 150, 150), 
                             (int(bubble_x), int(bubble_y)), 1)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class DepthCharge:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.fall_speed = DEPTH_CHARGE_FALL_SPEED
        self.damage = DEPTH_CHARGE_DAMAGE
        self.explosion_damage = DEPTH_CHARGE_EXPLOSION_DAMAGE
        self.explosion_timer = 0
        self.exploding = False
        
    def update(self):
        if not self.exploding:
            self.y += self.fall_speed
            self.fall_speed += 0.025
            
            if self.y > SCREEN_HEIGHT:
                return True
        else:
            self.explosion_timer += 1
            if self.explosion_timer > 20:
                return True
        return False
    
    def explode(self):
        self.exploding = True
    
    def draw(self, screen):
        if self.exploding:
            explosion_radius = 20 + self.explosion_timer * 2
            alpha = max(0, 255 - self.explosion_timer * 12)
            pygame.draw.circle(screen, (255, 150, 0), 
                             (int(self.x), int(self.y)), explosion_radius)
            pygame.draw.circle(screen, (255, 255, 0), 
                             (int(self.x), int(self.y)), explosion_radius // 2)
        else:
            pygame.draw.circle(screen, (50, 50, 50), 
                             (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (30, 30, 30), 
                             (int(self.x), int(self.y)), self.radius, 2)
            pygame.draw.line(screen, (80, 80, 80), 
                           (self.x - 5, self.y - 5), (self.x + 5, self.y + 5), 2)
            pygame.draw.line(screen, (80, 80, 80), 
                           (self.x + 5, self.y - 5), (self.x - 5, self.y + 5), 2)
    
    def get_rect(self):
        if self.exploding:
            explosion_radius = 20 + self.explosion_timer * 2
            return pygame.Rect(self.x - explosion_radius, self.y - explosion_radius, 
                             explosion_radius * 2, explosion_radius * 2)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                         self.radius * 2, self.radius * 2)
