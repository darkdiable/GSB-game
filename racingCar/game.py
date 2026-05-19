import pygame
from config import *
from player import Player
from vehicles import VehicleManager
from scenery import SceneryManager
from ui import UIManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('赛车游戏 - Racing Car')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'start'

        self.player = Player()
        self.vehicle_manager = VehicleManager()
        self.scenery_manager = SceneryManager()
        self.ui_manager = UIManager()

    def run(self):
        while self.running:
            self._handle_events()

            if self.game_state == 'start':
                self._start_screen()
            elif self.game_state == 'playing':
                self._update()
                self._draw()
            elif self.game_state == 'game_over':
                self._game_over_screen()

            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.game_state == 'start':
                    self.game_state = 'playing'
                elif self.game_state == 'game_over':
                    if event.key == pygame.K_r:
                        self._reset_game()

    def _start_screen(self):
        self.ui_manager.show_start_screen(self.screen)

    def _game_over_screen(self):
        self.ui_manager.show_game_over_screen(self.screen)

    def _update(self):
        keys = pygame.key.get_pressed()

        self.player.update(keys)

        self.scenery_manager.update(self.player.speed, self.ui_manager.score)

        self.vehicle_manager.update(self.player.speed, self.ui_manager.score)

        self.ui_manager.update(self.player.speed, self.player.collisions)

        self._check_collisions()

        if self.player.is_game_over():
            self.game_state = 'game_over'

    def _check_collisions(self):
        player_rect = self.player.get_rect()
        collided_vehicle = self.vehicle_manager.check_collision(player_rect)

        if collided_vehicle:
            if self.player.take_damage():
                self.ui_manager.notify_collision()
                if collided_vehicle in self.vehicle_manager.vehicles:
                    self.vehicle_manager.vehicles.remove(collided_vehicle)

    def _draw(self):
        self.scenery_manager.draw(self.screen)

        self.vehicle_manager.draw(self.screen)

        self.player.draw(self.screen)

        self.ui_manager.draw(self.screen, self.player)

        pygame.display.flip()

    def _reset_game(self):
        self.player.reset()
        self.vehicle_manager.reset()
        self.scenery_manager.reset()
        self.ui_manager.reset()
        self.game_state = 'playing'
