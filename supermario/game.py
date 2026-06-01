import pygame
from constants import *
from player import Player
from enemy import Enemy
from level import Level
from items import Coin


class Game:
    """游戏主逻辑类"""

    def __init__(self, screen):
        self.screen = screen
        self.level = Level()
        self.level.coins_to_spawn = []

        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        self.player = Player(100, ground_y - PLAYER_HEIGHT - 10)

        self.enemies = []
        self.coins = []
        self.camera_x = 0

        self.game_over = False
        self.win = False
        self.paused = False

        self.font = pygame.font.Font(FONT_PATH, 28)
        self.small_font = pygame.font.Font(FONT_PATH, 20)
        self.big_font = pygame.font.Font(FONT_PATH, 64)

        self.enemy_spawn_cooldown = 0
        self.spawned_enemy_indices = set()

        self._spawn_initial_coins()

    def _spawn_initial_coins(self):
        """生成初始金币"""
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        coin_positions = [
            (450, ground_y - 160),
            (482, ground_y - 160),
            (514, ground_y - 160),
            (1150, ground_y - 200),
            (1182, ground_y - 200),
            (2250, ground_y - 160),
            (2282, ground_y - 160),
            (2314, ground_y - 160),
            (3150, ground_y - 200),
            (3182, ground_y - 200),
            (4050, ground_y - 230),
            (4082, ground_y - 230),
            (4114, ground_y - 230),
            (4450, ground_y - 160),
            (4482, ground_y - 160),
            (4514, ground_y - 160),
        ]
        for x, y in coin_positions:
            self.coins.append(Coin(x, y))

    def handle_events(self, events):
        """处理事件"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

    def update(self, keys):
        """更新游戏状态"""
        if self.paused:
            return

        if self.game_over or self.win:
            return

        self.player.handle_input(keys)

        solids = self.level.get_all_solids()
        self.player.update(solids, self.level)

        self._update_camera()

        self.level.update()

        for coin in self.level.coins_to_spawn:
            self.coins.append(coin)
        self.level.coins_to_spawn = []

        for coin in self.coins:
            coin.update(solids)

        self._spawn_enemies()

        for enemy in self.enemies:
            enemy.update(solids)

        self._check_collisions()

        self._check_win()

        self._cleanup()

        if not self.player.is_alive():
            if self.player.death_timer > 60:
                self.game_over = True

    def _update_camera(self):
        """更新相机位置"""
        target_camera_x = self.player.x - CAMERA_OFFSET

        if target_camera_x > self.camera_x:
            self.camera_x = target_camera_x

        self.camera_x = max(0, min(self.camera_x, LEVEL_WIDTH - SCREEN_WIDTH))

    def _spawn_enemies(self):
        """生成敌人"""
        self.enemy_spawn_cooldown -= 16
        if self.enemy_spawn_cooldown > 0:
            return

        for i, (x, y) in enumerate(self.level.enemy_spawn_points):
            if i in self.spawned_enemy_indices:
                continue

            if self.camera_x < x < self.camera_x + SCREEN_WIDTH + 200:
                self.enemies.append(Enemy(x, y))
                self.spawned_enemy_indices.add(i)
                self.enemy_spawn_cooldown = 500
                break

    def _check_collisions(self):
        """检测碰撞"""
        player_rect = self.player.get_rect()
        player_full_rect = self.player.get_full_rect()

        for coin in self.coins:
            if coin.active and not coin.collected and coin.get_rect().colliderect(player_rect):
                score = coin.collect()
                if score > 0:
                    self.player.add_coin()

        for enemy in self.enemies:
            if not enemy.active or enemy.squished:
                continue

            enemy_rect = enemy.get_rect()
            stomp_rect = enemy.get_stomp_rect()

            if self.player.vel_y > 0 and player_rect.colliderect(stomp_rect):
                if player_rect.bottom < enemy_rect.top + enemy_rect.height // 2 + 10:
                    if enemy.stomp():
                        self.player.vel_y = -8
                        self.player.add_score(200)
                        continue

            if player_rect.colliderect(enemy_rect):
                if not self.player.invincible:
                    self.player.take_damage()

    def _check_win(self):
        """检测是否胜利"""
        if self.player.x >= self.level.goal_x:
            self.win = True

    def _cleanup(self):
        """清理失效对象"""
        self.enemies = [e for e in self.enemies if e.active]
        self.coins = [c for c in self.coins if c.active]

    def draw(self):
        """绘制游戏"""
        self.level.draw_background(self.screen, self.camera_x)

        for coin in self.coins:
            coin.draw(self.screen, self.camera_x)

        self.level.draw_foreground(self.screen, self.camera_x)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x)

        self.player.draw(self.screen, self.camera_x)

        self._draw_ui()

        if self.paused:
            self._draw_pause_screen()
        elif self.game_over:
            self._draw_game_over_screen()
        elif self.win:
            self._draw_win_screen()

    def _draw_ui(self):
        """绘制用户界面"""
        score_text = self.font.render(f'分数: {self.player.score}', True, WHITE)
        self.screen.blit(score_text, (20, 20))

        coin_icon = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(coin_icon, GOLD, (12, 12), 12)
        pygame.draw.circle(coin_icon, YELLOW, (10, 10), 8)
        coin_font = pygame.font.Font(None, 18)
        coin_text = coin_font.render('$', True, DARK_BROWN)
        coin_rect = coin_text.get_rect(center=(12, 12))
        coin_icon.blit(coin_text, coin_rect)
        self.screen.blit(coin_icon, (20, 60))

        coin_count_text = self.font.render(f'× {self.player.coins}', True, WHITE)
        self.screen.blit(coin_count_text, (50, 58))

        health_text = self.font.render('生命:', True, WHITE)
        self.screen.blit(health_text, (SCREEN_WIDTH - 200, 20))

        for i in range(self.player.max_health):
            heart_x = SCREEN_WIDTH - 140 + i * 35
            if i < self.player.health:
                self._draw_heart(heart_x, 28, RED)
            else:
                self._draw_heart(heart_x, 28, DARK_GRAY)

        progress = min(100, int(self.player.x / self.level.goal_x * 100))
        progress_bg = pygame.Rect(SCREEN_WIDTH // 2 - 100, 25, 200, 16)
        pygame.draw.rect(self.screen, DARK_GRAY, progress_bg, 2)
        progress_fill = pygame.Rect(SCREEN_WIDTH // 2 - 98, 27, int(196 * progress / 100), 12)
        pygame.draw.rect(self.screen, LIME_GREEN, progress_fill)
        progress_text = self.small_font.render(f'{progress}%', True, WHITE)
        self.screen.blit(progress_text, (SCREEN_WIDTH // 2 + 110, 25))

        controls_text = self.small_font.render('←→移动  空格跳跃  ESC暂停', True, LIGHT_GRAY)
        self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))

    def _draw_heart(self, x, y, color):
        """绘制心形"""
        pygame.draw.circle(self.screen, color, (x + 8, y + 6), 7)
        pygame.draw.circle(self.screen, color, (x + 22, y + 6), 7)
        pygame.draw.polygon(self.screen, color, [
            (x, y + 8),
            (x + 15, y + 28),
            (x + 30, y + 8)
        ])

    def _draw_pause_screen(self):
        """绘制暂停界面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.big_font.render('游戏暂停', True, YELLOW)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(pause_text, text_rect)

        hint_text = self.font.render('按 ESC 继续游戏', True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(hint_text, hint_rect)

    def _draw_game_over_screen(self):
        """绘制游戏结束界面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.big_font.render('游戏结束', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, text_rect)

        score_text = self.font.render(f'最终得分: {self.player.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)

        coin_text = self.font.render(f'收集金币: {self.player.coins}', True, YELLOW)
        coin_rect = coin_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(coin_text, coin_rect)

        hint_text = self.small_font.render('按 R 重新开始  按 M 返回菜单', True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        self.screen.blit(hint_text, hint_rect)

    def _draw_win_screen(self):
        """绘制胜利界面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        win_text = self.big_font.render('恭喜通关！', True, YELLOW)
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(win_text, text_rect)

        score_text = self.font.render(f'最终得分: {self.player.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(score_text, score_rect)

        coin_text = self.font.render(f'收集金币: {self.player.coins}', True, GOLD)
        coin_rect = coin_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(coin_text, coin_rect)

        hint_text = self.small_font.render('按 R 重新开始  按 M 返回菜单', True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(hint_text, hint_rect)

    def restart(self):
        """重新开始游戏"""
        self.__init__(self.screen)
