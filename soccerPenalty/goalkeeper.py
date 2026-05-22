# 守门员模块
# 定义守门员类，负责守门操作

import random
from typing import Tuple


class Goalkeeper:
    """
    守门员类，代表一名守门员
    """

    # 扑救方向选项
    SAVE_DIRECTIONS = ['左上', '右上', '左下', '右下', '正左', '正右', '正中']

    def __init__(self, name: str, is_ai: bool = True):
        """
        初始化守门员

        Args:
            name: 守门员名称
            is_ai: 是否为AI控制的守门员
        """
        self.name = name
        self.is_ai = is_ai
        self.save_direction = None  # 扑救方向
        self.save_count = 0  # 成功扑救次数

    def choose_save(self) -> str:
        """
        选择扑救方向

        Returns:
            str: 扑救方向
        """
        if self.is_ai:
            return self._ai_choose_save()
        else:
            return self._human_choose_save()

    def _ai_choose_save(self) -> str:
        """
        AI守门员随机选择扑救方向

        Returns:
            str: 扑救方向
        """
        direction = random.choice(self.SAVE_DIRECTIONS)
        self.save_direction = direction
        return direction

    def _human_choose_save(self) -> str:
        """
        人类守门员选择扑救方向

        Returns:
            str: 扑救方向
        """
        print(f"\n=== 守门员 {self.name} 准备防守 ===")
        print("请选择扑救方向:")
        for idx, direction in enumerate(self.SAVE_DIRECTIONS, 1):
            print(f"{idx}. {direction}")

        while True:
            try:
                choice = int(input("请输入方向编号 (1-7): "))
                if 1 <= choice <= 7:
                    direction = self.SAVE_DIRECTIONS[choice - 1]
                    self.save_direction = direction
                    return direction
                else:
                    print("请输入1-7之间的数字！")
            except ValueError:
                print("请输入有效的数字！")

    def check_save(self, shoot_direction: str, shoot_power: int) -> bool:
        """
        判断是否扑救成功

        Args:
            shoot_direction: 射门方向
            shoot_power: 射门力度

        Returns:
            bool: True表示扑救成功，False表示失败
        """
        # 方向完全一致时扑救成功
        if self.save_direction == shoot_direction:
            # 力度越大，扑救难度越高
            if shoot_power >= 8:
                # 高力度射门，有30%概率扑救失败（即使方向正确）
                success = random.random() > 0.3
            elif shoot_power >= 5:
                # 中等力度，10%概率扑救失败
                success = random.random() > 0.1
            else:
                # 低力度，必然扑救成功
                success = True

            if success:
                self.save_count += 1
            return success

        # 方向不一致，扑救失败
        return False

    def reset_stats(self):
        """
        重置守门员统计数据
        """
        self.save_count = 0
        self.save_direction = None

    def __str__(self) -> str:
        """
        返回守门员的字符串表示

        Returns:
            str: 守门员信息字符串
        """
        return f"守门员 {self.name} (扑救成功: {self.save_count}次)"
