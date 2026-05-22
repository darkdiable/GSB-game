# 游戏主逻辑模块
# 定义点球游戏的核心流程控制

from typing import List, Tuple
import time

from .player import Player
from .goalkeeper import Goalkeeper
from .referee import Referee


class PenaltyGame:
    """
    点球游戏主类，控制整个游戏流程
    """

    # 每队球员数量
    PLAYERS_PER_TEAM = 5

    def __init__(self, player_name: str = "玩家"):
        """
        初始化点球游戏

        Args:
            player_name: 玩家队伍名称
        """
        self.player_name = player_name
        self.computer_name = "电脑"

        # 初始化裁判
        self.referee = Referee()

        # 初始化球员列表（每队5人）
        self.player_players: List[Player] = self._create_players(
            player_name, is_ai=False
        )
        self.computer_players: List[Player] = self._create_players(
            self.computer_name, is_ai=True
        )

        # 初始化守门员
        self.player_goalkeeper = Goalkeeper(
            f"{player_name}门将", is_ai=False
        )
        self.computer_goalkeeper = Goalkeeper(
            f"{self.computer_name}门将", is_ai=True
        )

        # 比分记录
        self.player_score = 0
        self.computer_score = 0

        # 当前轮次
        self.current_round = 0

        # 游戏是否结束
        self.game_over = False

    def _create_players(self, team_name: str, is_ai: bool) -> List[Player]:
        """
        创建一支球队的5名球员

        Args:
            team_name: 队伍名称
            is_ai: 是否为AI控制

        Returns:
            List[Player]: 球员列表
        """
        players = []
        for i in range(1, self.PLAYERS_PER_TEAM + 1):
            player = Player(f"{team_name}{i}号", is_ai=is_ai)
            players.append(player)
        return players

    def start_game(self):
        """
        开始游戏
        """
        self._show_welcome()
        self._play_all_rounds()
        self._end_game()

    def _show_welcome(self):
        """
        显示欢迎信息
        """
        print("\n" + "="*60)
        print("⚽  欢迎来到足球点球大战！ ⚽")
        print("="*60)
        print(f"\n对阵双方:")
        print(f"  {self.player_name} (你) VS {self.computer_name}")
        print(f"\n比赛规则:")
        print(f"  - 每队各有 {self.PLAYERS_PER_TEAM} 名球员轮流射门")
        print(f"  - 每队各有一名守门员轮流守门")
        print(f"  - 裁判发令后才能射门")
        print(f"  - 进球多的队伍获胜")
        print("\n" + "="*60 + "\n")

        input("按回车键开始比赛...")

    def _play_all_rounds(self):
        """
        进行所有轮次的比赛
        """
        for round_num in range(1, self.PLAYERS_PER_TEAM + 1):
            self.current_round = round_num
            self._play_single_round(round_num)

            # 每轮之间暂停
            if round_num < self.PLAYERS_PER_TEAM:
                time.sleep(1)

    def _play_single_round(self, round_num: int):
        """
        进行单轮比赛（玩家射门 + 电脑射门）

        Args:
            round_num: 轮次编号
        """
        print(f"\n{'#'*60}")
        print(f"# 第 {round_num} 轮比赛")
        print(f"{'#'*60}")

        # 获取当前轮的球员
        player_shooter = self.player_players[round_num - 1]
        computer_shooter = self.computer_players[round_num - 1]

        # 第一部分：玩家射门，电脑守门
        print(f"\n--- 上半场：{self.player_name} 射门 ---")
        self._execute_shot(
            shooter=player_shooter,
            goalkeeper=self.computer_goalkeeper,
            is_player_team=True,
        )

        # 显示当前比分
        self._show_score()

        time.sleep(1)

        # 第二部分：电脑射门，玩家守门
        print(f"\n--- 下半场：{self.computer_name} 射门 ---")
        self._execute_shot(
            shooter=computer_shooter,
            goalkeeper=self.player_goalkeeper,
            is_player_team=False,
        )

        # 显示当前比分
        self._show_score()

    def _execute_shot(
        self,
        shooter: Player,
        goalkeeper: Goalkeeper,
        is_player_team: bool,
    ):
        """
        执行一次射门

        Args:
            shooter: 射门球员
            goalkeeper: 守门员
            is_player_team: 是否是玩家队伍射门
        """
        # 重置上一轮的方向选择
        shooter.shoot_direction = None
        shooter.shoot_power = 0
        goalkeeper.save_direction = None

        print(f"\n射门球员: {shooter.name}")
        print(f"守门员: {goalkeeper.name}")

        # 裁判发令
        self.referee.signal_start(delay=True)

        # 守门员先选择扑救方向（如果是人类守门员）
        save_direction = goalkeeper.choose_save()
        print(f"\n守门员选择了: {save_direction}")

        # 球员选择射门方向和力度
        shoot_direction, shoot_power = shooter.choose_shoot()
        print(f"\n球员射向: {shoot_direction}, 力度: {shoot_power}")

        # 判定结果
        save_successful = goalkeeper.check_save(shoot_direction, shoot_power)
        goal_scored = not save_successful

        # 裁判判定
        self.referee.check_goal_valid(goal_scored)

        # 更新比分
        if goal_scored:
            if is_player_team:
                self.player_score += 1
            else:
                self.computer_score += 1

        # 宣布本轮结果
        self.referee.announce_round_result(shooter.name, goal_scored)

        # 重置裁判状态
        self.referee.reset()

    def _show_score(self):
        """
        显示当前比分
        """
        print(f"\n当前比分:")
        print(f"  {self.player_name}: {self.player_score} 球")
        print(f"  {self.computer_name}: {self.computer_score} 球")
        print(f"  已完成: {self.current_round}/{self.PLAYERS_PER_TEAM} 轮")

    def _end_game(self):
        """
        结束游戏，显示最终结果
        """
        self.game_over = True

        # 裁判宣布最终结果
        self.referee.announce_final_result(
            team1_name=self.player_name,
            team1_score=self.player_score,
            team2_name=self.computer_name,
            team2_score=self.computer_score,
        )

        # 显示守门员统计
        print("\n守门员表现:")
        print(f"  {self.player_goalkeeper}")
        print(f"  {self.computer_goalkeeper}")
        print()

    def reset_game(self):
        """
        重置游戏状态，准备新一局
        """
        self.player_score = 0
        self.computer_score = 0
        self.current_round = 0
        self.game_over = False

        self.player_goalkeeper.reset_stats()
        self.computer_goalkeeper.reset_stats()

        self.referee.reset()

        for player in self.player_players + self.computer_players:
            player.shoot_direction = None
            player.shoot_power = 0

    def __str__(self) -> str:
        """
        返回游戏状态的字符串表示

        Returns:
            str: 游戏状态信息
        """
        return (
            f"点球游戏 - {self.player_name} VS {self.computer_name}\n"
            f"比分: {self.player_score} - {self.computer_score}\n"
            f"当前轮次: {self.current_round}/{self.PLAYERS_PER_TEAM}"
        )
