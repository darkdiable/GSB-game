# 裁判模块
# 定义裁判类，负责发出射门指令和判定比赛结果

import time
import random
from typing import List


class Referee:
    """
    裁判类，负责管理比赛流程和发出指令
    """

    def __init__(self, name: str = "主裁判"):
        """
        初始化裁判

        Args:
            name: 裁判名称
        """
        self.name = name
        self.can_shoot = False  # 是否可以射门
        self.current_message = ""  # 当前头顶提示信息

    def show_prompt(self, message: str):
        """
        显示裁判头顶提示信息

        Args:
            message: 提示信息
        """
        self.current_message = message
        # 用ASCII艺术显示裁判和头顶提示
        self._display_referee(message)

    def _display_referee(self, message: str):
        """
        用ASCII艺术显示裁判和头顶提示

        Args:
            message: 提示信息
        """
        # 计算提示框宽度
        msg_width = len(message) + 4
        border = "=" * msg_width

        print("\n" + " " * 10 + border)
        print(" " * 10 + f"| {message} |")
        print(" " * 10 + border)
        print(" " * 12 + "  |  ")
        print(" " * 12 + "  v  ")
        print(" " * 10 + "  O  ")  # 头
        print(" " * 9 + " /|\\ ")  # 身体和手臂
        print(" " * 9 + " / \\ ")  # 腿
        print(f"\n[{self.name}]: 准备就绪！")

    def signal_start(self, delay: bool = True) -> bool:
        """
        发出开始射门信号

        Args:
            delay: 是否添加随机延迟以增加真实感

        Returns:
            bool: True表示可以射门
        """
        # 先显示"准备"
        self.show_prompt("准备")
        if delay:
            # 随机等待1-3秒
            wait_time = random.uniform(1, 3)
            print(f"\n等待中... ({wait_time:.1f}秒)")
            time.sleep(wait_time)

        # 显示"开始"
        self.show_prompt("开始")
        self.can_shoot = True
        print(f"\n[{self.name}]: 可以射门了！")
        return True

    def check_goal_valid(self, shoot_result: bool) -> bool:
        """
        判定进球是否有效

        Args:
            shoot_result: 射门结果（True为进球，False为被扑出）

        Returns:
            bool: True表示进球有效
        """
        if shoot_result:
            print(f"\n[{self.name}]: 进球有效！")
        else:
            print(f"\n[{self.name}]: 扑救成功！")
        return shoot_result

    def announce_round_result(self, player_name: str, scored: bool):
        """
        宣布本轮结果

        Args:
            player_name: 射门球员名称
            scored: 是否进球
        """
        result = "进球" if scored else "未进"
        print(f"\n{'='*40}")
        print(f"[{self.name}]: 球员 {player_name} {result}！")
        print(f"{'='*40}\n")

    def announce_final_result(
        self,
        team1_name: str,
        team1_score: int,
        team2_name: str,
        team2_score: int,
    ):
        """
        宣布最终比赛结果

        Args:
            team1_name: 队伍1名称
            team1_score: 队伍1得分
            team2_name: 队伍2名称
            team2_score: 队伍2得分
        """
        print("\n" + "="*50)
        print(f"[{self.name}]: 比赛结束！")
        print(f"{'='*50}")
        print(f"\n最终比分:")
        print(f"  {team1_name}: {team1_score} 球")
        print(f"  {team2_name}: {team2_score} 球")
        print()

        if team1_score > team2_score:
            print(f"🏆 {team1_name} 获胜！🏆")
        elif team2_score > team1_score:
            print(f"🏆 {team2_name} 获胜！🏆")
        else:
            print("🤝 平局！🤝")

        print("\n" + "="*50)

    def reset(self):
        """
        重置裁判状态
        """
        self.can_shoot = False
        self.current_message = ""

    def __str__(self) -> str:
        """
        返回裁判的字符串表示

        Returns:
            str: 裁判信息字符串
        """
        return f"裁判 {self.name}"
