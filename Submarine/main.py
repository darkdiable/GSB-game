import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.engine import GameEngine
from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    pygame.init()
    pygame.display.set_caption("潜艇大战 - Submarine Battle")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    try:
        icon_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.ellipse(icon_surf, (50, 100, 150), (4, 10, 28, 14))
        pygame.draw.rect(icon_surf, (60, 110, 160), (14, 4, 8, 10))
        pygame.display.set_icon(icon_surf)
    except:
        pass

    engine = GameEngine(screen)
    engine.run()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
