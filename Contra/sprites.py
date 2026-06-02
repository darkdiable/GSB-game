import pygame
from constants import *


def create_player_stand_right():
    surf = pygame.Surface((32, 48), pygame.SRCALPHA)
    pygame.draw.rect(surf, SKIN, (12, 0, 8, 10))
    pygame.draw.rect(surf, BLUE, (12, 1, 8, 3))
    pygame.draw.rect(surf, BROWN, (11, 10, 10, 4))
    pygame.draw.rect(surf, RED, (8, 14, 16, 14))
    pygame.draw.rect(surf, RED, (10, 28, 6, 14))
    pygame.draw.rect(surf, RED, (16, 28, 6, 14))
    pygame.draw.rect(surf, DARK_BROWN, (10, 40, 6, 8))
    pygame.draw.rect(surf, DARK_BROWN, (16, 40, 6, 8))
    pygame.draw.rect(surf, SKIN, (22, 16, 6, 4))
    pygame.draw.rect(surf, SKIN, (2, 18, 8, 4))
    pygame.draw.rect(surf, RED, (0, 20, 6, 4))
    pygame.draw.rect(surf, SKIN, (26, 18, 4, 3))
    return surf


def create_player_stand_left():
    surf = create_player_stand_right()
    return pygame.transform.flip(surf, True, False)


def create_player_run_right():
    surf = pygame.Surface((36, 48), pygame.SRCALPHA)
    pygame.draw.rect(surf, SKIN, (14, 0, 8, 10))
    pygame.draw.rect(surf, BLUE, (14, 1, 8, 3))
    pygame.draw.rect(surf, BROWN, (13, 10, 10, 4))
    pygame.draw.rect(surf, RED, (10, 14, 16, 14))
    pygame.draw.rect(surf, RED, (12, 28, 6, 14))
    pygame.draw.rect(surf, RED, (18, 28, 6, 14))
    pygame.draw.rect(surf, DARK_BROWN, (8, 38, 6, 10))
    pygame.draw.rect(surf, DARK_BROWN, (22, 38, 6, 10))
    pygame.draw.rect(surf, SKIN, (24, 16, 8, 4))
    pygame.draw.rect(surf, SKIN, (4, 16, 8, 4))
    pygame.draw.rect(surf, RED, (0, 18, 6, 4))
    pygame.draw.rect(surf, SKIN, (30, 18, 4, 3))
    return surf


def create_player_run_left():
    surf = create_player_run_right()
    return pygame.transform.flip(surf, True, False)


def create_player_jump_right():
    surf = pygame.Surface((36, 48), pygame.SRCALPHA)
    pygame.draw.rect(surf, SKIN, (14, 0, 8, 10))
    pygame.draw.rect(surf, BLUE, (14, 1, 8, 3))
    pygame.draw.rect(surf, BROWN, (13, 10, 10, 4))
    pygame.draw.rect(surf, RED, (10, 14, 16, 14))
    pygame.draw.rect(surf, RED, (6, 28, 6, 12))
    pygame.draw.rect(surf, RED, (22, 20, 6, 12))
    pygame.draw.rect(surf, DARK_BROWN, (2, 36, 6, 8))
    pygame.draw.rect(surf, DARK_BROWN, (26, 30, 6, 8))
    pygame.draw.rect(surf, SKIN, (24, 14, 8, 4))
    pygame.draw.rect(surf, SKIN, (2, 28, 6, 4))
    pygame.draw.rect(surf, RED, (0, 28, 4, 6))
    pygame.draw.rect(surf, SKIN, (30, 14, 4, 3))
    return surf


def create_player_jump_left():
    surf = create_player_jump_right()
    return pygame.transform.flip(surf, True, False)


def create_player_prone_right():
    surf = pygame.Surface((44, 28), pygame.SRCALPHA)
    pygame.draw.rect(surf, SKIN, (4, 6, 8, 8))
    pygame.draw.rect(surf, BLUE, (4, 6, 8, 3))
    pygame.draw.rect(surf, RED, (10, 10, 20, 10))
    pygame.draw.rect(surf, RED, (28, 18, 8, 6))
    pygame.draw.rect(surf, RED, (10, 20, 8, 6))
    pygame.draw.rect(surf, DARK_BROWN, (10, 24, 8, 4))
    pygame.draw.rect(surf, DARK_BROWN, (34, 22, 6, 6))
    pygame.draw.rect(surf, SKIN, (28, 8, 6, 4))
    pygame.draw.rect(surf, SKIN, (32, 10, 8, 3))
    return surf


