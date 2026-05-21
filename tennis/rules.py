from constants import *


class TennisRules:
    def __init__(self):
        self.player_score = 0
        self.npc_score = 0
        self.player_games = 0
        self.npc_games = 0
        self.player_sets = 0
        self.npc_sets = 0
        self.serving = 'player'
        self.violation = None
        self.violation_timer = 0
        self.first_serve = True
        self.deuce = False
        self.advantage = None
        self.point_winner = None
        self.game_winner = None
        self.match_winner = None
        self.set_history = []

    def reset_game(self):
        self.player_score = 0
        self.npc_score = 0
        self.deuce = False
        self.advantage = None
        self.first_serve = True
        self.violation = None
        self.violation_timer = 0
        self.point_winner = None
        self.game_winner = None

    def reset_match(self):
        self.reset_game()
        self.player_games = 0
        self.npc_games = 0
        self.player_sets = 0
        self.npc_sets = 0
        self.serving = 'player'
        self.match_winner = None
        self.set_history = []

    def get_score_display(self, player=True):
        if self.match_winner:
            return 'WIN' if self.match_winner == ('player' if player else 'npc') else 'LOSE'
        
        if self.game_winner:
            return 'GAME' if self.game_winner == ('player' if player else 'npc') else ''
        
        score = self.player_score if player else self.npc_score
        
        if self.deuce:
            if self.advantage == ('player' if player else 'npc'):
                return 'AD'
            elif self.advantage is None:
                return '40'
            else:
                return '40'
        
        if score < len(SCORE_POINTS):
            return SCORE_POINTS[score]
        return '40'

    def win_point(self, winner):
        if self.match_winner:
            return

        self.point_winner = winner
        player_won = winner == 'player'

        if self.deuce:
            if self.advantage is None:
                self.advantage = winner
            elif self.advantage == winner:
                self._win_game(winner)
            else:
                self.advantage = None
        else:
            if player_won:
                self.player_score += 1
            else:
                self.npc_score += 1

            if self.player_score >= 3 and self.npc_score >= 3:
                if self.player_score == self.npc_score:
                    self.deuce = True
                    self.advantage = None
                elif self.player_score > 3 and self.player_score - self.npc_score >= 2:
                    self._win_game('player')
                elif self.npc_score > 3 and self.npc_score - self.player_score >= 2:
                    self._win_game('npc')
            elif self.player_score >= 4:
                self._win_game('player')
            elif self.npc_score >= 4:
                self._win_game('npc')

    def _win_game(self, winner):
        self.game_winner = winner
        
        if winner == 'player':
            self.player_games += 1
        else:
            self.npc_games += 1

        if (self.player_games >= 6 or self.npc_games >= 6) and abs(self.player_games - self.npc_games) >= 2:
            self._win_set(winner)
        else:
            self._switch_server()

    def _win_set(self, winner):
        set_score = (self.player_games, self.npc_games)
        self.set_history.append(set_score)
        
        if winner == 'player':
            self.player_sets += 1
        else:
            self.npc_sets += 1

        if self.player_sets >= 2 or self.npc_sets >= 2:
            self.match_winner = winner
        else:
            self.player_games = 0
            self.npc_games = 0
            self._switch_server()

    def _switch_server(self):
        self.serving = 'npc' if self.serving == 'player' else 'player'

    def call_violation(self, violation_type, point_to):
        self.violation = violation_type
        self.violation_timer = 180
        self.win_point(point_to)
        self.first_serve = True

    def fault(self):
        if self.first_serve:
            self.first_serve = False
            self.violation = VIOLATIONS[0]
            self.violation_timer = 120
        else:
            point_to = 'npc' if self.serving == 'player' else 'player'
            self.call_violation(VIOLATIONS[1], point_to)
            self.first_serve = True

    def out(self, hitter):
        point_to = 'npc' if hitter == 'player' else 'player'
        self.call_violation(VIOLATIONS[2], point_to)

    def net_touch(self, player):
        point_to = 'npc' if player == 'player' else 'player'
        self.call_violation(VIOLATIONS[3], point_to)

    def update(self):
        if self.violation_timer > 0:
            self.violation_timer -= 1
            if self.violation_timer <= 0:
                self.violation = None
                self.point_winner = None
                self.game_winner = None

    def can_start_serve(self):
        return self.violation is None and not self.match_winner

    def get_serve_side(self):
        total_points = self.player_score + self.npc_score
        total_games = self.player_games + self.npc_games
        return 'right' if (total_points + total_games) % 2 == 0 else 'left'
