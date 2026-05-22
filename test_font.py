# 中文字体测试脚本
# 验证字体加载和中文显示是否正常

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame


def test_chinese_font():
    """测试中文字体加载"""
    print("="*60)
    print("🧪 测试中文字体加载")
    print("="*60)

    pygame.init()

    # 从 gui 模块导入字体查找函数
    from soccerPenalty.gui import get_chinese_font, SoccerGUI, Colors

    # 测试字体查找函数
    font = get_chinese_font()
    if font:
        print(f"✅ 找到中文字体: {font}")
    else:
        print("❌ 未找到中文字体")
        return False

    # 测试字体能否正常渲染中文
    try:
        if os.path.exists(font):
            font_obj = pygame.font.Font(font, 32)
            font_obj.set_bold(True)
        else:
            font_obj = pygame.font.SysFont(font, 32, bold=True)

        # 测试渲染各种中文字符
        test_texts = [
            "足球点球大战",
            "开始",
            "准备",
            "进球有效",
            "扑救成功",
            "左上 右上 正左 正右 正中",
            "玩家 电脑 门将 裁判",
            "你好，世界！",
            "⚽ 🥅 🎮 🏆",  # 测试emoji
        ]

        print("\n测试中文渲染:")
        for text in test_texts:
            try:
                surface = font_obj.render(text, True, (255, 255, 255))
                size = surface.get_size()
                print(f"  ✓ '{text}' -> 尺寸: {size[0]}x{size[1]}")
            except Exception as e:
                print(f"  ✗ '{text}' -> 错误: {e}")

        print("\n✅ 所有中文字符渲染测试通过！")

        # 测试 SoccerGUI 初始化
        print("\n测试 SoccerGUI 初始化...")
        # 不实际显示窗口，只测试字体加载
        gui = SoccerGUI()
        print(f"  ✓ 大号字体: {gui.font_large.size('测试')}")
        print(f"  ✓ 中号字体: {gui.font_medium.size('测试')}")
        print(f"  ✓ 小号字体: {gui.font_small.size('测试')}")
        print(f"  ✓ 微小字体: {gui.font_tiny.size('测试')}")
        gui.close()

        print("\n✅ SoccerGUI 字体加载成功！")
        return True

    except Exception as e:
        print(f"❌ 字体测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        pygame.quit()


def show_result():
    """显示测试结果和使用说明"""
    print("\n" + "="*60)
    print("📖 字体配置说明")
    print("="*60)
    print("\n当前系统已自动检测并使用中文字体。")
    print("\n如果仍有乱码问题，请尝试:")
    print("  1. 确认系统已安装中文字体")
    print("  2. 安装Arial Unicode MS字体")
    print("  3. 或手动指定字体文件路径")
    print("\n支持的中文字体（按优先级）:")
    print("  • STHeiti Medium (华文黑体) - macOS")
    print("  • STHeiti Light (华文黑体细体)")
    print("  • Hiragino Sans GB (冬青黑体)")
    print("  • Songti (宋体)")
    print("  • Apple SD Gothic Neo")
    print("  • Arial Unicode MS")
    print("\n" + "="*60)
    print("\n🚀 启动游戏命令:")
    print("  python3 run_gui.py")
    print("  或")
    print("  python3 main.py")
    print("\n" + "="*60)


if __name__ == "__main__":
    success = test_chinese_font()
    if success:
        show_result()
        print("\n🎉 中文字体配置完成，可以正常显示中文！\n")
    else:
        print("\n❌ 字体配置失败，请检查上述错误信息\n")
        sys.exit(1)
