import pygame
import sys
from game.engine import GameEngine
from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    pygame.init()
    pygame.display.set_caption("1942 Dogfight")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    engine = GameEngine(screen)
    engine.run()
    sys.exit()


if __name__ == '__main__':
    main()
