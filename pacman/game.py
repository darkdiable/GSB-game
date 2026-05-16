import pygame
from constants import *
from maze import Maze
from pacman import Pacman
from ghost import Ghost


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 24)
        self.large_font = pygame.font.SysFont('arial', 48)
        self.running = True
        self.game_state = "start"
        self.score = 0
        self.lives = 3
        self.level = 1
        self._init_game_objects()

    def _init_game_objects(self):
        self.maze = Maze()
        self.pacman = Pacman(self.maze.pacman_start[0], self.maze.pacman_start[1])
        self.ghosts = []
        ghost_colors = [RED, PINK, CYAN, ORANGE]
        ghost_names = ["blinky", "pinky", "inky", "clyde"]

        for i, (color, name) in enumerate(zip(ghost_colors, ghost_names)):
            if i < len(self.maze.ghost_starts):
                start_pos = self.maze.ghost_starts[i]
            else:
                start_pos = self.maze.ghost_starts[0]
            ghost = Ghost(start_pos[0], start_pos[1], color, name)
            self.ghosts.append(ghost)

    def _reset_positions(self):
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()

    def _restart_game(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self._init_game_objects()
        self.game_state = "playing"

    def _next_level(self):
        self.level += 1
        self._init_game_objects()
        self.game_state = "playing"

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "start":
                    if event.key == pygame.K_SPACE:
                        self._restart_game()
                elif self.game_state == "gameover":
                    if event.key == pygame.K_SPACE:
                        self._restart_game()
                elif self.game_state == "win":
                    if event.key == pygame.K_SPACE:
                        self._restart_game()
                elif self.game_state == "playing":
                    if event.key == pygame.K_a:
                        self.pacman.set_direction(LEFT, self.maze)
                    elif event.key == pygame.K_d:
                        self.pacman.set_direction(RIGHT, self.maze)
                    elif event.key == pygame.K_w:
                        self.pacman.set_direction(UP, self.maze)
                    elif event.key == pygame.K_s:
                        self.pacman.set_direction(DOWN, self.maze)
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "paused"
                elif self.game_state == "paused":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "playing"

    def _update(self, dt):
        if self.game_state != "playing":
            return

        self.pacman.update(self.maze)

        pacman_rect = self.pacman.get_rect()
        eat_radius = CELL_SIZE // 2

        pellets_to_remove = []
        for px, py in self.maze.pellets:
            if abs(self.pacman.x - px) < eat_radius and abs(self.pacman.y - py) < eat_radius:
                pellets_to_remove.append((px, py))
                self.score += 10
        for p in pellets_to_remove:
            self.maze.remove_pellet(*p)

        power_pellets_to_remove = []
        for px, py in self.maze.power_pellets:
            if abs(self.pacman.x - px) < eat_radius and abs(self.pacman.y - py) < eat_radius:
                power_pellets_to_remove.append((px, py))
                self.score += 50
                for ghost in self.ghosts:
                    ghost.make_edible()
        for p in power_pellets_to_remove:
            self.maze.remove_power_pellet(*p)

        for ghost in self.ghosts:
            ghost.update(self.maze, self.pacman, dt)

        for ghost in self.ghosts:
            if not ghost.respawning:
                pacman_rect = self.pacman.get_rect()
                ghost_rect = ghost.get_rect()
                if pacman_rect.colliderect(ghost_rect):
                    if ghost.edible:
                        ghost.start_respawn()
                        self.score += 200
                    else:
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_state = "gameover"
                        else:
                            self._reset_positions()

        if self.maze.all_pellets_eaten():
            self.game_state = "win"

    def _draw(self):
        self.screen.fill(BLACK)

        if self.game_state == "start":
            self._draw_start_screen()
        elif self.game_state == "gameover":
            self._draw_gameover_screen()
        elif self.game_state == "win":
            self._draw_win_screen()
        else:
            self.maze.draw(self.screen)
            self.pacman.draw(self.screen)
            for ghost in self.ghosts:
                ghost.draw(self.screen)
            self._draw_ui()
            if self.game_state == "paused":
                self._draw_paused_screen()

        pygame.display.flip()

    def _draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, HEIGHT + 10))

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, HEIGHT + 10))

        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - 40, HEIGHT + 10))

    def _draw_start_screen(self):
        title = self.large_font.render("PAC-MAN", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

        instructions = [
            "Use WASD to move",
            "Eat all pellets to win",
            "Avoid the ghosts!",
            "",
            "Press SPACE to start",
        ]

        for i, line in enumerate(instructions):
            text = self.font.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 + i * 35))

    def _draw_gameover_screen(self):
        self.maze.draw(self.screen)
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        gameover_text = self.large_font.render("GAME OVER", True, RED)
        self.screen.blit(gameover_text, (SCREEN_WIDTH // 2 - gameover_text.get_width() // 2, 250))

        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 320))

        restart_text = self.font.render("Press SPACE to restart", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 380))

    def _draw_win_screen(self):
        win_text = self.large_font.render("YOU WIN!", True, YELLOW)
        self.screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 250))

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 320))

        next_text = self.font.render("Press SPACE for next level", True, WHITE)
        self.screen.blit(next_text, (SCREEN_WIDTH // 2 - next_text.get_width() // 2, 380))

    def _draw_paused_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        paused_text = self.large_font.render("PAUSED", True, YELLOW)
        self.screen.blit(paused_text, (SCREEN_WIDTH // 2 - paused_text.get_width() // 2, 300))

        resume_text = self.font.render("Press ESC to resume", True, WHITE)
        self.screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, 360))

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()
