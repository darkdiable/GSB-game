import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game


def main():
    pygame.init()
    pygame.display.set_caption("Contra - Jungle Mission")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(screen)
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
