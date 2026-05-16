import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import *
from game import Game


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.selected_option = 0
        self.options = ['NORMAL MODE', 'HELL MODE', 'QUIT']
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 72)

    def draw(self):
        self.screen.fill(BLUE_SKY)

        title_text = self.title_font.render('CONTRA', True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)

        subtitle_text = self.small_font.render('FC STYLE SHOOTING GAME', True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)

        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 70))
            self.screen.blit(text, rect)

            if i == self.selected_option:
                arrow = self.font.render('>', True, YELLOW)
                self.screen.blit(arrow, (rect.x - 50, rect.y))
                arrow = self.font.render('<', True, YELLOW)
                self.screen.blit(arrow, (rect.right + 20, rect.y))

        controls_title = self.small_font.render('CONTROLS:', True, YELLOW)
        self.screen.blit(controls_title, (50, 400))

        controls = [
            'W - Look Up',
            'A - Move Left',
            'S - Crouch / Look Down',
            'D - Move Right',
            'J - Shoot',
            'K - Jump',
            'ESC - Pause'
        ]

        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            self.screen.blit(text, (50, 430 + i * 22))

        mode_desc_title = self.small_font.render('MODE DIFFERENCES:', True, YELLOW)
        self.screen.blit(mode_desc_title, (400, 400))

        mode_descs = [
            'NORMAL:',
            '  Enemy speed: 1.5x',
            '  Spawn interval: 2s',
            '  Max enemies: 4',
            '',
            'HELL:',
            '  Enemy speed: 3x',
            '  Spawn interval: 0.8s',
            '  Max enemies: 8'
        ]

        for i, desc in enumerate(mode_descs):
            text = self.small_font.render(desc, True, WHITE)
            self.screen.blit(text, (400, 430 + i * 22))

        pygame.display.flip()

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.selected_option == 0:
                        return MODE_NORMAL
                    elif self.selected_option == 1:
                        return MODE_HELL
                    elif self.selected_option == 2:
                        return 'quit'
        return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Contra - FC Style Shooting Game')
    clock = pygame.time.Clock()

    menu = Menu(screen)
    game = None
    state = 'menu'

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if state == 'menu':
            result = menu.handle_input(events)
            if result == 'quit':
                running = False
            elif result in [MODE_NORMAL, MODE_HELL]:
                game = Game(screen, result)
                state = 'playing'
            menu.draw()

        elif state == 'playing':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if game.game_over or game.game_won:
                        if event.key == pygame.K_r:
                            game.restart()
                        elif event.key == pygame.K_m:
                            state = 'menu'

            keys = pygame.key.get_pressed()
            game.handle_events(events)
            game.update(keys)
            game.draw()
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
