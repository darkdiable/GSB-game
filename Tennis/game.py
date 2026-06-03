import pygame
import sys
from constants import *
from court import Court
from player import Player
from ball import Ball
from referee import Referee
from scoreboard import Scoreboard


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = STATE_MENU
        
        self.court = Court()
        self.player = Player(is_npc=False)
        self.npc = Player(is_npc=True)
        self.ball = Ball()
        self.referee = Referee()
        self.scoreboard = Scoreboard()
        
        self.rally = False
        self.fault_count = 0
        self.awaiting_serve = True
        self.pause_timer = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_key_down(event.key)
            
            self._update()
            self._draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

    def _handle_key_down(self, key):
        if self.state == STATE_MENU:
            if key == pygame.K_SPACE or key == pygame.K_RETURN:
                self._start_game()
        elif self.state == STATE_PLAYING:
            if key == pygame.K_ESCAPE:
                self.state = STATE_PAUSED
            elif key == pygame.K_SPACE:
                self._handle_space()
        elif self.state == STATE_PAUSED:
            if key == pygame.K_ESCAPE:
                self.state = STATE_PLAYING
            elif key == pygame.K_r:
                self._reset_game()
        elif self.state == STATE_GAME_OVER:
            if key == pygame.K_SPACE or key == pygame.K_RETURN:
                self._reset_game()

    def _handle_space(self):
        if self.awaiting_serve:
            if self.scoreboard.server == "player":
                self.player.swing()
                self.ball.serve(self.player)
                self.awaiting_serve = False
                self.rally = True
        else:
            self.player.swing()

    def _start_game(self):
        self.state = STATE_PLAYING
        self._reset_serve()

    def _reset_game(self):
        self.scoreboard.reset()
        self._reset_serve()
        self.state = STATE_PLAYING

    def _reset_serve(self):
        self.ball.reset()
        self.player.reset_position(serving=(self.scoreboard.server == "player"))
        self.npc.reset_position(serving=(self.scoreboard.server == "npc"))
        self.awaiting_serve = True
        self.rally = False
        self.fault_count = 0
        self.pause_timer = 0
        
        if self.scoreboard.server == "npc":
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500, 1)

    def _update(self):
        self.referee.update()
        
        if self.pause_timer > 0:
            self.pause_timer -= 1
            return
        
        if self.state != STATE_PLAYING:
            return
        
        keys = pygame.key.get_pressed()
        self.player.update(keys=keys, ball=self.ball)
        self.npc.update(ball=self.ball)
        
        if self.scoreboard.server == "npc" and self.awaiting_serve:
            for event in pygame.event.get(pygame.USEREVENT + 1):
                if event.type == pygame.USEREVENT + 1:
                    self.ball.serve(self.npc)
                    self.awaiting_serve = False
                    self.rally = True
        
        if self.ball.active:
            self.ball.update()
            
            self.ball.check_hit(self.player)
            self.ball.check_hit(self.npc)
            
            if self.rally:
                self._check_rally_rules()
        
        winner = self.scoreboard.check_match_winner()
        if winner:
            self.state = STATE_GAME_OVER

    def _check_rally_rules(self):
        if self.ball.serve_mode and self.ball.bounce_count >= 1:
            self._check_serve_result()
            return
        
        if not self.ball.serve_mode:
            if self.ball.x < SINGLES_LEFT or self.ball.x > SINGLES_RIGHT:
                if self.ball.last_hitter:
                    winner = "npc" if self.ball.last_hitter == "player" else "player"
                    self._point_won(winner, "出界!")
                return
            
            current_side = self.ball.get_side()
            if self.ball.last_hitter == "player" and current_side == "player":
                if self.ball.bounce_count >= 2:
                    self._point_won("npc", "两跳!")
                    return
            elif self.ball.last_hitter == "npc" and current_side == "npc":
                if self.ball.bounce_count >= 2:
                    self._point_won("player", "两跳!")
                    return

    def _check_serve_result(self):
        server = "player" if self.scoreboard.server == "player" else "npc"
        receiver_side = "npc" if server == "player" else "player"
        
        if self.ball.hit_net:
            self.referee.set_message("擦网! 重发", YELLOW)
            self.pause_timer = 60
            self._reset_serve()
            return
        
        receiver_in_bounds = self.referee.is_in_bounds(
            self.ball.x, self.ball.y, receiver_side)
        
        if not receiver_in_bounds:
            self.fault_count += 1
            if self.fault_count >= 2:
                winner = "player" if server == "npc" else "npc"
                self._point_won(winner, "双误!")
            else:
                self.referee.set_message("发球失误!", RED)
                self.pause_timer = 60
                self._reset_serve()
            return
        
        self.ball.serve_mode = False
        self.referee.set_message("发球有效!", GREEN)

    def _point_won(self, winner, message):
        self.scoreboard.add_point(winner)
        self.referee.set_message(message, RED)
        self.pause_timer = 90
        
        match_winner = self.scoreboard.check_match_winner()
        if match_winner:
            self.state = STATE_GAME_OVER
        else:
            pygame.time.set_timer(pygame.USEREVENT + 2, 1000, 1)
            self.awaiting_serve = True
            self.rally = False

    def _draw(self):
        self.screen.fill(GREEN)
        
        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_PLAYING or self.state == STATE_PAUSED:
            self.court.draw(self.screen)
            self.referee.draw(self.screen)
            self.ball.draw(self.screen)
            self.player.draw(self.screen)
            self.npc.draw(self.screen)
            self.scoreboard.draw(self.screen)
            
            if self.awaiting_serve and self.scoreboard.server == "player":
                font = pygame.font.Font(None, 36)
                text = font.render("按空格键发球", True, WHITE)
                self.screen.blit(text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 50))
            
            if self.state == STATE_PAUSED:
                self._draw_pause_overlay()
        elif self.state == STATE_GAME_OVER:
            self._draw_game_over()
        
        pygame.display.flip()

    def _draw_menu(self):
        self.court.draw(self.screen)
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 80)
        title = font_large.render("网球对战", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        
        font_medium = pygame.font.Font(None, 48)
        subtitle = font_medium.render("玩家 vs 电脑", True, WHITE)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 250))
        
        font_small = pygame.font.Font(None, 32)
        instructions = [
            "游戏规则: 三局两胜制",
            "WASD或方向键移动",
            "空格键击球",
            "",
            "按空格键开始游戏"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, WHITE)
            self.screen.blit(text, 
                           (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                            350 + i * 40))

    def _draw_pause_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 64)
        text = font_large.render("游戏暂停", True, YELLOW)
        self.screen.blit(text, 
                        (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 - 50))
        
        font_small = pygame.font.Font(None, 32)
        text2 = font_small.render("按ESC继续, 按R重新开始", True, WHITE)
        self.screen.blit(text2, 
                        (SCREEN_WIDTH // 2 - text2.get_width() // 2, 
                         SCREEN_HEIGHT // 2 + 20))

    def _draw_game_over(self):
        self.court.draw(self.screen)
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.Font(None, 72)
        winner = self.scoreboard.check_match_winner()
        if winner == "player":
            text = font_large.render("恭喜你获胜!", True, YELLOW)
        else:
            text = font_large.render("电脑获胜", True, RED)
        
        self.screen.blit(text, 
                        (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 - 80))
        
        font_medium = pygame.font.Font(None, 36)
        score_text = font_medium.render(
            f"最终比分: {self.scoreboard.player_sets} - {self.scoreboard.npc_sets}", 
            True, WHITE)
        self.screen.blit(score_text, 
                        (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2))
        
        font_small = pygame.font.Font(None, 28)
        restart_text = font_small.render("按空格键重新开始", True, WHITE)
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 + 60))
