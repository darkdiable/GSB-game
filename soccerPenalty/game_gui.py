# 图形界面版本游戏主逻辑
# 集成 Pygame 界面与点球游戏逻辑

import time
import random
from typing import Optional

from .player import Player
from .goalkeeper import Goalkeeper
from .referee import Referee
from .gui import SoccerGUI, GameState, Colors


class PenaltyGameGUI:
    """
    图形界面版本的点球游戏主类
    """

    PLAYERS_PER_TEAM = 5

    def __init__(self, player_name: str = "玩家"):
        """
        初始化图形界面游戏

        Args:
            player_name: 玩家队伍名称
        """
        self.player_name = player_name
        self.computer_name = "电脑"

        # 初始化 GUI
        self.gui = SoccerGUI()

        # 初始化裁判
        self.referee = Referee()

        # 初始化球员
        self.player_players = self._create_players(player_name, is_ai=False)
        self.computer_players = self._create_players(self.computer_name, is_ai=True)

        # 初始化守门员
        self.player_goalkeeper = Goalkeeper(
            f"{player_name}门将", is_ai=False
        )
        self.computer_goalkeeper = Goalkeeper(
            f"{self.computer_name}门将", is_ai=True
        )

        # 游戏状态
        self.player_score = 0
        self.computer_score = 0
        self.current_round = 0
        self.game_over = False

        # 当前回合状态
        self.current_phase = "player_shoot"  # player_shoot 或 computer_shoot
        self.shoot_direction = None
        self.shoot_power = None
        self.save_direction = None
        self.shooter = None
        self.goalkeeper = None
        self.is_player_team = None

        # 裁判计时
        self.referee_timer = 0
        self.referee_delay = 0

    def _create_players(self, team_name: str, is_ai: bool) -> list:
        """创建球队球员"""
        players = []
        for i in range(1, self.PLAYERS_PER_TEAM + 1):
            players.append(Player(f"{team_name}{i}号", is_ai=is_ai))
        return players

    def start(self):
        """启动游戏主循环"""
        running = True
        self.gui.state = GameState.MENU

        while running:
            # 处理事件
            running, direction, power_delta = self.gui.handle_events()
            if not running:
                break

            # 处理力度调整
            if power_delta != 0 and self.gui.state == GameState.CHOOSE_SHOOT:
                new_power = self.gui.selected_power + power_delta
                if 1 <= new_power <= 10:
                    self.gui.selected_power = new_power

            # 状态机处理
            self._update_state(direction)

            # 更新动画
            if self.gui.state == GameState.ANIMATING:
                self.gui.update_animation()

            # 渲染
            self._render()

        self.gui.close()

    def _update_state(self, direction: Optional[str]):
        """
        更新游戏状态

        Args:
            direction: 用户输入的方向或特殊按键
        """
        state = self.gui.state

        if state == GameState.MENU:
            if direction in ["SPACE", "CLICK", "ENTER"]:
                self._start_new_game()

        elif state == GameState.WAITING:
            # 等待裁判发令
            pass

        elif state == GameState.REFEREE_READY:
            # 裁判显示"准备"，等待随机时间后显示"开始"
            self.referee_timer += 1
            if self.referee_timer >= self.referee_delay:
                self.gui.state = GameState.REFEREE_START
                self.referee_timer = 0
                # 短暂显示"开始"后进入选择阶段
                self.referee_delay = 60  # 约1秒

        elif state == GameState.REFEREE_START:
            self.referee_timer += 1
            if self.referee_timer >= self.referee_delay:
                # 进入选择阶段
                if self.current_phase == "player_shoot":
                    # 玩家射门：先让电脑守门员选择方向（不显示）
                    self.save_direction = self.computer_goalkeeper._ai_choose_save()
                    self.gui.state = GameState.CHOOSE_SHOOT
                else:
                    # 电脑射门：玩家选择扑救方向
                    self.gui.state = GameState.CHOOSE_SAVE

        elif state == GameState.CHOOSE_SHOOT:
            # 玩家选择射门方向
            if direction and direction in Player.DIRECTIONS:
                self.shoot_direction = direction
                self.shoot_power = self.gui.selected_power
                self._execute_shot()

        elif state == GameState.CHOOSE_SAVE:
            # 玩家选择扑救方向
            if direction and direction in Goalkeeper.SAVE_DIRECTIONS:
                self.save_direction = direction
                # 电脑自动选择射门方向
                self.shoot_direction, self.shoot_power = self.shooter.choose_shoot()
                self._execute_shot()

        elif state == GameState.ANIMATING:
            # 动画播放中，由 update_animation 处理
            pass

        elif state == GameState.ROUND_RESULT:
            # 显示本轮结果，等待按键继续
            if direction in ["SPACE", "CLICK", "ENTER"]:
                self._next_phase()

        elif state == GameState.GAME_OVER:
            # 游戏结束，等待按键
            if direction in ["SPACE", "CLICK", "ENTER"]:
                # 询问是否再来一局（简化处理：直接返回菜单）
                self.gui.state = GameState.MENU
                self._reset_game()

    def _start_new_game(self):
        """开始新游戏"""
        self._reset_game()
        self.gui.state = GameState.WAITING
        self._start_round(1)

    def _reset_game(self):
        """重置游戏状态"""
        self.player_score = 0
        self.computer_score = 0
        self.current_round = 0
        self.game_over = False
        self.player_goalkeeper.reset_stats()
        self.computer_goalkeeper.reset_stats()
        self.referee.reset()
        self.gui.reset_positions()
        self.gui.selected_power = 5

    def _start_round(self, round_num: int):
        """
        开始新一轮

        Args:
            round_num: 轮次编号
        """
        self.current_round = round_num
        self.current_phase = "player_shoot"
        self.shooter = self.player_players[round_num - 1]
        self.goalkeeper = self.computer_goalkeeper
        self.is_player_team = True
        self.shoot_direction = None
        self.shoot_power = None
        self.save_direction = None

        # 重置位置
        self.gui.reset_positions()

        # 裁判发令
        self._referee_signal()

    def _referee_signal(self):
        """裁判发令流程"""
        self.referee_timer = 0
        # 随机等待 1-3 秒 (60fps)
        self.referee_delay = random.randint(60, 180)
        self.gui.state = GameState.REFEREE_READY

    def _execute_shot(self):
        """执行射门"""
        # 设置球员选择
        self.shooter.shoot_direction = self.shoot_direction
        self.shooter.shoot_power = self.shoot_power
        self.goalkeeper.save_direction = self.save_direction

        # 开始动画，完成后回调
        def on_animation_complete():
            self._check_shot_result()

        self.gui.start_animation(
            shoot_direction=self.shoot_direction,
            save_direction=self.save_direction,
            callback=on_animation_complete
        )

    def _check_shot_result(self):
        """检查射门结果"""
        # 判断扑救是否成功
        save_successful = self.goalkeeper.check_save(
            self.shoot_direction,
            self.shoot_power
        )
        goal_scored = not save_successful

        # 更新比分
        if goal_scored:
            if self.is_player_team:
                self.player_score += 1
            else:
                self.computer_score += 1

        # 保存结果供显示
        self.last_goal_scored = goal_scored
        self.last_shooter_name = self.shooter.name

        self.gui.state = GameState.ROUND_RESULT

    def _next_phase(self):
        """进入下一阶段"""
        if self.current_phase == "player_shoot":
            # 切换到电脑射门
            self.current_phase = "computer_shoot"
            self.shooter = self.computer_players[self.current_round - 1]
            self.goalkeeper = self.player_goalkeeper
            self.is_player_team = False
            self.shoot_direction = None
            self.shoot_power = None
            self.save_direction = None

            # 重置位置
            self.gui.reset_positions()

            # 裁判发令
            self._referee_signal()
        else:
            # 本轮结束，检查是否还有下一轮
            if self.current_round >= self.PLAYERS_PER_TEAM:
                # 游戏结束
                self.game_over = True
                self.gui.state = GameState.GAME_OVER
            else:
                # 下一轮
                self._start_round(self.current_round + 1)

    def _render(self):
        """渲染当前游戏状态"""
        self.gui.clear()

        state = self.gui.state

        if state == GameState.MENU:
            self.gui.draw_menu()

        else:
            # 绘制场景
            self.gui.draw_field()
            self.gui.draw_goal()

            # 绘制计分板
            self.gui.draw_scoreboard(
                self.player_score,
                self.computer_score,
                self.current_round,
                self.PLAYERS_PER_TEAM
            )

            # 绘制裁判
            ref_message = ""
            if state == GameState.REFEREE_READY:
                ref_message = "准备"
            elif state == GameState.REFEREE_START:
                ref_message = "开始"
            self.gui.draw_referee(750, 450, ref_message)

            # 绘制球员
            if self.current_phase == "player_shoot":
                # 玩家射门，电脑守门
                self.gui.draw_player(350, 500, Colors.RED, self.shooter.name)
                self.gui.draw_goalkeeper(
                    self.gui.gk_pos[0],
                    self.gui.gk_pos[1],
                    is_player=False
                )
            else:
                # 电脑射门，玩家守门
                self.gui.draw_player(550, 500, Colors.BLUE, self.shooter.name)
                self.gui.draw_goalkeeper(
                    self.gui.gk_pos[0],
                    self.gui.gk_pos[1],
                    is_player=True
                )

            # 绘制足球
            self.gui.draw_ball(
                int(self.gui.ball_pos[0]),
                int(self.gui.ball_pos[1])
            )

            # 状态特定的绘制
            if state == GameState.WAITING:
                self.gui.draw_message(f"第 {self.current_round} 轮", y_offset=-100)
                phase = "你射门" if self.current_phase == "player_shoot" else "你守门"
                self.gui.draw_sub_message(phase, y_offset=-50)

            elif state == GameState.REFEREE_READY:
                self.gui.draw_message("准备...", color=Colors.YELLOW)

            elif state == GameState.REFEREE_START:
                self.gui.draw_message("开始！", color=Colors.GOLD)

            elif state == GameState.CHOOSE_SHOOT:
                self.gui.draw_message("选择射门方向", y_offset=-150, color=Colors.YELLOW)
                self.gui.draw_sub_message("↑↓调整力度，点击球门选择方向", y_offset=-100)
                self.gui.draw_direction_zones(highlight=None)
                self.gui.draw_power_meter(self.gui.selected_power)
                # 显示当前射门球员
                self.gui.draw_sub_message(
                    f"射门球员: {self.shooter.name}",
                    y_offset=100
                )

            elif state == GameState.CHOOSE_SAVE:
                self.gui.draw_message("选择扑救方向", y_offset=-150, color=Colors.YELLOW)
                self.gui.draw_sub_message("点击球门选择扑救方向", y_offset=-100)
                self.gui.draw_direction_zones(highlight=None)
                self.gui.draw_sub_message(
                    f"射门球员: {self.shooter.name} (电脑)",
                    y_offset=100
                )

            elif state == GameState.ANIMATING:
                # 显示方向信息
                if self.current_phase == "player_shoot":
                    self.gui.draw_sub_message(
                        f"射门: {self.shoot_direction} 力度: {self.shoot_power}",
                        y_offset=100
                    )
                else:
                    self.gui.draw_sub_message(
                        f"扑救: {self.save_direction} | 射门: {self.shoot_direction}",
                        y_offset=100
                    )

            elif state == GameState.ROUND_RESULT:
                # 显示结果
                result = "⚽ 进球！⚽" if self.last_goal_scored else "🛡️  扑救成功！🛡️"
                color = Colors.GOLD if self.last_goal_scored else Colors.BLUE
                self.gui.draw_message(result, y_offset=-50, color=color)

                # 显示详细信息
                info = f"{self.last_shooter_name} "
                info += "进球" if self.last_goal_scored else "未进"
                self.gui.draw_sub_message(info, y_offset=20)

                # 继续提示
                self.gui.draw_sub_message(
                    "点击或按空格键继续",
                    y_offset=120
                )

            elif state == GameState.GAME_OVER:
                # 显示最终结果
                self.gui.draw_message("比赛结束！", y_offset=-120, color=Colors.GOLD)

                # 显示比分
                score_text = f"{self.player_name} {self.player_score} - {self.computer_score} {self.computer_name}"
                self.gui.draw_message(score_text, y_offset=-60)

                # 显示获胜者
                if self.player_score > self.computer_score:
                    winner_text = f"🏆 {self.player_name} 获胜！🏆"
                    winner_color = Colors.BLUE
                elif self.computer_score > self.player_score:
                    winner_text = f"🏆 {self.computer_name} 获胜！🏆"
                    winner_color = Colors.RED
                else:
                    winner_text = "🤝 平局！🤝"
                    winner_color = Colors.YELLOW

                self.gui.draw_message(winner_text, y_offset=20, color=winner_color)

                # 守门员表现
                gk_text = f"你的门将扑救: {self.player_goalkeeper.save_count}次 | " \
                          f"电脑门将扑救: {self.computer_goalkeeper.save_count}次"
                self.gui.draw_sub_message(gk_text, y_offset=80)

                # 继续提示
                self.gui.draw_sub_message(
                    "点击或按空格键返回主菜单",
                    y_offset=150
                )

        self.gui.render()
