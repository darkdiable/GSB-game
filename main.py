# 足球点球游戏 - 根目录入口文件
# 默认启动图形界面版本，加 --cli 参数启动命令行版本

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """
    主函数，启动点球游戏
    """
    # 检查是否使用命令行版本
    use_cli = len(sys.argv) > 1 and sys.argv[1] == '--cli'

    if use_cli:
        # 命令行版本
        from soccerPenalty.game import PenaltyGame

        print("\n" + "="*60)
        print("🎮  足球点球大战 (命令行版)  🎮")
        print("="*60)

        player_name = input("\n请输入你的队伍名称 (默认: 玩家): ").strip()
        if not player_name:
            player_name = "玩家"

        game = PenaltyGame(player_name=player_name)

        while True:
            game.start_game()

            while True:
                choice = input("\n是否再来一局？(y/n): ").strip().lower()
                if choice in ['y', 'yes', '是']:
                    game.reset_game()
                    print("\n" + "="*60)
                    print("🔄  新一局比赛开始！")
                    print("="*60)
                    break
                elif choice in ['n', 'no', '否']:
                    print("\n👋 感谢游玩！再见！\n")
                    return
                else:
                    print("请输入 y 或 n！")
    else:
        # 图形界面版本（默认）
        try:
            import pygame
            from soccerPenalty.game_gui import PenaltyGameGUI

            print("\n" + "="*60)
            print("🎮  足球点球大战 (图形界面版)  🎮")
            print("="*60)
            print("\n正在启动图形界面...")
            print("如需命令行版本，请运行: python3 main.py --cli")

            player_name = input("\n请输入你的队伍名称 (默认: 玩家): ").strip()
            if not player_name:
                player_name = "玩家"

            game = PenaltyGameGUI(player_name=player_name)
            game.start()

        except ImportError as e:
            print(f"\n❌ 无法启动图形界面: {e}")
            print("请确保已安装 pygame: pip3 install pygame")
            print("\n或使用命令行版本: python3 main.py --cli")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ 游戏发生错误: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 游戏已退出。再见！\n")
        sys.exit(0)
