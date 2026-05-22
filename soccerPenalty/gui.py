# 图形界面模块
# 使用 Pygame 创建足球点球游戏的可视化界面

import pygame
import sys
import math
import os
from typing import Tuple, List, Optional


# 颜色定义
class Colors:
    """颜色常量类"""
    GREEN = (34, 139, 34)          # 草坪绿
    DARK_GREEN = (22, 100, 22)     # 深绿（草坪条纹）
    WHITE = (255, 255, 255)        # 白色
    BLACK = (0, 0, 0)              # 黑色
    RED = (220, 20, 60)            # 红色（球员）
    BLUE = (30, 144, 255)          # 蓝色（守门员）
    YELLOW = (255, 215, 0)         # 黄色（裁判）
    ORANGE = (255, 140, 0)         # 橙色（足球）
    GRAY = (128, 128, 128)         # 灰色
    LIGHT_GRAY = (200, 200, 200)   # 浅灰色
    GOLD = (255, 215, 0)           # 金色


# 游戏状态
class GameState:
    """游戏状态枚举"""
    MENU = "menu"
    WAITING = "waiting"           # 等待裁判发令
    REFEREE_READY = "ready"       # 裁判显示"准备"
    REFEREE_START = "start"       # 裁判显示"开始"
    CHOOSE_SAVE = "choose_save"   # 选择扑救方向
    CHOOSE_SHOOT = "choose_shoot" # 选择射门方向
    ANIMATING = "animating"       # 动画播放中
    ROUND_RESULT = "round_result" # 显示本轮结果
    GAME_OVER = "game_over"       # 游戏结束


def get_chinese_font() -> Optional[str]:
    """
    查找系统中可用的中文字体

    Returns:
        Optional[str]: 中文字体名称或字体文件路径，找不到返回None
    """
    # 优先尝试的中文字体名称（按优先级排序）
    font_names = [
        'stheitimedium',      # 华文黑体 - Mac系统
        'stheitilight',       # 华文黑体细体
        'hiraginosansgb',   # 冬青黑体简体中文
        'songti',           # 宋体
        'applesdgothicneo', # Apple SD Gothic Neo
        'kailasa',         # 藏文，但可能支持部分中文
        'arialunicodems',      # Arial Unicode MS
    ]

    # 检查系统字体
    available_fonts = pygame.font.get_fonts()
    for font_name in font_names:
        if font_name in available_fonts:
            return font_name

    # 尝试查找字体文件
    font_files = [
        '/Library/Fonts/Arial Unicode.ttf',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/AppleSDGothicNeo.ttc',
    ]

    for font_file in font_files:
        if os.path.exists(font_file):
            return font_file

    return None


