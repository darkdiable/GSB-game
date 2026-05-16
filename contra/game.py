import pygame
import random
from constants import *
from player import Player
from enemy import Enemy
from level import Level


class Game:
    def __init__(self, screen, mode=MODE_NORMAL):
        self.screen = screen
        self.mode = mode
        self.player = Player(100, GROUND_HEIGHT - PLAYER_HEIGHT)
        self.level = Level()
        self.enemies = []
        self.bullets = []
        self.camera_x = 0
        self.enemy_spawn_timer = 0
        self.spawn_interval = NORMAL_ENEMY_SPAWN_INTERVAL if mode == MODE_NORMAL else HELL_ENEMY_SPAWN_INTERVAL
        self.max_enemies = NORMAL_MAX_ENEMIES if mode == MODE_NORMAL else HELL_MAX_ENEMIES
        self.game_over = False
        self.game_won = False
        self.paused = False
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.enemies_killed = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pygame.K_j and not self.paused and self.player.is_alive():
                    bullet = self.player.shoot()
                    if bullet:
                        self.bullets.append(bullet)

    def update(self, keys):
        if self.paused or self.game_over or self.game_won:
            return

        if not self.player.is_alive():
            self.game_over = True
            return

        if self.player.x >= self.level.level_width - 100:
            self.game_won = True
            return

        self.player.handle_input(keys)
        self.player.update(self.level.get_platforms())

        self.update_camera()
        self.spawn_enemies()
        self.update_enemies()
        self.update_bullets()
        self.check_collisions()
        self.cleanup()

    def update_camera(self):
        target_x = self.player.x - CAMERA_OFFSET
        if target_x > self.camera_x:
            self.camera_x = target_x
        if self.camera_x < 0:
            self.camera_x = 0
        if self.camera_x > self.level.level_width - SCREEN_WIDTH:
            self.camera_x = self.level.level_width - SCREEN_WIDTH

    def spawn_enemies(self):
        self.enemy_spawn_timer += 16
        if self.enemy_spawn_timer >= self.spawn_interval:
            self.enemy_spawn_timer = 0
            active_enemies = len([e for e in self.enemies if e.active])
            if active_enemies < self.max_enemies:
                spawn_x = self.camera_x + SCREEN_WIDTH + random.randint(50, 150)
                if spawn_x < self.level.level_width - 200:
                    enemy = Enemy(spawn_x, GROUND_HEIGHT - ENEMY_HEIGHT, self.mode)
                    self.enemies.append(enemy)

    def update_enemies(self):
        for enemy in self.enemies:
            if enemy.active:
                bullet = enemy.update(self.player.x, self.level.get_platforms())
                if bullet:
                    self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

    def check_collisions(self):
        for bullet in self.bullets:
            if not bullet.active:
                continue

            if not bullet.is_enemy:
                for enemy in self.enemies:
                    if enemy.active and bullet.get_rect().colliderect(enemy.get_rect()):
                        bullet.active = False
                        if enemy.take_damage():
                            self.player.score += 100
                            self.enemies_killed += 1
                        break
            else:
                if bullet.get_rect().colliderect(self.player.get_rect()):
                    bullet.active = False
                    self.player.take_damage()

        for enemy in self.enemies:
            if enemy.active and enemy.get_rect().colliderect(self.player.get_rect()):
                self.player.take_damage()

    def cleanup(self):
        self.bullets = [b for b in self.bullets if b.active]
        self.enemies = [e for e in self.enemies if e.active and e.x > self.camera_x - 200]

    def draw(self):
        self.level.draw_background(self.screen, self.camera_x)
        self.level.draw_ground(self.screen, self.camera_x)
        self.level.draw_platforms(self.screen, self.camera_x)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x)

        self.player.draw(self.screen, self.camera_x)

        for bullet in self.bullets:
            bullet.draw(self.screen, self.camera_x)

        self.draw_ui()

        if self.paused:
            self.draw_pause_screen()
        elif self.game_over:
            self.draw_game_over_screen()
        elif self.game_won:
            self.draw_win_screen()

    def draw_ui(self):
        score_text = self.font.render(f'SCORE: {self.player.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        health_text = self.font.render(f'HEALTH: {self.player.health}', True, WHITE)
        self.screen.blit(health_text, (10, 50))

        mode_text = self.small_font.render(
            f'MODE: {"HELL" if self.mode == MODE_HELL else "NORMAL"}', True, WHITE)
        self.screen.blit(mode_text, (10, 90))

        kills_text = self.small_font.render(f'KILLS: {self.enemies_killed}', True, WHITE)
        self.screen.blit(kills_text, (10, 120))

        progress = (self.player.x / self.level.level_width) * 100
        progress_text = self.small_font.render(f'PROGRESS: {int(progress)}%', True, WHITE)
        self.screen.blit(progress_text, (SCREEN_WIDTH - 180, 10))

        pygame.draw.rect(self.screen, (100, 100, 100), (SCREEN_WIDTH - 180, 40, 170, 15))
        pygame.draw.rect(self.screen, GREEN_GROUND, (SCREEN_WIDTH - 180, 40, int(170 * progress / 100), 15))

    def draw_pause_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font.render('PAUSED', True, YELLOW)
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(pause_text, text_rect)

        hint_text = self.small_font.render('Press ESC to continue', True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(hint_text, hint_rect)

    def draw_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render('GAME OVER', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(game_over_text, text_rect)

        score_text = self.small_font.render(f'Final Score: {self.player.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        kills_text = self.small_font.render(f'Enemies Killed: {self.enemies_killed}', True, WHITE)
        kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(kills_text, kills_rect)

        hint_text = self.small_font.render('Press R to restart or M for menu', True, YELLOW)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(hint_text, hint_rect)

    def draw_win_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        win_text = self.font.render('MISSION COMPLETE!', True, YELLOW)
        text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(win_text, text_rect)

        score_text = self.small_font.render(f'Final Score: {self.player.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)

        kills_text = self.small_font.render(f'Enemies Killed: {self.enemies_killed}', True, WHITE)
        kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(kills_text, kills_rect)

        hint_text = self.small_font.render('Press R to restart or M for menu', True, YELLOW)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(hint_text, hint_rect)

    def restart(self):
        self.__init__(self.screen, self.mode)

    def set_mode(self, mode):
        self.mode = mode
        self.spawn_interval = NORMAL_ENEMY_SPAWN_INTERVAL if mode == MODE_NORMAL else HELL_ENEMY_SPAWN_INTERVAL
        self.max_enemies = NORMAL_MAX_ENEMIES if mode == MODE_NORMAL else HELL_MAX_ENEMIES
        self.restart()
