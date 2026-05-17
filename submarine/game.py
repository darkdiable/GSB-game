import pygame
import random
import sys
from enum import Enum

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WATER_SURFACE_Y = SCREEN_HEIGHT // 4
FPS = 60

SKY_COLOR = (135, 206, 235)
WATER_COLOR = (0, 51, 102)
DEEP_WATER_COLOR = (0, 30, 60)

class WeaponType(Enum):
    MISSILE = 1
    TORPEDO = 2
    DEPTH_CHARGE = 3

class PlayerSubmarine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 40
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.missile_cooldown = 0
        self.torpedo_cooldown = 0
        self.missile_cooldown_time = 30
        self.torpedo_cooldown_time = 45
        
    def update(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y = max(WATER_SURFACE_Y + 20, self.y - self.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y = min(SCREEN_HEIGHT - self.height - 10, self.y + self.speed)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(10, self.x - self.speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = min(SCREEN_WIDTH - self.width - 10, self.x + self.speed)
        
        if self.missile_cooldown > 0:
            self.missile_cooldown -= 1
        if self.torpedo_cooldown > 0:
            self.torpedo_cooldown -= 1
    
    def fire_missile(self):
        if self.missile_cooldown <= 0:
            self.missile_cooldown = self.missile_cooldown_time
            return Missile(self.x + self.width, self.y + self.height // 2)
        return None
    
    def fire_torpedo(self):
        if self.torpedo_cooldown <= 0:
            self.torpedo_cooldown = self.torpedo_cooldown_time
            return Torpedo(self.x + self.width, self.y + self.height // 2, is_player=True)
        return None
    
    def draw(self, screen):
        points = [
            (self.x, self.y + self.height // 2),
            (self.x + 20, self.y),
            (self.x + self.width - 10, self.y),
            (self.x + self.width, self.y + self.height // 2),
            (self.x + self.width - 10, self.y + self.height),
            (self.x + 20, self.y + self.height),
        ]
        pygame.draw.polygon(screen, (128, 128, 128), points)
        pygame.draw.polygon(screen, (100, 100, 100), points, 2)
        
        periscope_x = self.x + 30
        periscope_y = self.y - 15
        pygame.draw.rect(screen, (80, 80, 80), (periscope_x, periscope_y, 8, 20))
        pygame.draw.circle(screen, (60, 60, 60), (periscope_x + 4, periscope_y), 5)
        
        propeller_x = self.x - 5
        pygame.draw.ellipse(screen, (150, 150, 150), 
                          (propeller_x, self.y + self.height // 2 - 8, 10, 16))
        
        health_bar_width = 80
        health_bar_height = 8
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x + 10, self.y - 25, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), 
                        (self.x + 10, self.y - 25, int(health_bar_width * health_ratio), health_bar_height))
        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.x + 10, self.y - 25, health_bar_width, health_bar_height), 1)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class EnemyDestroyer:
    def __init__(self):
        self.width = 120
        self.height = 50
        self.x = SCREEN_WIDTH + random.randint(50, 200)
        self.y = WATER_SURFACE_Y - self.height + 15
        self.speed = random.uniform(1.5, 3.0)
        self.health = 80
        self.max_health = 80
        self.depth_charge_cooldown = random.randint(60, 120)
        self.score_value = 100
        
    def update(self):
        self.x -= self.speed
        if self.depth_charge_cooldown > 0:
            self.depth_charge_cooldown -= 1
        return self.x < -self.width
    
    def fire_depth_charge(self):
        if self.depth_charge_cooldown <= 0:
            self.depth_charge_cooldown = random.randint(90, 150)
            return DepthCharge(self.x + self.width // 2, self.y + self.height)
        return None
    
    def draw(self, screen):
        hull_points = [
            (self.x, self.y + self.height - 10),
            (self.x + 10, self.y + self.height),
            (self.x + self.width - 10, self.y + self.height),
            (self.x + self.width, self.y + self.height - 10),
            (self.x + self.width - 5, self.y + 20),
            (self.x + 5, self.y + 20),
        ]
        pygame.draw.polygon(screen, (139, 69, 19), hull_points)
        pygame.draw.polygon(screen, (100, 50, 10), hull_points, 2)
        
        deck_y = self.y + 20
        pygame.draw.rect(screen, (160, 82, 45), 
                        (self.x + 10, deck_y, self.width - 20, 15))
        
        bridge_x = self.x + self.width // 2 - 15
        bridge_y = self.y
        pygame.draw.rect(screen, (128, 128, 128), (bridge_x, bridge_y, 30, 20))
        pygame.draw.rect(screen, (100, 100, 100), (bridge_x + 10, bridge_y - 10, 10, 10))
        
        gun_x = self.x + 20
        pygame.draw.rect(screen, (80, 80, 80), (gun_x, self.y - 5, 8, 15))
        pygame.draw.circle(screen, (60, 60, 60), (gun_x + 4, self.y - 5), 6)
        
        health_bar_width = 60
        health_bar_height = 6
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x + self.width // 2 - health_bar_width // 2, 
                         self.y - 20, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), 
                        (self.x + self.width // 2 - health_bar_width // 2, 
                         self.y - 20, int(health_bar_width * health_ratio), health_bar_height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class EnemySubmarine:
    def __init__(self):
        self.width = 90
        self.height = 35
        self.x = SCREEN_WIDTH + random.randint(50, 200)
        self.y = random.randint(WATER_SURFACE_Y + 80, SCREEN_HEIGHT - 100)
        self.speed = random.uniform(1.0, 2.5)
        self.health = 60
        self.max_health = 60
        self.torpedo_cooldown = random.randint(60, 120)
        self.score_value = 150
        self.vertical_direction = random.choice([-1, 1])
        self.vertical_timer = 0
        
    def update(self):
        self.x -= self.speed
        
        self.vertical_timer += 1
        if self.vertical_timer > 60:
            self.vertical_timer = 0
            if random.random() < 0.3:
                self.vertical_direction *= -1
        
        self.y += self.vertical_direction * 0.5
        self.y = max(WATER_SURFACE_Y + 50, min(SCREEN_HEIGHT - self.height - 20, self.y))
        
        if self.torpedo_cooldown > 0:
            self.torpedo_cooldown -= 1
        
        return self.x < -self.width
    
    def fire_torpedo(self):
        if self.torpedo_cooldown <= 0:
            self.torpedo_cooldown = random.randint(90, 150)
            return Torpedo(self.x - 10, self.y + self.height // 2, is_player=False)
        return None
    
    def draw(self, screen):
        points = [
            (self.x, self.y + self.height // 2),
            (self.x + 15, self.y),
            (self.x + self.width - 10, self.y),
            (self.x + self.width, self.y + self.height // 2),
            (self.x + self.width - 10, self.y + self.height),
            (self.x + 15, self.y + self.height),
        ]
        pygame.draw.polygon(screen, (180, 50, 50), points)
        pygame.draw.polygon(screen, (140, 30, 30), points, 2)
        
        conning_x = self.x + self.width - 30
        conning_y = self.y - 10
        pygame.draw.rect(screen, (160, 40, 40), (conning_x, conning_y, 15, 15))
        
        propeller_x = self.x - 5
        pygame.draw.ellipse(screen, (200, 60, 60), 
                          (propeller_x, self.y + self.height // 2 - 6, 8, 12))
        
        health_bar_width = 50
        health_bar_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x + 20, self.y - 15, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), 
                        (self.x + 20, self.y - 15, int(health_bar_width * health_ratio), health_bar_height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Missile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 8
        self.speed = 10
        self.vertical_speed = -8
        self.damage = 40
        
    def update(self):
        self.x += self.speed * 0.3
        self.y += self.vertical_speed
        return self.y < 0
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 200, 0), 
                          (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, (255, 100, 0), 
                          (self.x - 8, self.y + 1, 10, 6))
        
        for i in range(3):
            trail_y = self.y + self.height // 2 + random.randint(-2, 2)
            pygame.draw.circle(screen, (255, 150, 0), 
                             (int(self.x - 5 - i * 4), int(trail_y)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Torpedo:
    def __init__(self, x, y, is_player=True):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 8
        self.speed = 7 if is_player else -5
        self.is_player = is_player
        self.damage = 35
        
    def update(self):
        self.x += self.speed
        if self.is_player:
            return self.x > SCREEN_WIDTH
        else:
            return self.x < -self.width
    
    def draw(self, screen):
        color = (0, 255, 255) if self.is_player else (255, 100, 100)
        pygame.draw.ellipse(screen, color, 
                          (self.x, self.y, self.width, self.height))
        
        if self.is_player:
            trail_x = self.x - 10
        else:
            trail_x = self.x + self.width
        pygame.draw.circle(screen, (200, 200, 200), (int(trail_x), int(self.y + 4)), 3)
        
        for i in range(5):
            bubble_x = trail_x + random.randint(-5, 5)
            bubble_y = self.y + random.randint(-3, self.height + 3)
            pygame.draw.circle(screen, (150, 150, 150), 
                             (int(bubble_x), int(bubble_y)), 1)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class DepthCharge:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.fall_speed = 2
        self.damage = 30
        self.explosion_timer = 0
        self.exploding = False
        
    def update(self):
        if not self.exploding:
            self.y += self.fall_speed
            self.fall_speed += 0.05
            
            if self.y > SCREEN_HEIGHT:
                return True
        else:
            self.explosion_timer += 1
            if self.explosion_timer > 20:
                return True
        return False
    
    def explode(self):
        self.exploding = True
    
    def draw(self, screen):
        if self.exploding:
            explosion_radius = 20 + self.explosion_timer * 2
            alpha = max(0, 255 - self.explosion_timer * 12)
            pygame.draw.circle(screen, (255, 150, 0), 
                             (int(self.x), int(self.y)), explosion_radius)
            pygame.draw.circle(screen, (255, 255, 0), 
                             (int(self.x), int(self.y)), explosion_radius // 2)
        else:
            pygame.draw.circle(screen, (50, 50, 50), 
                             (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (30, 30, 30), 
                             (int(self.x), int(self.y)), self.radius, 2)
            pygame.draw.line(screen, (80, 80, 80), 
                           (self.x - 5, self.y - 5), (self.x + 5, self.y + 5), 2)
            pygame.draw.line(screen, (80, 80, 80), 
                           (self.x + 5, self.y - 5), (self.x - 5, self.y + 5), 2)
    
    def get_rect(self):
        if self.exploding:
            explosion_radius = 20 + self.explosion_timer * 2
            return pygame.Rect(self.x - explosion_radius, self.y - explosion_radius, 
                             explosion_radius * 2, explosion_radius * 2)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                         self.radius * 2, self.radius * 2)

class Explosion:
    def __init__(self, x, y, size=30):
        self.x = x
        self.y = y
        self.size = size
        self.max_size = size
        self.timer = 0
        self.max_timer = 20
        
    def update(self):
        self.timer += 1
        return self.timer >= self.max_timer
    
    def draw(self, screen):
        progress = self.timer / self.max_timer
        current_size = int(self.max_size * (1 - progress * 0.5))
        alpha = int(255 * (1 - progress))
        
        for i in range(3):
            radius = current_size - i * 5
            if radius > 0:
                color = (255, 150 - i * 30, 0)
                pygame.draw.circle(screen, color, (int(self.x), int(self.y)), radius)
        
        for i in range(8):
            angle = i * 45 + self.timer * 10
            import math
            dist = current_size + self.timer * 2
            px = self.x + math.cos(math.radians(angle)) * dist
            py = self.y + math.sin(math.radians(angle)) * dist
            pygame.draw.circle(screen, (255, 200, 0), (int(px), int(py)), 3)

class Bubble:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 6)
        self.speed = random.uniform(0.5, 2)
        self.wobble = random.uniform(0, 6.28)
        
    def update(self):
        self.y -= self.speed
        self.wobble += 0.1
        self.x += math.sin(self.wobble) * 0.5
        return self.y < WATER_SURFACE_Y
    
    def draw(self, screen):
        pygame.draw.circle(screen, (100, 150, 200), 
                         (int(self.x), int(self.y)), self.radius, 1)

import math

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
        
        self.score = 0
        self.game_over = False
        self.paused = False
        
        self.spawn_timer = 0
        self.destroyer_spawn_interval = 180
        self.submarine_spawn_interval = 240
        
        self.bubble_timer = 0
    
    def spawn_enemies(self):
        self.spawn_timer += 1
        
        if self.spawn_timer % self.destroyer_spawn_interval == 0:
            self.destroyers.append(EnemyDestroyer())
        
        if self.spawn_timer % self.submarine_spawn_interval == 0:
            self.enemy_submarines.append(EnemySubmarine())
    
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
                depth_charge = destroyer.fire_depth_charge()
                if depth_charge:
                    self.depth_charges.append(depth_charge)
        
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
            for destroyer in self.destroyers[:]:
                if missile.get_rect().colliderect(destroyer.get_rect()):
                    destroyer.health -= missile.damage
                    if missile in self.player_missiles:
                        self.player_missiles.remove(missile)
                    self.explosions.append(Explosion(missile.x, missile.y, 20))
                    
                    if destroyer.health <= 0:
                        self.destroyers.remove(destroyer)
                        self.score += destroyer.score_value
                        self.explosions.append(Explosion(destroyer.x + destroyer.width // 2, 
                                                        destroyer.y + destroyer.height // 2, 50))
                    break
        
        for torpedo in self.player_torpedoes[:]:
            for submarine in self.enemy_submarines[:]:
                if torpedo.get_rect().colliderect(submarine.get_rect()):
                    submarine.health -= torpedo.damage
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
                        self.player.health -= 5
    
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
        
        restart_text = self.font.render("Press R to Restart", True, (255, 255, 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        self.draw_background()
        
        for bubble in self.bubbles:
            bubble.draw(self.screen)
        
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
