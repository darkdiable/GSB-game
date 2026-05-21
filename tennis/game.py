import pygame
import math
from constants import *
from rules import TennisRules
from ball import Ball
from player import Player
from npc import NPC
from court import Court
from referee import Referee
from ui import UIManager


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('网球对战 - Tennis Match')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'start'

        self.rules = TennisRules()
        self.ball = Ball()
        self.player = Player()
        self.npc = NPC(difficulty='medium')
        self.court = Court()
        self.referee = Referee()
        self.ui = UIManager()

        self.space_pressed = False
        self.space_hold_time = 0
        self.point_end_timer = 0
        self.serve_ready = True

    def run(self):
        while self.running:
            self._handle_events()

            if self.game_state == 'start':
                self._start_screen()
            elif self.game_state in ['serve', 'playing']:
                self._update()
                self._draw()
            elif self.game_state == 'point_end':
                self._point_end_update()
                self._draw()
            elif self.game_state == 'game_over':
                self._game_over_screen()
                self._draw()

            self.clock.tick(FPS)

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.game_state == 'start':
                    self.game_state = 'serve'
                    self.rules.reset_match()
                elif self.game_state == 'game_over':
                    if event.key == pygame.K_r:
                        self._reset_game()
                elif self.game_state in ['serve', 'playing']:
                    if event.key == pygame.K_r:
                        self._reset_game()
                    elif event.key == pygame.K_SPACE:
                        self.space_pressed = True
                        self.space_hold_time = 0
                        self._handle_space_press()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and self.space_pressed:
                    self.space_pressed = False
                    self._handle_space_release()

        if self.space_pressed:
            self.space_hold_time += 1

    def _handle_space_press(self):
        if self.game_state == 'serve' and self.rules.serving == 'player' and self.rules.can_start_serve():
            self.player.serve(self.ball, self.rules)
            self.game_state = 'playing'
        elif self.game_state == 'playing' and not self.player.hitting:
            self.player.start_charge()

    def _handle_space_release(self):
        if self.game_state == 'playing' and self.player.charging:
            if self.player.is_near_ball(self.ball) and self.ball.in_play and self.ball.last_hit_by != 'player':
                target_x, target_y = self._get_hit_target()
                self.player.hit_ball(self.ball, target_x, target_y)
            else:
                self.player.charging = False
                self.player.power = 0.0

    def _get_hit_target(self):
        target_options = [
            (COURT_LEFT + 80, COURT_TOP + 80),
            (COURT_RIGHT - 80, COURT_TOP + 80),
            (CENTER_MARK_X, COURT_TOP + 60),
            (COURT_LEFT + 60, NET_Y - 60),
            (COURT_RIGHT - 60, NET_Y - 60),
        ]
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if mouse_y < NET_Y:
            return mouse_x, mouse_y
        
        best_target = target_options[0]
        min_dist = float('inf')
        
        for option in target_options:
            dist = math.sqrt((option[0] - mouse_x) ** 2 + (option[1] - mouse_y) ** 2)
            if dist < min_dist:
                min_dist = dist
                best_target = option
        
        return best_target

    def _update(self):
        keys = pygame.key.get_pressed()
        
        can_hit = self.game_state == 'playing'
        self.player.update(keys, self.ball, self.rules, can_hit)
        
        npc_served = self.npc.update(self.ball, self.rules, self.game_state)
        if npc_served and self.game_state == 'serve':
            self.game_state = 'playing'
        
        self.ball.update()
        self.rules.update()
        self.referee.update(self.rules)
        self.ui.update()

        if self.game_state == 'playing':
            self._check_violations()
            self._check_point_end()

        if self.rules.match_winner:
            self.game_state = 'game_over'

    def _check_violations(self):
        if not self.ball.in_play:
            return

        if self.player.check_net_touch():
            self.ball.in_play = False
            self.rules.net_touch('player')
            self.game_state = 'point_end'
            return

        if self.npc.check_net_touch():
            self.ball.in_play = False
            self.rules.net_touch('npc')
            self.game_state = 'point_end'
            return

        if self.ball.first_bounce_checked:
            serve_side = self.rules.get_serve_side()
            
            if self.ball.last_hit_by == 'player':
                in_box = self.ball.is_in_service_box('player', serve_side)
            else:
                in_box = self.ball.is_in_service_box('npc', serve_side)
            
            if not in_box:
                self.ball.in_play = False
                self.rules.fault()
                if self.rules.violation == VIOLATIONS[1]:
                    self.game_state = 'point_end'
                else:
                    self._restart_serve()
                return
            
            self.ball.first_bounce_checked = False

        if self.ball.z <= 0 and self.ball.vz <= 0.5 and self.ball.bounce_count >= 1:
            if not self.ball.is_in_court():
                self.ball.in_play = False
                if self.ball.bounce_count >= 2 and self.ball.last_hit_by:
                    self.rules.out(self.ball.last_hit_by)
                elif self.ball.last_hit_by:
                    winner = 'npc' if self.ball.last_hit_by == 'player' else 'player'
                    self.rules.win_point(winner)
                self.game_state = 'point_end'
                return

        if self.ball.last_hit_by and self.ball.bounce_count >= 2:
            expected_side = 'bottom' if self.ball.last_hit_by == 'npc' else 'top'
            if not self.ball.is_in_court(expected_side):
                self.ball.in_play = False
                self.rules.out(self.ball.last_hit_by)
                self.game_state = 'point_end'
                return

        if self.ball.bounce_count >= 3:
            self.ball.in_play = False
            if self.ball.y > NET_Y:
                self.rules.win_point('npc')
            else:
                self.rules.win_point('player')
            self.game_state = 'point_end'
            return

        if self.ball.y < COURT_TOP - 50 or self.ball.y > COURT_BOTTOM + 50:
            self.ball.in_play = False
            if self.ball.last_hit_by:
                self.rules.out(self.ball.last_hit_by)
            self.game_state = 'point_end'
            return

        if self.ball.x < COURT_LEFT - 50 or self.ball.x > COURT_RIGHT + 50:
            self.ball.in_play = False
            if self.ball.last_hit_by:
                self.rules.out(self.ball.last_hit_by)
            self.game_state = 'point_end'
            return

    def _check_point_end(self):
        if not self.ball.in_play and self.ball.last_hit_by is None:
            return

        if self.npc.is_near_ball(self.ball) and not self.npc.hitting:
            pass

    def _point_end_update(self):
        self.point_end_timer += 1
        
        self.player.update(pygame.key.get_pressed(), self.ball, self.rules, False)
        self.npc.update(self.ball, self.rules, self.game_state)
        self.rules.update()
        self.referee.update(self.rules)

        if self.point_end_timer >= 120:
            self._next_point()

    def _next_point(self):
        self.point_end_timer = 0
        
        if self.rules.match_winner:
            self.game_state = 'game_over'
            return

        if self.rules.game_winner:
            self.rules.reset_game()
        
        self.ball.reset()
        self.player.reset()
        self.npc.reset()
        
        serve_side = self.rules.get_serve_side()
        if self.rules.serving == 'player':
            self.player.x = CENTER_MARK_X + 80 if serve_side == 'right' else CENTER_MARK_X - 80
            self.player.y = COURT_BOTTOM - 60
        else:
            self.npc.x = CENTER_MARK_X + 80 if serve_side == 'right' else CENTER_MARK_X - 80
            self.npc.y = COURT_TOP + 60
        
        self.game_state = 'serve'
        self.serve_ready = True

    def _restart_serve(self):
        self.ball.reset()
        self.player.reset()
        self.npc.reset()
        
        serve_side = self.rules.get_serve_side()
        if self.rules.serving == 'player':
            self.player.x = CENTER_MARK_X + 80 if serve_side == 'right' else CENTER_MARK_X - 80
            self.player.y = COURT_BOTTOM - 60
        
        self.game_state = 'serve'

    def _start_screen(self):
        self.court.draw(self.screen)
        self.ui.draw_start_screen(self.screen)
        pygame.display.flip()

    def _game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        if self.rules.match_winner == 'player':
            text = FONT_LARGE.render('恭喜获胜！', True, COLORS['player'])
        else:
            text = FONT_LARGE.render('比赛结束', True, COLORS['npc'])
        
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        subtext = FONT_MEDIUM.render('按 R 键重新开始', True, COLORS['text'])
        self.screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    def _draw(self):
        self.court.draw(self.screen)
        
        if self.ball.in_play:
            self.ball.draw(self.screen)
        
        self.npc.draw(self.screen)
        self.player.draw(self.screen)
        self.referee.draw(self.screen)
        
        self.ui.draw_scoreboard(self.screen, self.rules)
        self.ui.draw_controls(self.screen, self.game_state, self.rules)
        self.ui.draw_point_indicator(self.screen, self.rules)
        
        if self.space_pressed and self.game_state == 'playing':
            self._draw_target_indicator()

        pygame.display.flip()

    def _draw_target_indicator(self):
        target_x, target_y = self._get_hit_target()
        pygame.draw.circle(self.screen, (255, 0, 0), (int(target_x), int(target_y)), 15, 3)
        pygame.draw.line(self.screen, (255, 0, 0), 
                        (self.player.x, self.player.y - 30), 
                        (int(target_x), int(target_y)), 2)

    def _reset_game(self):
        self.rules.reset_match()
        self.ball.reset()
        self.player.reset()
        self.npc.reset()
        self.game_state = 'serve'
        self.point_end_timer = 0
        self.space_pressed = False
        self.space_hold_time = 0
