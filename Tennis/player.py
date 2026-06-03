import pygame
import random
import math
from constants import *


class Player:
    def __init__(self, is_npc=False):
        self.is_npc = is_npc
        self.size = PLAYER_SIZE
        self.speed = NPC_SPEED if is_npc else PLAYER_SPEED
        
        if is_npc:
            self.x = COURT_X + COURT_WIDTH // 2
            self.y = COURT_Y + 150
            self.color = RED
        else:
            self.x = COURT_X + COURT_WIDTH // 2
            self.y = COURT_Y + COURT_HEIGHT - 150
            self.color = BLUE
        
        self.dx = 0
        self.dy = 0
        self.swinging = False
        self.swing_frame = 0
        self.has_ball = False
        self.serving = False
        self.serve_count = 0

    def update(self, keys=None, ball=None):
        if self.is_npc:
            self._update_npc(ball)
        else:
            self._update_player(keys)
        
        self._move()
        self._update_swing()

    def _update_player(self, keys):
        self.dx = 0
        self.dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dy = self.speed

    def _update_npc(self, ball):
        target_x = COURT_X + COURT_WIDTH // 2
        target_y = COURT_Y + 150
        
        if ball and ball.active:
            if ball.y < CENTER_LINE_X:
                target_x = ball.x
                if ball.dy > 0:
                    target_y = COURT_Y + 120
                else:
                    target_y = min(ball.y + 50, CENTER_LINE_X - 50)
            
            dist = math.hypot(ball.x - self.x, ball.y - self.y)
            if dist < 50 and ball.y < CENTER_LINE_X:
                if not self.swinging:
                    self.swing()
        
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        
        if dist > 5:
            self.dx = (dx / dist) * self.speed
            self.dy = (dy / dist) * self.speed
        else:
            self.dx = 0
            self.dy = 0
        
        if self.serving and self.serve_count < 60:
            self.serve_count += 1
            if self.serve_count >= 40:
                self.swing()

    def _move(self):
        self.x += self.dx
        self.y += self.dy
        
        if self.is_npc:
            self.x = max(SINGLES_LEFT + self.size // 2, 
                        min(SINGLES_RIGHT - self.size // 2, self.x))
            self.y = max(BASELINE_TOP + self.size // 2, 
                        min(CENTER_LINE_X - self.size // 2, self.y))
        else:
            self.x = max(SINGLES_LEFT + self.size // 2, 
                        min(SINGLES_RIGHT - self.size // 2, self.x))
            self.y = max(CENTER_LINE_X + self.size // 2, 
                        min(BASELINE_BOTTOM - self.size // 2, self.y))

    def _update_swing(self):
        if self.swinging:
            self.swing_frame += 1
            if self.swing_frame > 20:
                self.swinging = False
                self.swing_frame = 0

    def swing(self):
        if not self.swinging:
            self.swinging = True
            self.swing_frame = 0

    def get_hit_zone(self):
        hit_radius = 50
        return (self.x, self.y, hit_radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, 
                         (int(self.x), int(self.y)), self.size // 2)
        pygame.draw.circle(screen, SKIN, 
                         (int(self.x), int(self.y - self.size // 2 - 8)), 12)
        
        if self.swinging:
            angle = (self.swing_frame / 20) * 180 - 90
            if self.is_npc:
                angle = -angle
            
            rad = math.radians(angle)
            racket_x = self.x + math.cos(rad) * 35
            racket_y = self.y + math.sin(rad) * 35
            
            pygame.draw.line(screen, BROWN, 
                           (self.x, self.y), 
                           (racket_x, racket_y), 4)
            pygame.draw.circle(screen, YELLOW, 
                             (int(racket_x), int(racket_y)), 12, 2)
        else:
            side = 1 if self.is_npc else -1
            pygame.draw.line(screen, BROWN,
                           (self.x, self.y),
                           (self.x + side * 25, self.y - 10), 4)
            pygame.draw.circle(screen, YELLOW,
                             (int(self.x + side * 35), int(self.y - 10)), 12, 2)

    def reset_position(self, serving=False):
        self.serving = serving
        self.serve_count = 0
        if self.is_npc:
            self.x = COURT_X + COURT_WIDTH // 2
            self.y = COURT_Y + 150
        else:
            self.x = COURT_X + COURT_WIDTH // 2
            self.y = COURT_Y + COURT_HEIGHT - 150
        
        if serving:
            self.has_ball = True
