import pygame
from constants import *


class Referee:
    def __init__(self):
        self.x = COURT_RIGHT + 40
        self.y = NET_Y
        self.size = 30
        self.anim_frame = 0
        self.anim_timer = 0
        self.message = None
        self.message_timer = 0
        self.message_alpha = 255

    def update(self, rules):
        self.anim_timer += 1
        if self.anim_timer >= 30:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 2

        if rules.violation:
            self.message = rules.violation
            self.message_timer = rules.violation_timer
            self.message_alpha = min(255, 255)
        elif rules.point_winner and not rules.violation:
            if self.message_timer <= 0:
                winner = "玩家" if rules.point_winner == 'player' else "电脑"
                self.message = f"{winner}得分！"
                self.message_timer = 90
                self.message_alpha = 255
        elif rules.game_winner and not rules.violation:
            winner = "玩家" if rules.game_winner == 'player' else "电脑"
            self.message = f"{winner}赢下这一局！"
            self.message_timer = 120
            self.message_alpha = 255
        elif rules.match_winner:
            winner = "玩家" if rules.match_winner == 'player' else "电脑"
            self.message = f"比赛结束！{winner}获胜！"
            self.message_timer = 300
            self.message_alpha = 255

        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer < 30:
                self.message_alpha = int(255 * (self.message_timer / 30))
            if self.message_timer <= 0:
                self.message = None
                self.message_alpha = 255

    def draw(self, screen):
        self._draw_referee(screen)
        self._draw_message(screen)

    def _draw_referee(self, screen):
        shadow_surface = pygame.Surface((self.size + 10, self.size // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 80), shadow_surface.get_rect())
        screen.blit(shadow_surface, (self.x - (self.size + 10) // 2, self.y + self.size // 2 - 5))

        body_y = self.y
        head_radius = self.size // 4
        body_height = self.size // 2 + 5
        body_width = self.size // 2

        head_y = body_y - body_height - head_radius + 5

        pygame.draw.circle(screen, COLORS['referee_shirt'], (self.x, head_y), head_radius)
        pygame.draw.circle(screen, (255, 220, 177), (self.x, head_y), head_radius - 2)

        body_rect = pygame.Rect(self.x - body_width // 2, body_y - body_height, body_width, body_height)
        pygame.draw.ellipse(screen, COLORS['referee_shirt'], body_rect)

        pants_rect = pygame.Rect(self.x - body_width // 2, body_y - body_height // 2 - 5, body_width, body_height // 2 + 5)
        pygame.draw.ellipse(screen, COLORS['referee_pants'], pants_rect)

        leg_offset = 3 if self.anim_frame == 0 else -3
        pygame.draw.line(screen, COLORS['referee_pants'], (self.x - 6, body_y), (self.x - 6 + leg_offset, body_y + 8), 5)
        pygame.draw.line(screen, COLORS['referee_pants'], (self.x + 6, body_y), (self.x + 6 - leg_offset, body_y + 8), 5)

        pygame.draw.circle(screen, (255, 215, 0), (self.x, head_y - 5), 8)
        pygame.draw.rect(screen, (255, 215, 0), (self.x - 6, head_y - 2, 12, 8))

    def _draw_message(self, screen):
        if not self.message:
            return

        message_surface = FONT_VIOLATION.render(self.message, True, COLORS['text_violation'])
        
        bg_padding = 15
        bg_surface = pygame.Surface(
            (message_surface.get_width() + bg_padding * 2, 
             message_surface.get_height() + bg_padding * 2),
            pygame.SRCALPHA
        )
        bg_alpha = min(200, self.message_alpha)
        pygame.draw.rect(bg_surface, (0, 0, 0, bg_alpha), bg_surface.get_rect(), border_radius=10)
        pygame.draw.rect(bg_surface, (255, 0, 0, bg_alpha), bg_surface.get_rect(), 3, border_radius=10)

        message_y = self.y - 80
        
        arrow_points = [
            (self.x, message_y + bg_surface.get_height()),
            (self.x - 12, message_y + bg_surface.get_height() - 15),
            (self.x + 12, message_y + bg_surface.get_height() - 15),
        ]
        pygame.draw.polygon(bg_surface, (0, 0, 0, bg_alpha), 
                           [(12, bg_surface.get_height() - 5), (0, bg_surface.get_height() + 10), (24, bg_surface.get_height() + 10)])

        bg_surface.blit(message_surface, (bg_padding, bg_padding))
        bg_surface.set_alpha(self.message_alpha)

        screen.blit(bg_surface, (self.x - bg_surface.get_width() // 2, message_y))

        if self.message_timer > 0:
            pulse_scale = 1.0 + 0.1 * abs(pygame.time.get_ticks() % 500 - 250) / 250
            scaled_surface = pygame.transform.scale(
                bg_surface,
                (int(bg_surface.get_width() * pulse_scale),
                 int(bg_surface.get_height() * pulse_scale))
            )
            scaled_surface.set_alpha(self.message_alpha)
            screen.blit(scaled_surface, 
                       (self.x - scaled_surface.get_width() // 2, 
                        message_y - (scaled_surface.get_height() - bg_surface.get_height()) // 2))
