import pygame
import math
from constants import *


class Gate:
    def __init__(self, gate_type, x, y):
        self.gate_type = gate_type
        self.color = GATE_COLORS[gate_type]
        self.x = x
        self.y = y
        self.size = GATE_SIZE
        self.pulse_phase = 0
        self.highlight = False
        self.match_animation = 0
        self.matched_count = 0

    def update(self):
        self.pulse_phase += 0.05
        if self.match_animation > 0:
            self.match_animation -= 0.05

    def draw(self, surface):
        pulse = 1 + 0.1 * math.sin(self.pulse_phase)
        current_size = int(self.size * pulse)
        
        if self.match_animation > 0:
            glow_surface = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
            glow_alpha = int(255 * self.match_animation)
            pygame.draw.circle(glow_surface, (*self.color, glow_alpha // 2), 
                             (current_size, current_size), current_size)
            surface.blit(glow_surface, (self.x - current_size, self.y - current_size))
        
        rect = pygame.Rect(self.x - current_size // 2, self.y - current_size // 2,
                          current_size, current_size)
        
        pygame.draw.rect(surface, (30, 30, 60), rect, border_radius=15)
        pygame.draw.rect(surface, self.color, rect, width=3, border_radius=15)
        
        if self.highlight:
            highlight_surface = pygame.Surface((current_size, current_size), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, (*self.color, 80), highlight_surface.get_rect(), border_radius=12)
            surface.blit(highlight_surface, (self.x - current_size // 2, self.y - current_size // 2))
        
        font = pygame.font.Font(None, 48)
        text = font.render(self.gate_type, True, self.color)
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)
        
        if self.matched_count > 0:
            count_font = pygame.font.Font(None, 20)
            count_text = count_font.render(str(self.matched_count), True, (255, 255, 255))
            count_rect = count_text.get_rect(center=(self.x + current_size // 2 - 10, self.y - current_size // 2 + 10))
            pygame.draw.circle(surface, (255, 100, 100), count_rect.center, 12)
            surface.blit(count_text, count_rect)

    def contains_point(self, pos):
        return (self.x - self.size // 2 <= pos[0] <= self.x + self.size // 2 and
                self.y - self.size // 2 <= pos[1] <= self.y + self.size // 2)

    def check_match(self, particle):
        return particle.gate_type == self.gate_type

    def trigger_match(self):
        self.match_animation = 1.0
        self.matched_count += 1
