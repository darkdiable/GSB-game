# 球员模块
# 定义球员类，负责射门操作

import random
from typing import Tuple


class Player:
    """
    球员类，代表一名参与点球的球员
    """

    # 射门方向选项
    DIRECTIONS = ['左上', '右上', '左下', '右下', '正左', '正右', '正中']

    def __init__(self, name: str, is_ai: bool = False):
        """
        初始化球员

        Args:
            name: 球员名称
            is_ai: 是否为AI控制的球员（电脑玩家）
        """
        self.name = name
        self.is_ai = is_ai
        self.shoot_direction = None  # 射门方向
        self.shoot_power = 0  # 射门力度 (1-10)

    def choose_shoot(self) -> Tuple[str, int]:
        """
        选择射门方向和力度

        Returns:
            Tuple[str, int]: (射门方向, 射门力度)
        """
        if self.is_ai:
            return self._ai_choose_shoot()
        else:
            return self._human_choose_shoot()

    def _ai_choose_shoot(self) -> Tuple[str, int]:
        """
        AI球员随机选择射门方向和力度

        Returns:
            Tuple[str, int]: (射门方向, 射门力度)
        """
        direction = random.choice(self.DIRECTIONS)
        power = random.randint(5, 10)  # AI球员力度5-10
        self.shoot_direction = direction
        self.shoot_power = power
        return direction, power

    def _human_choose_shoot(self) -> Tuple[str, int]:
        """
        人类玩家选择射门方向和力度

        Returns:
            Tuple[str, int]: (射门方向, 射门力度)
        """
        print(f"\n=== 球员 {self.name} 准备射门 ===")
        print("请选择射门方向:")
        for idx, direction in enumerate(self.DIRECTIONS, 1):
            print(f"{idx}. {direction}")

        # 选择方向
        while True:
            try:
                choice = int(input("请输入方向编号 (1-7): "))
                if 1 <= choice <= 7:
                    direction = self.DIRECTIONS[choice - 1]
                    break
                else:
                    print("请输入1-7之间的数字！")
            except ValueError:
                print("请输入有效的数字！")

        # 选择力度
        while True:
            try:
                power = int(input("请输入射门力度 (1-10): "))
                if 1 <= power <= 10:
                    break
                else:
                    print("请输入1-10之间的数字！")
            except ValueError:
                print("请输入有效的数字！")

        self.shoot_direction = direction
        self.shoot_power = power
        return direction, power

    def __str__(self) -> str:
        """
        返回球员的字符串表示

        Returns:
            str: 球员信息字符串
        """
        return f"球员 {self.name}"
