import pygame
import random
import math
from .config import *
from .player import PlayerSubmarine
from .enemies import Destroyer, EnemySubmarine
from .effects import Explosion, WaterBubble


class GameEngine:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'menu'
        self.score = 0
        self.high_score = 0

        self.player = PlayerSubmarine()
        self.missiles = []
        self.torpedoes = []
        self.destroyers = []
        self.enemy_subs = []
        self.depth_charges = []
        self.enemy_torpedoes = []
        self.explosions = []
        self.water_bubbles = []

        self.destroyer_spawn_timer = DESTROYER_SPAWN_RATE
        self.sub_spawn_timer = ENEMY_SUB_SPAWN_RATE
        self.bubble_spawn_timer = 0

        self.keys = {}
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self._init_fonts()

    def _init_fonts(self):
        try:
            self.font_large = pygame.font.SysFont('simhei,microsoftyahei,arial', 48)
            self.font_medium = pygame.font.SysFont('simhei,microsoftyahei,arial', 32)
            self.font_small = pygame.font.SysFont('simhei,microsoftyahei,arial', 20)
        except:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 20)

    def reset_game(self):
        self.player = PlayerSubmarine()
        self.missiles = []
        self.torpedoes = []
        self.destroyers = []
        self.enemy_subs = []
        self.depth_charges = []
        self.enemy_torpedoes = []
        self.explosions = []
        self.water_bubbles = []
        self.destroyer_spawn_timer = DESTROYER_SPAWN_RATE
        self.sub_spawn_timer = ENEMY_SUB_SPAWN_RATE
        self.score = 0
        self.game_state = 'playing'

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == 'playing':
                        self.game_state = 'paused'
                    elif self.game_state == 'paused':
                        self.game_state = 'playing'
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if self.game_state == 'menu':
                        self.reset_game()
                    elif self.game_state == 'gameover':
                        self.game_state = 'menu'
            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False

    def update(self):
        if self.game_state != 'playing':
            return

        move_y = 0
        if self.keys.get(pygame.K_UP) or self.keys.get(pygame.K_w):
            move_y = -1
        elif self.keys.get(pygame.K_DOWN) or self.keys.get(pygame.K_s):
            move_y = 1
        self.player.move(move_y)

        if self.keys.get(pygame.K_SPACE):
            missile = self.player.fire_missile()
            if missile:
                self.missiles.append(missile)

        if self.keys.get(pygame.K_LCTRL) or self.keys.get(pygame.K_RCTRL):
            torpedo = self.player.fire_torpedo()
            if torpedo:
                self.torpedoes.append(torpedo)

        self.player.update()

        self.destroyer_spawn_timer -= 1
        if self.destroyer_spawn_timer <= 0:
            self.destroyer_spawn_timer = DESTROYER_SPAWN_RATE + random.randint(-50, 50)
            self.destroyers.append(Destroyer())

        self.sub_spawn_timer -= 1
        if self.sub_spawn_timer <= 0:
            self.sub_spawn_timer = ENEMY_SUB_SPAWN_RATE + random.randint(-40, 40)
            self.enemy_subs.append(EnemySubmarine())

        self.bubble_spawn_timer -= 1
        if self.bubble_spawn_timer <= 0:
            self.bubble_spawn_timer = random.randint(10, 30)
            self.water_bubbles.append(WaterBubble())

        for destroyer in self.destroyers[:]:
            destroyer.update()
            bomb = destroyer.drop_depth_charge(self.player.y)
            if bomb:
                self.depth_charges.append(bomb)
            if not destroyer.active:
                self.destroyers.remove(destroyer)

        for sub in self.enemy_subs[:]:
            sub.update()
            torpedo = sub.fire_torpedo(self.player.x)
            if torpedo:
                self.enemy_torpedoes.append(torpedo)
            if not sub.active:
                self.enemy_subs.remove(sub)

        for missile in self.missiles[:]:
            missile.update()
            if not missile.active:
                self.missiles.remove(missile)

        for torpedo in self.torpedoes[:]:
            torpedo.update()
            if not torpedo.active:
                self.torpedoes.remove(torpedo)

        for charge in self.depth_charges[:]:
            charge.update()
            if not charge.active:
                self.depth_charges.remove(charge)

        for torpedo in self.enemy_torpedoes[:]:
            torpedo.update()
            if not torpedo.active:
                self.enemy_torpedoes.remove(torpedo)

        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.active:
                self.explosions.remove(explosion)

        for bubble in self.water_bubbles[:]:
            if not bubble.update():
                self.water_bubbles.remove(bubble)

        self._check_collisions()

        if self.score > self.high_score:
            self.high_score = self.score

    def _check_collisions(self):
        player_rect = self.player.get_rect()

        for missile in self.missiles[:]:
            missile_rect = missile.get_rect()
            for destroyer in self.destroyers[:]:
                if missile_rect.colliderect(destroyer.get_rect()):
                    if destroyer.take_damage(missile.damage):
                        self.explosions.append(Explosion(destroyer.x, destroyer.y, 'large'))
                        self.score += 100
                    else:
                        self.explosions.append(Explosion(missile.x, missile.y, 'small'))
                    missile.active = False
                    self.missiles.remove(missile)
                    break

            if missile in self.missiles:
                for sub in self.enemy_subs[:]:
                    if missile_rect.colliderect(sub.get_rect()):
                        if sub.take_damage(missile.damage):
                            self.explosions.append(Explosion(sub.x, sub.y, 'large'))
                            self.score += 80
                        else:
                            self.explosions.append(Explosion(missile.x, missile.y, 'small'))
                        missile.active = False
                        if missile in self.missiles:
                            self.missiles.remove(missile)
                        break

        for torpedo in self.torpedoes[:]:
            torpedo_rect = torpedo.get_rect()
            for sub in self.enemy_subs[:]:
                if torpedo_rect.colliderect(sub.get_rect()):
                    if sub.take_damage(torpedo.damage):
                        self.explosions.append(Explosion(sub.x, sub.y, 'large'))
                        self.score += 80
                    else:
                        self.explosions.append(Explosion(torpedo.x, torpedo.y, 'small'))
                    torpedo.active = False
                    self.torpedoes.remove(torpedo)
                    break

        for charge in self.depth_charges[:]:
            if charge.get_rect().colliderect(player_rect):
                if self.player.take_damage(charge.damage):
                    self.explosions.append(Explosion(self.player.x, self.player.y, 'large'))
                    self.game_state = 'gameover'
                else:
                    self.explosions.append(Explosion(charge.x, charge.y, 'medium'))
                charge.active = False
                self.depth_charges.remove(charge)

        for torpedo in self.enemy_torpedoes[:]:
            if torpedo.get_rect().colliderect(player_rect):
                if self.player.take_damage(torpedo.damage):
                    self.explosions.append(Explosion(self.player.x, self.player.y, 'large'))
                    self.game_state = 'gameover'
                else:
                    self.explosions.append(Explosion(torpedo.x, torpedo.y, 'medium'))
                torpedo.active = False
                self.enemy_torpedoes.remove(torpedo)

    def draw(self):
        self.screen.fill(SKY_BLUE)

        pygame.draw.rect(self.screen, OCEAN_DEEP,
                        (0, WATER_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT - WATER_LEVEL))

        for i in range(5):
            y = WATER_LEVEL + i * 20
            alpha = 255 - i * 40
            color = (min(OCEAN_LIGHT[0] + alpha // 10, 255),
                    min(OCEAN_LIGHT[1] + alpha // 10, 255),
                    min(OCEAN_LIGHT[2] + alpha // 10, 255))
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y), 1)

        wave_offset = pygame.time.get_ticks() // 50
        for x in range(0, SCREEN_WIDTH, 8):
            y = WATER_LEVEL + int(math.sin((x + wave_offset) * 0.05) * 3)
            pygame.draw.line(self.screen, (150, 200, 230), (x, y), (x + 4, y), 2)

        for bubble in self.water_bubbles:
            bubble.draw(self.screen)

        for destroyer in self.destroyers:
            destroyer.draw(self.screen)

        for sub in self.enemy_subs:
            sub.draw(self.screen)

        for missile in self.missiles:
            missile.draw(self.screen)

        for torpedo in self.torpedoes:
            torpedo.draw(self.screen)

        for charge in self.depth_charges:
            charge.draw(self.screen)

        for torpedo in self.enemy_torpedoes:
            torpedo.draw(self.screen)

        if self.game_state == 'playing' or self.game_state == 'paused':
            self.player.draw(self.screen)

        for explosion in self.explosions:
            explosion.draw(self.screen)

        self._draw_ui()

        if self.game_state == 'menu':
            self._draw_menu()
        elif self.game_state == 'paused':
            self._draw_pause()
        elif self.game_state == 'gameover':
            self._draw_gameover()

    def _draw_ui(self):
        score_text = self.font_small.render(f'得分: {self.score}', True, WHITE)
        self.screen.blit(score_text, (20, 20))

        high_text = self.font_small.render(f'最高分: {self.high_score}', True, WHITE)
        self.screen.blit(high_text, (20, 45))

        if self.game_state == 'playing':
            bar_width = 150
            bar_height = 15
            bar_x = SCREEN_WIDTH - bar_width - 20
            bar_y = 20

            pygame.draw.rect(self.screen, (50, 50, 50),
                            (bar_x, bar_y, bar_width, bar_height))

            health_pct = self.player.health / self.player.max_health
            health_color = GREEN if health_pct > 0.5 else YELLOW if health_pct > 0.25 else RED
            pygame.draw.rect(self.screen, health_color,
                            (bar_x, bar_y, int(bar_width * health_pct), bar_height))

            pygame.draw.rect(self.screen, WHITE,
                            (bar_x, bar_y, bar_width, bar_height), 2)

            health_text = self.font_small.render('生命值', True, WHITE)
            self.screen.blit(health_text, (bar_x, bar_y - 20))

        if self.game_state == 'playing':
            hint_text = self.font_small.render(
                '空格=发射飞弹  Ctrl=发射鱼雷  ↑↓/WS=移动  ESC=暂停', True, WHITE)
            self.screen.blit(hint_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 30))

    def _draw_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title_text = self.font_large.render('潜 艇 大 战', True, (100, 200, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        subtitle_text = self.font_medium.render('Submarine Battle', True, (150, 200, 230))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50))
        self.screen.blit(subtitle_text, subtitle_rect)

        start_text = self.font_medium.render('按 空格键 或 回车 开始游戏', True, YELLOW)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)

        instructions = [
            '操作说明:',
            '↑ ↓ 或 W S - 控制潜艇上下移动',
            '空格键 - 向上发射飞弹攻击水面舰艇和潜艇',
            'Ctrl键 - 向前发射鱼雷攻击敌方潜艇',
            'ESC键 - 暂停游戏',
            '',
            '消灭敌方驱逐舰(+100分)和敌方潜艇(+80分)!'
        ]

        for i, line in enumerate(instructions):
            text = self.font_small.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60 + i * 25))
            self.screen.blit(text, text_rect)

    def _draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font_large.render('游 戏 暂 停', True, YELLOW)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(pause_text, pause_rect)

        resume_text = self.font_medium.render('按 ESC 继续游戏', True, WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(resume_text, resume_rect)

    def _draw_gameover(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        over_text = self.font_large.render('游 戏 结 束', True, RED)
        over_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(over_text, over_rect)

        score_text = self.font_medium.render(f'最终得分: {self.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)

        if self.score >= self.high_score and self.score > 0:
            new_record = self.font_medium.render('🎉 新纪录! 🎉', True, YELLOW)
            record_rect = new_record.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(new_record, record_rect)

        restart_text = self.font_medium.render('按 空格键 或 回车 返回菜单', True, YELLOW)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