class SoccerGUI:
    """
    足球点球游戏图形界面类
    """

    # 窗口尺寸
    WIDTH = 900
    HEIGHT = 700

    # 球门尺寸和位置
    GOAL_X = 250
    GOAL_Y = 50
    GOAL_WIDTH = 400
    GOAL_HEIGHT = 200
    POST_WIDTH = 8

    # 方向选择区域（7个方向）
    DIRECTION_ZONES = {
        '左上': (270, 70, 80, 80),
        '右上': (550, 70, 80, 80),
        '左下': (270, 150, 80, 80),
        '右下': (550, 150, 80, 80),
        '正左': (270, 110, 80, 80),
        '正右': (550, 110, 80, 80),
        '正中': (410, 110, 80, 80),
    }

    def __init__(self):
        """初始化图形界面"""
        pygame.init()
        pygame.display.set_caption("⚽ 足球点球大战 ⚽")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        # 获取中文字体
        self.chinese_font = get_chinese_font()
        if self.chinese_font:
            print(f"✅ 使用中文字体: {self.chinese_font}")
            if os.path.exists(self.chinese_font):
                # 从文件加载字体
                self.font_large = pygame.font.Font(self.chinese_font, 48)
                self.font_large.set_bold(True)
                self.font_medium = pygame.font.Font(self.chinese_font, 32)
                self.font_medium.set_bold(True)
                self.font_small = pygame.font.Font(self.chinese_font, 20)
                self.font_tiny = pygame.font.Font(self.chinese_font, 16)
            else:
                # 使用系统字体名称
                self.font_large = pygame.font.SysFont(self.chinese_font, 48, bold=True)
                self.font_medium = pygame.font.SysFont(self.chinese_font, 32, bold=True)
                self.font_small = pygame.font.SysFont(self.chinese_font, 20)
                self.font_tiny = pygame.font.SysFont(self.chinese_font, 16)
        else:
            # 找不到中文字体时的降级方案
            print("⚠️  未找到中文字体，使用默认字体，可能存在乱码")
            self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
            self.font_medium = pygame.font.SysFont("Arial", 32, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 20)
            self.font_tiny = pygame.font.SysFont("Arial", 16)

        # 足球位置（用于动画）
        self.ball_start_pos = (450, 500)
        self.ball_pos = list(self.ball_start_pos)
        self.ball_target_pos = None
        self.ball_speed = 0

        # 守门员位置
        self.gk_start_pos = (450, 150)
        self.gk_pos = list(self.gk_start_pos)
        self.gk_target_pos = None
        self.gk_speed = 0

        # 游戏状态
        self.state = GameState.MENU
        self.selected_direction = None
        self.selected_power = 5
        self.animation_progress = 0

        # 动画回调
        self.animation_complete_callback = None

    def draw_field(self):
        """绘制足球场"""
        # 草坪底色
        self.screen.fill(Colors.GREEN)

        # 草坪条纹效果
        for y in range(0, self.HEIGHT, 40):
            if (y // 40) % 2 == 0:
                pygame.draw.rect(
                    self.screen,
                    Colors.DARK_GREEN,
                    (0, y, self.WIDTH, 40)
                )

        # 禁区线
        pygame.draw.rect(
            self.screen,
            Colors.WHITE,
            (self.GOAL_X - 50, self.GOAL_Y, self.GOAL_WIDTH + 100, self.GOAL_HEIGHT + 250),
            3
        )

        # 小禁区线
        pygame.draw.rect(
            self.screen,
            Colors.WHITE,
            (self.GOAL_X + 50, self.GOAL_Y, self.GOAL_WIDTH - 100, self.GOAL_HEIGHT + 100),
            2
        )

        # 点球点
        pygame.draw.circle(
            self.screen,
            Colors.WHITE,
            (450, 500),
            6
        )

        # 禁区弧
        pygame.draw.arc(
            self.screen,
            Colors.WHITE,
            (370, 450, 160, 100),
            math.pi * 0.2,
            math.pi * 0.8,
            2
        )

    def draw_goal(self):
        """绘制球门"""
        # 球门柱
        pygame.draw.rect(
            self.screen,
            Colors.WHITE,
            (self.GOAL_X - self.POST_WIDTH, self.GOAL_Y,
             self.POST_WIDTH, self.GOAL_HEIGHT)
        )
        pygame.draw.rect(
            self.screen,
            Colors.WHITE,
            (self.GOAL_X + self.GOAL_WIDTH, self.GOAL_Y,
             self.POST_WIDTH, self.GOAL_HEIGHT)
        )
        # 横梁
        pygame.draw.rect(
            self.screen,
            Colors.WHITE,
            (self.GOAL_X - self.POST_WIDTH, self.GOAL_Y - self.POST_WIDTH,
             self.GOAL_WIDTH + self.POST_WIDTH * 2, self.POST_WIDTH)
        )

        # 球网（简化绘制）
        net_color = (200, 200, 200)
        for i in range(0, self.GOAL_WIDTH, 20):
            pygame.draw.line(
                self.screen,
                net_color,
                (self.GOAL_X + i, self.GOAL_Y),
                (self.GOAL_X + i, self.GOAL_Y + self.GOAL_HEIGHT),
                1
            )
        for i in range(0, self.GOAL_HEIGHT, 20):
            pygame.draw.line(
                self.screen,
                net_color,
                (self.GOAL_X, self.GOAL_Y + i),
                (self.GOAL_X + self.GOAL_WIDTH, self.GOAL_Y + i),
                1
            )

    def draw_player(self, x: int, y: int, color: Tuple[int, int, int], name: str = ""):
        """绘制球员"""
        # 身体
        pygame.draw.circle(self.screen, color, (x, y), 20)
        pygame.draw.rect(self.screen, color, (x - 12, y + 10, 24, 30))

        # 腿
        pygame.draw.rect(self.screen, Colors.WHITE, (x - 10, y + 35, 8, 20))
        pygame.draw.rect(self.screen, Colors.WHITE, (x + 2, y + 35, 8, 20))

        # 手臂
        pygame.draw.rect(self.screen, color, (x - 22, y + 12, 10, 8))
        pygame.draw.rect(self.screen, color, (x + 12, y + 12, 10, 8))

        # 头部
        pygame.draw.circle(self.screen, (255, 220, 177), (x, y - 25), 15)

        # 名字标签
        if name:
            text = self.font_tiny.render(name, True, Colors.BLACK)
            text_rect = text.get_rect(center=(x, y - 50))
            self.screen.blit(text, text_rect)

    def draw_goalkeeper(self, x: int, y: int, is_player: bool = True):
        """绘制守门员"""
        color = Colors.BLUE if is_player else Colors.RED
        name = "你" if is_player else "电脑"

        # 身体（守门员更壮一些）
        pygame.draw.circle(self.screen, color, (x, y), 22)
        pygame.draw.rect(self.screen, color, (x - 15, y + 10, 30, 32))

        # 手臂张开
        pygame.draw.rect(self.screen, color, (x - 30, y + 5, 15, 10))
        pygame.draw.rect(self.screen, color, (x + 15, y + 5, 15, 10))

        # 手套
        pygame.draw.circle(self.screen, Colors.YELLOW, (x - 30, y + 10), 8)
        pygame.draw.circle(self.screen, Colors.YELLOW, (x + 30, y + 10), 8)

        # 腿
        pygame.draw.rect(self.screen, Colors.WHITE, (x - 12, y + 38, 10, 22))
        pygame.draw.rect(self.screen, Colors.WHITE, (x + 2, y + 38, 10, 22))

        # 头部
        pygame.draw.circle(self.screen, (255, 220, 177), (x, y - 28), 16)

        # 名字标签
        text = self.font_tiny.render(f"门将-{name}", True, Colors.BLACK)
        text_rect = text.get_rect(center=(x, y - 55))
        self.screen.blit(text, text_rect)

    def draw_referee(self, x: int, y: int, message: str = ""):
        """绘制裁判"""
        # 身体（黄色裁判服）
        pygame.draw.circle(self.screen, Colors.YELLOW, (x, y), 18)
        pygame.draw.rect(self.screen, Colors.YELLOW, (x - 10, y + 8, 20, 25))

        # 黑色条纹
        pygame.draw.rect(self.screen, Colors.BLACK, (x - 10, y + 12, 20, 3))
        pygame.draw.rect(self.screen, Colors.BLACK, (x - 10, y + 20, 20, 3))

        # 腿
        pygame.draw.rect(self.screen, Colors.BLACK, (x - 8, y + 30, 7, 18))
        pygame.draw.rect(self.screen, Colors.BLACK, (x + 1, y + 30, 7, 18))

        # 头部
        pygame.draw.circle(self.screen, (255, 220, 177), (x, y - 22), 13)

        # 头顶提示气泡
        if message:
            bubble_color = Colors.WHITE
            text = self.font_medium.render(message, True, Colors.RED)
            text_rect = text.get_rect()

            # 气泡背景
            bubble_width = text_rect.width + 30
            bubble_height = text_rect.height + 20
            bubble_x = x - bubble_width // 2
            bubble_y = y - 90

            pygame.draw.ellipse(
                self.screen,
                bubble_color,
                (bubble_x, bubble_y, bubble_width, bubble_height)
            )
            pygame.draw.ellipse(
                self.screen,
                Colors.BLACK,
                (bubble_x, bubble_y, bubble_width, bubble_height),
                2
            )

            # 气泡尾巴
            pygame.draw.polygon(
                self.screen,
                bubble_color,
                [(x - 10, bubble_y + bubble_height),
                 (x + 10, bubble_y + bubble_height),
                 (x, bubble_y + bubble_height + 15)]
            )
            pygame.draw.polygon(
                self.screen,
                Colors.BLACK,
                [(x - 10, bubble_y + bubble_height),
                 (x + 10, bubble_y + bubble_height),
                 (x, bubble_y + bubble_height + 15)],
                2
            )

            # 文字
            text_rect.center = (x, bubble_y + bubble_height // 2)
            self.screen.blit(text, text_rect)

    def draw_ball(self, x: int, y: int):
        """绘制足球"""
        # 足球主体
        pygame.draw.circle(self.screen, Colors.WHITE, (x, y), 14)
        pygame.draw.circle(self.screen, Colors.BLACK, (x, y), 14, 2)

        # 五边形图案
        for angle in range(0, 360, 72):
            rad = math.radians(angle)
            px = x + math.cos(rad) * 6
            py = y + math.sin(rad) * 6
            pygame.draw.polygon(
                self.screen,
                Colors.BLACK,
                [
                    (px, py - 4),
                    (px + 4, py),
                    (px, py + 4),
                    (px - 4, py)
                ]
            )

    def draw_direction_zones(self, highlight: str = None):
        """绘制方向选择区域"""
        for direction, (x, y, w, h) in self.DIRECTION_ZONES.items():
            # 半透明背景
            s = pygame.Surface((w, h))
            if highlight == direction:
                s.set_alpha(180)
                s.fill(Colors.GOLD)
            else:
                s.set_alpha(100)
                s.fill(Colors.LIGHT_GRAY)
            self.screen.blit(s, (x, y))

            # 边框
            pygame.draw.rect(
                self.screen,
                Colors.BLACK,
                (x, y, w, h),
                2
            )

            # 方向文字
            text = self.font_small.render(direction, True, Colors.BLACK)
            text_rect = text.get_rect(center=(x + w // 2, y + h // 2))
            self.screen.blit(text, text_rect)

    def draw_power_meter(self, power: int):
        """绘制力度条"""
        meter_x = 50
        meter_y = 250
        meter_width = 30
        meter_height = 200

        # 背景
        pygame.draw.rect(
            self.screen,
            Colors.BLACK,
            (meter_x - 2, meter_y - 2, meter_width + 4, meter_height + 4)
        )
        pygame.draw.rect(
            self.screen,
            Colors.LIGHT_GRAY,
            (meter_x, meter_y, meter_width, meter_height)
        )

        # 力度填充
        fill_height = int((power / 10) * meter_height)
        if power >= 8:
            color = Colors.RED
        elif power >= 5:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN

        pygame.draw.rect(
            self.screen,
            color,
            (meter_x, meter_y + meter_height - fill_height,
             meter_width, fill_height)
        )

        # 刻度
        for i in range(0, 11, 2):
            y_pos = meter_y + meter_height - int((i / 10) * meter_height)
            pygame.draw.line(
                self.screen,
                Colors.BLACK,
                (meter_x - 5, y_pos),
                (meter_x, y_pos),
                2
            )
            text = self.font_tiny.render(str(i), True, Colors.BLACK)
            self.screen.blit(text, (meter_x - 25, y_pos - 8))

        # 标签
        label = self.font_small.render("力度", True, Colors.WHITE)
        label_rect = label.get_rect(center=(meter_x + meter_width // 2, meter_y - 30))
        self.screen.blit(label, label_rect)

        # 当前力度值
        power_text = self.font_small.render(str(power), True, Colors.WHITE)
        power_rect = power_text.get_rect(
            center=(meter_x + meter_width // 2, meter_y + meter_height + 30)
        )
        self.screen.blit(power_text, power_rect)

    def draw_scoreboard(
        self,
        player_score: int,
        computer_score: int,
        current_round: int,
        total_rounds: int
    ):
        """绘制计分板"""
        panel_x = self.WIDTH - 200
        panel_y = 50
        panel_width = 150
        panel_height = 150

        # 半透明背景
        s = pygame.Surface((panel_width, panel_height))
        s.set_alpha(200)
        s.fill(Colors.BLACK)
        self.screen.blit(s, (panel_x, panel_y))

        # 边框
        pygame.draw.rect(
            self.screen,
            Colors.GOLD,
            (panel_x, panel_y, panel_width, panel_height),
            3
        )

        # 标题
        title = self.font_small.render("比分", True, Colors.GOLD)
        title_rect = title.get_rect(
            center=(panel_x + panel_width // 2, panel_y + 25)
        )
        self.screen.blit(title, title_rect)

        # 玩家分数
        player_text = self.font_medium.render(f"你: {player_score}", True, Colors.BLUE)
        player_rect = player_text.get_rect(
            center=(panel_x + panel_width // 2, panel_y + 60)
        )
        self.screen.blit(player_text, player_rect)

        # 电脑分数
        comp_text = self.font_medium.render(f"电脑: {computer_score}", True, Colors.RED)
        comp_rect = comp_text.get_rect(
            center=(panel_x + panel_width // 2, panel_y + 95)
        )
        self.screen.blit(comp_text, comp_rect)

        # 轮次
        round_text = self.font_small.render(
            f"第 {current_round}/{total_rounds} 轮",
            True,
            Colors.WHITE
        )
        round_rect = round_text.get_rect(
            center=(panel_x + panel_width // 2, panel_y + 130)
        )
        self.screen.blit(round_text, round_rect)

    def draw_message(self, message: str, y_offset: int = 0, color: Tuple[int, int, int] = Colors.WHITE):
        """在屏幕中央显示消息"""
        text = self.font_large.render(message, True, color)
        text_rect = text.get_rect(
            center=(self.WIDTH // 2, self.HEIGHT // 2 + y_offset)
        )

        # 阴影效果
        shadow = self.font_large.render(message, True, Colors.BLACK)
        shadow_rect = shadow.get_rect(
            center=(self.WIDTH // 2 + 3, self.HEIGHT // 2 + y_offset + 3)
        )
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)

    def draw_sub_message(self, message: str, y_offset: int = 50):
        """显示子消息"""
        text = self.font_medium.render(message, True, Colors.WHITE)
        text_rect = text.get_rect(
            center=(self.WIDTH // 2, self.HEIGHT // 2 + y_offset)
        )
        self.screen.blit(text, text_rect)

    def draw_menu(self):
        """绘制主菜单"""
        self.draw_field()
        self.draw_goal()

        # 标题
        title = self.font_large.render("⚽ 足球点球大战 ⚽", True, Colors.GOLD)
        title_rect = title.get_rect(center=(self.WIDTH // 2, 150))
        shadow = self.font_large.render("⚽ 足球点球大战 ⚽", True, Colors.BLACK)
        shadow_rect = shadow.get_rect(center=(self.WIDTH // 2 + 3, 153))
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)

        # 说明文字
        instructions = [
            "游戏规则:",
            "1. 每队各有5名球员轮流射门",
            "2. 每队各有一名守门员轮流守门",
            "3. 裁判头顶显示'开始'后才能射门",
            "4. 点击球门区域选择射门/扑救方向",
            "5. 按 ↑↓ 键调整射门力度",
            "6. 进球多的队伍获胜",
        ]

        y_pos = 250
        for inst in instructions:
            text = self.font_small.render(inst, True, Colors.WHITE)
            text_rect = text.get_rect(center=(self.WIDTH // 2, y_pos))
            self.screen.blit(text, text_rect)
            y_pos += 35

        # 开始提示
        start_text = self.font_medium.render(
            "点击任意位置或按空格键开始游戏",
            True,
            Colors.YELLOW
        )
        start_rect = start_text.get_rect(center=(self.WIDTH // 2, 580))
        self.screen.blit(start_text, start_rect)

        # 绘制装饰性的球员和裁判
        self.draw_player(200, 400, Colors.RED, "球员")
        self.draw_goalkeeper(450, 150, True)
        self.draw_referee(650, 450, "")

    def draw_shot_indicator(self, direction: str):
        """绘制射门方向指示线"""
        if direction not in self.DIRECTION_ZONES:
            return

        zone = self.DIRECTION_ZONES[direction]
        target_x = zone[0] + zone[2] // 2
        target_y = zone[1] + zone[3] // 2

        # 绘制虚线
        start_x, start_y = self.ball_start_pos
        for i in range(0, 100, 10):
            t = i / 100
            x = start_x + (target_x - start_x) * t
            y = start_y + (target_y - start_y) * t
            pygame.draw.circle(self.screen, Colors.ORANGE, (int(x), int(y)), 3)

    def get_direction_at_pos(self, pos: Tuple[int, int]) -> Optional[str]:
        """获取鼠标位置对应的方向"""
        for direction, (x, y, w, h) in self.DIRECTION_ZONES.items():
            if x <= pos[0] <= x + w and y <= pos[1] <= y + h:
                return direction
        return None

    def start_animation(
        self,
        shoot_direction: str,
        save_direction: str,
        callback
    ):
        """开始射门动画"""
        self.state = GameState.ANIMATING
        self.animation_progress = 0

        # 设置目标位置
        if shoot_direction in self.DIRECTION_ZONES:
            zone = self.DIRECTION_ZONES[shoot_direction]
            self.ball_target_pos = (
                zone[0] + zone[2] // 2,
                zone[1] + zone[3] // 2
            )
        else:
            self.ball_target_pos = self.gk_start_pos

        if save_direction in self.DIRECTION_ZONES:
            zone = self.DIRECTION_ZONES[save_direction]
            self.gk_target_pos = (
                zone[0] + zone[2] // 2,
                zone[1] + zone[3] // 2
            )
        else:
            self.gk_target_pos = self.gk_start_pos

        self.ball_speed = 8
        self.gk_speed = 6
        self.animation_complete_callback = callback

    def update_animation(self) -> bool:
        """更新动画，返回是否完成"""
        if self.state != GameState.ANIMATING:
            return False

        self.animation_progress += 1

        # 更新足球位置
        if self.ball_target_pos:
            dx = self.ball_target_pos[0] - self.ball_pos[0]
            dy = self.ball_target_pos[1] - self.ball_pos[1]
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < self.ball_speed:
                self.ball_pos = list(self.ball_target_pos)
            else:
                self.ball_pos[0] += (dx / dist) * self.ball_speed
                self.ball_pos[1] += (dy / dist) * self.ball_speed

        # 更新守门员位置
        if self.gk_target_pos and self.animation_progress > 10:
            dx = self.gk_target_pos[0] - self.gk_pos[0]
            dy = self.gk_target_pos[1] - self.gk_pos[1]
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < self.gk_speed:
                self.gk_pos = list(self.gk_target_pos)
            else:
                self.gk_pos[0] += (dx / dist) * self.gk_speed
                self.gk_pos[1] += (dy / dist) * self.gk_speed

        # 检查动画是否完成
        ball_reached = (abs(self.ball_pos[0] - self.ball_target_pos[0]) < 2 and
                        abs(self.ball_pos[1] - self.ball_target_pos[1]) < 2)
        gk_reached = (abs(self.gk_pos[0] - self.gk_target_pos[0]) < 2 and
                      abs(self.gk_pos[1] - self.gk_target_pos[1]) < 2)

        if ball_reached and gk_reached and self.animation_progress > 40:
            # 动画完成，等待一会儿后回调
            if self.animation_progress > 80:
                if self.animation_complete_callback:
                    self.animation_complete_callback()
                return True

        return False

    def reset_positions(self):
        """重置球和守门员位置"""
        self.ball_pos = list(self.ball_start_pos)
        self.gk_pos = list(self.gk_start_pos)
        self.ball_target_pos = None
        self.gk_target_pos = None

    def handle_events(self) -> Tuple[bool, Optional[str], Optional[int]]:
        """
        处理事件

        Returns:
            Tuple[bool, Optional[str], Optional[int]]:
                (是否应该继续运行, 选择的方向, 调整的力度)
        """
        direction = None
        power_delta = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None, None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False, None, None
                elif event.key == pygame.K_SPACE:
                    direction = "SPACE"
                elif event.key == pygame.K_UP:
                    power_delta = 1
                elif event.key == pygame.K_DOWN:
                    power_delta = -1
                elif event.key == pygame.K_RETURN:
                    direction = "ENTER"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                direction = self.get_direction_at_pos(mouse_pos)
                if direction is None:
                    direction = "CLICK"

        return True, direction, power_delta

    def render(self):
        """渲染当前帧"""
        pygame.display.flip()
        self.clock.tick(60)

    def clear(self):
        """清除屏幕"""
        self.screen.fill(Colors.BLACK)

    def close(self):
        """关闭界面"""
        pygame.quit()
