import pygame
from constants import *


class Referee:
    def __init__(self):
        self.x = REFEREE_X
        self.y = REFEREE_Y
        self.width = REFEREE_WIDTH
        self.height = REFEREE_HEIGHT
        self.message = ""
        self.message_timer = 0
        self.message_color = RED

    def set_message(self, message, color=RED):
        self.message = message
        self.message_timer = 180
        self.message_color = color

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""

    def check_serve(self, ball, server):
        if ball.hit_net:
            return "net"
        
        receiver_side = "npc" if server.is_npc else "player"
        if not ball.is_in_bounds(ball.x, ball.y, receiver_side):
            return "fault"
        
        return "good"

    def check_point(self, ball, court):
        if ball.x < SINGLES_LEFT or ball.x > SINGLES_RIGHT:
            return "out"
        
        if ball.bounce_count >= 2:
            return "double_bounce"
        
        return None

    def draw(self, screen):
        body_y = self.y + 20
        pygame.draw.rect(screen, (50, 50, 100), 
                        (self.x - self.width // 2, body_y, 
                         self.width, self.height - 20))
        
        head_y = self.y
        pygame.draw.circle(screen, SKIN, (self.x, head_y), 18)
        
        pygame.draw.arc(screen, BLACK, 
                       (self.x - 8, head_y - 5, 16, 12), 
                       0, 3.14, 2)
        
        if self.message and self.message_timer > 0:
            font = pygame.font.Font(None, 28)
            text = font.render(self.message, True, self.message_color)
            text_rect = text.get_rect(center=(self.x, self.y - 40))
            
            bg_rect = text_rect.copy()
            bg_rect.inflate_ip(20, 10)
            pygame.draw.rect(screen, WHITE, bg_rect)
            pygame.draw.rect(screen, BLACK, bg_rect, 2)
            
            screen.blit(text, text_rect)

    def is_in_bounds(self, x, y, side=None):
        if side == "player":
            return (SINGLES_LEFT <= x <= SINGLES_RIGHT and 
                    CENTER_LINE_X <= y <= BASELINE_BOTTOM)
        elif side == "npc":
            return (SINGLES_LEFT <= x <= SINGLES_RIGHT and 
                    BASELINE_TOP <= y <= CENTER_LINE_X)
        else:
            return (SINGLES_LEFT <= x <= SINGLES_RIGHT and 
                    COURT_Y <= y <= COURT_Y + COURT_HEIGHT)
