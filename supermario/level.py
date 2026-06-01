import pygame
from constants import *
import random


class Ground:
    """地面类"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        pygame.draw.rect(screen, DARK_BROWN, (draw_x, self.y, self.width, self.height))
        pygame.draw.rect(screen, FOREST_GREEN, (draw_x, self.y, self.width, 12))

        # 绘制草地纹理
        for i in range(0, self.width, 16):
            pygame.draw.rect(screen, LIME_GREEN, (draw_x + i, self.y, 8, 6))

        # 绘制土块纹理
        for row in range(2, self.height // 16):
            for col in range(0, self.width // 16):
                offset_x = (row % 2) * 8
                tile_x = draw_x + col * 16 + offset_x
                tile_y = self.y + row * 16
                if tile_x < draw_x + self.width:
                    pygame.draw.rect(screen, BROWN, (tile_x, tile_y, 14, 14))
                    pygame.draw.rect(screen, LIGHT_BROWN, (tile_x + 2, tile_y + 2, 4, 4))


class Brick:
    """普通砖块类"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.active = True
        self.hit_animation = 0

    def hit(self):
        """被顶时的动画"""
        if self.hit_animation == 0:
            self.hit_animation = 10

    def update(self):
        if self.hit_animation > 0:
            self.hit_animation -= 1

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_x):
        if not self.active:
            return

        draw_x = self.x - camera_x
        offset_y = 0
        if self.hit_animation > 0:
            offset_y = -self.hit_animation * 2

        # 砖块主体
        pygame.draw.rect(screen, LIGHT_BROWN, (draw_x, self.y + offset_y, self.width, self.height))
        pygame.draw.rect(screen, BROWN, (draw_x, self.y + offset_y, self.width, self.height), 2)

        # 砖块纹理
        pygame.draw.line(screen, DARK_BROWN, (draw_x, self.y + offset_y + self.height // 2),
                         (draw_x + self.width, self.y + offset_y + self.height // 2), 2)
        pygame.draw.line(screen, DARK_BROWN, (draw_x + self.width // 2, self.y + offset_y),
                         (draw_x + self.width // 2, self.y + offset_y + self.height // 2), 2)
        pygame.draw.line(screen, DARK_BROWN, (draw_x + self.width // 4, self.y + offset_y + self.height // 2),
                         (draw_x + self.width // 4, self.y + offset_y + self.height), 2)
        pygame.draw.line(screen, DARK_BROWN, (draw_x + self.width * 3 // 4, self.y + offset_y + self.height // 2),
                         (draw_x + self.width * 3 // 4, self.y + offset_y + self.height), 2)


class QuestionBrick:
    """问号砖块类"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = QUESTION_BRICK_SIZE
        self.height = QUESTION_BRICK_SIZE
        self.active = True
        self.used = False
        self.hit_animation = 0
        self.anim_frame = 0

    def hit(self):
        """被顶时的动画"""
        if not self.used and self.hit_animation == 0:
            self.hit_animation = 12
            self.used = True
            return True
        return False

    def update(self):
        if self.hit_animation > 0:
            self.hit_animation -= 1
        self.anim_frame = (self.anim_frame + 1) % 60

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_x):
        if not self.active:
            return

        draw_x = self.x - camera_x
        offset_y = 0
        if self.hit_animation > 0:
            offset_y = -self.hit_animation * 2

        if self.used:
            # 已使用的砖块
            pygame.draw.rect(screen, DARK_BROWN, (draw_x, self.y + offset_y, self.width, self.height))
            pygame.draw.rect(screen, BROWN, (draw_x + 2, self.y + offset_y + 2, self.width - 4, self.height - 4))
        else:
            # 闪烁效果
            brightness = 0.8 + 0.2 * (pygame.time.get_ticks() // 200 % 2)
            color = (int(YELLOW[0] * brightness), int(YELLOW[1] * brightness), int(YELLOW[2] * brightness))

            # 砖块主体
            pygame.draw.rect(screen, GOLD, (draw_x, self.y + offset_y, self.width, self.height))
            pygame.draw.rect(screen, color, (draw_x + 2, self.y + offset_y + 2, self.width - 4, self.height - 4))

            # 问号
            font = pygame.font.Font(None, 28)
            text = font.render('?', True, BROWN)
            text_rect = text.get_rect(center=(draw_x + self.width // 2, self.y + offset_y + self.height // 2))
            screen.blit(text, text_rect)

        # 边框
        pygame.draw.rect(screen, DARK_BROWN, (draw_x, self.y + offset_y, self.width, self.height), 2)


class Pipe:
    """水管类"""

    def __init__(self, x, y, height=PIPE_HEIGHT):
        self.x = x
        self.y = y
        self.width = PIPE_WIDTH
        self.height = height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x

        # 水管主体
        pygame.draw.rect(screen, FOREST_GREEN, (draw_x, self.y, self.width, self.height))
        pygame.draw.rect(screen, DARK_GREEN, (draw_x, self.y, self.width, self.height), 2)

        # 水管顶部
        top_height = 16
        pygame.draw.rect(screen, LIME_GREEN, (draw_x - 4, self.y, self.width + 8, top_height))
        pygame.draw.rect(screen, DARK_GREEN, (draw_x - 4, self.y, self.width + 8, top_height), 2)

        # 水管高光
        pygame.draw.rect(screen, LIME_GREEN, (draw_x + 6, self.y + top_height, 8, self.height - top_height))

        # 水管阴影
        pygame.draw.rect(screen, DARK_GREEN, (draw_x + self.width - 12, self.y + top_height, 8, self.height - top_height))


class Cloud:
    """云朵背景类"""

    def __init__(self, x, y, size=1):
        self.x = x
        self.y = y
        self.size = size
        self.parallax_factor = 0.3

    def update(self, player_x):
        pass

    def draw(self, screen, camera_x):
        draw_x = int(self.x - camera_x * self.parallax_factor) % (SCREEN_WIDTH + 200) - 100

        base_radius = int(20 * self.size)

        # 云朵由多个圆形组成
        pygame.draw.circle(screen, WHITE, (draw_x, self.y), base_radius)
        pygame.draw.circle(screen, WHITE, (draw_x + base_radius, self.y - base_radius // 2), base_radius)
        pygame.draw.circle(screen, WHITE, (draw_x + base_radius * 2, self.y), base_radius)
        pygame.draw.circle(screen, WHITE, (draw_x + base_radius // 2, self.y - base_radius // 3), int(base_radius * 0.8))
        pygame.draw.circle(screen, WHITE, (draw_x + base_radius * 1.5, self.y - base_radius // 3), int(base_radius * 0.8))


class Hill:
    """山丘背景类"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.parallax_factor = 0.5

    def draw(self, screen, camera_x):
        draw_x = int(self.x - camera_x * self.parallax_factor)

        # 绘制山丘
        pygame.draw.ellipse(screen, FOREST_GREEN, (draw_x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, LIME_GREEN, (draw_x + 10, self.y + 5, self.width - 20, self.height - 10))


class Level:
    """关卡管理类"""

    def __init__(self):
        self.grounds = []
        self.bricks = []
        self.question_bricks = []
        self.pipes = []
        self.clouds = []
        self.hills = []
        self.enemy_spawn_points = []
        self.goal_x = LEVEL_WIDTH - 200
        self._generate_level()

    def _generate_level(self):
        """生成关卡"""
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT

        # 地面 - 分段生成，包含坑洞
        segments = [
            (0, 800),
            (900, 1800),
            (1900, 2800),
            (2900, 3800),
            (3900, LEVEL_WIDTH)
        ]
        for start, end in segments:
            self.grounds.append(Ground(start, ground_y, end - start, GROUND_HEIGHT))

        # 云朵
        for i in range(20):
            x = random.randint(0, LEVEL_WIDTH)
            y = random.randint(30, 180)
            size = random.choice([0.8, 1.0, 1.2, 1.5])
            self.clouds.append(Cloud(x, y, size))

        # 山丘
        hill_positions = [(200, 3), (800, 2), (1500, 4), (2400, 3), (3200, 5), (4200, 3)]
        for x, size in hill_positions:
            width = size * 80
            height = size * 50
            self.hills.append(Hill(x, ground_y - height + 20, width, height))

        # 砖块和问号砖块组合
        brick_layouts = [
            # 第一段
            (300, ground_y - 128, 'question'),
            (332, ground_y - 128, 'brick'),
            (364, ground_y - 128, 'question'),
            (396, ground_y - 128, 'brick'),
            (332, ground_y - 160, 'question'),

            # 第二段
            (600, ground_y - 128, 'brick'),
            (632, ground_y - 128, 'brick'),
            (664, ground_y - 128, 'brick'),

            # 第三段
            (1000, ground_y - 160, 'question'),
            (1032, ground_y - 160, 'brick'),
            (1064, ground_y - 160, 'question'),

            # 第四段
            (1300, ground_y - 128, 'brick'),
            (1332, ground_y - 128, 'brick'),
            (1364, ground_y - 128, 'question'),
            (1396, ground_y - 128, 'brick'),
            (1428, ground_y - 128, 'brick'),

            # 第五段 - 高空平台
            (1700, ground_y - 224, 'brick'),
            (1732, ground_y - 224, 'brick'),
            (1764, ground_y - 224, 'brick'),

            # 第六段
            (2100, ground_y - 128, 'question'),
            (2132, ground_y - 128, 'question'),
            (2164, ground_y - 128, 'question'),

            # 第七段 - 阶梯
            (2400, ground_y - 32, 'brick'),
            (2432, ground_y - 64, 'brick'),
            (2464, ground_y - 96, 'brick'),
            (2496, ground_y - 128, 'brick'),
            (2528, ground_y - 160, 'brick'),

            # 第八段
            (3000, ground_y - 160, 'brick'),
            (3032, ground_y - 160, 'question'),
            (3064, ground_y - 160, 'brick'),
            (3096, ground_y - 160, 'question'),

            # 第九段
            (3400, ground_y - 128, 'brick'),
            (3432, ground_y - 128, 'brick'),
            (3464, ground_y - 128, 'brick'),
            (3496, ground_y - 128, 'question'),
            (3528, ground_y - 128, 'brick'),
            (3560, ground_y - 128, 'brick'),
            (3592, ground_y - 128, 'brick'),

            # 第十段 - 高空平台
            (3900, ground_y - 192, 'brick'),
            (3932, ground_y - 192, 'brick'),
            (3964, ground_y - 192, 'question'),
            (3996, ground_y - 192, 'brick'),
            (4028, ground_y - 192, 'brick'),

            # 第十一段
            (4300, ground_y - 128, 'question'),
            (4332, ground_y - 128, 'brick'),
            (4364, ground_y - 128, 'question'),
            (4396, ground_y - 128, 'brick'),
            (4428, ground_y - 128, 'question'),
        ]

        for x, y, brick_type in brick_layouts:
            if brick_type == 'brick':
                self.bricks.append(Brick(x, y))
            else:
                self.question_bricks.append(QuestionBrick(x, y))

        # 水管
        pipe_positions = [
            (500, ground_y - 96, 96),
            (1100, ground_y - 128, 128),
            (2000, ground_y - 96, 96),
            (2700, ground_y - 160, 160),
            (3200, ground_y - 96, 96),
            (3700, ground_y - 128, 128),
            (4500, ground_y - 96, 96),
        ]
        for x, y, height in pipe_positions:
            self.pipes.append(Pipe(x, y, height))

        # 敌人生成点
        self.enemy_spawn_points = [
            (400, ground_y - ENEMY_HEIGHT),
            (700, ground_y - ENEMY_HEIGHT),
            (1200, ground_y - ENEMY_HEIGHT),
            (1500, ground_y - ENEMY_HEIGHT),
            (2200, ground_y - ENEMY_HEIGHT),
            (2500, ground_y - ENEMY_HEIGHT),
            (3100, ground_y - ENEMY_HEIGHT),
            (3500, ground_y - ENEMY_HEIGHT),
            (4100, ground_y - ENEMY_HEIGHT),
            (4400, ground_y - ENEMY_HEIGHT),
            (4700, ground_y - ENEMY_HEIGHT),
        ]

    def update(self):
        """更新关卡元素"""
        for brick in self.bricks:
            brick.update()
        for q_brick in self.question_bricks:
            q_brick.update()

    def get_all_solids(self):
        """获取所有可碰撞的实体"""
        solids = []
        for ground in self.grounds:
            solids.append(ground.get_rect())
        for brick in self.bricks:
            if brick.active:
                solids.append(brick.get_rect())
        for q_brick in self.question_bricks:
            if q_brick.active:
                solids.append(q_brick.get_rect())
        for pipe in self.pipes:
            solids.append(pipe.get_rect())
        return solids

    def get_bricks(self):
        """获取所有砖块（用于头顶碰撞检测）"""
        bricks = []
        for brick in self.bricks:
            if brick.active:
                bricks.append(brick)
        for q_brick in self.question_bricks:
            if q_brick.active:
                bricks.append(q_brick)
        return bricks

    def draw_background(self, screen, camera_x):
        """绘制背景"""
        # 绘制渐变天空
        for y in range(SCREEN_HEIGHT - GROUND_HEIGHT):
            t = y / (SCREEN_HEIGHT - GROUND_HEIGHT)
            r = int(SKY_BLUE[0] * (1 - t) + DEEP_SKY_BLUE[0] * t)
            g = int(SKY_BLUE[1] * (1 - t) + DEEP_SKY_BLUE[1] * t)
            b = int(SKY_BLUE[2] * (1 - t) + DEEP_SKY_BLUE[2] * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # 绘制山丘
        for hill in self.hills:
            hill.draw(screen, camera_x)

        # 绘制云朵
        for cloud in self.clouds:
            cloud.draw(screen, camera_x)

    def draw_foreground(self, screen, camera_x):
        """绘制前景（可交互元素）"""
        # 绘制地面
        for ground in self.grounds:
            ground.draw(screen, camera_x)

        # 绘制砖块
        for brick in self.bricks:
            brick.draw(screen, camera_x)

        # 绘制问号砖块
        for q_brick in self.question_bricks:
            q_brick.draw(screen, camera_x)

        # 绘制水管
        for pipe in self.pipes:
            pipe.draw(screen, camera_x)

        # 绘制终点旗杆
        goal_draw_x = self.goal_x - camera_x
        if 0 < goal_draw_x < SCREEN_WIDTH + 100:
            ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
            pygame.draw.rect(screen, WHITE, (goal_draw_x, ground_y - 300, 6, 300))
            pygame.draw.polygon(screen, GREEN, [
                (goal_draw_x + 6, ground_y - 300),
                (goal_draw_x + 6, ground_y - 260),
                (goal_draw_x + 50, ground_y - 280)
            ])
            # 顶部圆球
            pygame.draw.circle(screen, YELLOW, (goal_draw_x + 3, ground_y - 305), 8)
