# 足球点球大战 - 图形界面启动脚本
# 直接运行此文件启动图形界面版本游戏

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """
    启动图形界面版本的点球游戏
    """
    try:
        # 检查 pygame 是否安装
        import pygame
        print("✅ Pygame 版本:", pygame.__version__)
    except ImportError:
        print("\n❌ 错误: 未检测到 Pygame 库")
        print("\n请先安装 Pygame:")
        print("  pip3 install pygame")
        print("\n或者使用命令行版本:")
        print("  python3 main.py --cli")
        sys.exit(1)

    try:
        from soccerPenalty.game_gui import PenaltyGameGUI

        print("\n" + "="*60)
        print("⚽  足球点球大战 - 图形界面版  ⚽")
        print("="*60)
        print("\n正在启动游戏窗口...")
        print("\n操作说明:")
        print("  • 鼠标点击球门区域选择射门/扑救方向")
        print("  • 按 ↑↓ 键调整射门力度 (1-10)")
        print("  • 按 空格键 或 回车键 继续")
        print("  • 按 ESC 键 关闭窗口")
        print("\n" + "="*60)

        # 输入队伍名称
        player_name = input("\n请输入你的队伍名称 (默认: 玩家): ").strip()
        if not player_name:
            player_name = "玩家"

        print(f"\n你好, {player_name}! 游戏即将开始...\n")

        # 创建并启动游戏
        game = PenaltyGameGUI(player_name=player_name)
        game.start()

    except ImportError as e:
        print(f"\n❌ 导入模块失败: {e}")
        print("请确保文件结构完整")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 游戏已退出。再见！\n")
        sys.exit(0)
