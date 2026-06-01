import pygame
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import *
from game import Game


class Menu:
    """菜单类"""

    def __init__(self, screen):
        self.screen = screen
        self.selected_option = 0
        self.options = ['开始游戏', '退出游戏']
        self.font = pygame.font.Font(FONT_PATH, 48)
        self.small_font = pygame.font.Font(FONT_PATH, 24)
        self.title_font = pygame.font.Font(FONT_PATH, 72)
        self.anim_frame = 0

    def draw(self):
        """绘制菜单"""
        self._draw_background()
        self._draw_title()
        self._draw_menu()
        self._draw_controls()

        pygame.display.flip()

    def _draw_background(self):
        """绘制背景"""
        for y in range(SCREEN_HEIGHT - GROUND_HEIGHT):
            t = y / (SCREEN_HEIGHT - GROUND_HEIGHT)
            r = int(SKY_BLUE[0] * (1 - t) + DEEP_SKY_BLUE[0] * t)
            g = int(SKY_BLUE[1] * (1 - t) + DEEP_SKY_BLUE[1] * t)
            b = int(SKY_BLUE[2] * (1 - t) + DEEP_SKY_BLUE[2] * t)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        cloud_x = (pygame.time.get_ticks() // 50) % (SCREEN_WIDTH + 200) - 100
        self._draw_cloud(cloud_x, 80, 1.2)
        self._draw_cloud((cloud_x + 400) % (SCREEN_WIDTH + 200) - 100, 150, 1.0)
        self._draw_cloud((cloud_x + 700) % (SCREEN_WIDTH + 200) - 100, 60, 0.8)

        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        pygame.draw.rect(self.screen, DARK_BROWN, (0, ground_y, SCREEN_WIDTH, GROUND_HEIGHT))
        pygame.draw.rect(self.screen, FOREST_GREEN, (0, ground_y, SCREEN_WIDTH, 12))

        for i in range(0, SCREEN_WIDTH, 16):
            pygame.draw.rect(self.screen, LIME_GREEN, (i, ground_y, 8, 6))

        hill_x = 150
        pygame.draw.ellipse(self.screen, FOREST_GREEN, (hill_x, ground_y - 80, 200, 100))
        pygame.draw.ellipse(self.screen, LIME_GREEN, (hill_x + 10, ground_y - 75, 180, 90))

        hill_x2 = 550
        pygame.draw.ellipse(self.screen, FOREST_GREEN, (hill_x2, ground_y - 60, 160, 80))
        pygame.draw.ellipse(self.screen, LIME_GREEN, (hill_x2 + 8, ground_y - 55, 144, 70))

        self._draw_mario_preview(380, ground_y - 80)

    def _draw_cloud(self, x, y, size):
        """绘制云朵"""
        base_radius = int(20 * size)
        pygame.draw.circle(self.screen, WHITE, (x, y), base_radius)
        pygame.draw.circle(self.screen, WHITE, (x + base_radius, y - base_radius // 2), base_radius)
        pygame.draw.circle(self.screen, WHITE, (x + base_radius * 2, y), base_radius)
        pygame.draw.circle(self.screen, WHITE, (x + base_radius // 2, y - base_radius // 3), int(base_radius * 0.8))
        pygame.draw.circle(self.screen, WHITE, (x + base_radius * 1.5, y - base_radius // 3), int(base_radius * 0.8))

    def _draw_mario_preview(self, x, y):
        """绘制预览马里奥"""
        bounce = int(5 * math.sin(pygame.time.get_ticks() * 0.005))
        y -= bounce

        pygame.draw.rect(self.screen, RED, (x + 4, y + 0, 24, 8))
        pygame.draw.rect(self.screen, RED, (x + 8, y + 4, 20, 4))
        pygame.draw.rect(self.screen, DARK_RED, (x + 4, y + 6, 24, 2))
        pygame.draw.rect(self.screen, RED, (x + 2, y + 8, 28, 4))
        pygame.draw.rect(self.screen, SKIN, (x + 8, y + 12, 16, 12))
        pygame.draw.rect(self.screen, BLACK, (x + 18, y + 14, 4, 4))
        pygame.draw.rect(self.screen, BLACK, (x + 10, y + 14, 4, 4))
        pygame.draw.rect(self.screen, BROWN, (x + 10, y + 20, 14, 3))
        pygame.draw.rect(self.screen, BLUE, (x + 6, y + 24, 20, 16))
        pygame.draw.rect(self.screen, RED, (x + 4, y + 24, 24, 8))
        pygame.draw.circle(self.screen, YELLOW, (x + 10, y + 32), 2)
        pygame.draw.circle(self.screen, YELLOW, (x + 22, y + 32), 2)
        pygame.draw.rect(self.screen, RED, (x + 0, y + 24, 6, 8))
        pygame.draw.rect(self.screen, RED, (x + 26, y + 24, 6, 8))
        pygame.draw.rect(self.screen, SKIN, (x + 0, y + 30, 6, 4))
        pygame.draw.rect(self.screen, SKIN, (x + 26, y + 30, 6, 4))
        pygame.draw.rect(self.screen, BLUE, (x + 6, y + 40, 8, 8))
        pygame.draw.rect(self.screen, BROWN, (x + 4, y + 44, 12, 4))
        pygame.draw.rect(self.screen, BLUE, (x + 18, y + 40, 8, 8))
        pygame.draw.rect(self.screen, BROWN, (x + 16, y + 44, 12, 4))

    def _draw_title(self):
        """绘制标题"""
        title_offset = int(5 * math.sin(pygame.time.get_ticks() * 0.003))

        title_bg = self.title_font.render('超级玛丽', True, DARK_RED)
        title_bg_rect = title_bg.get_rect(center=(SCREEN_WIDTH // 2 + 4, 120 + title_offset + 4))
        self.screen.blit(title_bg, title_bg_rect)

        title_text = self.title_font.render('超级玛丽', True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120 + title_offset))
        self.screen.blit(title_text, title_rect)

        subtitle_text = self.font.render('Super Mario', True, YELLOW)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 190))
        self.screen.blit(subtitle_text, subtitle_rect)

    def _draw_menu(self):
        """绘制菜单选项"""
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = YELLOW
                scale = 1.1
            else:
                color = WHITE
                scale = 1.0

            text = self.font.render(option, True, color)
            text = pygame.transform.scale(text, (int(text.get_width() * scale), int(text.get_height() * scale)))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 350 + i * 70))
            self.screen.blit(text, rect)

            if i == self.selected_option:
                arrow_y = rect.y + rect.height // 2 - 15
                arrow1 = self.font.render('▶', True, YELLOW)
                self.screen.blit(arrow1, (rect.x - 50, arrow_y))
                arrow2 = self.font.render('◀', True, YELLOW)
                self.screen.blit(arrow2, (rect.right + 20, arrow_y))

    def _draw_controls(self):
        """绘制操作说明"""
        controls_title = self.small_font.render('操作说明', True, YELLOW)
        controls_rect = controls_title.get_rect(center=(SCREEN_WIDTH // 2, 480))
        self.screen.blit(controls_title, controls_rect)

        controls = [
            ('← → 方向键', '左右移动'),
            ('空格键 / ↑', '跳跃'),
            ('顶问号砖', '获得金币'),
            ('踩蘑菇怪', '消灭敌人'),
        ]

        for i, (key, action) in enumerate(controls):
            key_text = self.small_font.render(key, True, YELLOW)
            action_text = self.small_font.render(action, True, WHITE)
            self.screen.blit(key_text, (200, 510 + i * 25))
            self.screen.blit(action_text, (400, 510 + i * 25))

    def handle_input(self, events):
        """处理菜单输入"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.selected_option == 0:
                        return 'start'
                    elif self.selected_option == 1:
                        return 'quit'
        return None


def main():
    """主函数"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('超级玛丽 - Super Mario')
    clock = pygame.time.Clock()

    menu = Menu(screen)
    game = None
    state = STATE_MENU

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if state == STATE_MENU:
            result = menu.handle_input(events)
            if result == 'quit':
                running = False
            elif result == 'start':
                game = Game(screen)
                state = STATE_PLAYING
            menu.draw()

        elif state == STATE_PLAYING:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if game.game_over or game.win:
                        if event.key == pygame.K_r:
                            game.restart()
                        elif event.key == pygame.K_m:
                            state = STATE_MENU

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
