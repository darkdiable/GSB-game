import pygame
import math
import random
from constants import *


class NPC:
    def __init__(self, difficulty='medium'):
        self.x = NPC_START_X
        self.y = NPC_START_Y
        self.size = PLAYER_SIZE
        self.facing = 'down'
        self.hitting = False
        self.hit_timer = 0
        self.swing_type = 'forehand'
        self.power = 0.6
        self.anim_frame = 0
        self.anim_timer = 0
        self.difficulty = difficulty
        self.reaction_counter = 0
        self.target_x = NPC_START_X
        self.target_y = NPC_START_Y
        self.decision_timer = 0
        self.will_hit = False
        self.hit_target = (CENTER_MARK_X, COURT_BOTTOM - 60)

        if difficulty == 'easy':
            self.speed = NPC_SPEED * 0.8
            self.accuracy = 0.6
            self.reaction_delay = NPC_REACTION_DELAY * 2
        elif difficulty == 'hard':
            self.speed = NPC_SPEED * 1.1
            self.accuracy = 0.9
            self.reaction_delay = NPC_REACTION_DELAY // 2
        else:
            self.speed = NPC_SPEED
            self.accuracy = 0.75
            self.reaction_delay = NPC_REACTION_DELAY

    def reset(self):
        self.x = NPC_START_X
        self.y = NPC_START_Y
        self.hitting = False
        self.hit_timer = 0
        self.power = 0.6
        self.anim_frame = 0
        self.target_x = NPC_START_X
        self.target_y = NPC_START_Y
        self.reaction_counter = 0
        self.decision_timer = 0
        self.will_hit = False

    def update(self, ball, rules, game_state):
        self.reaction_counter += 1
        self.decision_timer += 1

        if self.hitting:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.hitting = False
            return False

        if game_state == 'serve' and rules.serving == 'npc' and rules.can_start_serve():
            if self.decision_timer > 60:
                self._serve(ball, rules)
                self.decision_timer = 0
                return True
            return False

        if ball.in_play and ball.last_hit_by != 'npc':
            if self.reaction_counter >= self.reaction_delay:
                self._decide_action(ball)
                self._move_to_target()
                if ball.y < NET_Y:
                    self._check_hit(ball)
        else:
            self._return_to_ready()

        self.x = max(COURT_LEFT + self.size // 2, min(COURT_RIGHT - self.size // 2, self.x))
        self.y = max(COURT_TOP + self.size // 2, min(NET_Y - self.size // 2, self.y))

        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4

        return False

    def _decide_action(self, ball):
        ball_reach_y = self._predict_ball_y(ball)
        
        if ball_reach_y and COURT_TOP < ball_reach_y < NET_Y:
            self.target_x = ball.x
            self.target_y = ball_reach_y - 30
            
            dist = math.sqrt((self.x - ball.x) ** 2 + (self.y - ball_reach_y) ** 2)
            self.will_hit = dist < self.size + 50 and ball.bounce_count <= 1
        else:
            self.target_x = NPC_START_X
            self.target_y = NPC_START_Y
            self.will_hit = False

        if self.will_hit and self.decision_timer >= 15:
            self.decision_timer = 0
            self._choose_hit_target(ball)

    def _predict_ball_y(self, ball):
        if ball.vy <= 0:
            return None
        
        time_to_reach = (self.y - ball.y) / ball.vy if ball.vy > 0 else 100
        
        if time_to_reach < 0 or time_to_reach > 60:
            return None
        
        predicted_y = ball.y + ball.vy * time_to_reach
        return predicted_y

    def _choose_hit_target(self, ball):
        target_options = [
            (COURT_LEFT + 80, COURT_BOTTOM - 80),
            (COURT_RIGHT - 80, COURT_BOTTOM - 80),
            (CENTER_MARK_X, COURT_BOTTOM - 40),
            (COURT_LEFT + 60, NET_Y + 60),
            (COURT_RIGHT - 60, NET_Y + 60),
        ]
        
        best_target = target_options[0]
        min_dist = float('inf')
        
        for option in target_options:
            if random.random() < self.accuracy:
                dist = math.sqrt((option[0] - ball.x) ** 2 + (option[1] - ball.y) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    best_target = option
            else:
                best_target = random.choice(target_options)
                break
        
        self.hit_target = best_target
        self.power = random.uniform(0.5, 0.9)

    def _move_to_target(self):
        if self.hitting:
            return

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 5:
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed
            
            if abs(dx) > abs(dy):
                self.facing = 'right' if dx > 0 else 'left'
            else:
                self.facing = 'up' if dy < 0 else 'down'
            
            self.x += move_x
            self.y += move_y

    def _check_hit(self, ball):
        if not ball.in_play or self.hitting:
            return

        dist = math.sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
        if dist < self.size + BALL_RADIUS + 15 and self.will_hit:
            self._hit_ball(ball)

    def _hit_ball(self, ball):
        self.hitting = True
        self.hit_timer = 20
        
        if self.x < CENTER_MARK_X:
            self.swing_type = 'backhand'
        else:
            self.swing_type = 'forehand'
        
        target_x, target_y = self.hit_target
        
        if random.random() > self.accuracy:
            target_x += random.uniform(-50, 50)
            target_y += random.uniform(-30, 30)
        
        ball.hit('npc', target_x, target_y, self.power)

    def _serve(self, ball, rules):
        serve_side = rules.get_serve_side()
        if serve_side == 'right':
            serve_x = CENTER_MARK_X + 80
        else:
            serve_x = CENTER_MARK_X - 80
        
        serve_y = COURT_TOP + 30
        self.x = serve_x
        self.y = serve_y
        
        target_side = 'left' if serve_side == 'right' else 'right'
        if target_side == 'left':
            target_x = CENTER_MARK_X - SERVICE_BOX_WIDTH // 2
        else:
            target_x = CENTER_MARK_X + SERVICE_BOX_WIDTH // 2
        target_y = NET_Y + 80
        
        if random.random() > self.accuracy:
            target_x += random.uniform(-30, 30)
            target_y += random.uniform(-20, 20)
        
        self.hitting = True
        self.hit_timer = 25
        
        ball.serve(serve_x, serve_y, target_x, target_y, BALL_SERVE_SPEED * 1.0)

    def _return_to_ready(self):
        dx = NPC_START_X - self.x
        dy = NPC_START_Y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 5:
            self.x += (dx / dist) * self.speed * 0.5
            self.y += (dy / dist) * self.speed * 0.5

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

        pygame.draw.circle(screen, COLORS['npc_shirt'], (self.x, head_y), head_radius)
        pygame.draw.circle(screen, (255, 220, 177), (self.x, head_y), head_radius - 2)

        body_rect = pygame.Rect(self.x - body_width // 2, body_y - body_height, body_width, body_height)
        pygame.draw.ellipse(screen, COLORS['npc_shirt'], body_rect)

        shorts_rect = pygame.Rect(self.x - body_width // 2, body_y - body_height // 2 - 5, body_width, body_height // 2 + 5)
        pygame.draw.ellipse(screen, COLORS['npc_shorts'], shorts_rect)

        leg_offset = math.sin(self.anim_frame * math.pi / 2) * 5 if not self.hitting else 0
        pygame.draw.line(screen, COLORS['npc_shorts'], (self.x - 8, body_y), (self.x - 8 + leg_offset, body_y + 10), 6)
        pygame.draw.line(screen, COLORS['npc_shorts'], (self.x + 8, body_y), (self.x + 8 - leg_offset, body_y + 10), 6)

        if self.hitting:
            swing_angle = (20 - self.hit_timer) * 15
            if self.swing_type == 'backhand':
                swing_angle = -swing_angle
            swing_angle += 180
            racket_length = 25
            racket_end_x = self.x + math.cos(math.radians(swing_angle - 90)) * racket_length
            racket_end_y = body_y - body_height // 2 + math.sin(math.radians(swing_angle - 90)) * racket_length
            pygame.draw.line(screen, (139, 69, 19), (self.x, body_y - body_height // 2), (racket_end_x, racket_end_y), 4)
            pygame.draw.ellipse(screen, (255, 200, 200), (racket_end_x - 8, racket_end_y - 12, 16, 24), 2)
        else:
            racket_angle = -30 if self.facing == 'right' else 30
            racket_end_x = self.x + math.cos(math.radians(racket_angle + 180)) * 20
            racket_end_y = body_y - body_height // 2 - 5 + math.sin(math.radians(racket_angle + 180)) * 20
            pygame.draw.line(screen, (139, 69, 19), (self.x, body_y - body_height // 2), (racket_end_x, racket_end_y), 3)
            pygame.draw.ellipse(screen, (255, 200, 200), (racket_end_x - 6, racket_end_y - 10, 12, 20), 2)

    def check_net_touch(self):
        return abs(self.y - NET_Y) < self.size // 2 + 5
