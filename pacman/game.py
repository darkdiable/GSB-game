import pygame
import sys
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_HEIGHT,
    FPS, BLACK, WHITE, YELLOW,
    UP, DOWN, LEFT, RIGHT,
    DOT_POINTS, POWER_DOT_POINTS, GHOST_POINTS
)
from maze import Maze
from pacman import Pacman
from ghost import Ghost


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pacman")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.large_font = pygame.font.SysFont('Arial', 48, bold=True)

        self.maze = Maze()
        self.pacman = Pacman()
        self.ghosts = [
            Ghost('blinky', 13, 11),
            Ghost('pinky', 12, 14),
            Ghost('inky', 14, 14),
            Ghost('clyde', 13, 14)
        ]

        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.level = 1
        self.state = 'playing'
        self.game_over = False
        self.game_won = False
        self.pause_timer = 0
        self.last_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.game_over or self.game_won:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.pacman.set_direction(LEFT)
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.pacman.set_direction(RIGHT)
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.pacman.set_direction(UP)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.pacman.set_direction(DOWN)
                    elif event.key == pygame.K_p:
                        if self.state == 'playing':
                            self.state = 'paused'
                        elif self.state == 'paused':
                            self.state = 'playing'

    def update(self):
        if self.state != 'playing':
            return

        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        if self.pause_timer > 0:
            self.pause_timer -= delta_time
            if self.pause_timer <= 0:
                if self.game_over or self.game_won:
                    return
                self._reset_positions()
            return

        self.pacman.update(self.maze)

        if self.pacman._is_centered():
            self._check_dot_collision()

        for ghost in self.ghosts:
            ghost.update(self.maze, self.pacman, delta_time)

        self._check_ghost_collisions()
        self._check_level_complete()

    def _check_dot_collision(self):
        px, py = self.pacman.get_grid_position()
        eaten, points = self.maze.eat_dot(px, py)
        if eaten:
            self.score += points
            if points == POWER_DOT_POINTS:
                for ghost in self.ghosts:
                    ghost.make_vulnerable()
            if self.score > self.high_score:
                self.high_score = self.score

    def _check_ghost_collisions(self):
        for ghost in self.ghosts:
            if self.pacman.check_collision(ghost):
                if ghost.vulnerable and not ghost.eaten:
                    ghost.get_eaten()
                    self.score += GHOST_POINTS
                elif not ghost.eaten:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    self.pacman.die()
                    self.pause_timer = 2000
                    return

    def _check_level_complete(self):
        if self.maze.is_complete():
            self.level += 1
            self.game_won = True
            self.pause_timer = 3000

    def _reset_positions(self):
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()

    def reset_game(self):
        self.maze = Maze()
        self.pacman = Pacman()
        self.ghosts = [
            Ghost('blinky', 13, 11),
            Ghost('pinky', 12, 14),
            Ghost('inky', 14, 14),
            Ghost('clyde', 13, 14)
        ]
        self.score = 0
        self.lives = 3
        self.level = 1
        self.state = 'playing'
        self.game_over = False
        self.game_won = False
        self.pause_timer = 0
        self.last_time = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill(BLACK)

        self.maze.draw(self.screen)

        for ghost in self.ghosts:
            ghost.draw(self.screen)

        self.pacman.draw(self.screen)

        self._draw_hud()

        if self.state == 'paused':
            self._draw_centered_text("PAUSED", YELLOW, SCREEN_HEIGHT // 2)

        if self.pause_timer > 0:
            if self.game_over:
                self._draw_centered_text("GAME OVER", YELLOW, SCREEN_HEIGHT // 2 - 30)
                self._draw_centered_text("Press R to Restart", WHITE, SCREEN_HEIGHT // 2 + 30, 24)
            elif self.game_won:
                self._draw_centered_text(f"LEVEL {self.level - 1} COMPLETE!", YELLOW, SCREEN_HEIGHT // 2 - 30)
                self._draw_centered_text("Press R to Play Again", WHITE, SCREEN_HEIGHT // 2 + 30, 24)

        pygame.display.flip()

    def _draw_hud(self):
        score_text = self.font.render(f"SCORE: {self.score}", True, WHITE)
        high_score_text = self.font.render(f"HIGH: {self.high_score}", True, WHITE)
        level_text = self.font.render(f"LEVEL: {self.level}", True, WHITE)
        lives_text = self.font.render(f"LIVES: {self.lives}", True, WHITE)

        self.screen.blit(score_text, (20, GRID_HEIGHT * CELL_SIZE + 15))
        self.screen.blit(high_score_text, (220, GRID_HEIGHT * CELL_SIZE + 15))
        self.screen.blit(level_text, (460, GRID_HEIGHT * CELL_SIZE + 15))
        self.screen.blit(lives_text, (660, GRID_HEIGHT * CELL_SIZE + 15))

        for i in range(self.lives):
            mini_x = 780 + i * 35
            mini_y = GRID_HEIGHT * CELL_SIZE + 30
            pygame.draw.circle(self.screen, YELLOW, (mini_x, mini_y), 10)
            pygame.draw.polygon(
                self.screen, BLACK,
                [
                    (mini_x, mini_y),
                    (mini_x + 10, mini_y - 5),
                    (mini_x + 10, mini_y + 5)
                ]
            )

    def _draw_centered_text(self, text, color, y_pos, font_size=48):
        if font_size == 48:
            text_surface = self.large_font.render(text, True, color)
        else:
            font = pygame.font.SysFont('Arial', font_size, bold=True)
            text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