def create_player_prone_left():
    surf = create_player_prone_right()
    return pygame.transform.flip(surf, True, False)


def create_player_up_right():
    surf = pygame.Surface((32, 52), pygame.SRCALPHA)
    pygame.draw.rect(surf, SKIN, (12, 0, 8, 10))
    pygame.draw.rect(surf, BLUE, (12, 1, 8, 3))
    pygame.draw.rect(surf, BROWN, (11, 10, 10, 4))
    pygame.draw.rect(surf, RED, (8, 14, 16, 14))
    pygame.draw.rect(surf, RED, (10, 28, 6, 14))
    pygame.draw.rect(surf, RED, (16, 28, 6, 14))
    pygame.draw.rect(surf, DARK_BROWN, (10, 40, 6, 12))
    pygame.draw.rect(surf, DARK_BROWN, (16, 40, 6, 12))
    pygame.draw.rect(surf, SKIN, (14, 2, 4, 14))
    pygame.draw.rect(surf, SKIN, (16, 0, 6, 3))
    return surf


def create_player_up_left():
    surf = create_player_up_right()
    return pygame.transform.flip(surf, True, False)


def create_soldier_right():
    surf = pygame.Surface((28, 44), pygame.SRCALPHA)
    pygame.draw.rect(surf, SKIN, (10, 0, 8, 8))
    pygame.draw.rect(surf, DARK_GREEN, (10, 1, 8, 3))
    pygame.draw.rect(surf, DARK_GREEN, (8, 8, 12, 14))
    pygame.draw.rect(surf, DARK_GREEN, (10, 22, 5, 12))
    pygame.draw.rect(surf, DARK_GREEN, (15, 22, 5, 12))
    pygame.draw.rect(surf, DARK_BROWN, (10, 32, 5, 12))
    pygame.draw.rect(surf, DARK_BROWN, (15, 32, 5, 12))
    pygame.draw.rect(surf, SKIN, (18, 12, 6, 4))
    pygame.draw.rect(surf, SKIN, (4, 14, 6, 4))
    pygame.draw.rect(surf, SKIN, (22, 14, 4, 3))
    return surf


def create_soldier_left():
    surf = create_soldier_right()
    return pygame.transform.flip(surf, True, False)


def create_turret():
    surf = pygame.Surface((36, 28), pygame.SRCALPHA)
    pygame.draw.rect(surf, GRAY, (0, 14, 36, 14))
    pygame.draw.rect(surf, DARK_GRAY, (2, 16, 32, 10))
    pygame.draw.rect(surf, GRAY, (14, 4, 8, 14))
    pygame.draw.rect(surf, DARK_GRAY, (14, 0, 8, 6))
    pygame.draw.rect(surf, RED, (16, 1, 4, 3))
    return surf


def create_sniper_right():
    surf = pygame.Surface((28, 44), pygame.SRCALPHA)
    pygame.draw.rect(surf, SKIN, (10, 0, 8, 8))
    pygame.draw.rect(surf, DARK_RED, (10, 1, 8, 3))
    pygame.draw.rect(surf, DARK_RED, (8, 8, 12, 14))
    pygame.draw.rect(surf, DARK_RED, (10, 22, 5, 12))
    pygame.draw.rect(surf, DARK_RED, (15, 22, 5, 12))
    pygame.draw.rect(surf, DARK_BROWN, (10, 32, 5, 12))
    pygame.draw.rect(surf, DARK_BROWN, (15, 32, 5, 12))
    pygame.draw.rect(surf, SKIN, (18, 10, 8, 3))
    pygame.draw.rect(surf, SKIN, (24, 12, 4, 3))
    return surf


def create_sniper_left():
    surf = create_sniper_right()
    return pygame.transform.flip(surf, True, False)


def create_bullet():
    surf = pygame.Surface((8, 4), pygame.SRCALPHA)
    pygame.draw.rect(surf, YELLOW, (0, 0, 6, 4))
    pygame.draw.rect(surf, ORANGE, (0, 1, 3, 2))
    return surf


def create_enemy_bullet():
    surf = pygame.Surface((6, 6), pygame.SRCALPHA)
    pygame.draw.circle(surf, RED, (3, 3), 3)
    pygame.draw.circle(surf, ORANGE, (3, 3), 2)
    return surf


def create_ground_tile():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(surf, BROWN, (0, 0, 32, 32))
    for i in range(0, 32, 4):
        pygame.draw.rect(surf, DARK_BROWN, (i, 0, 1, 32))
        pygame.draw.rect(surf, DARK_BROWN, (0, i, 32, 1))
    pygame.draw.rect(surf, DARK_GREEN, (0, 0, 32, 4))
    pygame.draw.rect(surf, GREEN, (0, 0, 32, 2))
    return surf


