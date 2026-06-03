import pygame
from constants import *


class Scoreboard:
    def __init__(self):
        self.player_points = 0
        self.npc_points = 0
        self.player_games = 0
        self.npc_games = 0
        self.player_sets = 0
        self.npc_sets = 0
        self.server = "player"
        self.tiebreak = False
        self.tiebreak_score = {"player": 0, "npc": 0}

    def point_to_score(self, points):
        if points == 0:
            return "0"
        elif points == 1:
            return "15"
        elif points == 2:
            return "30"
        elif points == 3:
            return "40"
        else:
            return "AD"

    def add_point(self, winner):
        if self.tiebreak:
            self.tiebreak_score[winner] += 1
            self._check_tiebreak()
            return

        if winner == "player":
            if self.player_points < 3:
                self.player_points += 1
            elif self.player_points == 3:
                if self.npc_points < 3:
                    self._win_game("player")
                elif self.npc_points == 3:
                    self.player_points = 4
                elif self.npc_points == 4:
                    self.npc_points = 3
            elif self.player_points == 4:
                self._win_game("player")
        else:
            if self.npc_points < 3:
                self.npc_points += 1
            elif self.npc_points == 3:
                if self.player_points < 3:
                    self._win_game("npc")
                elif self.player_points == 3:
                    self.npc_points = 4
                elif self.player_points == 4:
                    self.player_points = 3
            elif self.npc_points == 4:
                self._win_game("npc")

    def _win_game(self, winner):
        if winner == "player":
            self.player_games += 1
        else:
            self.npc_games += 1
        
        self.player_points = 0
        self.npc_points = 0
        
        self.server = "npc" if self.server == "player" else "player"
        
        self._check_set()

    def _check_set(self):
        if self.player_games >= 6 and self.npc_games >= 6:
            if not self.tiebreak:
                self.tiebreak = True
                self.tiebreak_score = {"player": 0, "npc": 0}
            return
        
        if self.player_games >= 6 and self.player_games - self.npc_games >= 2:
            self._win_set("player")
        elif self.npc_games >= 6 and self.npc_games - self.player_games >= 2:
            self._win_set("npc")

    def _check_tiebreak(self):
        player = self.tiebreak_score["player"]
        npc = self.tiebreak_score["npc"]
        
        if (player >= 7 or npc >= 7) and abs(player - npc) >= 2:
            if player > npc:
                self.player_games += 1
                self._win_set("player")
            else:
                self.npc_games += 1
                self._win_set("npc")

    def _win_set(self, winner):
        if winner == "player":
            self.player_sets += 1
        else:
            self.npc_sets += 1
        
        self.player_games = 0
        self.npc_games = 0
        self.tiebreak = False
        self.tiebreak_score = {"player": 0, "npc": 0}

    def check_match_winner(self):
        if self.player_sets >= 2:
            return "player"
        elif self.npc_sets >= 2:
            return "npc"
        return None

    def reset(self):
        self.player_points = 0
        self.npc_points = 0
        self.player_games = 0
        self.npc_games = 0
        self.player_sets = 0
        self.npc_sets = 0
        self.server = "player"
        self.tiebreak = False
        self.tiebreak_score = {"player": 0, "npc": 0}

    def draw(self, screen):
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)
        
        bg_rect = pygame.Rect(20, 20, 350, 180)
        pygame.draw.rect(screen, WHITE, bg_rect)
        pygame.draw.rect(screen, BLACK, bg_rect, 3)
        
        title = font_large.render("网球对战", True, BLUE)
        screen.blit(title, (bg_rect.centerx - title.get_width() // 2, 25))
        
        set_text = font_medium.render(f"盘分: {self.player_sets} - {self.npc_sets}", True, BLACK)
        screen.blit(set_text, (bg_rect.centerx - set_text.get_width() // 2, 70))
        
        game_text = font_medium.render(f"局分: {self.player_games} - {self.npc_games}", True, BLACK)
        screen.blit(game_text, (bg_rect.centerx - game_text.get_width() // 2, 105))
        
        if self.tiebreak:
            score_text = font_small.render(
                f"抢七: {self.tiebreak_score['player']} - {self.tiebreak_score['npc']}", 
                True, RED)
        else:
            player_score = self.point_to_score(self.player_points)
            npc_score = self.point_to_score(self.npc_points)
            if self.player_points == 4 and self.npc_points == 3:
                player_score = "AD"
                npc_score = "40"
            elif self.npc_points == 4 and self.player_points == 3:
                player_score = "40"
                npc_score = "AD"
            score_text = font_small.render(
                f"比分: 玩家 {player_score} - {npc_score} 电脑", 
                True, BLACK)
        
        screen.blit(score_text, (bg_rect.centerx - score_text.get_width() // 2, 140))
        
        server_text = font_small.render(
            f"发球方: {'玩家' if self.server == 'player' else '电脑'}", 
            True, GREEN)
        screen.blit(server_text, (bg_rect.centerx - server_text.get_width() // 2, 170))
        
        help_rect = pygame.Rect(SCREEN_WIDTH - 220, 20, 200, 120)
        pygame.draw.rect(screen, WHITE, help_rect)
        pygame.draw.rect(screen, BLACK, help_rect, 2)
        
        help_title = font_small.render("操作说明", True, BLUE)
        screen.blit(help_title, (help_rect.centerx - help_title.get_width() // 2, 25))
        
        controls = [
            "WASD / 方向键: 移动",
            "空格键: 击球/发球",
            "ESC: 暂停"
        ]
        
        for i, control in enumerate(controls):
            text = pygame.font.Font(None, 22).render(control, True, BLACK)
            screen.blit(text, (help_rect.x + 10, 50 + i * 25))
