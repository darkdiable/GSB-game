import pygame
from constants import (
    ROAD_LEFT, ROAD_RIGHT, ROAD_WIDTH, SCREEN_HEIGHT,
    ROAD_COLOR, ROAD_LINE_COLOR, ROAD_EDGE_COLOR, GRASS_COLOR,
    LANE_COUNT, LANE_WIDTH,
)


class Road:
    def __init__(self):
        self.scroll_y = 0.0
        self.dash_length = 40
        self.dash_gap = 30
        self.edge_line_width = 4
        self.lane_line_width = 2

    def update(self, player_speed):
        self.scroll_y += player_speed
        period = self.dash_length + self.dash_gap
        if self.scroll_y > period:
            self.scroll_y -= period

    def draw(self, surface):
        pygame.draw.rect(surface, GRASS_COLOR, (0, 0, ROAD_LEFT, SCREEN_HEIGHT))
        pygame.draw.rect(surface, GRASS_COLOR, (ROAD_RIGHT, 0, ROAD_LEFT, SCREEN_HEIGHT))

        pygame.draw.rect(surface, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        pygame.draw.rect(surface, ROAD_EDGE_COLOR, (ROAD_LEFT, 0, self.edge_line_width, SCREEN_HEIGHT))
        pygame.draw.rect(surface, ROAD_EDGE_COLOR, (ROAD_RIGHT - self.edge_line_width, 0, self.edge_line_width, SCREEN_HEIGHT))

        for i in range(1, LANE_COUNT):
            x = ROAD_LEFT + i * LANE_WIDTH - self.lane_line_width // 2
            self._draw_dashed_line(surface, x)

    def _draw_dashed_line(self, surface, x):
        period = self.dash_length + self.dash_gap
        offset = self.scroll_y % period
        y = -period + offset
        while y < SCREEN_HEIGHT:
            dash_top = max(0, y)
            dash_bottom = min(SCREEN_HEIGHT, y + self.dash_length)
            if dash_bottom > dash_top:
                pygame.draw.rect(
                    surface, ROAD_LINE_COLOR,
                    (x, dash_top, self.lane_line_width, dash_bottom - dash_top),
                )
            y += period

    def reset(self):
        self.scroll_y = 0.0