def create_platform_tile():
    surf = pygame.Surface((32, 16), pygame.SRCALPHA)
    pygame.draw.rect(surf, BROWN, (0, 0, 32, 16))
    pygame.draw.rect(surf, DARK_BROWN, (0, 0, 32, 2))
    for i in range(0, 32, 8):
        pygame.draw.rect(surf, DARK_BROWN, (i, 0, 1, 16))
    return surf


def create_bridge_tile():
    surf = pygame.Surface((32, 16), pygame.SRCALPHA)
    pygame.draw.rect(surf, DARK_BROWN, (0, 0, 32, 12))
    for i in range(0, 32, 4):
        pygame.draw.rect(surf, SAND, (i, 0, 2, 12))
    pygame.draw.rect(surf, DARK_BROWN, (0, 12, 32, 4))
    return surf


def create_water_tile():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(surf, WATER_BLUE, (0, 0, 32, 32))
    for i in range(0, 32, 8):
        pygame.draw.rect(surf, WATER_LIGHT, (i, 2, 4, 2))
        pygame.draw.rect(surf, WATER_LIGHT, (i + 4, 8, 4, 2))
        pygame.draw.rect(surf, WATER_LIGHT, (i, 14, 4, 2))
    return surf


def create_bush():
    surf = pygame.Surface((48, 24), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, DARK_GREEN, (0, 8, 48, 16))
    pygame.draw.ellipse(surf, FOREST_GREEN, (4, 4, 20, 16))
    pygame.draw.ellipse(surf, FOREST_GREEN, (20, 2, 20, 18))
    pygame.draw.ellipse(surf, GREEN, (8, 6, 14, 10))
    pygame.draw.ellipse(surf, GREEN, (22, 4, 14, 12))
    return surf


def create_tree():
    surf = pygame.Surface((64, 96), pygame.SRCALPHA)
    pygame.draw.rect(surf, DARK_BROWN, (26, 48, 12, 48))
    pygame.draw.rect(surf, BROWN, (28, 48, 4, 48))
    pygame.draw.ellipse(surf, DARK_GREEN, (0, 0, 64, 56))
    pygame.draw.ellipse(surf, FOREST_GREEN, (8, 8, 48, 40))
    pygame.draw.ellipse(surf, GREEN, (16, 12, 32, 28))
    return surf


def create_explosion_frame(frame):
    size = 16 + frame * 12
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    if frame < 2:
        pygame.draw.circle(surf, YELLOW, (center, center), size // 2)
        pygame.draw.circle(surf, ORANGE, (center, center), size // 3)
        pygame.draw.circle(surf, RED, (center, center), size // 5)
    elif frame < 4:
        pygame.draw.circle(surf, ORANGE, (center, center), size // 2)
        pygame.draw.circle(surf, RED, (center, center), size // 3)
        pygame.draw.circle(surf, DARK_RED, (center, center), size // 5)
    else:
        pygame.draw.circle(surf, RED, (center, center), size // 2)
        pygame.draw.circle(surf, DARK_RED, (center, center), size // 3)
    return surf


def create_wall_tile():
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.rect(surf, GRAY, (0, 0, 32, 32))
    pygame.draw.rect(surf, DARK_GRAY, (0, 0, 32, 1))
    pygame.draw.rect(surf, DARK_GRAY, (0, 15, 32, 2))
    pygame.draw.rect(surf, DARK_GRAY, (0, 0, 1, 32))
    pygame.draw.rect(surf, DARK_GRAY, (15, 0, 2, 16))
    pygame.draw.rect(surf, DARK_GRAY, (16, 16, 2, 16))
    return surf


def create_fortress():
    surf = pygame.Surface((128, 160), pygame.SRCALPHA)
    pygame.draw.rect(surf, GRAY, (0, 40, 128, 120))
    pygame.draw.rect(surf, DARK_GRAY, (0, 40, 128, 4))
    for i in range(0, 128, 16):
        pygame.draw.rect(surf, DARK_GRAY, (i, 36, 12, 8))
    pygame.draw.rect(surf, DARK_GRAY, (50, 100, 28, 60))
    pygame.draw.rect(surf, BLACK, (54, 104, 20, 20))
    pygame.draw.rect(surf, RED, (56, 106, 4, 4))
    pygame.draw.rect(surf, RED, (68, 106, 4, 4))
    for i in range(0, 128, 16):
        pygame.draw.rect(surf, DARK_GRAY, (i, 38, 2, 2))
    return surf
