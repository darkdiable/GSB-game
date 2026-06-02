import pygame
from constants import *
from player import Player
from enemy import EnemySpawner
from level import Level
from ui import UI


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.state = STATE_MENU
        self.difficulty = DIFFICULTY_NORMAL
        self.player = None
        self.level = None
        self.enemy_spawner = None
        self.running = True

    def run(self):
        while self.running:
            if self.state == STATE_MENU:
                self._handle_menu()
            elif self.state == STATE_PLAYING:
                self._handle_playing()
            elif self.state == STATE_GAME_OVER:
                self._handle_game_over()
            elif self.state == STATE_VICTORY:
                self._handle_victory()
            elif self.state == STATE_PAUSED:
                self._handle_paused()
            self.clock.tick(FPS)
        return False

    def _init_game(self):
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.player = Player(100, GROUND_Y - 60, lives=settings["player_lives"])
        self.level = Level()
        self.enemy_spawner = EnemySpawner(settings)
        self._setup_enemy_spawn_points()
        self.state = STATE_PLAYING

    def _setup_enemy_spawn_points(self):
        sp = self.enemy_spawner
        sp.add_spawn_point(400, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(600, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(850, GROUND_Y - 44, "soldier")

        sp.add_spawn_point(1400, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(1500, GROUND_Y - 124, "soldier")
        sp.add_spawn_point(1650, GROUND_Y - 204, "sniper")
        sp.add_spawn_point(1900, GROUND_Y - 144, "soldier")
        sp.add_spawn_point(2100, GROUND_Y - 224, "sniper")
        sp.add_spawn_point(2300, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(2400, GROUND_Y - 44, "soldier")

        sp.add_spawn_point(3300, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(3500, GROUND_Y - 44, "sniper")
        sp.add_spawn_point(3650, GROUND_Y - 44, "turret")
        sp.add_spawn_point(3900, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(4100, GROUND_Y - 44, "sniper")

        sp.add_spawn_point(4900, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(5100, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(5300, GROUND_Y - 44, "turret")
        sp.add_spawn_point(5500, GROUND_Y - 44, "sniper")
        sp.add_spawn_point(5700, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(5900, GROUND_Y - 44, "soldier")
        sp.add_spawn_point(6050, GROUND_Y - 44, "sniper")

    def _handle_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.ui.menu_up()
                elif event.key == pygame.K_DOWN:
                    self.ui.menu_down()
                elif event.key == pygame.K_RETURN:
                    self.difficulty = self.ui.get_selected_difficulty()
                    self._init_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

        self.ui.draw_menu(self.screen)
        pygame.display.flip()

    def _handle_playing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    if self.player and self.player.alive:
                        self.player.jump()
                if event.key == pygame.K_ESCAPE:
                    self.state = STATE_PAUSED

        keys = pygame.key.get_pressed()
        if not self.player:
            return

        game_over = self.player.update(keys, self.level.get_platforms(),
                                       self.level.get_camera_x())
        if game_over:
            self.state = STATE_GAME_OVER
            return

        self.level.update(self.player)
        camera_x = self.level.get_camera_x()

        self.enemy_spawner.update(self.player, self.level.get_platforms(), camera_x)

        all_player_bullets = list(self.player.bullets)
        scores = self.enemy_spawner.check_bullet_hits(all_player_bullets)
        for s in scores:
            self.player.score += s

        for bullet in self.player.bullets[:]:
            if not bullet.active:
                self.player.bullets.remove(bullet)

        if self.player.alive and not self.player.invincible:
            if self.enemy_spawner.check_player_hit(self.player.get_rect()):
                self.player.hit()

        if self.level.is_level_end(self.player.rect.x):
            self.state = STATE_VICTORY

        self._draw_game()

    def _draw_game(self):
        self.level.draw(self.screen)
        camera_x = self.level.get_camera_x()

        self.enemy_spawner.draw(self.screen, camera_x)

        self.player.draw(self.screen, camera_x)

        for bullet in self.player.bullets:
            bullet.draw(self.screen, camera_x)

        self.ui.draw_hud(self.screen, self.player, self.difficulty)

        pygame.display.flip()

    def _handle_game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._init_game()
                elif event.key == pygame.K_ESCAPE:
                    self.state = STATE_MENU

        self._draw_game()
        self.ui.draw_game_over(self.screen, self.player.score if self.player else 0)
        pygame.display.flip()

    def _handle_victory(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._init_game()
                elif event.key == pygame.K_ESCAPE:
                    self.state = STATE_MENU

        self._draw_game()
        self.ui.draw_victory(self.screen, self.player.score if self.player else 0)
        pygame.display.flip()

    def _handle_paused(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = STATE_PLAYING
                elif event.key == pygame.K_q:
                    self.state = STATE_MENU

        self._draw_game()
        self.ui.draw_pause(self.screen)
        pygame.display.flip()
