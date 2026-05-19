import pygame
import random
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WATER_SURFACE_Y,
    DIVER_SPEED, DIVER_HEALTH_BONUS, DIVER_WIDTH, DIVER_HEIGHT
)

class Diver:
    def __init__(self):
        self.width = DIVER_WIDTH
        self.height = DIVER_HEIGHT
        self.x = random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - 100)
        self.y = random.randint(WATER_SURFACE_Y + 50, SCREEN_HEIGHT - 100)
        self.speed = DIVER_SPEED
        self.health_bonus = DIVER_HEALTH_BONUS
        self.wobble = random.uniform(0, 6.28)
        self.direction = -1
        
    def update(self):
        self.x += self.speed * self.direction
        self.wobble += 0.1
        self.y += random.uniform(-0.5, 0.5)
        self.y = max(WATER_SURFACE_Y + 30, min(SCREEN_HEIGHT - self.height - 10, self.y))
        
        return self.x < -self.width or self.x > SCREEN_WIDTH + self.width
    
    def draw(self, screen):
        body_color = (255, 200, 150)
        suit_color = (0, 100, 150)
        
        pygame.draw.ellipse(screen, suit_color, 
                          (self.x + 5, self.y + 10, self.width - 10, self.height - 15))
        
        pygame.draw.circle(screen, body_color, 
                         (int(self.x + self.width // 2), int(self.y + 10)), 8)
        
        pygame.draw.rect(screen, (100, 100, 100), 
                        (self.x + self.width // 2 - 6, self.y + 5, 12, 8))
        
        pygame.draw.circle(screen, (200, 200, 255), 
                         (int(self.x + self.width // 2), int(self.y + 8)), 4)
        
        arm_swing = random.uniform(-5, 5)
        pygame.draw.line(screen, body_color, 
                        (self.x + 8, self.y + 20), 
                        (self.x - 2, self.y + 25 + arm_swing), 3)
        pygame.draw.line(screen, body_color, 
                        (self.x + self.width - 8, self.y + 20), 
                        (self.x + self.width + 2, self.y + 25 - arm_swing), 3)
        
        leg_swing = random.uniform(-3, 3)
        pygame.draw.line(screen, suit_color, 
                        (self.x + 10, self.y + self.height - 8), 
                        (self.x + 5, self.y + self.height + leg_swing), 4)
        pygame.draw.line(screen, suit_color, 
                        (self.x + self.width - 10, self.y + self.height - 8), 
                        (self.x + self.width - 5, self.y + self.height - leg_swing), 4)
        
        oxygen_tank_color = (50, 50, 50)
        pygame.draw.rect(screen, oxygen_tank_color, 
                        (self.x + self.width // 2 - 4, self.y + 12, 8, 15))
        
        text_color = (255, 255, 0)
        font = pygame.font.Font(None, 20)
        plus_text = font.render("+HP", True, text_color)
        screen.blit(plus_text, (self.x + self.width // 2 - 10, self.y - 15))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_health_bonus(self):
        return self.health_bonus
