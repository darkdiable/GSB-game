import pygame
from constants import *
from bullet import Bullet


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vx = 0
        self.vy = 0
        self.direction = 1
        self.on_ground = False
        self.health = PLAYER_MAX_HEALTH
        self.score = 0
        self.anim_frame = 0
        self.anim_timer = 0
        self.shoot_cooldown = 0
        self.invincible = 0
        self.is_moving = False
        self.looking_up = False
        self.looking_down = False
        self.crouching = False

    def handle_input(self, keys):
        self.vx = 0
        self.is_moving = False
        self.looking_up = False
        self.looking_down = False
        self.crouching = False

        if keys[pygame.K_w]:
            self.looking_up = True
        if keys[pygame.K_s]:
            if self.on_ground:
                self.crouching = True
            else:
                self.looking_down = True
        if keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
            self.direction = -1
            self.is_moving = True
        if keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            self.direction = 1
            self.is_moving = True

        if self.crouching:
            self.vx = 0

        if keys[pygame.K_k] and self.on_ground and not self.crouching:
            self.vy = -PLAYER_JUMP_POWER
            self.on_ground = False

    def shoot(self):
        if self.shoot_cooldown <= 0:
            bullet_y = self.y + self.height // 2 - 2
            if self.looking_up:
                bullet_y = self.y
            if self.crouching:
                bullet_y = self.y + self.height - 8
            bullet_x = self.x + (self.width if self.direction > 0 else -BULLET_WIDTH)
            self.shoot_cooldown = 8
            return Bullet(bullet_x, bullet_y, self.direction)
        return None

    def update(self, platforms):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.x = 0

        self.on_ground = False
        for platform in platforms:
            if self.check_platform_collision(platform):
                if self.vy > 0 and self.y + self.height - self.vy <= platform.y:
                    self.y = platform.y - self.height
                    self.vy = 0
                    self.on_ground = True

        if self.y + self.height >= GROUND_HEIGHT:
            self.y = GROUND_HEIGHT - self.height
            self.vy = 0
            self.on_ground = True

        self.shoot_cooldown -= 1
        if self.shoot_cooldown < 0:
            self.shoot_cooldown = 0

        self.invincible -= 1
        if self.invincible < 0:
            self.invincible = 0

        self.anim_timer += 1
        if self.anim_timer >= 8:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4

    def check_platform_collision(self, platform):
        return (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y)

    def take_damage(self):
        if self.invincible <= 0:
            self.health -= 1
            self.invincible = 60
            return True
        return False

    def is_alive(self):
        return self.health > 0

    def draw(self, screen, camera_x):
        if self.invincible > 0 and self.invincible % 8 < 4:
            return

        draw_x = self.x - camera_x
        body_color = (0, 0, 200)
        skin_color = (255, 220, 177)
        bandana_color = RED
        gun_color = (80, 80, 80)

        actual_height = self.height // 2 if self.crouching else self.height
        actual_y = self.y + (self.height - actual_height) if self.crouching else self.y

        pygame.draw.rect(screen, body_color, (draw_x + 4, actual_y + 12, self.width - 8, actual_height - 20))

        pygame.draw.rect(screen, skin_color, (draw_x + 6, actual_y + 4, self.width - 12, 10))
        pygame.draw.rect(screen, bandana_color, (draw_x + 4, actual_y + 2, self.width - 8, 4))

        if self.direction > 0:
            pygame.draw.rect(screen, BLACK, (draw_x + 14, actual_y + 8, 2, 2))
        else:
            pygame.draw.rect(screen, BLACK, (draw_x + 8, actual_y + 8, 2, 2))

        leg_offset = self.anim_frame % 2 if self.is_moving and self.on_ground else 0
        if not self.crouching:
            pygame.draw.rect(screen, body_color, (draw_x + 5, actual_y + actual_height - 10, 5, 10 - leg_offset))
            pygame.draw.rect(screen, body_color, (draw_x + self.width - 10, actual_y + actual_height - 10, 5, 10 + leg_offset - (10 if leg_offset else 0)))

        gun_y = actual_y + 16
        if self.looking_up:
            gun_y = actual_y + 4
            pygame.draw.rect(screen, gun_color, (draw_x + self.width // 2 - 2, gun_y - 8, 4, 16))
        elif self.crouching:
            gun_y = actual_y + actual_height - 8
            gun_start = draw_x + (self.width if self.direction > 0 else -8)
            pygame.draw.rect(screen, gun_color, (gun_start, gun_y, 8 * self.direction, 3))
        else:
            gun_start = draw_x + (self.width if self.direction > 0 else -8)
            pygame.draw.rect(screen, gun_color, (gun_start, gun_y, 8 * self.direction, 3))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
