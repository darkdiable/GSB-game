import pygame
import random
from constants import *
from bullet import Bullet


class Enemy:
    def __init__(self, x, y, mode=MODE_NORMAL):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.vy = 0
        self.direction = -1
        self.health = 1
        self.active = True
        self.shoot_timer = random.randint(60, 120)
        self.anim_frame = 0
        self.anim_timer = 0
        self.on_ground = False
        self.speed = NORMAL_ENEMY_SPEED if mode == MODE_NORMAL else HELL_ENEMY_SPEED
        self.type = random.choice(['soldier', 'soldier', 'soldier', 'turret'])
        if self.type == 'turret':
            self.health = 2
            self.speed = 0

    def update(self, player_x, platforms):
        if not self.active:
            return None

        bullet = None
        if self.type == 'soldier':
            self.vy += GRAVITY
            self.x += self.speed * self.direction
            self.y += self.vy

            if self.y + self.height >= GROUND_HEIGHT:
                self.y = GROUND_HEIGHT - self.height
                self.vy = 0
                self.on_ground = True

            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = random.randint(90, 180)
                bullet_y = self.y + self.height // 2 - 2
                bullet_x = self.x + (self.width if self.direction > 0 else -BULLET_WIDTH)
                bullet = Bullet(bullet_x, bullet_y, self.direction, is_enemy=True)

            self.anim_timer += 1
            if self.anim_timer >= 12:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 2

        elif self.type == 'turret':
            if self.y + self.height >= GROUND_HEIGHT:
                self.y = GROUND_HEIGHT - self.height

            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = random.randint(60, 120)
                direction = 1 if player_x > self.x else -1
                self.direction = direction
                bullet_y = self.y + self.height // 2 - 2
                bullet_x = self.x + (self.width if direction > 0 else -BULLET_WIDTH)
                bullet = Bullet(bullet_x, bullet_y, direction, is_enemy=True)

        return bullet

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.active = False
            return True
        return False

    def draw(self, screen, camera_x):
        if not self.active:
            return

        draw_x = self.x - camera_x

        if self.type == 'soldier':
            body_color = (139, 0, 0)
            skin_color = (255, 220, 177)
            hat_color = (0, 100, 0)
            gun_color = (80, 80, 80)

            pygame.draw.rect(screen, body_color, (draw_x + 4, self.y + 12, self.width - 8, self.height - 20))
            pygame.draw.rect(screen, skin_color, (draw_x + 6, self.y + 6, self.width - 12, 8))
            pygame.draw.rect(screen, hat_color, (draw_x + 4, self.y + 2, self.width - 8, 6))

            if self.direction > 0:
                pygame.draw.rect(screen, BLACK, (draw_x + 14, self.y + 9, 2, 2))
            else:
                pygame.draw.rect(screen, BLACK, (draw_x + 8, self.y + 9, 2, 2))

            leg_offset = self.anim_frame * 3
            pygame.draw.rect(screen, body_color, (draw_x + 5, self.y + self.height - 10, 5, 10 - leg_offset))
            pygame.draw.rect(screen, body_color, (draw_x + self.width - 10, self.y + self.height - 10, 5, 10 - (3 - leg_offset)))

            gun_start = draw_x + (self.width if self.direction > 0 else -8)
            pygame.draw.rect(screen, gun_color, (gun_start, self.y + 16, 8 * self.direction, 3))

        elif self.type == 'turret':
            base_color = (100, 100, 100)
            gun_color = (60, 60, 60)

            pygame.draw.rect(screen, base_color, (draw_x + 2, self.y + self.height - 16, self.width - 4, 16))
            pygame.draw.rect(screen, base_color, (draw_x + 4, self.y + 8, self.width - 8, 12))

            gun_start = draw_x + (self.width if self.direction > 0 else -10)
            pygame.draw.rect(screen, gun_color, (gun_start, self.y + 12, 10 * self.direction, 4))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
