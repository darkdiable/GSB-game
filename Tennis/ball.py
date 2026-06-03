import pygame
import math
import random
from constants import *


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = NET_X
        self.y = COURT_Y + COURT_HEIGHT // 2
        self.dx = 0
        self.dy = 0
        self.radius = BALL_RADIUS
        self.active = False
        self.serve_mode = False
        self.last_hitter = None
        self.bounce_count = 0
        self.hit_net = False

    def serve(self, from_player, to_left=False):
        self.active = True
        self.serve_mode = True
        self.last_hitter = "player" if not from_player.is_npc else "npc"
        self.bounce_count = 0
        self.hit_net = False
        
        if from_player.is_npc:
            self.x = from_player.x
            self.y = from_player.y + 30
            self.dy = BALL_SPEED * 0.8
            self.dx = random.uniform(-2, 2)
        else:
            self.x = from_player.x
            self.y = from_player.y - 30
            self.dy = -BALL_SPEED * 0.8
            self.dx = random.uniform(-2, 2)

    def update(self):
        if not self.active:
            return
        
        self.dy += GRAVITY
        
        self.x += self.dx
        self.y += self.dy
        
        self._check_net()
        
        if self.y >= COURT_Y + COURT_HEIGHT - self.radius:
            self.y = COURT_Y + COURT_HEIGHT - self.radius
            self.dy = -self.dy * BOUNCE_FACTOR
            self.bounce_count += 1
        elif self.y <= COURT_Y + self.radius:
            self.y = COURT_Y + self.radius
            self.dy = -self.dy * BOUNCE_FACTOR
            self.bounce_count += 1
        
        if self.x <= COURT_X + self.radius:
            self.x = COURT_X + self.radius
            self.dx = -self.dx * BOUNCE_FACTOR
        elif self.x >= COURT_X + COURT_WIDTH - self.radius:
            self.x = COURT_X + COURT_WIDTH - self.radius
            self.dx = -self.dx * BOUNCE_FACTOR

    def _check_net(self):
        net_x = NET_X
        if abs(self.x - net_x) < self.radius + 2:
            if self.y > COURT_Y and self.y < COURT_Y + COURT_HEIGHT:
                if self.dx > 0:
                    self.x = net_x - self.radius - 5
                else:
                    self.x = net_x + self.radius + 5
                self.dx = -self.dx * 0.5
                self.hit_net = True

    def hit_by(self, player, direction_x=0):
        self.last_hitter = "player" if not player.is_npc else "npc"
        self.bounce_count = 0
        self.serve_mode = False
        self.hit_net = False
        
        if player.is_npc:
            self.dy = BALL_SPEED * 0.9
            target_x = random.choice([SINGLES_LEFT + 50, SINGLES_RIGHT - 50, NET_X])
            dx = target_x - self.x
            self.dx = max(-8, min(8, dx * 0.1))
            if direction_x != 0:
                self.dx = direction_x * 8
        else:
            self.dy = -BALL_SPEED * 0.9
            if direction_x != 0:
                self.dx = direction_x * 8
            else:
                self.dx = random.uniform(-5, 5)
        
        self.dy += random.uniform(-2, 2)

    def check_hit(self, player):
        if not self.active or not player.swinging:
            return False
        
        hit_x, hit_y, hit_radius = player.get_hit_zone()
        dist = math.hypot(self.x - hit_x, self.y - hit_y)
        
        if dist < hit_radius:
            direction_x = 0
            if player.swing_frame < 7:
                direction_x = -1
            elif player.swing_frame > 13:
                direction_x = 1
            self.hit_by(player, direction_x)
            return True
        
        return False

    def is_out_of_bounds(self):
        return (self.x < SINGLES_LEFT or self.x > SINGLES_RIGHT or
                self.y < COURT_Y or self.y > COURT_Y + COURT_HEIGHT)

    def get_side(self):
        if self.y < CENTER_LINE_X:
            return "npc"
        else:
            return "player"

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, YELLOW, 
                             (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, WHITE,
                             (int(self.x), int(self.y)), self.radius, 1)
