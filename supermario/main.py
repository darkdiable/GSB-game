# -*- coding: utf-8 -*-
"""
超级玛丽游戏 - 主入口文件
运行此文件以启动游戏

操作说明：
    - 方向键 ← → 或 A D : 左右移动
    - 空格键 或 ↑ 或 W : 跳跃
    - 踩敌人头顶可消灭敌人
    - 顶问号方块获得金币
    - ESC : 返回菜单
"""

from game import Game


def main():
    """主函数 - 启动游戏"""
    # 创建游戏实例
    game = Game()

    # 运行游戏
    game.run()


if __name__ == "__main__":
    main()