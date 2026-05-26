# -*- coding: utf-8 -*-
"""
工具函数模块 - 提供游戏中使用的辅助函数
"""

import pygame
from constants import *


def draw_background(screen, camera_x):
    """
    绘制卷轴背景
    包含天空、云朵和远山

    Args:
        screen: 游戏屏幕
        camera_x: 摄像机X坐标
    """
    # 绘制天空渐变
    for y in range(SCREEN_HEIGHT):
        # 从上到下的天空渐变
        r = int(135 + (65 - 135) * (y / SCREEN_HEIGHT))
        g = int(206 + (105 - 206) * (y / SCREEN_HEIGHT))
        b = int(235 + (225 - 235) * (y / SCREEN_HEIGHT))
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # 绘制远山（视差滚动，速度较慢）
    mountain_offset = camera_x * 0.3
    for i in range(5):
        mountain_x = int(i * 400 - mountain_offset) % (SCREEN_WIDTH + 400) - 200
        draw_mountain(screen, mountain_x, SCREEN_HEIGHT - 200, (100, 149, 237))

    # 绘制近山（视差滚动，速度较快）
    mountain_offset = camera_x * 0.6
    for i in range(6):
        mountain_x = int(i * 350 - mountain_offset) % (SCREEN_WIDTH + 350) - 175
        draw_mountain(screen, mountain_x, SCREEN_HEIGHT - 150, (70, 130, 180))

    # 绘制云朵（视差滚动）
    cloud_offset = camera_x * 0.2
    for i in range(4):
        cloud_x = int(i * 500 - cloud_offset) % (SCREEN_WIDTH + 500) - 250
        draw_cloud(screen, cloud_x, 50 + i * 30)


def draw_mountain(screen, x, y, color):
    """
    绘制三角形山

    Args:
        screen: 游戏屏幕
        x, y: 位置坐标
        color: 颜色
    """
    points = [(x, y + 120), (x + 150, y), (x + 300, y + 120)]
    pygame.draw.polygon(screen, color, points)


def draw_cloud(screen, x, y):
    """
    绘制云朵

    Args:
        screen: 游戏屏幕
        x, y: 位置坐标
    """
    cloud_color = WHITE
    pygame.draw.ellipse(screen, cloud_color, (x, y, 80, 40))
    pygame.draw.ellipse(screen, cloud_color, (x + 30, y - 20, 60, 50))
    pygame.draw.ellipse(screen, cloud_color, (x + 60, y, 70, 45))
    pygame.draw.ellipse(screen, cloud_color, (x + 20, y + 10, 80, 40))


def draw_text(screen, text, x, y, size=36, color=BLACK, font_type=None):
    """
    绘制文本

    Args:
        screen: 游戏屏幕
        text: 文本内容
        x, y: 位置坐标
        size: 字体大小
        color: 字体颜色
        font_type: 字体类型（None时使用系统中文字体）
    """
    if font_type is None:
        # 使用系统中文字体（按优先级排序）
        chinese_fonts = ['stheitimedium', 'stheitilight', 'songti', 'arialunicode', 'Arial Unicode MS']
        font = None
        for font_name in chinese_fonts:
            try:
                font = pygame.font.SysFont(font_name, size)
                # 测试字体是否能正确渲染
                test_surface = font.render('测试', True, color)
                if test_surface.get_width() > 0:
                    break
            except:
                continue
        if font is None:
            font = pygame.font.SysFont('arial', size)
    else:
        font = pygame.font.Font(font_type, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def check_collision(rect1, rect2):
    """
    检测两个矩形是否碰撞

    Args:
        rect1: 矩形1 (pygame.Rect)
        rect2: 矩形2 (pygame.Rect)

    Returns:
        bool: 是否碰撞
    """
    return rect1.colliderect(rect2)


def clamp(value, min_value, max_value):
    """
    将值限制在范围内

    Args:
        value: 输入值
        min_value: 最小值
        max_value: 最大值

    Returns:
        限制后的值
    """
    return max(min_value, min(value, max_value))