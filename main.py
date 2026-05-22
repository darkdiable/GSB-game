# 足球点球游戏 - 根目录入口文件
# 运行此文件开始游戏

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from soccerPenalty.game import PenaltyGame


def main():
    """
    主函数，启动点球游戏
    """
    print("\n" + "="*60)
    print("🎮  足球点球大战  🎮")
    print("="*60)

    # 获取玩家名称
    player_name = input("\n请输入你的队伍名称 (默认: 玩家): ").strip()
    if not player_name:
        player_name = "玩家"

    # 创建游戏实例
    game = PenaltyGame(player_name=player_name)

    # 游戏主循环，支持多局
    while True:
        # 开始一局游戏
        game.start_game()

        # 询问是否再来一局
        while True:
            choice = input("\n是否再来一局？(y/n): ").strip().lower()
            if choice in ['y', 'yes', '是']:
                # 重置游戏状态
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 游戏已退出。再见！\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 游戏发生错误: {e}")
        sys.exit(1)
