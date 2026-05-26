# -*- coding: utf-8 -*-
"""
玩家角色模块 - 实现马里奥角色的移动、跳跃和碰撞检测
"""

import pygame
from constants import *
from entities import Coin


class Player:
    """玩家角色类 - 马里奥"""

    def __init__(self, x, y):
        """
        初始化玩家

        Args:
            x, y: 初始位置坐标
        """
        # 位置和尺寸
        self.x = float(x)
        self.y = float(y)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)

        # 速度
        self.velocity_x = 0
        self.velocity_y = 0

        # 状态
        self.on_ground = False
        self.facing = 1  # 1为右，-1为左
        self.lives = PLAYER_MAX_LIVES
        self.score = 0
        self.coins = 0

        # 无敌状态
        self.invincible = False
        self.invincible_timer = 0

        # 动画
        self.animation_timer = 0
        self.walk_frame = 0

        # 跳跃控制
        self.can_jump = True
        self.jump_hold_time = 0

    def handle_input(self, keys):
        """
        处理键盘输入

        Args:
            keys: 按键状态
        """
        # 水平移动
        self.velocity_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED
            self.facing = 1

        # 跳跃
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.can_jump:
            if self.on_ground:
                self.velocity_y = PLAYER_JUMP_FORCE
                self.on_ground = False
                self.can_jump = False
                self.jump_hold_time = 0
            elif self.jump_hold_time < 10 and self.velocity_y < 0:
                # 跳跃高度控制（长按跳更高）
                self.velocity_y -= 0.5
                self.jump_hold_time += 1

        # 松开跳跃键后重置
        if not (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
            self.can_jump = True
            self.jump_hold_time = 0

    def update(self, platforms, entities):
        """
        更新玩家状态

        Args:
            platforms: 平台列表（地面、砖块、管道等）
            entities: 所有实体列表

        Returns:
            dict: 包含事件信息的字典
        """
        events = {
            'coin_collected': False,
            'enemy_squashed': False,
            'brick_hit': None,
            'question_hit': None,
            'player_damaged': False,
            'player_died': False
        }

        # 更新无敌状态
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        # 应用重力
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED

        # 水平移动和碰撞检测
        self.x += self.velocity_x
        self.rect.x = int(self.x)
        self._check_horizontal_collision(platforms)

        # 垂直移动和碰撞检测
        self.y += self.velocity_y
        self.rect.y = int(self.y)
        self.on_ground = False

        hit_result = self._check_vertical_collision(platforms, entities)
        if hit_result:
            if hit_result['type'] == 'brick':
                events['brick_hit'] = hit_result['object']
            elif hit_result['type'] == 'question':
                events['question_hit'] = hit_result['object']

        # 检查金币收集
        for entity in entities:
            if entity.entity_type == TYPE_COIN and entity.active and not entity.collected:
                if self.rect.colliderect(entity.rect):
                    entity.collect()
                    self.coins += 1
                    self.score += COIN_SCORE
                    events['coin_collected'] = True

        # 检查敌人碰撞
        for entity in entities:
            if entity.entity_type == TYPE_ENEMY and entity.active and entity.alive:
                if self.rect.colliderect(entity.rect):
                    # 判断是否从上方踩下
                    if self.velocity_y > 0 and self.rect.bottom < entity.rect.top + 20:
                        entity.squash()
                        self.velocity_y = PLAYER_JUMP_FORCE * 0.6
                        self.score += 200
                        events['enemy_squashed'] = True
                    elif not self.invincible:
                        events['player_damaged'] = True

        # 检查是否掉落出屏幕
        if self.y > LEVEL_HEIGHT + 100:
            events['player_died'] = True

        # 更新动画
        if self.velocity_x != 0:
            self.animation_timer += 1
            if self.animation_timer >= 6:
                self.animation_timer = 0
                self.walk_frame = (self.walk_frame + 1) % 4
        else:
            self.walk_frame = 0

        return events

    def _check_horizontal_collision(self, platforms):
        """
        检测水平碰撞

        Args:
            platforms: 平台列表
        """
        for platform in platforms:
            if not platform.active:
                continue
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.x = platform.rect.left - self.width
                elif self.velocity_x < 0:
                    self.x = platform.rect.right
                self.rect.x = int(self.x)

    def _check_vertical_collision(self, platforms, entities):
        """
        检测垂直碰撞

        Args:
            platforms: 平台列表
            entities: 实体列表

        Returns:
            dict or None: 碰撞信息
        """
        hit_info = None

        for platform in platforms:
            if not platform.active:
                continue
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    # 从上方落下
                    self.y = platform.rect.top - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                    self.rect.y = int(self.y)
                elif self.velocity_y < 0:
                    # 从下方顶到
                    self.y = platform.rect.bottom
                    self.velocity_y = 0
                    self.rect.y = int(self.y)

                    # 检查是否顶到砖块或问号方块
                    if platform.entity_type == TYPE_BRICK:
                        hit_info = {'type': 'brick', 'object': platform}
                    elif platform.entity_type == TYPE_QUESTION:
                        hit_info = {'type': 'question', 'object': platform}

                    # 顶到方块后立即返回，避免继续检测导致多次碰撞
                    return hit_info

        return hit_info

    def take_damage(self):
        """玩家受伤"""
        if self.invincible:
            return False

        self.lives -= 1
        self.invincible = True
        self.invincible_timer = INVINCIBLE_TIME // 16  # 转换为帧数

        if self.lives <= 0:
            return True
        return False

    def reset(self, x, y):
        """
        重置玩家位置

        Args:
            x, y: 新位置
        """
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.invincible = True
        self.invincible_timer = INVINCIBLE_TIME // 16
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen, camera_x=0):
        """
        绘制玩家（马里奥）

        Args:
            screen: 游戏屏幕
            camera_x: 摄像机X坐标
        """
        draw_x = int(self.x - camera_x)
        draw_y = int(self.y)

        # 无敌时闪烁
        if self.invincible and (self.invincible_timer // 3) % 2 == 0:
            return

        # 简化的马里奥像素风格绘制
        # 帽子
        pygame.draw.rect(screen, RED,
                        (draw_x + 4, draw_y, 24, 10))
        pygame.draw.rect(screen, RED,
                        (draw_x, draw_y + 5, 32, 8))

        # 脸
        pygame.draw.rect(screen, (255, 200, 150),
                        (draw_x + 6, draw_y + 13, 20, 15))

        # 眼睛
        eye_x = draw_x + 18 if self.facing > 0 else draw_x + 10
        pygame.draw.rect(screen, BLACK,
                        (eye_x, draw_y + 16, 4, 6))

        # 胡子
        pygame.draw.rect(screen, BLACK,
                        (draw_x + 8, draw_y + 22, 16, 4))

        # 身体（工作服）
        pygame.draw.rect(screen, BLUE,
                        (draw_x + 4, draw_y + 28, 24, 15))

        # 吊带
        pygame.draw.rect(screen, BLUE,
                        (draw_x + 8, draw_y + 26, 4, 6))
        pygame.draw.rect(screen, BLUE,
                        (draw_x + 20, draw_y + 26, 4, 6))

        # 衬衫
        pygame.draw.rect(screen, RED,
                        (draw_x + 4, draw_y + 26, 24, 4))

        # 按钮
        pygame.draw.rect(screen, YELLOW,
                        (draw_x + 12, draw_y + 32, 3, 3))
        pygame.draw.rect(screen, YELLOW,
                        (draw_x + 17, draw_y + 32, 3, 3))

        # 腿和鞋（行走动画）
        if not self.on_ground:
            # 跳跃姿势
            pygame.draw.rect(screen, BLUE,
                            (draw_x + 4, draw_y + 40, 10, 5))
            pygame.draw.rect(screen, BLUE,
                            (draw_x + 18, draw_y + 40, 10, 5))
            pygame.draw.rect(screen, (100, 50, 0),
                            (draw_x + 2, draw_y + 43, 12, 5))
            pygame.draw.rect(screen, (100, 50, 0),
                            (draw_x + 18, draw_y + 43, 12, 5))
        elif self.walk_frame == 1 or self.walk_frame == 3:
            # 行走交替
            pygame.draw.rect(screen, BLUE,
                            (draw_x + 2, draw_y + 40, 12, 5))
            pygame.draw.rect(screen, BLUE,
                            (draw_x + 18, draw_y + 40, 12, 5))
            pygame.draw.rect(screen, (100, 50, 0),
                            (draw_x, draw_y + 43, 14, 5))
            pygame.draw.rect(screen, (100, 50, 0),
                            (draw_x + 18, draw_y + 43, 14, 5))
        else:
            # 站立姿势
            pygame.draw.rect(screen, BLUE,
                            (draw_x + 4, draw_y + 40, 10, 5))
            pygame.draw.rect(screen, BLUE,
                            (draw_x + 18, draw_y + 40, 10, 5))
            pygame.draw.rect(screen, (100, 50, 0),
                            (draw_x + 2, draw_y + 43, 12, 5))
            pygame.draw.rect(screen, (100, 50, 0),
                            (draw_x + 18, draw_y + 43, 12, 5))

        # 手臂
        if self.velocity_x != 0:
            if self.walk_frame < 2:
                pygame.draw.rect(screen, (255, 200, 150),
                                (draw_x - 2, draw_y + 30, 6, 10))
                pygame.draw.rect(screen, (255, 200, 150),
                                (draw_x + 28, draw_y + 28, 6, 10))
            else:
                pygame.draw.rect(screen, (255, 200, 150),
                                (draw_x - 2, draw_y + 28, 6, 10))
                pygame.draw.rect(screen, (255, 200, 150),
                                (draw_x + 28, draw_y + 30, 6, 10))
        else:
            pygame.draw.rect(screen, (255, 200, 150),
                            (draw_x - 2, draw_y + 28, 6, 12))
            pygame.draw.rect(screen, (255, 200, 150),
                            (draw_x + 28, draw_y + 28, 6, 12))