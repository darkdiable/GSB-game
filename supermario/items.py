import pygame
import math
from constants import *


class Coin:
    """金币类"""

    def __init__(self, x, y, is_spawning=False):
        self.x = x
        self.y = y
        self.width = COIN_SIZE
        self.height = COIN_SIZE
        self.active = True
        self.is_spawning = is_spawning
        self.vel_y = COIN_SPAWN_SPEED if is_spawning else 0
        self.anim_frame = 0
        self.rotation_angle = 0
        self.collected = False
        self.collect_animation = 0

    def update(self, solids):
        """更新金币"""
        if self.collected:
            self.collect_animation += 1
            if self.collect_animation > 20:
                self.active = False
            return

        self.anim_frame = (self.anim_frame + 1) % 30
        self.rotation_angle = (self.rotation_angle + 8) % 360

        if self.is_spawning:
            # 从问号砖中弹出的动画
            self.vel_y += GRAVITY * 0.5
            self.y += self.vel_y

            # 检查是否落地
            coin_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            for solid in solids:
                if coin_rect.colliderect(solid) and self.vel_y > 0:
                    self.y = solid.top - self.height
                    self.vel_y = 0
                    self.is_spawning = False
                    break
        else:
            # 普通金币的上下浮动
            self.y += 0.5 * math.sin(pygame.time.get_ticks() * 0.005 + self.x * 0.1)

    def collect(self):
        """收集金币"""
        if not self.collected:
            self.collected = True
            return COIN_SCORE
        return 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_x):
        if not self.active:
            return

        draw_x = self.x - camera_x
        draw_y = self.y

        if self.collected:
            # 收集动画 - 向上飘动并淡出
            alpha = 255 - self.collect_animation * 12
            scale = 1 + self.collect_animation * 0.05
            current_size = int(self.width * scale)
            offset_y = self.collect_animation * -2

            coin_surface = pygame.Surface((current_size, current_size), pygame.SRCALPHA)

            # 绘制金币
            pygame.draw.circle(coin_surface, GOLD, (current_size // 2, current_size // 2), current_size // 2)
            pygame.draw.circle(coin_surface, YELLOW, (current_size // 2 - 2, current_size // 2 - 2), current_size // 2 - 4)

            # $符号
            font = pygame.font.Font(None, int(current_size * 0.7))
            text = font.render('$', True, DARK_BROWN)
            text_rect = text.get_rect(center=(current_size // 2, current_size // 2))
            coin_surface.blit(text, text_rect)

            coin_surface.set_alpha(alpha)
            screen.blit(coin_surface, (draw_x - (current_size - self.width) // 2, draw_y + offset_y))

            # 显示得分
            if self.collect_animation < 15:
                score_font = pygame.font.Font(FONT_PATH, 20)
                score_text = score_font.render(f'+{COIN_SCORE}', True, YELLOW)
                score_rect = score_text.get_rect(center=(draw_x + self.width // 2, draw_y - 20 - self.collect_animation))
                score_text.set_alpha(alpha)
                screen.blit(score_text, score_rect)
        else:
            # 正常绘制 - 带旋转压扁效果
            scale_x = abs(math.cos(self.rotation_angle * math.pi / 180))
            current_width = max(4, int(self.width * scale_x))
            offset_x = (self.width - current_width) // 2

            # 金币主体
            pygame.draw.ellipse(screen, GOLD, (draw_x + offset_x, draw_y, current_width, self.height))
            pygame.draw.ellipse(screen, YELLOW, (draw_x + offset_x + 2, draw_y + 2,
                                                max(2, current_width - 4), self.height - 4))

            # 高光
            if current_width > 10:
                pygame.draw.ellipse(screen, WHITE, (draw_x + offset_x + 4, draw_y + 4,
                                                    max(2, current_width // 4), self.height // 4))

            # $符号（仅在金币正对时显示）
            if scale_x > 0.5:
                font = pygame.font.Font(None, 18)
                text = font.render('$', True, DARK_BROWN)
                text.set_alpha(int(255 * (scale_x - 0.5) * 2))
                text_rect = text.get_rect(center=(draw_x + self.width // 2, draw_y + self.height // 2))
                screen.blit(text, text_rect)
