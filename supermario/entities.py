# -*- coding: utf-8 -*-
"""
实体类模块 - 定义游戏中的所有实体对象
包含：地面、砖块、问号方块、管道、金币、蘑菇怪
"""

import pygame
import random
from constants import *


class Entity:
    """实体基类"""

    def __init__(self, x, y, width, height, entity_type):
        """
        初始化实体

        Args:
            x, y: 位置坐标
            width, height: 尺寸
            entity_type: 实体类型
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.entity_type = entity_type
        self.active = True  # 是否活跃（未被销毁或收集）

    def update(self, *args):
        """更新实体状态"""
        pass

    def draw(self, screen, camera_x=0):
        """
        绘制实体

        Args:
            screen: 游戏屏幕
            camera_x: 摄像机X坐标
        """
        pass


class Ground(Entity):
    """地面类"""

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, TYPE_GROUND)

    def draw(self, screen, camera_x=0):
        """绘制地面"""
        draw_x = int(self.x - camera_x)
        # 地面主体
        pygame.draw.rect(screen, (139, 90, 43),
                         (draw_x, self.y, self.width, self.height))
        # 草地顶部
        pygame.draw.rect(screen, GREEN,
                         (draw_x, self.y, self.width, 10))
        # 纹理线条
        for i in range(0, self.width, 20):
            pygame.draw.line(screen, (100, 60, 20),
                           (draw_x + i, self.y + 15),
                           (draw_x + i, self.y + self.height))


class Brick(Entity):
    """砖块类 - 可以被顶破"""

    def __init__(self, x, y):
        super().__init__(x, y, BRICK_SIZE, BRICK_SIZE, TYPE_BRICK)
        self.breaking = False
        self.break_timer = 0
        self.particles = []

    def hit(self):
        """被玩家从下方顶到"""
        self.breaking = True
        self.break_timer = 20
        # 生成碎片粒子
        for i in range(8):
            self.particles.append({
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-8, -3),
                'life': 30
            })

    def update(self):
        """更新砖块状态"""
        if self.breaking:
            self.break_timer -= 1
            # 更新粒子
            for particle in self.particles:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.5
                particle['life'] -= 1
            # 移除死亡粒子
            self.particles = [p for p in self.particles if p['life'] > 0]
            if self.break_timer <= 0 and not self.particles:
                self.active = False

    def draw(self, screen, camera_x=0):
        """绘制砖块"""
        draw_x = int(self.x - camera_x)
        if self.breaking:
            # 绘制碎片粒子
            for particle in self.particles:
                pygame.draw.rect(screen, (180, 100, 50),
                               (int(particle['x'] - camera_x), int(particle['y']), 8, 8))
        else:
            # 绘制砖块
            pygame.draw.rect(screen, (180, 100, 50),
                           (draw_x, self.y, self.width, self.height))
            # 砖块纹理
            pygame.draw.rect(screen, (140, 70, 30),
                           (draw_x, self.y, self.width, self.height), 2)
            # 砖缝
            pygame.draw.line(screen, (140, 70, 30),
                           (draw_x + self.width // 2, self.y),
                           (draw_x + self.width // 2, self.y + self.height // 2))
            pygame.draw.line(screen, (140, 70, 30),
                           (draw_x, self.y + self.height // 2),
                           (draw_x + self.width, self.y + self.height // 2))


class QuestionBlock(Entity):
    """问号方块类 - 顶出金币"""

    def __init__(self, x, y):
        super().__init__(x, y, QUESTION_SIZE, QUESTION_SIZE, TYPE_QUESTION)
        self.has_coin = True  # 是否还有金币
        self.hit_animation = 0
        self.original_y = y
        self.bounce_offset = 0

    def hit(self):
        """被玩家从下方顶到"""
        if self.has_coin:
            self.has_coin = False
            self.hit_animation = 15
            return True  # 产生金币
        return False

    def update(self):
        """更新问号方块状态"""
        if self.hit_animation > 0:
            self.hit_animation -= 1
            # 弹跳动画
            progress = self.hit_animation / 15
            self.bounce_offset = int(-10 * (1 - progress) * progress * 4)
        else:
            self.bounce_offset = 0

    def draw(self, screen, camera_x=0):
        """绘制问号方块"""
        draw_x = int(self.x - camera_x)
        draw_y = self.y + self.bounce_offset

        if self.has_coin:
            # 有金币时的问号方块
            pygame.draw.rect(screen, YELLOW,
                           (draw_x, draw_y, self.width, self.height))
            pygame.draw.rect(screen, ORANGE,
                           (draw_x, draw_y, self.width, self.height), 3)
            # 绘制问号
            font = pygame.font.Font(None, 32)
            text = font.render("?", True, BLACK)
            text_rect = text.get_rect(center=(draw_x + self.width // 2,
                                            draw_y + self.height // 2))
            screen.blit(text, text_rect)
        else:
            # 空方块
            pygame.draw.rect(screen, (180, 140, 0),
                           (draw_x, draw_y, self.width, self.height))
            pygame.draw.rect(screen, (120, 90, 0),
                           (draw_x, draw_y, self.width, self.height), 3)


class Pipe(Entity):
    """管道类"""

    def __init__(self, x, y):
        super().__init__(x, y, PIPE_WIDTH, PIPE_HEIGHT, TYPE_PIPE)

    def draw(self, screen, camera_x=0):
        """绘制管道"""
        draw_x = int(self.x - camera_x)
        # 管道主体
        pygame.draw.rect(screen, GREEN,
                        (draw_x + 10, self.y + 20,
                         self.width - 20, self.height - 20))
        # 管道顶部
        pygame.draw.rect(screen, GREEN,
                        (draw_x, self.y, self.width, 25))
        # 管道边框
        pygame.draw.rect(screen, DARK_GREEN,
                        (draw_x + 10, self.y + 20,
                         self.width - 20, self.height - 20), 3)
        pygame.draw.rect(screen, DARK_GREEN,
                        (draw_x, self.y, self.width, 25), 3)
        # 高光
        pygame.draw.rect(screen, (100, 200, 100),
                        (draw_x + 15, self.y + 25, 8, self.height - 30))


class Coin(Entity):
    """金币类"""

    def __init__(self, x, y, is_animation=False):
        """
        初始化金币

        Args:
            x, y: 位置坐标
            is_animation: 是否为弹出动画的金币
        """
        super().__init__(x, y, COIN_SIZE, COIN_SIZE, TYPE_COIN)
        self.collected = False
        self.animation_timer = random.randint(0, 60)
        self.is_animation = is_animation
        self.animation_velocity = -12 if is_animation else 0
        self.animation_life = 40 if is_animation else 99999

    def update(self):
        """更新金币状态"""
        self.animation_timer += 1
        if self.is_animation:
            self.y += self.animation_velocity
            self.animation_velocity += 0.8
            self.animation_life -= 1
            self.rect.y = int(self.y)
            if self.animation_life <= 0:
                self.active = False

    def draw(self, screen, camera_x=0):
        """绘制金币"""
        if not self.active or self.collected:
            return
        draw_x = int(self.x - camera_x)
        # 金币旋转动画
        rotation = int(self.animation_timer / 5) % 4
        widths = [self.width, self.width * 0.7, self.width * 0.3, self.width * 0.7]
        current_width = int(widths[rotation])
        offset_x = (self.width - current_width) // 2

        # 金币主体
        pygame.draw.ellipse(screen, YELLOW,
                          (draw_x + offset_x, self.y,
                           current_width, self.height))
        # 金币高光
        pygame.draw.ellipse(screen, (255, 255, 150),
                          (draw_x + offset_x + 2, self.y + 5,
                           max(2, current_width // 3), self.height // 3))
        # 金币边框
        pygame.draw.ellipse(screen, ORANGE,
                          (draw_x + offset_x, self.y,
                           current_width, self.height), 2)

    def collect(self):
        """收集金币"""
        self.collected = True
        self.active = False


class Enemy(Entity):
    """蘑菇怪类 - 敌人"""

    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_WIDTH, ENEMY_HEIGHT, TYPE_ENEMY)
        self.direction = -1  # 移动方向，-1向左，1向右
        self.velocity_y = 0
        self.squashed = False  # 是否被踩扁
        self.squash_timer = 0
        self.alive = True

    def update(self, platforms=None):
        """
        更新敌人状态

        Args:
            platforms: 平台列表（用于碰撞检测）
        """
        if not self.alive or not self.active:
            return

        if self.squashed:
            self.squash_timer -= 1
            if self.squash_timer <= 0:
                self.active = False
            return

        # 水平移动
        self.x += self.direction * ENEMY_SPEED

        # 重力
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        self.y += self.velocity_y

        # 平台碰撞检测
        if platforms:
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

            for platform in platforms:
                if not platform.active:
                    continue
                if self.rect.colliderect(platform.rect):
                    # 检查与平台的相对位置
                    if self.velocity_y > 0 and self.rect.bottom > platform.rect.top:
                        self.y = platform.rect.top - self.height
                        self.velocity_y = 0
                        self.rect.y = int(self.y)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def change_direction(self):
        """改变移动方向"""
        self.direction *= -1

    def squash(self):
        """被玩家踩扁"""
        self.squashed = True
        self.squash_timer = 30
        self.height = 15
        self.y += 20
        self.rect.height = 15
        self.rect.y = int(self.y)

    def draw(self, screen, camera_x=0):
        """绘制蘑菇怪"""
        if not self.active:
            return
        draw_x = int(self.x - camera_x)

        if self.squashed:
            # 被踩扁的状态
            pygame.draw.ellipse(screen, (139, 69, 19),
                              (draw_x, self.y + 10,
                               self.width, self.height - 10))
            pygame.draw.ellipse(screen, (100, 50, 10),
                              (draw_x, self.y + 10,
                               self.width, self.height - 10), 2)
        else:
            # 身体
            pygame.draw.ellipse(screen, (139, 69, 19),
                              (draw_x, self.y, self.width, self.height))
            # 身体高光
            pygame.draw.ellipse(screen, (160, 80, 30),
                              (draw_x + 5, self.y + 5,
                               self.width - 20, self.height // 3))
            # 白色眼睛
            pygame.draw.ellipse(screen, WHITE,
                              (draw_x + 8, self.y + 10, 10, 12))
            pygame.draw.ellipse(screen, WHITE,
                              (draw_x + 20, self.y + 10, 10, 12))
            # 黑色瞳孔
            pupil_x = 13 if self.direction > 0 else 11
            pygame.draw.ellipse(screen, BLACK,
                              (draw_x + pupil_x, self.y + 14, 4, 6))
            pygame.draw.ellipse(screen, BLACK,
                              (draw_x + pupil_x + 12, self.y + 14, 4, 6))
            # 愤怒的眉毛
            pygame.draw.line(screen, BLACK,
                           (draw_x + 6, self.y + 8),
                           (draw_x + 16, self.y + 12), 2)
            pygame.draw.line(screen, BLACK,
                           (draw_x + 22, self.y + 12),
                           (draw_x + 32, self.y + 8), 2)
            # 脚
            pygame.draw.ellipse(screen, (100, 50, 10),
                              (draw_x + 2, self.y + self.height - 10,
                               12, 10))
            pygame.draw.ellipse(screen, (100, 50, 10),
                              (draw_x + self.width - 14, self.y + self.height - 10,
                               12, 10))