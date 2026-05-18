import pygame
import random
from constants import *
from player import Player
from bullet import Bullet
from enemy import Enemy
from background import Background


class Game:
    def __init__(self, screen, mode=MODE_NORMAL):
        self.screen = screen
        self.mode = mode
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - 150)
        self.background = Background()
        self.enemies = []
        self.bullets = []
        self.explosions = []
        self.enemy_spawn_timer = 0
        self.spawn_interval = NORMAL_SPAWN_INTERVAL if mode == MODE_NORMAL else HARD_SPAWN_INTERVAL
        self.max_enemies = NORMAL_MAX_ENEMIES if mode == MODE_NORMAL else HARD_MAX_ENEMIES
        self.game_over = False
        self.paused = False
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.enemies_killed = 0
        self.bombs_dropped = 0
        self.score = 0
        self.wave = 1
        self.wave_timer = 0
        self.big_plane_timer = 0
        self.big_plane_spawned = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pygame.K_SPACE and not self.paused and self.player.is_alive():
                    bullets = self.player.shoot()
                    if bullets:
                        for b in bullets:
                            self.bullets.append(Bullet(b[0], b[1], b[2], b[3]))
                if event.key == pygame.K_b and not self.paused and self.player.is_alive():
                    bomb = self.player.drop_bomb()
                    if bomb:
                        self.bullets.append(Bullet(bomb[0], bomb[1], bomb[2], False))
                        self.bombs_dropped += 1

    def update(self, keys):
        if self.paused or self.game_over:
            return

        if not self.player.is_alive():
            self.game_over = True
            return

        self.player.handle_input(keys)
        self.player.update()
        self.background.update(self.player.y)

        self.wave_timer += 16
        if self.wave_timer >= 30000:
            self.wave_timer = 0
            self.wave += 1
            self.spawn_interval = max(500, self.spawn_interval - 100)

        aa_positions = self.background.check_island_aa_spawn()
        for pos in aa_positions:
            self.enemies.append(Enemy(pos[0], pos[1], 'aa_gun'))

        self.spawn_big_plane()
        self.spawn_enemies()
        self.update_enemies()
        self.update_bullets()
        self.update_explosions()
        self.check_collisions()
        self.cleanup()

    def spawn_big_plane(self):
        self.big_plane_timer += 16

        has_big_plane = any(e.enemy_type == 'big_plane' and e.active for e in self.enemies)
        if has_big_plane:
            self.big_plane_spawned = True
            return
        else:
            if self.big_plane_spawned:
                self.big_plane_spawned = False
                self.big_plane_timer = 0

        if self.big_plane_timer >= BIG_PLANE_SPAWN_INTERVAL:
            self.big_plane_timer = 0
            x = SCREEN_WIDTH // 2 - BIG_PLANE_WIDTH // 2
            y = -BIG_PLANE_HEIGHT
            self.enemies.append(Enemy(x, y, 'big_plane'))
            self.big_plane_spawned = True

    def spawn_enemies(self):
        self.enemy_spawn_timer += 16
        if self.enemy_spawn_timer >= self.spawn_interval:
            self.enemy_spawn_timer = 0
            active_enemies = len([e for e in self.enemies if e.active and e.enemy_type != 'big_plane'])
            if active_enemies < self.max_enemies:
                enemy_type = random.choice(['plane', 'plane', 'plane', 'ship'])
                if enemy_type == 'plane':
                    x = random.randint(50, SCREEN_WIDTH - ENEMY_PLANE_WIDTH - 50)
                    y = -ENEMY_PLANE_HEIGHT
                    self.enemies.append(Enemy(x, y, 'plane'))
                else:
                    areas = self.background.get_ship_spawn_area()
                    if areas:
                        area = random.choice(areas)
                        x = random.randint(area[0], area[1])
                        y = -SHIP_HEIGHT - random.randint(0, 200)
                        self.enemies.append(Enemy(x, y, 'ship'))

    def update_enemies(self):
        for enemy in self.enemies:
            if enemy.active:
                enemy.update(self.player.x, self.player.y)
                bullets = enemy.shoot(self.player.x, self.player.y)
                if bullets:
                    for b in bullets:
                        self.bullets.append(Bullet(b[0], b[1], b[2], b[3]))

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

    def update_explosions(self):
        for exp in self.explosions:
            exp['timer'] -= 16

    def check_collisions(self):
        for bullet in self.bullets:
            if not bullet.active:
                continue

            if bullet.is_enemy:
                if bullet.get_rect().colliderect(self.player.get_rect()):
                    bullet.active = False
                    self.player.take_damage()
            else:
                for enemy in self.enemies:
                    if enemy.active:
                        if bullet.is_bomb:
                            if enemy.enemy_type in ['ship', 'aa_gun']:
                                if bullet.get_rect().colliderect(enemy.get_rect()):
                                    bullet.active = False
                                    if enemy.take_damage(bullet.damage):
                                        self.score += enemy.score
                                        self.enemies_killed += 1
                                        self._add_explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, 'large')
                                    else:
                                        self._add_explosion(bullet.x, bullet.y, 'small')
                                    break
                        else:
                            if enemy.enemy_type in ['plane', 'big_plane']:
                                if bullet.get_rect().colliderect(enemy.get_rect()):
                                    bullet.active = False
                                    if enemy.take_damage(bullet.damage):
                                        self.score += enemy.score
                                        self.enemies_killed += 1
                                        if enemy.enemy_type == 'big_plane':
                                            self._add_explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, 'large')
                                        else:
                                            self._add_explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, 'medium')
                                    break

        for enemy in self.enemies:
            if enemy.active and enemy.enemy_type in ['plane', 'big_plane'] and enemy.get_rect().colliderect(self.player.get_rect()):
                self.player.take_damage()
                if enemy.enemy_type != 'big_plane':
                    enemy.active = False
                    self._add_explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, 'medium')
                else:
                    enemy.take_damage(5)
                    self._add_explosion(self.player.x + self.player.width // 2, self.player.y + self.player.height // 2, 'small')

    def _add_explosion(self, x, y, size):
        self.explosions.append({'x': x, 'y': y, 'size': size, 'timer': 500})

    def cleanup(self):
        self.bullets = [b for b in self.bullets if b.active]
        self.enemies = [e for e in self.enemies if e.active]
        self.explosions = [e for e in self.explosions if e['timer'] > 0]

    def draw(self):
        self.background.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        self._draw_explosions()
        self.draw_ui()

        if self.paused:
            self._draw_pause_screen()
        elif self.game_over:
            self._draw_game_over_screen()

    def _draw_explosions(self):
        for exp in self.explosions:
            progress = 1 - exp['timer'] / 500
            if exp['size'] == 'small':
                radius = int(10 + progress * 15)
            elif exp['size'] == 'medium':
                radius = int(15 + progress * 25)
            else:
                radius = int(25 + progress * 40)

            alpha = int(255 * (1 - progress))
            color1 = (255, int(140 * (1 - progress)), 0)
            color2 = (255, int(215 * (1 - progress)), 0)

            pygame.draw.circle(self.screen, color1, (exp['x'], exp['y']), radius)
            pygame.draw.circle(self.screen, color2, (exp['x'], exp['y']), int(radius * 0.6))
            if progress < 0.5:
                pygame.draw.circle(self.screen, WHITE, (exp['x'], exp['y']), int(radius * 0.3))

    def draw_ui(self):
        score_text = self.font.render(f'得分: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        wave_text = self.font.render(f'波次: {self.wave}', True, WHITE)
        self.screen.blit(wave_text, (10, 50))

        kills_text = self.small_font.render(f'击杀: {self.enemies_killed}', True, WHITE)
        self.screen.blit(kills_text, (10, 90))

        health_text = self.font.render('生命:', True, WHITE)
        self.screen.blit(health_text, (SCREEN_WIDTH - 180, 10))
        for i in range(self.player.max_health):
            color = RED if i < self.player.health else DARK_GRAY
            pygame.draw.rect(self.screen, color, (SCREEN_WIDTH - 180 + i * 25, 45, 20, 20))
            if i < self.player.health:
                pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH - 180 + i * 25 + 5, 50, 10, 10))

        mode_text = self.small_font.render(
            f'模式: {"困难" if self.mode == MODE_HARD else "普通"}', True, WHITE)
        self.screen.blit(mode_text, (SCREEN_WIDTH - 180, 80))

    def _draw_pause_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font.render('游戏暂停', True, YELLOW)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(pause_text, text_rect)

        hint_text = self.small_font.render('按 ESC 继续游戏', True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(hint_text, hint_rect)

    def _draw_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render('任务失败', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, text_rect)

        score_text = self.small_font.render(f'最终得分: {self.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(score_text, score_rect)

        kills_text = self.small_font.render(f'击杀敌人: {self.enemies_killed}', True, WHITE)
        kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(kills_text, kills_rect)

        wave_text = self.small_font.render(f'存活波次: {self.wave}', True, WHITE)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(wave_text, wave_rect)

        hint_text = self.small_font.render('按 R 重新开始 或 按 M 返回菜单', True, YELLOW)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(hint_text, hint_rect)

    def restart(self):
        self.__init__(self.screen, self.mode)

    def set_mode(self, mode):
        self.mode = mode
        self.restart()
