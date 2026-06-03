import pygame
from . import config


class Menu:
    def __init__(self):
        self.font_title = pygame.font.SysFont('arial', 48, bold=True)
        self.font_subtitle = pygame.font.SysFont('arial', 20)
        self.font_text = pygame.font.SysFont('arial', 16)
        self.font_small = pygame.font.SysFont('arial', 14)
        self.blink_timer = 0

    def draw(self, surface):
        surface.fill((10, 20, 50))
        self._draw_title_bg(surface)
        title = self.font_title.render("1942", True, config.YELLOW)
        title_shadow = self.font_title.render("1942", True, (80, 60, 0))
        tr = title.get_rect(center=(config.SCREEN_WIDTH // 2, 80))
        surface.blit(title_shadow, (tr.x + 2, tr.y + 2))
        surface.blit(title, tr)
        subtitle = self.font_subtitle.render("DOGFIGHT", True, config.WHITE)
        sr = subtitle.get_rect(center=(config.SCREEN_WIDTH // 2, 120))
        surface.blit(subtitle, sr)
        self._draw_bomber_art(surface, config.SCREEN_WIDTH // 2, 170)
        self._draw_instructions(surface)
        self.blink_timer = (self.blink_timer + 1) % 60
        if self.blink_timer < 40:
            start_text = self.font_subtitle.render("Press ENTER to Start", True, config.YELLOW)
            start_rect = start_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 50))
            surface.blit(start_text, start_rect)
        quit_text = self.font_small.render("Press Q to Quit", True, config.GRAY)
        quit_rect = quit_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 25))
        surface.blit(quit_text, quit_rect)

    def _draw_title_bg(self, surface):
        for y in range(0, config.SCREEN_HEIGHT, 3):
            wave_val = (y * 0.02) + (self.blink_timer * 0.03)
            r = int(10 + 10 * abs(pygame.math.Vector2(1, 0).rotate(wave_val * 57).x))
            g = int(20 + 15 * abs(pygame.math.Vector2(1, 0).rotate(wave_val * 40).x))
            b = int(50 + 20 * abs(pygame.math.Vector2(1, 0).rotate(wave_val * 30).x))
            pygame.draw.line(surface, (r, g, b), (0, y), (config.SCREEN_WIDTH, y))

    def _draw_bomber_art(self, surface, cx, cy):
        pygame.draw.ellipse(surface, (70, 110, 70), (cx - 20, cy - 8, 40, 24))
        pygame.draw.polygon(surface, (90, 90, 100), [
            (cx, cy - 12), (cx - 8, cy), (cx + 8, cy)
        ])
        pygame.draw.polygon(surface, (80, 80, 90), [
            (cx - 30, cy + 6), (cx - 16, cy - 4), (cx - 14, cy + 10)
        ])
        pygame.draw.polygon(surface, (80, 80, 90), [
            (cx + 30, cy + 6), (cx + 16, cy - 4), (cx + 14, cy + 10)
        ])
        flame_off = 4 if self.blink_timer < 30 else 0
        for ex in [cx - 18, cx - 8, cx + 8, cx + 18]:
            pygame.draw.polygon(surface, config.ORANGE, [
                (ex - 2, cy + 12), (ex, cy + 18 + flame_off), (ex + 2, cy + 12)
            ])
            pygame.draw.polygon(surface, config.YELLOW, [
                (ex - 1, cy + 12), (ex, cy + 15 + flame_off), (ex + 1, cy + 12)
            ])

    def _draw_instructions(self, surface):
        instructions = [
            ("=== OPERATION MANUAL ===", config.YELLOW, True),
            ("", config.WHITE, False),
            ("MOVEMENT:", config.ORANGE, True),
            ("  Arrow Keys / WASD  -  Move bomber", config.WHITE, False),
            ("", config.WHITE, False),
            ("ATTACK:", config.ORANGE, True),
            ("  SPACE  -  Fire machine guns", config.WHITE, False),
            ("  B  -  Drop bomb on ships/islands", config.WHITE, False),
            ("", config.WHITE, False),
            ("OBJECTIVES:", config.ORANGE, True),
            ("  * Shoot down enemy fighters & bombers", config.WHITE, False),
            ("  * Bomb warships on the sea", config.WHITE, False),
            ("  * Destroy AA guns on islands", config.WHITE, False),
            ("", config.WHITE, False),
            ("TIPS:", config.ORANGE, True),
            ("  * Bombs deal area damage", config.WHITE, False),
            ("  * Dodge enemy fire to survive", config.WHITE, False),
            ("  * Press P to pause the game", config.WHITE, False),
        ]
        y = 220
        for text, color, bold in instructions:
            if text:
                font = self.font_text if not bold else self.font_subtitle
                rendered = font.render(text, True, color)
                rect = rendered.get_rect(center=(config.SCREEN_WIDTH // 2, y))
                surface.blit(rendered, rect)
            y += 22 if not bold else 26
