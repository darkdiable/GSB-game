import pygame
import math
from constants import *


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = CENTER_MARK_X
        self.y = COURT_TOP + COURT_HEIGHT // 2
        self.z = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.in_play = False
        self.last_hit_by = None
        self.bounce_count = 0
        self.rotation = 0
        self.trail = []
        self.first_bounce_checked = False
        self.first_bounce_in_service_box = False

    def serve(self, server_x, server_y, target_x, target_y, speed=BALL_SERVE_SPEED):
        self.x = server_x
        self.y = server_y
        self.z = 25
        self.last_hit_by = 'player' if server_y > NET_Y else 'npc'
        
        dx = target_x - server_x
        dy = target_y - server_y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0:
            gravity = 0.5
            
            time_to_target = dist / speed
            
            required_vz = (0 - self.z + 0.5 * gravity * time_to_target * time_to_target) / max(time_to_target, 0.1)
            
            net_y = NET_Y
            time_to_net = abs(net_y - server_y) / max(abs(dy / dist * speed), 0.1)
            z_at_net = self.z + required_vz * time_to_net - 0.5 * gravity * time_to_net * time_to_net
            
            min_z_at_net = NET_HEIGHT + 20
            if z_at_net < min_z_at_net:
                extra_vz = (min_z_at_net - z_at_net) / max(time_to_net, 0.1)
                required_vz += extra_vz
            
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
            self.vz = max(8, required_vz)
        
        self.in_play = True
        self.bounce_count = 0
        self.trail = []

    def update(self):
        if not self.in_play:
            return

        self.rotation += 0.3

        if len(self.trail) < 10:
            self.trail.append((self.x, self.y, self.z))
        else:
            self.trail.pop(0)
            self.trail.append((self.x, self.y, self.z))

        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.vz -= 0.5

        self._check_bounce()
        self._check_net_collision()

    def _check_bounce(self):
        if self.z <= 0 and self.vz < 0:
            self.z = 0
            self.vz = -self.vz * BALL_BOUNCE_DAMPING
            self.vx *= 0.95
            self.vy *= 0.95
            
            if self.bounce_count == 0 and self.last_hit_by:
                self.first_bounce_checked = True
            
            self.bounce_count += 1

            if abs(self.vz) < 1:
                self.vz = 0

    def _check_net_collision(self):
        if self.z <= NET_HEIGHT and abs(self.y - NET_Y) < 5:
            if self.vy > 0 and self.y < NET_Y:
                self.y = NET_Y - 6
            elif self.vy < 0 and self.y > NET_Y:
                self.y = NET_Y + 6
            
            self.vy = -self.vy * 0.3
            self.vx *= 0.8
            self.vz *= 0.5
            self.z += 2

    def hit(self, hitter, target_x, target_y, power=1.0):
        self.last_hit_by = hitter
        
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0:
            speed = min(BALL_MAX_SPEED * power, BALL_MAX_SPEED)
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
            self.vz = 6 + 4 * power
        
        self.bounce_count = 0

    def is_in_court(self, side=None):
        in_x = COURT_LEFT < self.x < COURT_RIGHT
        
        if side == 'top':
            in_y = COURT_TOP < self.y < NET_Y
        elif side == 'bottom':
            in_y = NET_Y < self.y < COURT_BOTTOM
        else:
            in_y = COURT_TOP < self.y < COURT_BOTTOM
        
        return in_x and in_y

    def is_in_service_box(self, server_side, serve_side='right'):
        if server_side == 'player':
            target_side = 'top'
        else:
            target_side = 'bottom'

        target_half = 'left' if serve_side == 'right' else 'right'
        in_x = (CENTER_MARK_X - SERVICE_BOX_WIDTH < self.x < CENTER_MARK_X) if target_half == 'left' else (CENTER_MARK_X < self.x < CENTER_MARK_X + SERVICE_BOX_WIDTH)
        in_y = (SERVICE_LINE_TOP < self.y < NET_Y) if target_side == 'top' else (NET_Y < self.y < SERVICE_LINE_BOTTOM)
        
        return in_x and in_y

    def is_net_touched(self):
        return self.z <= NET_HEIGHT and abs(self.y - NET_Y) < NET_WIDTH

    def get_rect(self):
        size = BALL_RADIUS * 2 + int(self.z * 0.1)
        return pygame.Rect(self.x - size // 2, self.y - size // 2, size, size)

    def get_shadow_pos(self):
        shadow_y = min(self.y + self.z * 0.3, COURT_BOTTOM)
        return (self.x, shadow_y)

    def draw(self, screen):
        if not self.in_play and self.z == 0:
            return

        shadow_x, shadow_y = self.get_shadow_pos()
        shadow_surface = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, COLORS['ball_shadow'], shadow_surface.get_rect())
        shadow_scale = max(0.3, 1 - self.z * 0.02)
        shadow_surface = pygame.transform.scale(shadow_surface, 
            (int(BALL_RADIUS * 2 * shadow_scale), int(BALL_RADIUS * shadow_scale)))
        screen.blit(shadow_surface, (shadow_x - BALL_RADIUS * shadow_scale, shadow_y - BALL_RADIUS * shadow_scale / 2))

        for i, (tx, ty, tz) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)) * 0.5)
            trail_surface = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (*COLORS['ball'], alpha), 
                (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS * (i / len(self.trail)))
            screen.blit(trail_surface, (tx - BALL_RADIUS, ty - BALL_RADIUS - tz * 0.5))

        ball_size = int(BALL_RADIUS + self.z * 0.1)
        draw_y = self.y - self.z * 0.5
        
        ball_surface = pygame.Surface((ball_size * 2, ball_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(ball_surface, COLORS['ball'], (ball_size, ball_size), ball_size)
        pygame.draw.circle(ball_surface, (200, 200, 0), (ball_size, ball_size), ball_size, 2)
        
        rotated_surface = pygame.transform.rotate(ball_surface, self.rotation * 30)
        screen.blit(rotated_surface, (self.x - rotated_surface.get_width() // 2, 
            draw_y - rotated_surface.get_height() // 2))
