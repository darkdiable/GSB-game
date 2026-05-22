# 测试脚本 - 验证游戏模块功能
# 无需用户交互，自动测试核心逻辑

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from soccerPenalty.player import Player
from soccerPenalty.goalkeeper import Goalkeeper
from soccerPenalty.referee import Referee
from soccerPenalty.game import PenaltyGame


def test_player():
    """测试球员模块"""
    print("="*50)
    print("🧪 测试球员模块...")
    print("="*50)

    # 测试AI球员
    ai_player = Player("AI测试员", is_ai=True)
    direction, power = ai_player.choose_shoot()
    print(f"AI球员选择: 方向={direction}, 力度={power}")
    assert direction in Player.DIRECTIONS
    assert 5 <= power <= 10
    print("✓ AI球员测试通过")

    # 测试人类球员
    human_player = Player("人类测试员", is_ai=False)
    print(f"✓ 人类球员创建成功: {human_player}")
    print("✓ 球员模块测试通过\n")


def test_goalkeeper():
    """测试守门员模块"""
    print("="*50)
    print("🧪 测试守门员模块...")
    print("="*50)

    gk = Goalkeeper("测试门将", is_ai=True)

    # 测试方向选择
    direction = gk.choose_save()
    print(f"守门员选择方向: {direction}")
    assert direction in Goalkeeper.SAVE_DIRECTIONS

    # 测试扑救判定（相同方向，低力度）
    gk.save_direction = "正中"
    result = gk.check_save("正中", 3)
    print(f"相同方向低力度扑救: {'成功' if result else '失败'}")
    assert result == True

    # 测试扑救判定（不同方向）
    gk.save_direction = "左上"
    result = gk.check_save("右下", 5)
    print(f"不同方向扑救: {'成功' if result else '失败'}")
    assert result == False

    # 测试扑救统计
    print(f"✓ 成功扑救次数: {gk.save_count}")
    print("✓ 守门员模块测试通过\n")


def test_referee():
    """测试裁判模块"""
    print("="*50)
    print("🧪 测试裁判模块...")
    print("="*50)

    ref = Referee("测试裁判")

    # 测试提示显示（无延迟）
    print("测试裁判发令...")
    ref.signal_start(delay=False)
    assert ref.can_shoot == True
    assert ref.current_message == "开始"

    # 测试进球判定
    print("\n测试进球判定:")
    result = ref.check_goal_valid(True)
    assert result == True
    result = ref.check_goal_valid(False)
    assert result == False

    # 测试结果宣布
    ref.announce_round_result("测试球员", True)
    ref.announce_final_result("红队", 3, "蓝队", 2)

    # 测试重置
    ref.reset()
    assert ref.can_shoot == False
    assert ref.current_message == ""

    print("✓ 裁判模块测试通过\n")


def test_game():
    """测试游戏主逻辑模块"""
    print("="*50)
    print("🧪 测试游戏主逻辑模块...")
    print("="*50)

    game = PenaltyGame("测试队")

    # 检查初始化
    assert game.player_score == 0
    assert game.computer_score == 0
    assert game.current_round == 0
    assert len(game.player_players) == 5
    assert len(game.computer_players) == 5
    assert not game.game_over

    print(f"✓ 游戏初始化成功: {game}")
    print(f"✓ 玩家球员: {[p.name for p in game.player_players]}")
    print(f"✓ 电脑球员: {[p.name for p in game.computer_players]}")
    print(f"✓ 玩家门将: {game.player_goalkeeper.name}")
    print(f"✓ 电脑门将: {game.computer_goalkeeper.name}")

    # 测试重置
    game.player_score = 3
    game.computer_score = 2
    game.current_round = 3
    game.reset_game()
    assert game.player_score == 0
    assert game.computer_score == 0
    assert game.current_round == 0
    assert not game.game_over
    print("✓ 游戏重置功能正常")

    print("✓ 游戏主逻辑模块测试通过\n")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🚀 开始运行模块测试")
    print("="*60 + "\n")

    try:
        test_player()
        test_goalkeeper()
        test_referee()
        test_game()

        print("="*60)
        print("🎉 所有测试通过！游戏模块功能正常！")
        print("="*60 + "\n")
        return True
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
