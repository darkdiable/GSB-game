import pygame
import math
from constants import *


class Player:
    """玩家类 - 马里奥"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel_x = 0
        self.vel_y = 0
        self.speed = PLAYER_SPEED
        self.jump_force = JUMP_FORCE
        self.gravity = GRAVITY
        self.is_grounded = False
        self.facing_right = True
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.score = 0
        self.coins = 0
        self.active = True
        self.invincible = False
        self.invincible_timer = 0
        self.anim_frame = 0
        self.walk_animation = 0
        self.is_dead = False
        self.death_timer = 0

    def handle_input(self, keys):
        """处理键盘输入"""
        if self.is_dead:
            return

        self.vel_x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
            if self.is_grounded:
                self.vel_y = self.jump_force
                self.is_grounded = False

    def update(self, solids, level):
        """更新玩家状态"""
        if self.is_dead:
            self.death_timer += 1
            if self.death_timer < 60:
                self.vel_y += self.gravity
                self.y += self.vel_y
            else:
                self.active = False
            return

        if self.invincible:
            self.invincible_timer -= 16
            if self.invincible_timer <= 0:
                self.invincible = False

        if self.vel_x != 0:
            self.walk_animation = (self.walk_animation + 1) % 20
        else:
            self.walk_animation = 0

        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15

        self.x += self.vel_x

        self.x = max(0, self.x)

        self._check_horizontal_collisions(solids)

        self.y += self.vel_y

        self._check_vertical_collisions(solids, level)

        if self.y > SCREEN_HEIGHT + 100:
            self.take_damage(fall=True)

        self.anim_frame = (self.anim_frame + 1) % 60

    def _check_horizontal_collisions(self, solids):
        """检测水平碰撞"""
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for solid in solids:
            if player_rect.colliderect(solid):
                if self.vel_x > 0:
                    self.x = solid.left - self.width
                elif self.vel_x < 0:
                    self.x = solid.right
                self.vel_x = 0
                player_rect.x = self.x

    def _check_vertical_collisions(self, solids, level):
        """检测垂直碰撞"""
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_grounded = False

        if self.vel_y < 0:
            self._check_head_hit(level)

        for solid in solids:
            if player_rect.colliderect(solid):
                if self.vel_y > 0:
                    self.y = solid.top - self.height
                    self.vel_y = 0
                    self.is_grounded = True
                elif self.vel_y < 0:
                    self.y = solid.bottom
                    self.vel_y = 0
                player_rect.y = self.y

    def _check_head_hit(self, level):
        """检测头顶碰撞砖块，优先检测问号砖"""
        bricks = level.get_bricks()
        next_y = self.y + self.vel_y
        head_rect = pygame.Rect(self.x, next_y, self.width, abs(self.vel_y) + 2)

        question_bricks = [b for b in bricks if hasattr(b, 'used')]
        normal_bricks = [b for b in bricks if not hasattr(b, 'used')]
        
        for brick in question_bricks + normal_bricks:
            brick_rect = brick.get_rect()
            if head_rect.colliderect(brick_rect):
                if hasattr(brick, 'used'):
                    if brick.hit():
                        from items import Coin
                        coin_x = brick.x + (brick.width - COIN_SIZE) // 2
                        coin_y = brick.y - COIN_SIZE
                        level.coins_to_spawn.append(Coin(coin_x, coin_y, is_spawning=True))
                else:
                    brick.hit()
                break

    def take_damage(self, fall=False):
        """受伤"""
        if self.invincible or self.is_dead:
            return

        if fall:
            self.health = 0
        else:
            self.health -= 1

        self.invincible = True
        self.invincible_timer = PLAYER_INVINCIBLE_TIME

        if self.health <= 0:
            self.is_dead = True
            self.vel_y = -10
            self.active = False

    def is_alive(self):
        """是否存活"""
        return self.health > 0 and not self.is_dead

    def get_rect(self):
        return pygame.Rect(self.x + 4, self.y + 4, self.width - 8, self.height - 8)

    def get_full_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def add_score(self, points):
        """增加分数"""
        self.score += points

    def add_coin(self):
        """收集金币"""
        self.coins += 1
        self.score += COIN_SCORE

    def draw(self, screen, camera_x):
        """绘制马里奥"""
        if self.is_dead:
            self._draw_mario(screen, camera_x)
            return

        if self.invincible and (pygame.time.get_ticks() // 100) % 2 == 0:
            return

        self._draw_mario(screen, camera_x)

    def _draw_mario(self, screen, camera_x):
        """实际绘制马里奥"""
        draw_x = int(self.x - camera_x)
        draw_y = int(self.y)

        if not self.facing_right:
            surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self._draw_mario_body(surface, 0, 0)
            flipped_surface = pygame.transform.flip(surface, True, False)
            screen.blit(flipped_surface, (draw_x, draw_y))
        else:
            self._draw_mario_body(screen, draw_x, draw_y)

    def _draw_mario_body(self, surface, x, y):
        """绘制马里奥身体"""
        walk_offset = 0
        if self.vel_x != 0 and self.is_grounded:
            walk_offset = (self.walk_animation // 5) % 2

        arm_swing = 0
        if self.vel_x != 0 and self.is_grounded:
            arm_swing = int(5 * math.sin(self.walk_animation * 0.5))

        # 帽子
        pygame.draw.rect(surface, RED, (x + 4, y + 0, 24, 8))
        pygame.draw.rect(surface, RED, (x + 8, y + 4, 20, 4))
        pygame.draw.rect(surface, DARK_RED, (x + 4, y + 6, 24, 2))

        # 帽檐
        pygame.draw.rect(surface, RED, (x + 2, y + 8, 28, 4))

        # 脸部
        pygame.draw.rect(surface, SKIN, (x + 8, y + 12, 16, 12))

        # 眼睛
        pygame.draw.rect(surface, BLACK, (x + 18, y + 14, 4, 4))
        pygame.draw.rect(surface, BLACK, (x + 10, y + 14, 4, 4))

        # 胡子
        pygame.draw.rect(surface, BROWN, (x + 10, y + 20, 14, 3))
        pygame.draw.rect(surface, BROWN, (x + 8, y + 18, 4, 2))
        pygame.draw.rect(surface, BROWN, (x + 20, y + 18, 4, 2))

        # 身体（背带裤）
        pygame.draw.rect(surface, BLUE, (x + 6, y + 24, 20, 16))

        # 上衣
        pygame.draw.rect(surface, RED, (x + 4, y + 24, 24, 8))

        # 纽扣
        pygame.draw.circle(surface, YELLOW, (x + 10, y + 32), 2)
        pygame.draw.circle(surface, YELLOW, (x + 22, y + 32), 2)

        # 手臂
        pygame.draw.rect(surface, RED, (x + 0, y + 24 + arm_swing, 6, 8))
        pygame.draw.rect(surface, RED, (x + 26, y + 24 - arm_swing, 6, 8))

        # 手套
        pygame.draw.rect(surface, SKIN, (x + 0, y + 30 + arm_swing, 6, 4))
        pygame.draw.rect(surface, SKIN, (x + 26, y + 30 - arm_swing, 6, 4))

        # 腿部
        if self.is_grounded and self.vel_x != 0:
            if walk_offset == 0:
                pygame.draw.rect(surface, BLUE, (x + 6, y + 40, 8, 8))
                pygame.draw.rect(surface, BROWN, (x + 4, y + 44, 12, 4))
                pygame.draw.rect(surface, BLUE, (x + 18, y + 40, 8, 8))
                pygame.draw.rect(surface, BROWN, (x + 16, y + 44, 12, 4))
            else:
                pygame.draw.rect(surface, BLUE, (x + 6, y + 42, 8, 6))
                pygame.draw.rect(surface, BROWN, (x + 4, y + 44, 12, 4))
                pygame.draw.rect(surface, BLUE, (x + 18, y + 40, 8, 8))
                pygame.draw.rect(surface, BROWN, (x + 16, y + 44, 12, 4))
        else:
            pygame.draw.rect(surface, BLUE, (x + 6, y + 40, 8, 8))
            pygame.draw.rect(surface, BROWN, (x + 4, y + 44, 12, 4))
            pygame.draw.rect(surface, BLUE, (x + 18, y + 40, 8, 8))
            pygame.draw.rect(surface, BROWN, (x + 16, y + 44, 12, 4))
