import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game


def main():
    pygame.init()
    pygame.display.set_caption("网球对战游戏")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    game = Game(screen)
    game.run()


if __name__ == "__main__":
    main()
