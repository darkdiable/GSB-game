import pygame
from . import config


class UI:
    def __init__(self):
        self.font_large = pygame.font.SysFont('arial', 24, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 18)
        self.font_small = pygame.font.SysFont('arial', 14)

    def draw(self, surface, score, player, wave):
        self._draw_score(surface, score)
        self._draw_health(surface, player)
        self._draw_bombs(surface, player)
        self._draw_wave(surface, wave)

    def _draw_score(self, surface, score):
        score_text = self.font_large.render(f"SCORE: {score}", True, config.WHITE)
        surface.blit(score_text, (10, 10))

    def _draw_health(self, surface, player):
        bar_x = 10
        bar_y = 40
        bar_w = 120
        bar_h = 12
        pygame.draw.rect(surface, config.DARK_GRAY, (bar_x, bar_y, bar_w, bar_h))
        fill = int(bar_w * player.health / player.max_health)
        if player.health > player.max_health * 0.5:
            color = (0, 200, 0)
        elif player.health > player.max_health * 0.25:
            color = config.YELLOW
        else:
            color = config.RED
        pygame.draw.rect(surface, color, (bar_x, bar_y, fill, bar_h))
        pygame.draw.rect(surface, config.WHITE, (bar_x, bar_y, bar_w, bar_h), 1)
        hp_text = self.font_small.render(f"HP: {player.health}", True, config.WHITE)
        surface.blit(hp_text, (bar_x + bar_w + 5, bar_y - 1))

    def _draw_bombs(self, surface, player):
        x = 10
        y = 58
        text = self.font_small.render("BOMBS:", True, config.WHITE)
        surface.blit(text, (x, y))
        for i in range(player.max_bombs):
            bx = x + 55 + i * 16
            by = y + 2
            if i < player.bombs:
                pygame.draw.circle(surface, config.DARK_GRAY, (bx, by + 5), 5)
                pygame.draw.circle(surface, config.GRAY, (bx, by + 5), 3)
            else:
                pygame.draw.circle(surface, (40, 40, 40), (bx, by + 5), 5, 1)

    def _draw_wave(self, surface, wave):
        text = self.font_small.render(f"WAVE: {wave}", True, config.WHITE)
        surface.blit(text, (config.SCREEN_WIDTH - 80, 10))

    def draw_game_over(self, surface, score):
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        go_text = self.font_large.render("GAME OVER", True, config.RED)
        go_rect = go_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 30))
        surface.blit(go_text, go_rect)
        score_text = self.font_medium.render(f"Final Score: {score}", True, config.WHITE)
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 10))
        surface.blit(score_text, score_rect)
        restart_text = self.font_small.render("Press R to Restart or Q to Quit", True, config.YELLOW)
        restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 45))
        surface.blit(restart_text, restart_rect)
