import pygame
import math
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
GAME_DURATION = 90

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BG = (10, 10, 30)
PARTICLE_COLORS = [
    (255, 100, 100),
    (100, 255, 100),
    (100, 100, 255),
    (255, 255, 100),
    (255, 100, 255),
    (100, 255, 255),
]

GATE_TYPES = ["X", "H", "Y", "Z", "S", "T"]
GATE_COLORS = {
    "X": (255, 100, 100),
    "H": (100, 255, 100),
    "Y": (100, 100, 255),
    "Z": (255, 255, 100),
    "S": (255, 100, 255),
    "T": (100, 255, 255),
}

PARTICLE_RADIUS = 30
GATE_SIZE = 80
BASE_SPAWN_INTERVAL = 2500
MIN_SPAWN_INTERVAL = 500
COMBO_MULTIPLIER = 0.85
BASE_SCORE = 100
COMBO_BONUS = 50
