SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (180, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
FOREST_GREEN = (34, 100, 34)
BLUE = (0, 100, 200)
SKY_BLUE = (100, 180, 255)
BROWN = (139, 69, 19)
DARK_BROWN = (100, 50, 10)
SAND = (210, 180, 120)
GRAY = (128, 128, 128)
DARK_GRAY = (80, 80, 80)
LIGHT_GRAY = (192, 192, 192)
SKIN = (255, 200, 150)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
WATER_BLUE = (30, 80, 180)
WATER_LIGHT = (60, 120, 220)
PURPLE = (128, 0, 128)

GRAVITY = 0.6
PLAYER_SPEED = 4
PLAYER_JUMP_SPEED = -12
BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 5
FIRE_RATE = 150

DIFFICULTY_NORMAL = "normal"
DIFFICULTY_HELL = "hell"

DIFFICULTY_SETTINGS = {
    DIFFICULTY_NORMAL: {
        "enemy_spawn_rate": 3000,
        "enemy_speed_multiplier": 1.0,
        "enemy_count_multiplier": 1.0,
        "enemy_bullet_speed": 4,
        "enemy_fire_rate": 2000,
        "player_lives": 3,
    },
    DIFFICULTY_HELL: {
        "enemy_spawn_rate": 1200,
        "enemy_speed_multiplier": 1.8,
        "enemy_count_multiplier": 2.5,
        "enemy_bullet_speed": 7,
        "enemy_fire_rate": 1000,
        "player_lives": 3,
    },
}

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"
STATE_PAUSED = "paused"

LEVEL_WIDTH = 6400
GROUND_Y = SCREEN_HEIGHT - 60
