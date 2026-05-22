# 测试 GUI 模块能否正常导入和初始化
# 此测试不会实际打开窗口，仅验证模块导入和初始化

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_gui_imports():
    """测试 GUI 模块导入"""
    print("="*60)
    print("🧪 测试 GUI 模块导入...")
    print("="*60)

    try:
        import pygame
        print(f"✅ Pygame 导入成功，版本: {pygame.__version__}")
    except ImportError as e:
        print(f"❌ Pygame 导入失败: {e}")
        return False

    try:
        from soccerPenalty.gui import SoccerGUI, GameState, Colors
        print("✅ SoccerGUI, GameState, Colors 导入成功")
    except ImportError as e:
        print(f"❌ gui 模块导入失败: {e}")
        return False

    try:
        from soccerPenalty.game_gui import PenaltyGameGUI
        print("✅ PenaltyGameGUI 导入成功")
    except ImportError as e:
        print(f"❌ game_gui 模块导入失败: {e}")
        return False

    try:
        # 测试 Colors
        assert hasattr(Colors, 'GREEN')
        assert hasattr(Colors, 'WHITE')
        assert hasattr(Colors, 'RED')
        print("✅ Colors 常量验证通过")
    except Exception as e:
        print(f"❌ Colors 验证失败: {e}")
        return False

    try:
        # 测试 GameState
        assert hasattr(GameState, 'MENU')
        assert hasattr(GameState, 'CHOOSE_SHOOT')
        assert hasattr(GameState, 'ANIMATING')
        print("✅ GameState 常量验证通过")
    except Exception as e:
        print(f"❌ GameState 验证失败: {e}")
        return False

    try:
        # 测试 SoccerGUI 类属性
        assert hasattr(SoccerGUI, 'WIDTH')
        assert hasattr(SoccerGUI, 'HEIGHT')
        assert hasattr(SoccerGUI, 'DIRECTION_ZONES')
        assert len(SoccerGUI.DIRECTION_ZONES) == 7
        print(f"✅ SoccerGUI 属性验证通过")
        print(f"   - 窗口尺寸: {SoccerGUI.WIDTH} x {SoccerGUI.HEIGHT}")
        print(f"   - 方向区域数: {len(SoccerGUI.DIRECTION_ZONES)}")
        print(f"   - 方向列表: {list(SoccerGUI.DIRECTION_ZONES.keys())}")
    except Exception as e:
        print(f"❌ SoccerGUI 属性验证失败: {e}")
        return False

    try:
        # 测试 PenaltyGameGUI 类属性
        assert PenaltyGameGUI.PLAYERS_PER_TEAM == 5
        print("✅ PenaltyGameGUI 属性验证通过")
        print(f"   - 每队球员数: {PenaltyGameGUI.PLAYERS_PER_TEAM}")
    except Exception as e:
        print(f"❌ PenaltyGameGUI 属性验证失败: {e}")
        return False

    print("\n🎉 所有 GUI 模块测试通过！")
    return True


def show_startup_guide():
    """显示启动指南"""
    print("\n" + "="*60)
    print("🚀 图形界面版本启动方式")
    print("="*60)
    print("\n方式1 - 使用专用启动脚本 (推荐):")
    print("  python3 run_gui.py")
    print("\n方式2 - 使用主入口 (默认启动GUI):")
    print("  python3 main.py")
    print("\n方式3 - 命令行版本 (如需):")
    print("  python3 main.py --cli")
    print("\n" + "="*60)
    print("📖 操作说明")
    print("="*60)
    print("  • 鼠标点击球门区域选择射门/扑救方向")
    print("  • 球门被划分为7个区域:")
    print("    左上 | 正上 | 右上")
    print("    正左 | 正中 | 正右")
    print("    左下 | 正下 | 右下")
    print("  • 按 ↑↓ 键调整射门力度 (1-10)")
    print("  • 力度越大，守门员越难扑救")
    print("  • 按 空格键 或 回车键 继续")
    print("  • 按 ESC 键 关闭游戏窗口")
    print("\n" + "="*60)
    print("🎮 游戏规则")
    print("="*60)
    print("  • 每队各有5名球员轮流射门")
    print("  • 每队各有一名守门员轮流守门")
    print("  • 裁判头顶显示'准备'→等待→'开始'")
    print("  • 裁判显示'开始'后才能选择方向")
    print("  • 5轮结束后，进球多的队伍获胜")
    print("\n" + "="*60)


if __name__ == "__main__":
    success = test_gui_imports()
    if success:
        show_startup_guide()
        print("\n✅ GUI 模块准备就绪，可以启动游戏了！\n")
    else:
        print("\n❌ GUI 模块测试失败，请检查上述错误信息\n")
        sys.exit(1)
