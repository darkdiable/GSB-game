import pygame
from constants import *


class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        self.menu_selection = 0
        self.menu_options = ["Normal Mode", "Hell Mode"]
        self.flash_timer = 0

    def draw_menu(self, surface):
        surface.fill(BLACK)

        self.flash_timer += 1

        title_shadow = self.font_large.render("CONTRA", True, DARK_RED)
        title_text = self.font_large.render("CONTRA", True, RED)
        title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2
        surface.blit(title_shadow, (title_x + 3, 103))
        surface.blit(title_text, (title_x, 100))

        subtitle = self.font_medium.render("Jungle Mission", True, ORANGE)
        sub_x = SCREEN_WIDTH // 2 - subtitle.get_width() // 2
        surface.blit(subtitle, (sub_x, 170))

        deco_y = 230
        pygame.draw.line(surface, RED, (SCREEN_WIDTH // 2 - 150, deco_y),
                         (SCREEN_WIDTH // 2 + 150, deco_y), 2)
        pygame.draw.line(surface, ORANGE, (SCREEN_WIDTH // 2 - 140, deco_y + 4),
                         (SCREEN_WIDTH // 2 + 140, deco_y + 4), 1)

        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = self.font_medium.render(option, True, color)
            tx = SCREEN_WIDTH // 2 - text.get_width() // 2
            ty = 300 + i * 70

            if i == self.menu_selection:
                if (self.flash_timer // 20) % 2 == 0:
                    arrow = self.font_medium.render(">", True, YELLOW)
                    surface.blit(arrow, (tx - 40, ty))
                sel_rect = pygame.Rect(tx - 10, ty - 5,
                                       text.get_width() + 20, text.get_height() + 10)
                pygame.draw.rect(surface, YELLOW, sel_rect, 2)

            surface.blit(text, (tx, ty))

        controls = [
            "Controls:",
            "W - Aim Up  |  A - Move Left  |  S - Crouch/Down  |  D - Move Right",
            "J - Shoot  |  K - Jump",
            "ESC - Pause  |  Enter - Select",
        ]
        for i, line in enumerate(controls):
            color = ORANGE if i == 0 else LIGHT_GRAY
            font = self.font_small if i == 0 else self.font_tiny
            text = font.render(line, True, color)
            tx = SCREEN_WIDTH // 2 - text.get_width() // 2
            surface.blit(text, (tx, 470 + i * 28))

    def draw_hud(self, surface, player, difficulty):
        hud_bg = pygame.Surface((SCREEN_WIDTH, 36), pygame.SRCALPHA)
        hud_bg.fill((0, 0, 0, 150))
        surface.blit(hud_bg, (0, 0))

        lives_text = self.font_small.render(f"LIVES: {player.lives}", True, WHITE)
        surface.blit(lives_text, (10, 6))

        for i in range(player.lives):
            pygame.draw.rect(surface, RED, (110 + i * 20, 12, 12, 16))
            pygame.draw.rect(surface, SKIN, (112 + i * 20, 8, 8, 6))

        score_text = self.font_small.render(f"SCORE: {player.score:08d}", True, YELLOW)
        surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 6))

        diff_color = RED if difficulty == DIFFICULTY_HELL else GREEN
        diff_text = self.font_small.render(difficulty.upper(), True, diff_color)
        surface.blit(diff_text, (SCREEN_WIDTH - diff_text.get_width() - 10, 6))

    def draw_game_over(self, surface, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        go_text = self.font_large.render("GAME OVER", True, RED)
        go_x = SCREEN_WIDTH // 2 - go_text.get_width() // 2
        surface.blit(go_text, (go_x, 200))

        score_text = self.font_medium.render(f"SCORE: {score:08d}", True, YELLOW)
        sx = SCREEN_WIDTH // 2 - score_text.get_width() // 2
        surface.blit(score_text, (sx, 280))

        restart_text = self.font_small.render("Press ENTER to restart", True, WHITE)
        rx = SCREEN_WIDTH // 2 - restart_text.get_width() // 2
        surface.blit(restart_text, (rx, 360))

        menu_text = self.font_small.render("Press ESC for menu", True, LIGHT_GRAY)
        mx = SCREEN_WIDTH // 2 - menu_text.get_width() // 2
        surface.blit(menu_text, (mx, 400))

    def draw_victory(self, surface, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        self.flash_timer += 1
        color = YELLOW if (self.flash_timer // 15) % 2 == 0 else ORANGE

        vic_text = self.font_large.render("MISSION COMPLETE!", True, color)
        vx = SCREEN_WIDTH // 2 - vic_text.get_width() // 2
        surface.blit(vic_text, (vx, 180))

        score_text = self.font_medium.render(f"FINAL SCORE: {score:08d}", True, YELLOW)
        sx = SCREEN_WIDTH // 2 - score_text.get_width() // 2
        surface.blit(score_text, (sx, 260))

        rank = "S" if score > 50000 else "A" if score > 30000 else "B" if score > 15000 else "C"
        rank_color = YELLOW if rank == "S" else ORANGE if rank == "A" else WHITE
        rank_text = self.font_large.render(f"RANK: {rank}", True, rank_color)
        rrx = SCREEN_WIDTH // 2 - rank_text.get_width() // 2
        surface.blit(rank_text, (rrx, 320))

        restart_text = self.font_small.render("Press ENTER to play again", True, WHITE)
        rx = SCREEN_WIDTH // 2 - restart_text.get_width() // 2
        surface.blit(restart_text, (rx, 420))

        menu_text = self.font_small.render("Press ESC for menu", True, LIGHT_GRAY)
        mx = SCREEN_WIDTH // 2 - menu_text.get_width() // 2
        surface.blit(menu_text, (mx, 460))

    def draw_pause(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        pause_text = self.font_large.render("PAUSED", True, YELLOW)
        px = SCREEN_WIDTH // 2 - pause_text.get_width() // 2
        surface.blit(pause_text, (px, 220))

        resume_text = self.font_small.render("Press ESC to resume", True, WHITE)
        rx = SCREEN_WIDTH // 2 - resume_text.get_width() // 2
        surface.blit(resume_text, (rx, 300))

        menu_text = self.font_small.render("Press Q to quit to menu", True, LIGHT_GRAY)
        mx = SCREEN_WIDTH // 2 - menu_text.get_width() // 2
        surface.blit(menu_text, (mx, 340))

    def menu_up(self):
        self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)

    def menu_down(self):
        self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)

    def get_selected_difficulty(self):
        if self.menu_selection == 0:
            return DIFFICULTY_NORMAL
        return DIFFICULTY_HELL
