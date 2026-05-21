import pygame
import math
from constants import *


class Player:
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.size = PLAYER_SIZE
        self.facing = 'up'
        self.hitting = False
        self.hit_timer = 0
        self.swing_type = 'forehand'
        self.power = 0.0
        self.charging = False
        self.anim_frame = 0
        self.anim_timer = 0

    def reset(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.hitting = False
        self.hit_timer = 0
        self.power = 0.0
        self.charging = False
        self.anim_frame = 0

    def update(self, keys, ball, rules, can_hit):
        move_x = 0
        move_y = 0

        if not self.hitting:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                move_x = -PLAYER_SPEED
                self.facing = 'left'
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                move_x = PLAYER_SPEED
                self.facing = 'right'
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                move_y = -PLAYER_SPEED
                self.facing = 'up'
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                move_y = PLAYER_SPEED
                self.facing = 'down'

            if move_x != 0 and move_y != 0:
                move_x *= 0.707
                move_y *= 0.707

        self.x += move_x
        self.y += move_y

        self.x = max(COURT_LEFT + self.size // 2, min(COURT_RIGHT - self.size // 2, self.x))
        self.y = max(NET_Y + self.size // 2, min(COURT_BOTTOM - self.size // 2, self.y))

        if self.charging and self.power < 1.0:
            self.power = min(1.0, self.power + 0.02)

        if self.hitting:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.hitting = False
                self.power = 0.0

        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4

        if move_x != 0 or move_y != 0:
            if abs(move_x) > abs(move_y):
                self.facing = 'right' if move_x > 0 else 'left'
            else:
                self.facing = 'down' if move_y > 0 else 'up'

    def start_charge(self):
        self.charging = True
        self.power = 0.3

    def hit_ball(self, ball, target_x, target_y):
        self.charging = False
        self.hitting = True
        self.hit_timer = 20
        
        if self.x < CENTER_MARK_X:
            self.swing_type = 'forehand'
        else:
            self.swing_type = 'backhand'
        
        hit_power = max(0.5, self.power)
        ball.hit('player', target_x, target_y, hit_power)
        self.power = 0.0

    def serve(self, ball, rules):
        serve_side = rules.get_serve_side()
        if serve_side == 'right':
            serve_x = CENTER_MARK_X + 80
        else:
            serve_x = CENTER_MARK_X - 80
        
        serve_y = COURT_BOTTOM - 30
        self.x = serve_x
        self.y = serve_y
        
        target_side = 'left' if serve_side == 'right' else 'right'
        if target_side == 'left':
            target_x = CENTER_MARK_X - SERVICE_BOX_WIDTH // 2
        else:
            target_x = CENTER_MARK_X + SERVICE_BOX_WIDTH // 2
        target_y = SERVICE_LINE_TOP + 30
        
        self.hitting = True
        self.hit_timer = 25
        self.charging = False
        self.power = 0.8
        
        ball.serve(serve_x, serve_y, target_x, target_y, BALL_SERVE_SPEED)

    def is_near_ball(self, ball):
        if not ball.in_play:
            return False
        dist = math.sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
        return dist < self.size + BALL_RADIUS + 10

    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def draw(self, screen):
        shadow_surface = pygame.Surface((self.size + 10, self.size // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 80), shadow_surface.get_rect())
        screen.blit(shadow_surface, (self.x - (self.size + 10) // 2, self.y + self.size // 2 - 10))

        body_y = self.y
        head_radius = self.size // 4
        body_height = self.size // 2
        body_width = self.size // 2

        head_y = body_y - body_height - head_radius + 5

        pygame.draw.circle(screen, COLORS['player_shirt'], (self.x, head_y), head_radius)
        pygame.draw.circle(screen, (255, 220, 177), (self.x, head_y), head_radius - 2)

        body_rect = pygame.Rect(self.x - body_width // 2, body_y - body_height, body_width, body_height)
        pygame.draw.ellipse(screen, COLORS['player_shirt'], body_rect)

        shorts_rect = pygame.Rect(self.x - body_width // 2, body_y - body_height // 2 - 5, body_width, body_height // 2 + 5)
        pygame.draw.ellipse(screen, COLORS['player_shorts'], shorts_rect)

        leg_offset = math.sin(self.anim_frame * math.pi / 2) * 5 if not self.hitting else 0
        pygame.draw.line(screen, COLORS['player_shorts'], (self.x - 8, body_y), (self.x - 8 + leg_offset, body_y + 10), 6)
        pygame.draw.line(screen, COLORS['player_shorts'], (self.x + 8, body_y), (self.x + 8 - leg_offset, body_y + 10), 6)

        if self.hitting:
            swing_angle = (20 - self.hit_timer) * 15
            if self.swing_type == 'backhand':
                swing_angle = -swing_angle
            racket_length = 25
            racket_end_x = self.x + math.cos(math.radians(swing_angle - 90)) * racket_length
            racket_end_y = body_y - body_height // 2 + math.sin(math.radians(swing_angle - 90)) * racket_length
            pygame.draw.line(screen, (139, 69, 19), (self.x, body_y - body_height // 2), (racket_end_x, racket_end_y), 4)
            pygame.draw.ellipse(screen, (200, 200, 255), (racket_end_x - 8, racket_end_y - 12, 16, 24), 2)
        else:
            racket_angle = 30 if self.facing == 'right' else -30
            racket_end_x = self.x + math.cos(math.radians(racket_angle)) * 20
            racket_end_y = body_y - body_height // 2 - 5 + math.sin(math.radians(racket_angle)) * 20
            pygame.draw.line(screen, (139, 69, 19), (self.x, body_y - body_height // 2), (racket_end_x, racket_end_y), 3)
            pygame.draw.ellipse(screen, (200, 200, 255), (racket_end_x - 6, racket_end_y - 10, 12, 20), 2)

        if self.charging:
            power_bar_width = 40
            power_bar_height = 6
            pygame.draw.rect(screen, (100, 100, 100), 
                (self.x - power_bar_width // 2, self.y - self.size - 20, power_bar_width, power_bar_height), border_radius=3)
            pygame.draw.rect(screen, (255, 0, 0), 
                (self.x - power_bar_width // 2, self.y - self.size - 20, int(power_bar_width * self.power), power_bar_height), border_radius=3)

    def check_net_touch(self):
        return abs(self.y - NET_Y) < self.size // 2 + 5
