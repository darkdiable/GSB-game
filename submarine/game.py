import pygame
import random
import sys
import math
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WATER_SURFACE_Y, FPS,
    SKY_COLOR, WATER_COLOR,
    DESTROYER_SPAWN_INTERVAL, SUBMARINE_SPAWN_INTERVAL,
    DIVER_SPAWN_INTERVAL
)
from player import PlayerSubmarine
from enemies import EnemyDestroyer, EnemySubmarine
from weapons import Missile, Torpedo, DepthCharge
from effects import Explosion, Bubble
from diver import Diver

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("潜艇大战 - Submarine Battle")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        self.player = PlayerSubmarine(100, SCREEN_HEIGHT // 2)
        self.destroyers = []
        self.enemy_submarines = []
        self.player_missiles = []
        self.player_torpedoes = []
        self.enemy_torpedoes = []
        self.depth_charges = []
        self.explosions = []
        self.bubbles = []
        self.divers = []
        self.divers_rescued = 0
        
        self.score = 0
        self.game_over = False
        self.paused = False
        
        self.spawn_timer = 0
        self.destroyer_spawn_interval = DESTROYER_SPAWN_INTERVAL
        self.submarine_spawn_interval = SUBMARINE_SPAWN_INTERVAL
        self.diver_spawn_interval = DIVER_SPAWN_INTERVAL
        
        self.bubble_timer = 0
    
    def spawn_enemies(self):
        self.spawn_timer += 1
        
        if self.spawn_timer % self.destroyer_spawn_interval == 0:
            self.destroyers.append(EnemyDestroyer())
        
        if self.spawn_timer % self.submarine_spawn_interval == 0:
            self.enemy_submarines.append(EnemySubmarine())
        
        if self.spawn_timer % self.diver_spawn_interval == 0:
            self.divers.append(Diver())
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                else:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    
                    if not self.paused:
                        if event.key == pygame.K_SPACE:
                            missile = self.player.fire_missile()
                            if missile:
                                self.player_missiles.append(missile)
                        
                        if event.key == pygame.K_t:
                            torpedo = self.player.fire_torpedo()
                            if torpedo:
                                self.player_torpedoes.append(torpedo)
        
        return True
    
    def update(self):
        if self.game_over or self.paused:
            return
        
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        
        self.spawn_enemies()
        
        for destroyer in self.destroyers[:]:
            if destroyer.update():
                self.destroyers.remove(destroyer)
            else:
                charges = destroyer.fire_depth_charges()
                if charges:
                    self.depth_charges.extend(charges)
        
        for submarine in self.enemy_submarines[:]:
            if submarine.update():
                self.enemy_submarines.remove(submarine)
            else:
                torpedo = submarine.fire_torpedo()
                if torpedo:
                    self.enemy_torpedoes.append(torpedo)
        
        for missile in self.player_missiles[:]:
            if missile.update():
                self.player_missiles.remove(missile)
        
        for torpedo in self.player_torpedoes[:]:
            if torpedo.update():
                self.player_torpedoes.remove(torpedo)
        
        for torpedo in self.enemy_torpedoes[:]:
            if torpedo.update():
                self.enemy_torpedoes.remove(torpedo)
        
        for depth_charge in self.depth_charges[:]:
            if depth_charge.update():
                self.depth_charges.remove(depth_charge)
        
        for explosion in self.explosions[:]:
            if explosion.update():
                self.explosions.remove(explosion)
        
        for diver in self.divers[:]:
            if diver.update():
                self.divers.remove(diver)
        
        self.bubble_timer += 1
        if self.bubble_timer > 5:
            self.bubble_timer = 0
            if random.random() < 0.3:
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(WATER_SURFACE_Y + 50, SCREEN_HEIGHT)
                self.bubbles.append(Bubble(x, y))
        
        for bubble in self.bubbles[:]:
            if bubble.update():
                self.bubbles.remove(bubble)
        
        self.check_collisions()
        
        if self.player.health <= 0:
            self.game_over = True
    
    def check_collisions(self):
        for missile in self.player_missiles[:]:
            missile_removed = False
            for destroyer in self.destroyers[:]:
                if missile.get_rect().colliderect(destroyer.get_rect()):
                    destroyer.health -= missile.damage
                    if missile in self.player_missiles:
                        self.player_missiles.remove(missile)
                        missile_removed = True
                    self.explosions.append(Explosion(missile.x, missile.y, 20))
                    
                    if destroyer.health <= 0:
                        self.destroyers.remove(destroyer)
                        self.score += destroyer.score_value
                        self.explosions.append(Explosion(destroyer.x + destroyer.width // 2, 
                                                        destroyer.y + destroyer.height // 2, 50))
                    break
            
            if not missile_removed and missile in self.player_missiles:
                for submarine in self.enemy_submarines[:]:
                    if missile.get_rect().colliderect(submarine.get_rect()):
                        submarine.health -= missile.damage
                        if missile in self.player_missiles:
                            self.player_missiles.remove(missile)
                        self.explosions.append(Explosion(missile.x, missile.y, 20))
                        
                        if submarine.health <= 0:
                            self.enemy_submarines.remove(submarine)
                            self.score += submarine.score_value
                            self.explosions.append(Explosion(submarine.x + submarine.width // 2, 
                                                            submarine.y + submarine.height // 2, 40))
                        break
        
        for torpedo in self.player_torpedoes[:]:
            for submarine in self.enemy_submarines[:]:
                if torpedo.get_rect().colliderect(submarine.get_rect()):
                    submarine.take_damage(torpedo.damage, is_torpedo=True)
                    if torpedo in self.player_torpedoes:
                        self.player_torpedoes.remove(torpedo)
                    self.explosions.append(Explosion(torpedo.x, torpedo.y, 15))
                    
                    if submarine.health <= 0:
                        self.enemy_submarines.remove(submarine)
                        self.score += submarine.score_value
                        self.explosions.append(Explosion(submarine.x + submarine.width // 2, 
                                                        submarine.y + submarine.height // 2, 40))
                    break
        
        for torpedo in self.enemy_torpedoes[:]:
            if torpedo.get_rect().colliderect(self.player.get_rect()):
                self.player.health -= torpedo.damage
                if torpedo in self.enemy_torpedoes:
                    self.enemy_torpedoes.remove(torpedo)
                self.explosions.append(Explosion(torpedo.x, torpedo.y, 15))
        
        for depth_charge in self.depth_charges[:]:
            if not depth_charge.exploding:
                if depth_charge.get_rect().colliderect(self.player.get_rect()):
                    depth_charge.explode()
                    self.player.health -= depth_charge.damage
                    self.explosions.append(Explosion(depth_charge.x, depth_charge.y, 30))
            
            if depth_charge.exploding:
                explosion_rect = depth_charge.get_rect()
                if explosion_rect.colliderect(self.player.get_rect()):
                    if depth_charge.explosion_timer < 5:
                        self.player.health -= depth_charge.explosion_damage
        
        for diver in self.divers[:]:
            if diver.get_rect().colliderect(self.player.get_rect()):
                health_bonus = diver.get_health_bonus()
                self.player.heal(health_bonus)
                self.divers_rescued += 1
                self.score += 50
                self.divers.remove(diver)
    
    def draw_background(self):
        self.screen.fill(SKY_COLOR)
        
        water_rect = pygame.Rect(0, WATER_SURFACE_Y, SCREEN_WIDTH, SCREEN_HEIGHT - WATER_SURFACE_Y)
        pygame.draw.rect(self.screen, WATER_COLOR, water_rect)
        
        for i in range(5):
            y = WATER_SURFACE_Y + (SCREEN_HEIGHT - WATER_SURFACE_Y) * i // 5
            alpha_color = (
                max(0, WATER_COLOR[0] - i * 5),
                max(0, WATER_COLOR[1] - i * 10),
                max(0, WATER_COLOR[2] - i * 10)
            )
            pygame.draw.line(self.screen, alpha_color, (0, y), (SCREEN_WIDTH, y), 1)
        
        pygame.draw.line(self.screen, (200, 200, 200), 
                        (0, WATER_SURFACE_Y), (SCREEN_WIDTH, WATER_SURFACE_Y), 3)
        
        wave_points = []
        for x in range(0, SCREEN_WIDTH + 20, 20):
            y = WATER_SURFACE_Y + math.sin(x * 0.02 + pygame.time.get_ticks() * 0.002) * 5
            wave_points.append((x, y))
        
        if len(wave_points) > 1:
            pygame.draw.lines(self.screen, (150, 200, 255), False, wave_points, 2)
    
    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 50))
        
        diver_text = self.font.render(f"Divers Rescued: {self.divers_rescued}", True, (0, 255, 255))
        self.screen.blit(diver_text, (10, 90))
        
        controls = [
            "Controls:",
            "Arrow/WASD - Move",
            "SPACE - Fire Missile (Up)",
            "T - Fire Torpedo (Forward)",
            "P - Pause",
            "ESC - Quit"
        ]
        
        y_offset = 10
        for control in controls:
            text = self.small_font.render(control, True, (255, 255, 255))
            self.screen.blit(text, (SCREEN_WIDTH - 180, y_offset))
            y_offset += 20
        
        if self.paused:
            pause_text = self.large_font.render("PAUSED", True, (255, 255, 0))
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            bg_rect = text_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
            pygame.draw.rect(self.screen, (255, 255, 0), bg_rect, 3)
            
            self.screen.blit(pause_text, text_rect)
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.large_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        diver_text = self.font.render(f"Divers Rescued: {self.divers_rescued}", True, (0, 255, 255))
        diver_rect = diver_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(diver_text, diver_rect)
        
        restart_text = self.font.render("Press R to Restart", True, (255, 255, 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        self.draw_background()
        
        for bubble in self.bubbles:
            bubble.draw(self.screen)
        
        for diver in self.divers:
            diver.draw(self.screen)
        
        for destroyer in self.destroyers:
            destroyer.draw(self.screen)
        
        self.player.draw(self.screen)
        
        for submarine in self.enemy_submarines:
            submarine.draw(self.screen)
        
        for missile in self.player_missiles:
            missile.draw(self.screen)
        
        for torpedo in self.player_torpedoes:
            torpedo.draw(self.screen)
        
        for torpedo in self.enemy_torpedoes:
            torpedo.draw(self.screen)
        
        for depth_charge in self.depth_charges:
            depth_charge.draw(self.screen)
        
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
