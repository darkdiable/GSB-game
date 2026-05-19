import pygame
import math
import random
from constants import WATER_SURFACE_Y, EXPLOSION_MAX_TIMER

class Explosion:
    def __init__(self, x, y, size=30):
        self.x = x
        self.y = y
        self.size = size
        self.max_size = size
        self.timer = 0
        self.max_timer = EXPLOSION_MAX_TIMER
        
    def update(self):
        self.timer += 1
        return self.timer >= self.max_timer
    
    def draw(self, screen):
        progress = self.timer / self.max_timer
        current_size = int(self.max_size * (1 - progress * 0.5))
        alpha = int(255 * (1 - progress))
        
        for i in range(3):
            radius = current_size - i * 5
            if radius > 0:
                color = (255, 150 - i * 30, 0)
                pygame.draw.circle(screen, color, (int(self.x), int(self.y)), radius)
        
        for i in range(8):
            angle = i * 45 + self.timer * 10
            dist = current_size + self.timer * 2
            px = self.x + math.cos(math.radians(angle)) * dist
            py = self.y + math.sin(math.radians(angle)) * dist
            pygame.draw.circle(screen, (255, 200, 0), (int(px), int(py)), 3)

class Bubble:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 6)
        self.speed = random.uniform(0.5, 2)
        self.wobble = random.uniform(0, 6.28)
        
    def update(self):
        self.y -= self.speed
        self.wobble += 0.1
        self.x += math.sin(self.wobble) * 0.5
        return self.y < WATER_SURFACE_Y
    
    def draw(self, screen):
        pygame.draw.circle(screen, (100, 150, 200), 
                         (int(self.x), int(self.y)), self.radius, 1)
