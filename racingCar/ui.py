import pygame
from config import *


class UIManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.collision_flash_timer = 0

    def update(self, player_speed, player_collisions):
        self.score += int(player_speed)
        if self.collision_flash_timer > 0:
            self.collision_flash_timer -= 1

    def draw(self, screen, player):
        self._draw_hud(screen, player)
        self._draw_hearts(screen, player.collisions)

        if self.collision_flash_timer > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((255, 0, 0, 50))
            screen.blit(flash_surface, (0, 0))

    def _draw_hud(self, screen, player):
        hud_rect = pygame.Rect(10, 10, 200, 100)
        pygame.draw.rect(screen, (0, 0, 0, 180), hud_rect, border_radius=10)

        score_text = FONT_MEDIUM.render(f'{self.score}', True, COLORS['text'])
        screen.blit(score_text, (20, 20))

        score_label = FONT_SMALL.render('分数', True, COLORS['text'])
        screen.blit(score_label, (20, 65))

        speed_text = FONT_SMALL.render(f'速度: {int(player.speed * 20)} km/h', True, COLORS['text'])
        screen.blit(speed_text, (20, 90))

    def _draw_hearts(self, screen, collisions):
        hearts_x = SCREEN_WIDTH - 180
        hearts_y = 20

        hud_rect = pygame.Rect(hearts_x - 10, 10, 170, 50)
        pygame.draw.rect(screen, (0, 0, 0, 180), hud_rect, border_radius=10)

        for i in range(MAX_COLLISIONS):
            heart_x = hearts_x + i * 30
            if i < MAX_COLLISIONS - collisions:
                self._draw_heart(screen, heart_x, hearts_y, (255, 0, 0))
            else:
                self._draw_heart(screen, heart_x, hearts_y, (80, 80, 80))

    def _draw_heart(self, screen, x, y, color):
        pygame.draw.circle(screen, color, (x + 8, y + 8), 8)
        pygame.draw.circle(screen, color, (x + 22, y + 8), 8)
        points = [
            (x, y + 10),
            (x + 15, y + 30),
            (x + 30, y + 10)
        ]
        pygame.draw.polygon(screen, color, points)

    def show_start_screen(self, screen):
        screen.fill((0, 0, 0))

        title_text = FONT_LARGE.render('赛车游戏', True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)

        subtitle_text = FONT_MEDIUM.render('Racing Car', True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80))
        screen.blit(subtitle_text, subtitle_rect)

        controls_text = [
            '控制说明:',
            'W - 加速',
            'S - 减速 (长按刹车)',
            'A - 向左移动',
            'D - 向右移动',
            '',
            '碰撞5次游戏结束',
            '',
            '按任意键开始游戏'
        ]

        for i, line in enumerate(controls_text):
            text = FONT_SMALL.render(line, True, COLORS['text'])
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 30))
            screen.blit(text, text_rect)

        pygame.display.flip()

    def show_game_over_screen(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        game_over_text = FONT_LARGE.render('游戏结束', True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(game_over_text, game_over_rect)

        score_text = FONT_MEDIUM.render(f'最终分数: {self.score}', True, COLORS['text'])
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_text, score_rect)

        if self.score > self.high_score:
            self.high_score = self.score
            new_record_text = FONT_MEDIUM.render('新纪录!', True, (255, 215, 0))
            new_record_rect = new_record_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(new_record_text, new_record_rect)

        high_score_text = FONT_SMALL.render(f'最高分: {self.high_score}', True, COLORS['text'])
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(high_score_text, high_score_rect)

        restart_text = FONT_SMALL.render('按 R 键重新开始', True, COLORS['text'])
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def notify_collision(self):
        self.collision_flash_timer = 20

    def reset(self):
        self.score = 0
        self.collision_flash_timer = 0
