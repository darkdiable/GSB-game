import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

ROAD_WIDTH = 400
ROAD_LEFT = (SCREEN_WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

LANE_COUNT = 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 90
PLAYER_START_X = SCREEN_WIDTH // 2
PLAYER_START_Y = SCREEN_HEIGHT - 120

MAX_SPEED = 12
MIN_SPEED = 0
ACCELERATION = 0.15
BRAKE_DECELERATION = 0.3
FRICTION = 0.02
TURN_SPEED = 5

MAX_COLLISIONS = 5

VEHICLE_TYPES = ['sports', 'suv', 'truck', 'obstacle']
VEHICLE_SPEEDS = {
    'sports': 3,
    'suv': 2,
    'truck': 1,
    'obstacle': 0
}
VEHICLE_SIZES = {
    'sports': (45, 80),
    'suv': (55, 95),
    'truck': (65, 130),
    'obstacle': (40, 40)
}

SCENERY_TYPES = ['beach', 'town', 'desert']
SCENERY_CHANGE_DISTANCE = 3000

COLORS = {
    'road': (50, 50, 50),
    'road_line': (255, 255, 255),
    'grass': (34, 139, 34),
    'sand': (238, 214, 175),
    'beach_water': (0, 191, 255),
    'beach_sand': (244, 164, 96),
    'town_building': (100, 100, 120),
    'town_roof': (139, 69, 19),
    'desert': (210, 180, 140),
    'desert_rock': (160, 140, 120),
    'player_car': (255, 0, 0),
    'sports_car': (0, 100, 255),
    'suv_car': (0, 150, 0),
    'truck_car': (255, 165, 0),
    'obstacle': (100, 100, 100),
    'text': (255, 255, 255),
    'ui_bg': (0, 0, 0, 180)
}

pygame.font.init()

def get_chinese_font(size):
    font_names = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    for name in font_names:
        font = pygame.font.SysFont(name, size)
        if font:
            return font
    return pygame.font.SysFont(None, size)

FONT_SMALL = get_chinese_font(20)
FONT_MEDIUM = get_chinese_font(36)
FONT_LARGE = get_chinese_font(72)
