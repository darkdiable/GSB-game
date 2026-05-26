# -*- coding: utf-8 -*-
"""
关卡设计模块 - 定义游戏关卡和地图加载
"""

from constants import *
from entities import Ground, Brick, QuestionBlock, Pipe, Coin, Enemy


class Level:
    """关卡类 - 负责关卡加载和管理"""

    def __init__(self):
        """初始化关卡"""
        self.platforms = []  # 平台列表（地面、砖块、管道等）
        self.coins = []      # 金币列表
        self.enemies = []    # 敌人列表
        self.level_width = LEVEL_WIDTH
        self.level_height = LEVEL_HEIGHT

    def load_level(self):
        """加载默认关卡"""
        self.platforms = []
        self.coins = []
        self.enemies = []

        # 地面Y坐标
        ground_y = SCREEN_HEIGHT - 80

        # 创建地面（分段，有坑洞）
        ground_segments = [
            (0, 600),          # 起始地面
            (700, 900),        # 第二段地面
            (1000, 1500),      # 第三段地面
            (1600, 2200),      # 第四段地面
            (2300, 2800),      # 第五段地面
            (2900, LEVEL_WIDTH) # 终点地面
        ]

        for start_x, end_x in ground_segments:
            width = end_x - start_x
            ground = Ground(start_x, ground_y, width, 80)
            self.platforms.append(ground)

        # 创建砖块平台（浮空）
        brick_blocks = [
            # (x, y, 数量)
            (300, ground_y - 120, 1),    # 起始区域砖块
            (380, ground_y - 120, 1),    # 起始区域砖块
            (500, ground_y - 200, 1),    # 高处砖块
            (580, ground_y - 200, 1),    # 高处砖块
            (800, ground_y - 160, 2),    # 第二段地面砖块
            (920, ground_y - 160, 2),    # 第二段地面砖块
            (1200, ground_y - 180, 2),   # 第三段地面砖块
            (1320, ground_y - 180, 1),   # 第三段地面砖块
            (1400, ground_y - 260, 1),   # 高处砖块
            (1480, ground_y - 260, 1),   # 高处砖块
            (1700, ground_y - 160, 2),   # 第四段地面砖块
            (1820, ground_y - 160, 2),   # 第四段地面砖块
            (2000, ground_y - 240, 1),   # 高处砖块
            (2080, ground_y - 240, 1),   # 高处砖块
            (2400, ground_y - 180, 2),   # 第五段地面砖块
            (2520, ground_y - 180, 1),   # 第五段地面砖块
            (2600, ground_y - 260, 1),   # 高处砖块
            (2680, ground_y - 260, 1),   # 高处砖块
            (3000, ground_y - 160, 2),   # 终点区域砖块
            (3120, ground_y - 160, 1),   # 终点区域砖块
        ]

        for x, y, count in brick_blocks:
            for i in range(count):
                brick = Brick(x + i * BRICK_SIZE, y)
                self.platforms.append(brick)

        # 创建问号方块
        question_blocks = [
            (340, ground_y - 120),   # 起始区域问号
            (540, ground_y - 200),   # 高处问号
            (880, ground_y - 160),   # 第二段地面问号
            (1280, ground_y - 180),  # 第三段地面问号
            (1440, ground_y - 260),  # 高处问号
            (1780, ground_y - 160),  # 第四段地面问号
            (2040, ground_y - 240),  # 高处问号
            (2480, ground_y - 180),  # 第五段地面问号
            (2640, ground_y - 260),  # 高处问号
            (3080, ground_y - 160),  # 终点区域问号
        ]

        for x, y in question_blocks:
            question = QuestionBlock(x, y)
            self.platforms.append(question)

        # 创建管道
        pipes = [
            (750, ground_y - PIPE_HEIGHT),    # 第一个管道
            (1100, ground_y - PIPE_HEIGHT),   # 第二个管道
            (1550, ground_y - PIPE_HEIGHT),   # 第三个管道
            (2100, ground_y - PIPE_HEIGHT),   # 第四个管道
            (2700, ground_y - PIPE_HEIGHT),   # 第五个管道
        ]

        for x, y in pipes:
            pipe = Pipe(x, y)
            self.platforms.append(pipe)

        # 创建散布的金币（地面上）
        coin_positions = [
            (200, ground_y - 40),
            (250, ground_y - 40),
            (400, ground_y - 40),
            (450, ground_y - 40),
            (650, ground_y - 40),
            (700, ground_y - 40),
            (1050, ground_y - 40),
            (1100, ground_y - 40),
            (1650, ground_y - 40),
            (1700, ground_y - 40),
            (1750, ground_y - 40),
            (2350, ground_y - 40),
            (2400, ground_y - 40),
            (2450, ground_y - 40),
            (2950, ground_y - 40),
            (3000, ground_y - 40),
        ]

        for x, y in coin_positions:
            coin = Coin(x, y)
            self.coins.append(coin)

        # 创建浮空金币（砖块上方）
        floating_coins = [
            (340, ground_y - 160),
            (540, ground_y - 240),
            (880, ground_y - 200),
            (1280, ground_y - 220),
            (1440, ground_y - 300),
            (1780, ground_y - 200),
            (2040, ground_y - 280),
            (2480, ground_y - 220),
            (2640, ground_y - 300),
            (3080, ground_y - 200),
        ]

        for x, y in floating_coins:
            coin = Coin(x, y)
            self.coins.append(coin)

        # 创建敌人（蘑菇怪）
        enemy_positions = [
            (400, ground_y - ENEMY_HEIGHT),
            (850, ground_y - ENEMY_HEIGHT),
            (1250, ground_y - ENEMY_HEIGHT),
            (1350, ground_y - ENEMY_HEIGHT),
            (1750, ground_y - ENEMY_HEIGHT),
            (1900, ground_y - ENEMY_HEIGHT),
            (2450, ground_y - ENEMY_HEIGHT),
            (2550, ground_y - ENEMY_HEIGHT),
            (3050, ground_y - ENEMY_HEIGHT),
        ]

        for x, y in enemy_positions:
            enemy = Enemy(x, y)
            self.enemies.append(enemy)

    def get_all_entities(self):
        """获取所有实体"""
        return self.platforms + self.coins + self.enemies

    def get_platforms(self):
        """获取所有平台实体"""
        return [p for p in self.platforms if p.active]

    def get_visible_entities(self, camera_x):
        """
        获取可见范围内的实体

        Args:
            camera_x: 摄像机X坐标

        Returns:
            list: 可见实体列表
        """
        visible = []
        for entity in self.get_all_entities():
            if not entity.active:
                continue
            # 检查是否在屏幕可见范围内
            if (entity.x + entity.width > camera_x - 100 and
                entity.x < camera_x + SCREEN_WIDTH + 100):
                visible.append(entity)
        return visible

    def update_enemies(self):
        """更新所有敌人"""
        platforms = self.get_platforms()
        for enemy in self.enemies:
            if enemy.active and enemy.alive:
                old_x = enemy.x
                enemy.update(platforms)

                # 检查是否碰到墙壁或悬崖
                if enemy.x == old_x or self._check_cliff(enemy, platforms):
                    enemy.change_direction()

    def _check_cliff(self, enemy, platforms):
        """
        检查敌人前方是否有悬崖

        Args:
            enemy: 敌人对象
            platforms: 平台列表

        Returns:
            bool: 是否有悬崖
        """
        # 检查敌人前方脚下是否有平台
        check_x = enemy.x + (enemy.width if enemy.direction > 0 else -10)
        check_y = enemy.y + enemy.height + 5

        for platform in platforms:
            if (platform.entity_type in [TYPE_GROUND, TYPE_PIPE] and
                platform.rect.collidepoint(check_x, check_y)):
                return False

        # 如果在地面上且前方没有平台，则是悬崖
        if enemy.y + enemy.height >= SCREEN_HEIGHT - 100:
            return True

        return False

    def check_level_complete(self, player):
        """
        检查关卡是否完成

        Args:
            player: 玩家对象

        Returns:
            bool: 是否完成
        """
        return player.x >= self.level_width - 100