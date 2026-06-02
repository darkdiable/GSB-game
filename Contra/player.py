import pygame
from constants import *
from bullet import Bullet
from sprites import (
    create_player_stand_right, create_player_stand_left,
    create_player_run_right, create_player_run_left,
    create_player_jump_right, create_player_jump_left,
    create_player_prone_right, create_player_prone_left,
    create_player_up_right, create_player_up_left,
    create_explosion_frame,
)


class Player:
    def __init__(self, x, y, lives=3):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.width = 32
        self.height = 48
        self.lives = lives
        self.alive = True
        self.facing_right = True
        self.on_ground = False
        self.proning = False
        self.aiming_up = False
        self.moving = False
        self.jumping = False
        self.shooting = False
        self.was_jump_pressed = False
        self.last_shot_time = 0
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 2000
        self.death_timer = 0
        self.death_duration = 1500
        self.explosion_frame = 0
        self.explosion_timer = 0
        self.score = 0
        self.bullets = []

        self.sprites = {
            "stand_right": create_player_stand_right(),
            "stand_left": create_player_stand_left(),
            "run_right": create_player_run_right(),
            "run_left": create_player_run_left(),
            "jump_right": create_player_jump_right(),
            "jump_left": create_player_jump_left(),
            "prone_right": create_player_prone_right(),
            "prone_left": create_player_prone_left(),
            "up_right": create_player_up_right(),
            "up_left": create_player_up_left(),
        }

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, keys, platforms, camera_x):
        if not self.alive:
            self.death_timer += 16
            self.explosion_timer += 16
            if self.explosion_timer > 100:
                self.explosion_frame += 1
                self.explosion_timer = 0
            if self.death_timer > self.death_duration:
                if self.lives > 0:
                    self.respawn()
                else:
                    return True
            return False

        if self.invincible:
            self.invincible_timer += 16
            if self.invincible_timer > self.invincible_duration:
                self.invincible = False
                self.invincible_timer = 0

        self.vel_x = 0
        self.aiming_up = False
        self.proning = False
        self.moving = False

        jump_pressed = keys[pygame.K_k]
        if jump_pressed and not self.was_jump_pressed:
            self.jump()
        self.was_jump_pressed = jump_pressed

        if keys[pygame.K_w]:
            self.aiming_up = True

        if keys[pygame.K_s]:
            if self.on_ground:
                self.proning = True
                self.height = 28
                self.width = 44
            else:
                self.vel_y += 1

        if not self.proning:
            self.height = 48
            self.width = 32

        if keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
            self.moving = True
        if keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True
            self.moving = True

        self.vel_y += GRAVITY
        if self.vel_y > 15:
            self.vel_y = 15

        self.x += self.vel_x
        self.rect.width = self.width
        self.rect.height = self.height

        if self.x < 0:
            self.x = 0
        if self.x > LEVEL_WIDTH - self.width:
            self.x = LEVEL_WIDTH - self.width

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
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
            if self.vel_y >= 0:
                player_bottom = self.y + self.height
                prev_bottom = player_bottom - self.vel_y
                if prev_bottom <= plat.top and player_bottom >= plat.top:
                    if self.x + self.width > plat.left and self.x < plat.right:
                        self.y = plat.top - self.height
                        self.rect.y = int(self.y)
                        self.vel_y = 0
                        self.on_ground = True
                        self.jumping = False
            else:
                if self.rect.colliderect(plat):
                    self.rect.top = plat.bottom
                    self.vel_y = 0
                    self.y = self.rect.y

        if self.y > SCREEN_HEIGHT:
            self.hit()
            self.y = GROUND_Y - self.height - 10
            self.x = max(0, self.x - 200)

        if keys[pygame.K_j]:
            self.shoot()

        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)

        return False

    def jump(self):
        if self.on_ground and not self.proning:
            self.vel_y = PLAYER_JUMP_SPEED
            self.on_ground = False
            self.jumping = True

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < FIRE_RATE:
            return
        self.last_shot_time = current_time

        if self.proning:
            if self.facing_right:
                bx = self.rect.right
                by = self.rect.centery
                dx, dy = 1, 0
            else:
                bx = self.rect.left - 8
                by = self.rect.centery
                dx, dy = -1, 0
        elif self.aiming_up:
            bx = self.rect.centerx - 4
            by = self.rect.top - 8
            dx, dy = 0, -1
        elif self.jumping and not self.on_ground:
            if self.facing_right:
                if self.vel_y < 0:
                    bx = self.rect.right
                    by = self.rect.top + 10
                    dx, dy = 1, -1
                else:
                    bx = self.rect.right
                    by = self.rect.bottom - 10
                    dx, dy = 1, 1
            else:
                if self.vel_y < 0:
                    bx = self.rect.left - 8
                    by = self.rect.top + 10
                    dx, dy = -1, -1
                else:
                    bx = self.rect.left - 8
                    by = self.rect.bottom - 10
                    dx, dy = -1, 1
        else:
            if self.facing_right:
                bx = self.rect.right
                by = self.rect.centery - 4
                dx, dy = 1, 0
            else:
                bx = self.rect.left - 8
                by = self.rect.centery - 4
                dx, dy = -1, 0

        import math
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            dx /= length
            dy /= length

        bullet = Bullet(bx, by, dx, dy, is_player=True)
        self.bullets.append(bullet)

    def hit(self):
        if self.invincible or not self.alive:
            return
        self.lives -= 1
        self.alive = False
        self.death_timer = 0
        self.explosion_frame = 0
        self.explosion_timer = 0
        self.bullets.clear()

    def respawn(self):
        self.alive = True
        self.invincible = True
        self.invincible_timer = 0
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.jumping = False
        self.proning = False
        self.height = 48
        self.width = 32
        self.rect.width = self.width
        self.rect.height = self.height

    def get_current_sprite(self):
        if not self.alive:
            return None

        if self.proning:
            return self.sprites["prone_right" if self.facing_right else "prone_left"]
        if self.aiming_up:
            return self.sprites["up_right" if self.facing_right else "up_left"]
        if not self.on_ground:
            return self.sprites["jump_right" if self.facing_right else "jump_left"]
        if self.moving:
            return self.sprites["run_right" if self.facing_right else "run_left"]
        return self.sprites["stand_right" if self.facing_right else "stand_left"]

    def draw(self, surface, camera_x):
        if not self.alive:
            if self.explosion_frame < 6:
                explosion = create_explosion_frame(self.explosion_frame)
                ex = self.rect.centerx - explosion.get_width() // 2 - camera_x
                ey = self.rect.centery - explosion.get_height() // 2
                surface.blit(explosion, (ex, ey))
            return

        sprite = self.get_current_sprite()
        if sprite is None:
            return

        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y

        if self.invincible and (self.invincible_timer // 80) % 2 == 0:
            return

        surface.blit(sprite, (draw_x, draw_y))

    def get_rect(self):
        return self.rect
