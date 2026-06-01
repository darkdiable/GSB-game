import pygame
import math
from constants import *


class Enemy:
    """敌人类 - 蘑菇仔（Goomba）"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.vel_x = -ENEMY_SPEED
        self.vel_y = 0
        self.gravity = ENEMY_GRAVITY
        self.active = True
        self.is_dead = False
        self.death_timer = 0
        self.anim_frame = 0
        self.direction = -1
        self.squished = False

    def update(self, solids):
        """更新敌人状态"""
        if self.squished:
            self.death_timer += 1
            if self.death_timer > 30:
                self.active = False
            return

        self.anim_frame = (self.anim_frame + 1) % 40

        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10

        self.x += self.vel_x
        self._check_horizontal_collisions(solids)

        self.y += self.vel_y
        self._check_vertical_collisions(solids)

        if self.y > SCREEN_HEIGHT + 100:
            self.active = False

    def _check_horizontal_collisions(self, solids):
        """水平碰撞检测"""
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for solid in solids:
            if enemy_rect.colliderect(solid):
                if self.vel_x > 0:
                    self.x = solid.left - self.width
                elif self.vel_x < 0:
                    self.x = solid.right
                self.vel_x = -self.vel_x
                self.direction = -self.direction
                enemy_rect.x = self.x

    def _check_vertical_collisions(self, solids):
        """垂直碰撞检测"""
        enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for solid in solids:
            if enemy_rect.colliderect(solid):
                if self.vel_y > 0:
                    self.y = solid.top - self.height
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.y = solid.bottom
                    self.vel_y = 0
                enemy_rect.y = self.y

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_stomp_rect(self):
        """踩踏检测区域（玩家从上往下踩）"""
        return pygame.Rect(self.x, self.y, self.width, self.height // 2)

    def stomp(self):
        """被踩踏"""
        if not self.squished:
            self.squished = True
            self.vel_x = 0
            self.death_timer = 0
            return True
        return False

    def draw(self, screen, camera_x):
        """绘制蘑菇仔"""
        if not self.active:
            return

        draw_x = int(self.x - camera_x)
        draw_y = int(self.y)

        if self.squished:
            self._draw_squished(screen, draw_x, draw_y)
        else:
            self._draw_goomba(screen, draw_x, draw_y)

    def _draw_goomba(self, screen, x, y):
        """绘制正常状态的蘑菇仔"""
        walk_offset = int(2 * math.sin(self.anim_frame * 0.3))

        # 身体
        pygame.draw.ellipse(screen, BROWN, (x, y + 8, self.width, self.height - 8))
        pygame.draw.ellipse(screen, LIGHT_BROWN, (x + 2, y + 10, self.width - 4, self.height - 12))

        # 头部
        pygame.draw.ellipse(screen, LIGHT_BROWN, (x + 2, y, self.width - 4, self.height - 8))

        # 眼睛
        eye_offset = 4 if self.direction > 0 else -4
        pygame.draw.ellipse(screen, WHITE, (x + 6, y + 8, 8, 10))
        pygame.draw.ellipse(screen, WHITE, (x + 18, y + 8, 8, 10))

        # 瞳孔
        pygame.draw.circle(screen, BLACK, (x + 9 + eye_offset, y + 13), 3)
        pygame.draw.circle(screen, BLACK, (x + 21 + eye_offset, y + 13), 3)

        # 眉毛
        pygame.draw.line(screen, BLACK, (x + 4, y + 6), (x + 10, y + 8), 2)
        pygame.draw.line(screen, BLACK, (x + 22, y + 6), (x + 28, y + 8), 2)

        # 脚
        if walk_offset > 0:
            pygame.draw.ellipse(screen, DARK_BROWN, (x, y + self.height - 8, 12, 8))
            pygame.draw.ellipse(screen, DARK_BROWN, (x + 20, y + self.height - 10, 12, 10))
        else:
            pygame.draw.ellipse(screen, DARK_BROWN, (x, y + self.height - 10, 12, 10))
            pygame.draw.ellipse(screen, DARK_BROWN, (x + 20, y + self.height - 8, 12, 8))

        # 牙齿
        pygame.draw.rect(screen, WHITE, (x + 12, y + 20, 8, 3))
        pygame.draw.rect(screen, BLACK, (x + 14, y + 20, 2, 3))
        pygame.draw.rect(screen, BLACK, (x + 18, y + 20, 2, 3))

    def _draw_squished(self, screen, x, y):
        """绘制被踩扁的蘑菇仔"""
        alpha = 255 - int(self.death_timer * 8)
        if alpha < 0:
            alpha = 0

        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 扁扁的身体
        pygame.draw.ellipse(surf, BROWN, (0, self.height - 16, self.width, 16))
        pygame.draw.ellipse(surf, LIGHT_BROWN, (2, self.height - 14, self.width - 4, 12))

        # X 眼睛
        pygame.draw.line(surf, BLACK, (8, self.height - 10), (12, self.height - 6), 2)
        pygame.draw.line(surf, BLACK, (12, self.height - 10), (8, self.height - 6), 2)
        pygame.draw.line(surf, BLACK, (20, self.height - 10), (24, self.height - 6), 2)
        pygame.draw.line(surf, BLACK, (24, self.height - 10), (20, self.height - 6), 2)

        surf.set_alpha(alpha)
        screen.blit(surf, (x, y))
