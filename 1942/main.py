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
        self.options = ['普通模式', '困难模式', '退出游戏']
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.show_controls = False

    def draw(self):
        self._draw_background()
        self._draw_title()

        if self.show_controls:
            self._draw_controls()
        else:
            self._draw_menu()

        pygame.display.flip()

    def _draw_background(self):
        for y in range(SCREEN_HEIGHT // 2):
            color = (
                int(SKY_BLUE[0] * (1 - y / (SCREEN_HEIGHT // 2)) + OCEAN_BLUE[0] * (y / (SCREEN_HEIGHT // 2))),
                int(SKY_BLUE[1] * (1 - y / (SCREEN_HEIGHT // 2)) + OCEAN_BLUE[1] * (y / (SCREEN_HEIGHT // 2))),
                int(SKY_BLUE[2] * (1 - y / (SCREEN_HEIGHT // 2)) + OCEAN_BLUE[2] * (y / (SCREEN_HEIGHT // 2)))
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

        pygame.draw.rect(self.screen, OCEAN_BLUE, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))

        for i in range(5):
            y = SCREEN_HEIGHT // 2 + 30 + i * 60
            pygame.draw.line(self.screen, OCEAN_LIGHT, (0, y), (SCREEN_WIDTH, y), 1)

        pygame.draw.ellipse(self.screen, SAND, (50, SCREEN_HEIGHT - 120, 120, 60))
        pygame.draw.ellipse(self.screen, GREEN, (55, SCREEN_HEIGHT - 115, 110, 50))
        pygame.draw.ellipse(self.screen, DARK_GREEN, (65, SCREEN_HEIGHT - 110, 90, 40))

        pygame.draw.ellipse(self.screen, SAND, (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 150, 150, 80))
        pygame.draw.ellipse(self.screen, GREEN, (SCREEN_WIDTH - 165, SCREEN_HEIGHT - 145, 140, 70))
        pygame.draw.ellipse(self.screen, DARK_GREEN, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 135, 110, 55))
        pygame.draw.polygon(self.screen, BROWN, [
            (SCREEN_WIDTH - 95, SCREEN_HEIGHT - 130),
            (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 150),
            (SCREEN_WIDTH - 65, SCREEN_HEIGHT - 130)
        ])

        px, py = SCREEN_WIDTH // 2 - 40, 180
        pygame.draw.rect(self.screen, DARK_GRAY, (px + 25, py + 10, 30, 40))
        pygame.draw.rect(self.screen, GRAY, (px + 20, py + 15, 40, 30))
        pygame.draw.polygon(self.screen, DARK_GRAY, [
            (px + 40, py),
            (px + 30, py + 15),
            (px + 50, py + 15)
        ])
        pygame.draw.rect(self.screen, GRAY, (px, py + 20, 80, 8))
        pygame.draw.rect(self.screen, DARK_GRAY, (px + 5, py + 18, 70, 12))
        pygame.draw.rect(self.screen, GRAY, (px + 20, py + 35, 40, 20))
        for ex in [px + 8, px + 62]:
            pygame.draw.rect(self.screen, DARK_GRAY, (ex, py + 15, 10, 20))
            pygame.draw.rect(self.screen, DARK_GRAY, (ex, py + 40, 10, 15))
        pygame.draw.rect(self.screen, RED, (px + 38, py + 42, 4, 12))
        pygame.draw.rect(self.screen, RED, (px + 38, py + 42, 12, 4))

    def _draw_title(self):
        title_text = self.title_font.render('1942', True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)

        subtitle_text = self.subtitle_font.render('太平洋空战', True, YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 130))
        self.screen.blit(subtitle_text, subtitle_rect)

    def _draw_menu(self):
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 320 + i * 70))
            self.screen.blit(text, rect)

            if i == self.selected_option:
                arrow = self.font.render('>', True, YELLOW)
                self.screen.blit(arrow, (rect.x - 50, rect.y))
                arrow = self.font.render('<', True, YELLOW)
                self.screen.blit(arrow, (rect.right + 20, rect.y))

        hint_text = self.small_font.render('按 C 键查看操作说明', True, LIGHT_GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(hint_text, hint_rect)

    def _draw_controls(self):
        controls_title = self.font.render('操作说明', True, YELLOW)
        controls_rect = controls_title.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(controls_title, controls_rect)

        controls = [
            ('W / 上箭头', '向上移动'),
            ('S / 下箭头', '向下移动'),
            ('A / 左箭头', '向左移动'),
            ('D / 右箭头', '向右移动'),
            ('空格键', '发射机枪'),
            ('B 键', '投掷炸弹'),
            ('ESC 键', '暂停游戏'),
        ]

        for i, (key, action) in enumerate(controls):
            key_text = self.small_font.render(key, True, YELLOW)
            action_text = self.small_font.render(action, True, WHITE)
            self.screen.blit(key_text, (120, 330 + i * 30))
            self.screen.blit(action_text, (320, 330 + i * 30))

        enemy_title = self.small_font.render('敌人类型:', True, YELLOW)
        self.screen.blit(enemy_title, (120, 550))

        enemies = [
            ('战斗机', '用机枪击落 (+100 分)'),
            ('海军舰艇', '用炸弹摧毁 (+300 分)'),
            ('防空炮', '用炸弹摧毁 (+200 分)'),
            ('大型轰炸机', '用机枪击落 (+1000 分)'),
        ]

        for i, (enemy, desc) in enumerate(enemies):
            enemy_text = self.small_font.render(enemy + ':', True, ORANGE)
            desc_text = self.small_font.render(desc, True, WHITE)
            self.screen.blit(enemy_text, (120, 580 + i * 25))
            self.screen.blit(desc_text, (240, 580 + i * 25))

        back_text = self.small_font.render('按 C 键返回菜单', True, LIGHT_GRAY)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(back_text, back_rect)

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.show_controls:
                    if event.key == pygame.K_c:
                        self.show_controls = False
                else:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.selected_option == 0:
                            return MODE_NORMAL
                        elif self.selected_option == 1:
                            return MODE_HARD
                        elif self.selected_option == 2:
                            return 'quit'
                    elif event.key == pygame.K_c:
                        self.show_controls = True
        return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('1942 - 太平洋空战')
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
            elif result in [MODE_NORMAL, MODE_HARD]:
                game = Game(screen, result)
                state = 'playing'
            menu.draw()

        elif state == 'playing':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if game.game_over:
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
