import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MAX_COLLISIONS,
    VEHICLE_SPAWN_INTERVAL_MS, OBSTACLE_SPAWN_INTERVAL_MS,
    WHITE, BLACK, RED, YELLOW, GREEN,
)
from player import Player
from obstacles import VehicleSpawner
from scenery import SceneryManager
from road import Road


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing Car")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 28)
        self.font_small = pygame.font.SysFont("Arial", 20)

        self.player = Player()
        self.spawner = VehicleSpawner()
        self.scenery = SceneryManager()
        self.road = Road()

        self.collisions = 0
        self.distance = 0.0
        self.score = 0
        self.game_over = False
        self.running = True
        self.state = "menu"

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            self._handle_events()

            if self.state == "menu":
                self._draw_menu()
            elif self.state == "playing":
                self._update(dt)
                self._draw()
            elif self.state == "game_over":
                self._draw_game_over()

            pygame.display.flip()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    if event.key == pygame.K_RETURN:
                        self._start_game()
                elif self.state == "game_over":
                    if event.key == pygame.K_RETURN:
                        self._start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                elif self.state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"

    def _start_game(self):
        self.player.reset()
        self.spawner.reset()
        self.scenery.reset()
        self.road.reset()
        self.collisions = 0
        self.distance = 0.0
        self.score = 0
        self.game_over = False
        self.state = "playing"

    def _update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(keys, dt)

        self.road.update(self.player.speed)
        self.scenery.update(self.player.speed, dt)
        self.spawner.update(self.player.speed)

        current_time = pygame.time.get_ticks()
        self.spawner.try_spawn_vehicle(
            current_time, VEHICLE_SPAWN_INTERVAL_MS, OBSTACLE_SPAWN_INTERVAL_MS
        )

        self.distance += self.player.speed * 0.1
        self.score = int(self.distance)

        if not self.player.invincible:
            player_rect = self.player.get_rect()
            hit = self.spawner.check_collision(player_rect)
            if hit:
                self.collisions += 1
                self.player.trigger_invincibility()
                self.player.speed = max(self.player.speed * 0.5, 0)
                if self.collisions >= MAX_COLLISIONS:
                    self.game_over = True
                    self.state = "game_over"

    def _draw(self):
        self.scenery.draw(self.screen)
        self.road.draw(self.screen)
        self.spawner.draw(self.screen)
        self.player.draw(self.screen)
        self._draw_hud()

    def _draw_hud(self):
        speed_text = self.font_small.render(f"Speed: {self.player.speed:.1f} km/h", True, WHITE)
        self.screen.blit(speed_text, (10, 10))

        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 35))

        collision_text = self.font_small.render(f"Collisions: {self.collisions}/{MAX_COLLISIONS}", True, WHITE)
        self.screen.blit(collision_text, (10, 60))

        bar_x = 10
        bar_y = 90
        bar_w = 150
        bar_h = 12
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
        fill_w = int(bar_w * self.player.speed / self.player.max_speed)
        bar_color = GREEN if self.player.speed < self.player.max_speed * 0.7 else YELLOW if self.player.speed < self.player.max_speed * 0.9 else RED
        pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, fill_w, bar_h))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 1)

        heart_x = SCREEN_WIDTH - 30
        for i in range(MAX_COLLISIONS):
            hx = heart_x - i * 28
            color = RED if i < self.collisions else (80, 80, 80)
            self._draw_heart(hx, 18, 10, color)

    def _draw_heart(self, cx, cy, size, color):
        pygame.draw.circle(self.screen, color, (cx - size // 3, cy), size // 2)
        pygame.draw.circle(self.screen, color, (cx + size // 3, cy), size // 2)
        points = [
            (cx - size, cy + 2),
            (cx, cy + size),
            (cx + size, cy + 2),
        ]
        pygame.draw.polygon(self.screen, color, points)

    def _draw_menu(self):
        self.screen.fill((20, 20, 40))

        title = self.font_large.render("RACING CAR", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title, title_rect)

        subtitle = self.font_medium.render("Road Adventure", True, YELLOW)
        sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 170))
        self.screen.blit(subtitle, sub_rect)

        instructions = [
            "W - Accelerate",
            "S - Brake / Decelerate",
            "A - Move Left",
            "D - Move Right",
            f"Avoid vehicles & obstacles! {MAX_COLLISIONS} hits = Game Over",
        ]
        for i, text in enumerate(instructions):
            surf = self.font_small.render(text, True, WHITE)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, 260 + i * 35))
            self.screen.blit(surf, rect)

        start_text = self.font_medium.render("Press ENTER to Start", True, GREEN)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 480))
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            self.screen.blit(start_text, start_rect)

    def _draw_game_over(self):
        self.scenery.draw(self.screen)
        self.road.draw(self.screen)
        self.spawner.draw(self.screen)
        self.player.draw(self.screen)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        go_text = self.font_large.render("GAME OVER", True, RED)
        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(go_text, go_rect)

        score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(score_text, score_rect)

        collision_text = self.font_medium.render(
            f"Collisions: {self.collisions}/{MAX_COLLISIONS}", True, YELLOW
        )
        col_rect = collision_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
        self.screen.blit(collision_text, col_rect)

        restart_text = self.font_small.render("Press ENTER to Restart | ESC for Menu", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
        self.screen.blit(restart_text, restart_rect)
