import pygame
import math
import random
from constants import *
from bullet import Bullet
from sprites import (
    create_soldier_right, create_soldier_left,
    create_turret, create_sniper_right, create_sniper_left,
    create_explosion_frame,
)


class Enemy:
    def __init__(self, x, y, enemy_type, difficulty_settings):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.difficulty = difficulty_settings
        self.active = True
        self.alive = True
        self.facing_right = False
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.bullets = []
        self.last_shot_time = 0
        self.death_timer = 0
        self.explosion_frame = 0
        self.explosion_timer = 0
        self.patrol_timer = 0
        self.patrol_direction = -1
        self.spawn_x = x

        speed_mult = difficulty_settings["enemy_speed_multiplier"]

        if enemy_type == "soldier":
            self.image_right = create_soldier_right()
            self.image_left = create_soldier_left()
            self.width = 28
            self.height = 44
            self.speed = 1.5 * speed_mult
            self.hp = 1
            self.score_value = 100
            self.fire_rate = difficulty_settings["enemy_fire_rate"]
            self.detection_range = 400
            self.can_move = True
        elif enemy_type == "turret":
            self.image_right = create_turret()
            self.image_left = create_turret()
            self.width = 36
            self.height = 28
            self.speed = 0
            self.hp = 3
            self.score_value = 500
            self.fire_rate = difficulty_settings["enemy_fire_rate"] // 2
            self.detection_range = 500
            self.can_move = False
        elif enemy_type == "sniper":
            self.image_right = create_sniper_right()
            self.image_left = create_sniper_left()
            self.width = 28
            self.height = 44
            self.speed = 0.5 * speed_mult
            self.hp = 1
            self.score_value = 300
            self.fire_rate = difficulty_settings["enemy_fire_rate"] * 2
            self.detection_range = 600
            self.can_move = True
        else:
            self.width = 28
            self.height = 44
            self.speed = 1.0 * speed_mult
            self.hp = 1
            self.score_value = 100
            self.fire_rate = difficulty_settings["enemy_fire_rate"]
            self.detection_range = 400
            self.can_move = True
            self.image_right = create_soldier_right()
            self.image_left = create_soldier_left()

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, player, platforms):
        if not self.alive:
            self.death_timer += 16
            self.explosion_timer += 16
            if self.explosion_timer > 80:
                self.explosion_frame += 1
                self.explosion_timer = 0
            if self.death_timer > 600:
                self.active = False
            return

        if self.can_move:
            self._update_movement(player, platforms)
        else:
            self._update_stationary(player)

        self._update_shooting(player)

        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)

    def _update_movement(self, player, platforms):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < self.detection_range:
            if dx > 0:
                self.facing_right = True
                self.vel_x = self.speed
            elif dx < 0:
                self.facing_right = False
                self.vel_x = -self.speed
        else:
            self.patrol_timer += 16
            if self.patrol_timer > 2000:
                self.patrol_direction *= -1
                self.patrol_timer = 0
            self.vel_x = self.speed * 0.5 * self.patrol_direction
            self.facing_right = self.patrol_direction > 0

        if self.enemy_type == "sniper" and distance < self.detection_range * 0.5:
            self.vel_x = 0

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

        self.x += self.vel_x
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if self.x < self.spawn_x - 200:
            self.x = self.spawn_x - 200
            self.vel_x = 0
        if self.x > self.spawn_x + 200:
            self.x = self.spawn_x + 200
            self.vel_x = 0

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_x > 0:
                    self.rect.right = plat.left
                elif self.vel_x < 0:
                    self.rect.left = plat.right
                self.x = self.rect.x

        self.y += self.vel_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = plat.bottom
                    self.vel_y = 0
                self.y = self.rect.y

    def _update_stationary(self, player):
        dx = player.rect.centerx - self.rect.centerx
        if dx > 0:
            self.facing_right = True
        else:
            self.facing_right = False

    def _update_shooting(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.fire_rate:
            return

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > self.detection_range:
            return

        self.last_shot_time = current_time

        if self.enemy_type == "turret":
            angle = math.atan2(dy, dx)
            bdx = math.cos(angle)
            bdy = math.sin(angle)
            bx = self.rect.centerx
            by = self.rect.centery
            bullet = Bullet(bx, by, bdx, bdy, is_player=False,
                            speed=self.difficulty["enemy_bullet_speed"])
            self.bullets.append(bullet)

            angle2 = angle + random.uniform(-0.3, 0.3)
            bdx2 = math.cos(angle2)
            bdy2 = math.sin(angle2)
            bullet2 = Bullet(bx, by, bdx2, bdy2, is_player=False,
                             speed=self.difficulty["enemy_bullet_speed"])
            self.bullets.append(bullet2)
        else:
            if self.facing_right:
                bdx = 1.0
            else:
                bdx = -1.0
            bdy = 0.0

            if abs(dy) > abs(dx) * 0.5 and distance < 300:
                bdy = 0.5 if dy > 0 else -0.5
                length = math.sqrt(bdx * bdx + bdy * bdy)
                bdx /= length
                bdy /= length

            bx = self.rect.right if self.facing_right else self.rect.left - 6
            by = self.rect.centery

            bullet = Bullet(bx, by, bdx, bdy, is_player=False,
                            speed=self.difficulty["enemy_bullet_speed"])
            self.bullets.append(bullet)

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            self.death_timer = 0
            self.explosion_frame = 0
            self.explosion_timer = 0
            self.bullets.clear()
            return True
        return False

    def draw(self, surface, camera_x):
        draw_x = self.rect.x - camera_x
        if draw_x < -100 or draw_x > SCREEN_WIDTH + 100:
            return

        if not self.alive:
            if self.explosion_frame < 6:
                explosion = create_explosion_frame(self.explosion_frame)
                ex = self.rect.centerx - explosion.get_width() // 2 - camera_x
                ey = self.rect.centery - explosion.get_height() // 2
                surface.blit(explosion, (ex, ey))
            return

        image = self.image_right if self.facing_right else self.image_left
        surface.blit(image, (draw_x, self.rect.y))

        for bullet in self.bullets:
            bullet.draw(surface, camera_x)

    def get_rect(self):
        return self.rect


class EnemySpawner:
    def __init__(self, difficulty_settings):
        self.difficulty = difficulty_settings
        self.spawn_rate = difficulty_settings["enemy_spawn_rate"]
        self.last_spawn_time = 0
        self.spawn_points = []
        self.active_enemies = []

    def add_spawn_point(self, x, y, enemy_type="soldier"):
        self.spawn_points.append({"x": x, "y": y, "type": enemy_type, "spawned": False})

    def update(self, player, platforms, camera_x):
        current_time = pygame.time.get_ticks()

        for enemy in self.active_enemies[:]:
            enemy.update(player, platforms)
            if not enemy.active:
                self.active_enemies.remove(enemy)
            elif enemy.rect.x < camera_x - 400:
                self.active_enemies.remove(enemy)

        for sp in self.spawn_points:
            if not sp["spawned"] and sp["x"] < camera_x + SCREEN_WIDTH + 100:
                sp["spawned"] = True
                enemy = Enemy(sp["x"], sp["y"], sp["type"], self.difficulty)
                self.active_enemies.append(enemy)

        if current_time - self.last_spawn_time > self.spawn_rate:
            self.last_spawn_time = current_time
            self._spawn_random_enemy(camera_x, player)

    def _spawn_random_enemy(self, camera_x, player):
        max_enemies = int(10 * self.difficulty["enemy_count_multiplier"])
        if max_enemies > 25:
            max_enemies = 25
        if len(self.active_enemies) >= max_enemies:
            return

        spawn_x = camera_x + SCREEN_WIDTH + random.randint(50, 200)
        spawn_y = GROUND_Y - 44

        enemy_type = random.choices(
            ["soldier", "sniper", "turret"],
            weights=[60, 25, 15],
            k=1
        )[0]

        if enemy_type == "turret":
            spawn_y = GROUND_Y - 28

        count = 1
        if self.difficulty["enemy_speed_multiplier"] > 1.5:
            count = random.randint(1, 3)

        for _ in range(count):
            ex = spawn_x + random.randint(-50, 50)
            enemy = Enemy(ex, spawn_y, enemy_type, self.difficulty)
            self.active_enemies.append(enemy)

    def draw(self, surface, camera_x):
        for enemy in self.active_enemies:
            enemy.draw(surface, camera_x)

    def check_bullet_hits(self, player_bullets):
        hits = []
        for bullet in player_bullets[:]:
            if not bullet.is_player or not bullet.active:
                continue
            for enemy in self.active_enemies:
                if not enemy.alive:
                    continue
                if bullet.rect.colliderect(enemy.rect):
                    killed = enemy.hit()
                    bullet.active = False
                    if killed:
                        hits.append(enemy.score_value)
        return hits

    def check_player_hit(self, player_rect):
        for enemy in self.active_enemies:
            if not enemy.alive:
                continue
            for bullet in enemy.bullets:
                if bullet.active and bullet.rect.colliderect(player_rect):
                    bullet.active = False
                    return True
            if enemy.alive and enemy.rect.colliderect(player_rect):
                return True
        return False

    def clear(self):
        self.active_enemies.clear()
        for sp in self.spawn_points:
            sp["spawned"] = False
