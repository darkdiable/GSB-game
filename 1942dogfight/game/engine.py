import pygame
import random
from . import config
from .background import Background
from .player import Player
from .bullet import Bullet, EnemyBullet
from .bomb import Bomb
from .enemy import Enemy
from .ship import Ship
from .island import Island
from .effects import Explosion, BombSplash, ScorePopup
from .ui import UI
from .menu import Menu


class GameEngine:
    STATE_MENU = 'menu'
    STATE_PLAYING = 'playing'
    STATE_PAUSED = 'paused'
    STATE_GAME_OVER = 'game_over'

    def __init__(self, screen):
        self.screen = screen
        self.state = self.STATE_MENU
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.ui = UI()
        self.reset()

    def reset(self):
        self.player = Player()
        self.background = Background()
        self.bullets = []
        self.enemy_bullets = []
        self.bombs = []
        self.enemies = []
        self.ships = []
        self.islands = []
        self.effects = []
        self.score = 0
        self.wave = 1
        self.wave_timer = 0
        self.enemy_spawn_timer = 0
        self.ship_spawn_timer = 0
        self.island_spawn_timer = 0
        self.difficulty = 1.0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.state == self.STATE_MENU:
                        if event.key == pygame.K_RETURN:
                            self.reset()
                            self.state = self.STATE_PLAYING
                        elif event.key == pygame.K_q:
                            running = False
                    elif self.state == self.STATE_PLAYING:
                        if event.key == pygame.K_p:
                            self.state = self.STATE_PAUSED
                        elif event.key == pygame.K_b:
                            self._player_bomb()
                    elif self.state == self.STATE_PAUSED:
                        if event.key == pygame.K_p:
                            self.state = self.STATE_PLAYING
                    elif self.state == self.STATE_GAME_OVER:
                        if event.key == pygame.K_r:
                            self.reset()
                            self.state = self.STATE_PLAYING
                        elif event.key == pygame.K_q:
                            running = False

            if self.state == self.STATE_MENU:
                self._update_menu()
                self._draw_menu()
            elif self.state == self.STATE_PLAYING:
                self._update_game()
                self._draw_game()
            elif self.state == self.STATE_PAUSED:
                self._draw_game()
                self._draw_pause()
            elif self.state == self.STATE_GAME_OVER:
                self._draw_game()
                self.ui.draw_game_over(self.screen, self.score)

            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()

    def _update_menu(self):
        self.menu.blink_timer = getattr(self.menu, 'blink_timer', 0) + 1

    def _draw_menu(self):
        self.menu.draw(self.screen)

    def _update_game(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        if keys[pygame.K_SPACE]:
            self._player_shoot()

        self.background.update()
        self.wave_timer += 1
        if self.wave_timer > 1800:
            self.wave += 1
            self.wave_timer = 0
            self.difficulty += 0.15

        self._spawn_enemies()
        self._spawn_ships()
        self._spawn_islands()

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.active]

        for bullet in self.enemy_bullets:
            bullet.update()
        self.enemy_bullets = [b for b in self.enemy_bullets if b.active]

        for bomb in self.bombs:
            bomb.update()
        self.bombs = [b for b in self.bombs if b.active]

        for enemy in self.enemies:
            enemy.update(self.player.x + self.player.width // 2)
            new_bullets = enemy.shoot(self.player.x + self.player.width // 2,
                                      self.player.y + self.player.height // 2)
            self.enemy_bullets.extend(new_bullets)
        self.enemies = [e for e in self.enemies if e.active]

        for ship in self.ships:
            ship.update()
            new_bullets = ship.shoot(self.player.x + self.player.width // 2,
                                     self.player.y + self.player.height // 2)
            self.enemy_bullets.extend(new_bullets)
        self.ships = [s for s in self.ships if s.active]

        for island in self.islands:
            island.update()
            new_bullets = island.shoot(self.player.x + self.player.width // 2,
                                       self.player.y + self.player.height // 2)
            self.enemy_bullets.extend(new_bullets)
        self.islands = [i for i in self.islands if i.active]

        for effect in self.effects:
            effect.update()
        self.effects = [e for e in self.effects if e.active]

        self._check_collisions()

        if self.player.health <= 0:
            self.state = self.STATE_GAME_OVER
            self.effects.append(Explosion(
                self.player.x + self.player.width // 2,
                self.player.y + self.player.height // 2, 'large'))

        if random.random() < 0.002:
            self.player.bombs = min(self.player.max_bombs, self.player.bombs + 1)

    def _player_shoot(self):
        positions = self.player.shoot()
        if positions:
            for px, py in positions:
                self.bullets.append(Bullet(px, py))

    def _player_bomb(self):
        result = self.player.drop_bomb()
        if result:
            bx, by = result
            self.bombs.append(Bomb(bx, by))

    def _spawn_enemies(self):
        self.enemy_spawn_timer += 1
        rate = max(30, int(config.ENEMY_SPAWN_RATE / self.difficulty))
        if self.enemy_spawn_timer >= rate:
            self.enemy_spawn_timer = 0
            count = 1 if random.random() > 0.3 else 2
            for _ in range(count):
                self.enemies.append(Enemy())

    def _spawn_ships(self):
        self.ship_spawn_timer += 1
        rate = max(200, int(config.SHIP_SPAWN_RATE / self.difficulty))
        if self.ship_spawn_timer >= rate:
            self.ship_spawn_timer = 0
            self.ships.append(Ship())

    def _spawn_islands(self):
        self.island_spawn_timer += 1
        rate = max(400, int(config.ISLAND_SPAWN_RATE / self.difficulty))
        if self.island_spawn_timer >= rate:
            self.island_spawn_timer = 0
            self.islands.append(Island())

    def _check_collisions(self):
        player_rect = self.player.get_rect()

        for bullet in self.bullets:
            bullet_rect = bullet.get_rect()
            for enemy in self.enemies:
                if bullet_rect.colliderect(enemy.get_rect()):
                    bullet.active = False
                    destroyed = enemy.take_damage(1)
                    if destroyed:
                        self.score += enemy.score_value
                        self.effects.append(Explosion(
                            enemy.x + enemy.width // 2,
                            enemy.y + enemy.height // 2, 'medium'))
                        self.effects.append(ScorePopup(
                            enemy.x, enemy.y, enemy.score_value))
                    else:
                        self.effects.append(Explosion(
                            bullet.x, bullet.y, 'small'))
                    break

            for ship in self.ships:
                if bullet.active and bullet_rect.colliderect(ship.get_rect()):
                    bullet.active = False
                    destroyed = ship.take_damage(1)
                    if destroyed:
                        self.score += ship.score_value
                        self.effects.append(Explosion(
                            ship.x + ship.width // 2,
                            ship.y + ship.height // 2, 'large'))
                        self.effects.append(ScorePopup(
                            ship.x, ship.y, ship.score_value))
                    else:
                        self.effects.append(Explosion(
                            bullet.x, bullet.y, 'small'))
                    break

            if bullet.active:
                for island in self.islands:
                    if island.health > 0 and bullet_rect.colliderect(island.get_rect()):
                        bullet.active = False
                        destroyed = island.take_damage(1)
                        if destroyed:
                            self.score += island.score_value
                            self.effects.append(Explosion(
                                island.x + island.width // 2,
                                island.y + island.height // 2, 'large'))
                            self.effects.append(ScorePopup(
                                island.x, island.y, island.score_value))
                        else:
                            self.effects.append(Explosion(
                                bullet.x, bullet.y, 'small'))
                        break

        for eb in self.enemy_bullets:
            if eb.active and eb.get_rect().colliderect(player_rect):
                eb.active = False
                self.player.take_damage(10)
                self.effects.append(Explosion(eb.x, eb.y, 'small'))

        for enemy in self.enemies:
            if enemy.get_rect().colliderect(player_rect):
                enemy.active = False
                self.player.take_damage(20)
                self.effects.append(Explosion(
                    enemy.x + enemy.width // 2,
                    enemy.y + enemy.height // 2, 'medium'))
                self.score += enemy.score_value // 2

        for bomb in self.bombs:
            if not bomb.active:
                continue
            bomb_rect = bomb.get_rect()
            blast = pygame.Rect(
                bomb.x - bomb.blast_radius,
                bomb.y - bomb.blast_radius,
                bomb.blast_radius * 2,
                bomb.blast_radius * 2)
            for enemy in self.enemies:
                if blast.colliderect(enemy.get_rect()):
                    enemy.take_damage(10)
                    if not enemy.active:
                        self.score += enemy.score_value
                        self.effects.append(Explosion(
                            enemy.x + enemy.width // 2,
                            enemy.y + enemy.height // 2, 'medium'))
                        self.effects.append(ScorePopup(
                            enemy.x, enemy.y, enemy.score_value))

            for ship in self.ships:
                if blast.colliderect(ship.get_rect()):
                    ship.take_damage(4)
                    if not ship.active:
                        self.score += ship.score_value
                        self.effects.append(Explosion(
                            ship.x + ship.width // 2,
                            ship.y + ship.height // 2, 'large'))
                        self.effects.append(ScorePopup(
                            ship.x, ship.y, ship.score_value))

            for island in self.islands:
                if island.health > 0 and blast.colliderect(island.get_rect()):
                    island.take_damage(3)
                    if island.health <= 0:
                        self.score += island.score_value
                        self.effects.append(Explosion(
                            island.x + island.width // 2,
                            island.y + island.height // 2, 'large'))
                        self.effects.append(ScorePopup(
                            island.x, island.y, island.score_value))

            self.effects.append(BombSplash(bomb.x, bomb.y))
            bomb.active = False

    def _draw_game(self):
        self.background.draw(self.screen)
        for island in self.islands:
            island.draw(self.screen)
        for ship in self.ships:
            ship.draw(self.screen)
        for bomb in self.bombs:
            bomb.draw(self.screen)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for eb in self.enemy_bullets:
            eb.draw(self.screen)
        for effect in self.effects:
            if isinstance(effect, ScorePopup):
                effect.draw(self.screen, self.ui.font_small)
            else:
                effect.draw(self.screen)
        self.ui.draw(self.screen, self.score, self.player, self.wave)

    def _draw_pause(self):
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))
        font = pygame.font.SysFont('arial', 36, bold=True)
        text = font.render("PAUSED", True, config.WHITE)
        rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)
        sub_font = pygame.font.SysFont('arial', 16)
        sub_text = sub_font.render("Press P to resume", True, config.YELLOW)
        sub_rect = sub_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 35))
        self.screen.blit(sub_text, sub_rect)
