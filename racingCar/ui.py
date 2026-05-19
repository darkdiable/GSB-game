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
        screen.fill((20, 20, 30))

        bg_rect = pygame.Rect(50, 40, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 80)
        pygame.draw.rect(screen, (30, 30, 45), bg_rect, border_radius=20)
        pygame.draw.rect(screen, (255, 100, 0), bg_rect, width=3, border_radius=20)

        title_text = FONT_LARGE.render('赛车游戏', True, (255, 50, 50))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title_text, title_rect)

        subtitle_text = FONT_MEDIUM.render('Racing Car', True, (255, 200, 100))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 190))
        screen.blit(subtitle_text, subtitle_rect)

        controls_title = FONT_MEDIUM.render('操作说明', True, (100, 200, 255))
        controls_title_rect = controls_title.get_rect(center=(SCREEN_WIDTH // 2, 260))
        screen.blit(controls_title, controls_title_rect)

        line_y = 295
        pygame.draw.line(screen, (100, 200, 255), (SCREEN_WIDTH // 2 - 100, line_y), (SCREEN_WIDTH // 2 + 100, line_y), 2)

        controls_text = [
            ('W', '加速'),
            ('S', '减速 (长按刹车)'),
            ('A', '向左移动'),
            ('D', '向右移动'),
        ]

        start_y = 330
        for i, (key, desc) in enumerate(controls_text):
            y = start_y + i * 45

            key_rect = pygame.Rect(SCREEN_WIDTH // 2 - 140, y - 15, 60, 35)
            pygame.draw.rect(screen, (255, 165, 0), key_rect, border_radius=8)
            key_text = FONT_SMALL.render(key, True, (0, 0, 0))
            key_text_rect = key_text.get_rect(center=key_rect.center)
            screen.blit(key_text, key_text_rect)

            desc_text = FONT_SMALL.render(desc, True, COLORS['text'])
            desc_rect = desc_text.get_rect(midleft=(SCREEN_WIDTH // 2 - 60, y))
            screen.blit(desc_text, desc_rect)

        rule_text = FONT_SMALL.render('规则：碰撞 5 次游戏结束', True, (255, 200, 100))
        rule_rect = rule_text.get_rect(center=(SCREEN_WIDTH // 2, 520))
        screen.blit(rule_text, rule_rect)

        start_text = FONT_MEDIUM.render('按任意键开始游戏', True, (50, 255, 100))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 560))
        screen.blit(start_text, start_rect)

        pygame.display.flip()

    def show_game_over_screen(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        screen.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(100, 80, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 160)
        pygame.draw.rect(screen, (40, 20, 20), panel_rect, border_radius=20)
        pygame.draw.rect(screen, (255, 50, 50), panel_rect, width=3, border_radius=20)

        game_over_text = FONT_LARGE.render('游戏结束', True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(game_over_text, game_over_rect)

        score_label = FONT_SMALL.render('最终分数', True, (200, 200, 200))
        score_label_rect = score_label.get_rect(center=(SCREEN_WIDTH // 2, 230))
        screen.blit(score_label, score_label_rect)

        score_text = FONT_LARGE.render(f'{self.score}', True, (255, 200, 100))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 290))
        screen.blit(score_text, score_rect)

        if self.score > self.high_score:
            self.high_score = self.score
            new_record_text = FONT_MEDIUM.render('🎉 新纪录!', True, (255, 215, 0))
            new_record_rect = new_record_text.get_rect(center=(SCREEN_WIDTH // 2, 360))
            screen.blit(new_record_text, new_record_rect)

        high_score_text = FONT_SMALL.render(f'最高分: {self.high_score}', True, (255, 200, 100))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 410))
        screen.blit(high_score_text, high_score_rect)

        restart_text = FONT_MEDIUM.render('按 R 键重新开始', True, (50, 255, 100))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 490))
        screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def notify_collision(self):
        self.collision_flash_timer = 20

    def reset(self):
        self.score = 0
        self.collision_flash_timer = 0
