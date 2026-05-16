import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import Game


def main():
    try:
        import pygame
    except ImportError:
        print("Error: pygame is not installed.")
        print("Please install it using: pip install pygame")
        sys.exit(1)

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
