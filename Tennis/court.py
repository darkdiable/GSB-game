import pygame
from constants import *


class Court:
    def __init__(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, COURT_GREEN, 
                        (COURT_X, COURT_Y, COURT_WIDTH, COURT_HEIGHT))
        
        pygame.draw.rect(screen, COURT_LINE, 
                        (COURT_X, COURT_Y, COURT_WIDTH, COURT_HEIGHT), 3)
        
        pygame.draw.line(screen, COURT_LINE, 
                        (SINGLES_LEFT, COURT_Y), 
                        (SINGLES_LEFT, COURT_Y + COURT_HEIGHT), 2)
        pygame.draw.line(screen, COURT_LINE, 
                        (SINGLES_RIGHT, COURT_Y), 
                        (SINGLES_RIGHT, COURT_Y + COURT_HEIGHT), 2)
        
        pygame.draw.line(screen, COURT_LINE, 
                        (COURT_X, SERVICE_LINE_TOP), 
                        (COURT_X + COURT_WIDTH, SERVICE_LINE_TOP), 2)
        pygame.draw.line(screen, COURT_LINE, 
                        (COURT_X, SERVICE_LINE_BOTTOM), 
                        (COURT_X + COURT_WIDTH, SERVICE_LINE_BOTTOM), 2)
        
        pygame.draw.line(screen, COURT_LINE, 
                        (CENTER_LINE_X, COURT_Y), 
                        (CENTER_LINE_X, COURT_Y + COURT_HEIGHT), 2)
        
        self._draw_net(screen)

    def _draw_net(self, screen):
        net_x = NET_X
        net_y_start = COURT_Y
        net_y_end = COURT_Y + COURT_HEIGHT
        
        for y in range(net_y_start, net_y_end, 5):
            pygame.draw.line(screen, GRAY, (net_x, y), (net_x, y + 3), 1)
        
        pygame.draw.line(screen, WHITE, (net_x, net_y_start), (net_x, net_y_end), 3)
        
        net_post_y1 = COURT_Y - 20
        net_post_y2 = COURT_Y + COURT_HEIGHT + 20
        pygame.draw.line(screen, BROWN, (net_x, net_post_y1), (net_x, net_post_y2), 6)

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

    def is_in_service_box(self, x, y, server_side):
        if server_side == "player":
            return (SINGLES_LEFT <= x <= SINGLES_RIGHT and 
                    CENTER_LINE_X <= y <= SERVICE_LINE_BOTTOM)
        else:
            return (SINGLES_LEFT <= x <= SINGLES_RIGHT and 
                    SERVICE_LINE_TOP <= y <= CENTER_LINE_X)
