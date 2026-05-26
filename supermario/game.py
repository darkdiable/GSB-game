# -*- coding: utf-8 -*-
"""
游戏主循环模块 - 负责游戏状态管理和主循环逻辑
"""

import pygame
import sys
from constants import *
from player import Player
from level import Level
from entities import Coin
from utils import draw_background, draw_text


class Game:
    """游戏主类 - 管理游戏状态和主循环"""

    def __init__(self):
        """初始化游戏"""
        # 初始化pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        # 游戏状态
        self.state = STATE_MENU

        # 摄像机位置
        self.camera_x = 0

        # 创建玩家和关卡
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        self.level = Level()
        self.level.load_level()

        # 游戏时间
        self.game_time = 300  # 5分钟

        # 动画金币列表（从问号方块弹出的金币）
        self.animation_coins = []

    def run(self):
        """运行游戏主循环"""
        while True:
            self.clock.tick(FPS)

            # 处理事件
            self._handle_events()

            # 根据游戏状态执行不同逻辑
            if self.state == STATE_MENU:
                self._update_menu()
                self._draw_menu()
            elif self.state == STATE_PLAYING:
                self._update_playing()
                self._draw_playing()
            elif self.state == STATE_GAME_OVER:
                self._update_game_over()
                self._draw_game_over()
            elif self.state == STATE_WIN:
                self._update_win()
                self._draw_win()

            pygame.display.flip()

    def _handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 菜单状态下的按键处理
            if self.state == STATE_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self._start_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # 游戏结束状态下的按键处理
            elif self.state == STATE_GAME_OVER or self.state == STATE_WIN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self._reset_game()
                        self.state = STATE_MENU
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # 游戏进行中的按键处理
            elif self.state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU

    def _start_game(self):
        """开始新游戏"""
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        self.level = Level()
        self.level.load_level()
        self.camera_x = 0
        self.game_time = 300
        self.animation_coins = []
        self.state = STATE_PLAYING

    def _reset_game(self):
        """重置游戏到菜单状态"""
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        self.level = Level()
        self.level.load_level()
        self.camera_x = 0
        self.animation_coins = []

    def _update_menu(self):
        """更新菜单状态"""
        pass

    def _draw_menu(self):
        """绘制菜单界面"""
        # 绘制背景
        draw_background(self.screen, 0)

        # 绘制标题
        draw_text(self.screen, "SUPER MARIO",
                 SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 4,
                 size=72, color=RED)

        draw_text(self.screen, "像素冒险",
                 SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 4 + 80,
                 size=48, color=ORANGE)

        # 绘制开始提示
        draw_text(self.screen, "按 回车键 或 空格键 开始游戏",
                 SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100,
                 size=32, color=WHITE)

        # 绘制操作说明
        draw_text(self.screen, "操作说明:",
                 50, SCREEN_HEIGHT - 180,
                 size=28, color=WHITE)

        instructions = [
            "← → 或 A D : 左右移动",
            "空格 或 ↑ 或 W : 跳跃",
            "踩敌人头顶可消灭敌人",
            "顶问号方块获得金币",
            "ESC : 返回菜单"
        ]

        for i, instruction in enumerate(instructions):
            draw_text(self.screen, instruction,
                     50, SCREEN_HEIGHT - 150 + i * 30,
                     size=24, color=WHITE)

    def _update_playing(self):
        """更新游戏进行状态"""
        # 获取按键状态
        keys = pygame.key.get_pressed()

        # 处理玩家输入
        self.player.handle_input(keys)

        # 更新玩家
        platforms = self.level.get_platforms()
        all_entities = self.level.get_all_entities() + self.animation_coins
        events = self.player.update(platforms, all_entities)

        # 处理玩家事件
        self._handle_player_events(events)

        # 更新敌人
        self.level.update_enemies()

        # 更新动画金币
        self.animation_coins = [c for c in self.animation_coins if c.active]
        for coin in self.animation_coins:
            coin.update()

        # 更新关卡中的砖块和问号方块
        for platform in self.level.platforms:
            platform.update()

        # 更新摄像机位置（跟随玩家）
        self._update_camera()

        # 减少游戏时间
        if self.game_time > 0:
            self.game_time -= 1 / FPS

        # 检查游戏结束条件
        if self.player.lives <= 0 or self.game_time <= 0:
            self.state = STATE_GAME_OVER

        # 检查关卡完成
        if self.level.check_level_complete(self.player):
            self.state = STATE_WIN

    def _handle_player_events(self, events):
        """
        处理玩家事件

        Args:
            events: 事件字典
        """
        # 金币收集（已在player.update中处理）
        if events.get('coin_collected'):
            pass  # 分数已在player中更新

        # 敌人被踩扁
        if events.get('enemy_squashed'):
            pass  # 分数已在player中更新

        # 顶到砖块
        if events.get('brick_hit'):
            brick = events['brick_hit']
            brick.hit()

        # 顶到问号方块
        if events.get('question_hit'):
            question = events['question_hit']
            if question.hit():
                # 生成弹出金币动画
                coin = Coin(question.x + QUESTION_SIZE // 2 - COIN_SIZE // 2,
                          question.y - COIN_SIZE,
                          is_animation=True)
                self.animation_coins.append(coin)
                self.player.coins += 1
                self.player.score += COIN_SCORE

        # 玩家受伤
        if events.get('player_damaged'):
            if self.player.take_damage():
                self.state = STATE_GAME_OVER
            else:
                # 受伤后重置位置
                self.player.reset(PLAYER_START_X, PLAYER_START_Y)
                self.camera_x = 0

        # 玩家死亡（掉出屏幕）
        if events.get('player_died'):
            if self.player.take_damage():
                self.state = STATE_GAME_OVER
            else:
                self.player.reset(PLAYER_START_X, PLAYER_START_Y)
                self.camera_x = 0

    def _update_camera(self):
        """更新摄像机位置"""
        # 摄像机跟随玩家，但保持在关卡范围内
        target_x = self.player.x - SCREEN_WIDTH // 3
        self.camera_x = max(0, min(target_x,
                                   self.level.level_width - SCREEN_WIDTH))

    def _draw_playing(self):
        """绘制游戏进行界面"""
        # 绘制背景
        draw_background(self.screen, self.camera_x)

        # 绘制关卡实体
        for entity in self.level.get_visible_entities(self.camera_x):
            entity.draw(self.screen, self.camera_x)

        # 绘制动画金币
        for coin in self.animation_coins:
            coin.draw(self.screen, self.camera_x)

        # 绘制玩家
        self.player.draw(self.screen, self.camera_x)

        # 绘制HUD（抬头显示）
        self._draw_hud()

    def _draw_hud(self):
        """绘制游戏抬头显示"""
        # 显示分数
        draw_text(self.screen, f"分数: {self.player.score}",
                 SCORE_X, SCORE_Y, size=28, color=WHITE)

        # 显示金币数量
        draw_text(self.screen, f"金币: {self.player.coins}",
                 SCORE_X, SCORE_Y + 35, size=24, color=YELLOW)

        # 显示生命值
        lives_text = f"生命: {'❤' * self.player.lives}"
        draw_text(self.screen, lives_text,
                 LIVES_X, LIVES_Y, size=24, color=RED)

        # 显示时间
        time_text = f"时间: {int(self.game_time)}"
        draw_text(self.screen, time_text,
                 SCREEN_WIDTH // 2 - 50, SCORE_Y,
                 size=28, color=WHITE)

    def _update_game_over(self):
        """更新游戏结束状态"""
        pass

    def _draw_game_over(self):
        """绘制游戏结束界面"""
        # 绘制背景
        draw_background(self.screen, self.camera_x)

        # 绘制半透明黑色覆盖
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # 绘制游戏结束文字
        draw_text(self.screen, "游戏结束",
                 SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 3,
                 size=64, color=RED)

        # 显示最终分数
        draw_text(self.screen, f"最终分数: {self.player.score}",
                 SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2,
                 size=36, color=WHITE)

        # 显示金币数量
        draw_text(self.screen, f"收集金币: {self.player.coins}",
                 SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50,
                 size=28, color=YELLOW)

        # 绘制重新开始提示
        draw_text(self.screen, "按 回车键 返回菜单",
                 SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT * 2 // 3,
                 size=28, color=WHITE)

    def _update_win(self):
        """更新胜利状态"""
        pass

    def _draw_win(self):
        """绘制胜利界面"""
        # 绘制背景
        draw_background(self.screen, self.camera_x)

        # 绘制半透明黑色覆盖
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # 绘制胜利文字
        draw_text(self.screen, "恭喜通关!",
                 SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 3,
                 size=64, color=YELLOW)

        # 显示最终分数
        draw_text(self.screen, f"最终分数: {self.player.score}",
                 SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2,
                 size=36, color=WHITE)

        # 显示金币数量
        draw_text(self.screen, f"收集金币: {self.player.coins}",
                 SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50,
                 size=28, color=YELLOW)

        # 显示剩余时间奖励
        time_bonus = int(self.game_time) * 10
        draw_text(self.screen, f"时间奖励: +{time_bonus}",
                 SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100,
                 size=28, color=GREEN)

        # 绘制重新开始提示
        draw_text(self.screen, "按 回车键 返回菜单",
                 SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT * 2 // 3,
                 size=28, color=WHITE)