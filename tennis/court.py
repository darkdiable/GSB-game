import pygame
from constants import *


class Court:
    def __init__(self):
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._pre_render()

    def _pre_render(self):
        self.surface.fill((0, 0, 0, 0))
        
        self._draw_court_outline()
        self._draw_service_lines()
        self._draw_center_line()
        self._draw_net()

    def _draw_court_outline(self):
        court_rect = pygame.Rect(COURT_LEFT, COURT_TOP, COURT_WIDTH, COURT_HEIGHT)
        
        outer_margin = 30
        outer_rect = pygame.Rect(COURT_LEFT - outer_margin, COURT_TOP - outer_margin, 
                                 COURT_WIDTH + outer_margin * 2, COURT_HEIGHT + outer_margin * 2)
        pygame.draw.rect(self.surface, (30, 120, 30), outer_rect)
        
        inner_margin = 15
        inner_rect = pygame.Rect(COURT_LEFT - inner_margin, COURT_TOP - inner_margin,
                                 COURT_WIDTH + inner_margin * 2, COURT_HEIGHT + inner_margin * 2)
        pygame.draw.rect(self.surface, (25, 100, 25), inner_rect)
        
        pygame.draw.rect(self.surface, COLORS['court'], court_rect)
        
        pygame.draw.rect(self.surface, COLORS['court_line'], court_rect, 4)

    def _draw_service_lines(self):
        pygame.draw.line(self.surface, COLORS['court_line'],
                        (COURT_LEFT, SERVICE_LINE_TOP),
                        (COURT_RIGHT, SERVICE_LINE_TOP), 3)
        
        pygame.draw.line(self.surface, COLORS['court_line'],
                        (COURT_LEFT, SERVICE_LINE_BOTTOM),
                        (COURT_RIGHT, SERVICE_LINE_BOTTOM), 3)
        
        pygame.draw.line(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X, SERVICE_LINE_TOP),
                        (CENTER_MARK_X, NET_Y), 2)
        
        pygame.draw.line(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X, NET_Y),
                        (CENTER_MARK_X, SERVICE_LINE_BOTTOM), 2)
        
        pygame.draw.rect(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X - SERVICE_BOX_WIDTH, SERVICE_LINE_TOP,
                         SERVICE_BOX_WIDTH, NET_Y - SERVICE_LINE_TOP), 2)
        
        pygame.draw.rect(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X, SERVICE_LINE_TOP,
                         SERVICE_BOX_WIDTH, NET_Y - SERVICE_LINE_TOP), 2)
        
        pygame.draw.rect(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X - SERVICE_BOX_WIDTH, NET_Y,
                         SERVICE_BOX_WIDTH, SERVICE_LINE_BOTTOM - NET_Y), 2)
        
        pygame.draw.rect(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X, NET_Y,
                         SERVICE_BOX_WIDTH, SERVICE_LINE_BOTTOM - NET_Y), 2)
        
        pygame.draw.rect(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X - 3, COURT_TOP - 8, 6, 16), 2)
        
        pygame.draw.rect(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X - 3, COURT_BOTTOM - 8, 6, 16), 2)

    def _draw_center_line(self):
        pygame.draw.line(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X, COURT_TOP),
                        (CENTER_MARK_X, COURT_TOP + 10), 2)
        
        pygame.draw.line(self.surface, COLORS['court_line'],
                        (CENTER_MARK_X, COURT_BOTTOM - 10),
                        (CENTER_MARK_X, COURT_BOTTOM), 2)

    def _draw_net(self):
        post_left_x = COURT_LEFT - 15
        post_right_x = COURT_RIGHT + 15
        
        pygame.draw.rect(self.surface, COLORS['net_post'],
                        (post_left_x - 5, NET_Y - NET_HEIGHT, 10, NET_HEIGHT + 10))
        
        pygame.draw.rect(self.surface, COLORS['net_post'],
                        (post_right_x - 5, NET_Y - NET_HEIGHT, 10, NET_HEIGHT + 10))
        
        for i in range(0, COURT_WIDTH + 1, 8):
            x = COURT_LEFT + i
            pygame.draw.line(self.surface, COLORS['net'],
                            (x, NET_Y - NET_HEIGHT),
                            (x, NET_Y), 1)
        
        for i in range(0, NET_HEIGHT + 1, 6):
            y = NET_Y - NET_HEIGHT + i
            pygame.draw.line(self.surface, COLORS['net'],
                            (COURT_LEFT, y),
                            (COURT_RIGHT, y), 1)
        
        pygame.draw.line(self.surface, (255, 255, 255),
                        (COURT_LEFT - 15, NET_Y - NET_HEIGHT),
                        (COURT_RIGHT + 15, NET_Y - NET_HEIGHT), 3)
        
        pygame.draw.line(self.surface, (255, 255, 255),
                        (COURT_LEFT - 15, NET_Y),
                        (COURT_RIGHT + 15, NET_Y), 2)
        
        center_band_x = CENTER_MARK_X - 3
        pygame.draw.rect(self.surface, (255, 255, 255),
                        (center_band_x, NET_Y - NET_HEIGHT, 6, NET_HEIGHT))

    def draw(self, screen):
        screen.fill(COLORS['background'])
        screen.blit(self.surface, (0, 0))

    def is_in_court(self, x, y, side=None):
        in_x = COURT_LEFT < x < COURT_RIGHT
        
        if side == 'top':
            in_y = COURT_TOP < y < NET_Y
        elif side == 'bottom':
            in_y = NET_Y < y < COURT_BOTTOM
        else:
            in_y = COURT_TOP < y < COURT_BOTTOM
        
        return in_x and in_y

    def is_in_service_box(self, x, y, server_side):
        if server_side == 'player':
            target_y1 = SERVICE_LINE_TOP
            target_y2 = NET_Y
        else:
            target_y1 = NET_Y
            target_y2 = SERVICE_LINE_BOTTOM

        serve_side = 'right' if ((0) % 2 == 0) else 'left'
        
        if serve_side == 'left':
            x1, x2 = CENTER_MARK_X - SERVICE_BOX_WIDTH, CENTER_MARK_X
        else:
            x1, x2 = CENTER_MARK_X, CENTER_MARK_X + SERVICE_BOX_WIDTH

        return x1 < x < x2 and target_y1 < y < target_y2
