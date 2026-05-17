import pygame
import math
import random
from constants import *


class Particle:
    def __init__(self, gate_type, start_x=None, start_y=None):
        self.gate_type = gate_type
        self.color = GATE_COLORS[gate_type]
        self.radius = PARTICLE_RADIUS
        self.rotation = 0
        self.rotation_speed = random.uniform(1, 3) * random.choice([-1, 1])
        
        if start_x is None:
            self.x = random.randint(100, SCREEN_WIDTH - 100)
        else:
            self.x = start_x
            
        if start_y is None:
            self.y = random.randint(150, SCREEN_HEIGHT - 150)
        else:
            self.y = start_y
            
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.float_offset = random.uniform(0, math.pi * 2)
        self.float_speed = random.uniform(0.02, 0.05)
        self.dragging = False
        self.connected = False
        self.target_x = self.x
        self.target_y = self.y
        self.alpha = 255
        self.scale = 1.0
        self.born_time = pygame.time.get_ticks()

    def update(self, current_time):
        if not self.dragging:
            float_y = math.sin(current_time * 0.001 * self.float_speed + self.float_offset) * 0.5
            self.x += self.vx
            self.y += self.vy + float_y
            
            if self.x < self.radius or self.x > SCREEN_WIDTH - self.radius:
                self.vx *= -1
                self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
            if self.y < self.radius + 100 or self.y > SCREEN_HEIGHT - self.radius - 50:
                self.vy *= -1
                self.y = max(self.radius + 100, min(SCREEN_HEIGHT - self.radius - 50, self.y))
        
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360

    def draw(self, surface):
        temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        center = (self.radius, self.radius)
        
        pygame.draw.circle(temp_surface, (*self.color, self.alpha), center, self.radius)
        pygame.draw.circle(temp_surface, (0, 0, 0, self.alpha), center, self.radius, 2)
        
        rect = pygame.Rect(0, 0, self.radius * 2, self.radius)
        pygame.draw.arc(temp_surface, (0, 0, 0, self.alpha), rect, 0, math.pi, self.radius)
        rect2 = pygame.Rect(0, 0, self.radius * 2, self.radius)
        pygame.draw.arc(temp_surface, (255, 255, 255, self.alpha), rect2, math.pi, math.pi * 2, self.radius)
        
        small_radius = self.radius // 5
        pygame.draw.circle(temp_surface, (0, 0, 0, self.alpha), (self.radius, self.radius // 2), small_radius)
        pygame.draw.circle(temp_surface, (255, 255, 255, self.alpha), (self.radius, self.radius * 3 // 2), small_radius)
        
        rotated = pygame.transform.rotate(temp_surface, self.rotation)
        new_rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, new_rect)
        
        font = pygame.font.Font(None, 24)
        text = font.render(self.gate_type, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x, self.y + self.radius + 15))
        surface.blit(text, text_rect)

    def contains_point(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return math.sqrt(dx * dx + dy * dy) <= self.radius

    def start_drag(self, pos):
        self.dragging = True
        self.drag_offset_x = self.x - pos[0]
        self.drag_offset_y = self.y - pos[1]

    def update_drag(self, pos):
        if self.dragging:
            self.x = pos[0] + self.drag_offset_x
            self.y = pos[1] + self.drag_offset_y

    def stop_drag(self):
        self.dragging = False
