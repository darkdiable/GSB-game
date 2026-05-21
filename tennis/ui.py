import pygame
from constants import *


class UIManager:
    def __init__(self):
        self.animate_score = False
        self.anim_timer = 0

    def draw_scoreboard(self, screen, rules):
        scoreboard_width = 350
        scoreboard_height = 180
        x = (SCREEN_WIDTH - scoreboard_width) // 2
        y = 5

        bg_surface = pygame.Surface((scoreboard_width, scoreboard_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, COLORS['score_bg'], bg_surface.get_rect(), border_radius=10)
        pygame.draw.rect(bg_surface, (255, 255, 255, 100), bg_surface.get_rect(), 2, border_radius=10)
        screen.blit(bg_surface, (x, y))

        title_text = FONT_MEDIUM.render('网球对战', True, COLORS['text'])
        screen.blit(title_text, (x + scoreboard_width // 2 - title_text.get_width() // 2, y + 8))

        header_y = y + 45
        headers = ['', '比分', '局', '盘']
        col_widths = [80, 80, 60, 60]
        start_x = x + 20

        for i, header in enumerate(headers):
            text = FONT_SMALL.render(header, True, COLORS['text'])
            screen.blit(text, (start_x + sum(col_widths[:i]) + col_widths[i] // 2 - text.get_width() // 2, header_y))

        player_row_y = y + 75
        npc_row_y = y + 115

        player_name = FONT_SMALL.render('玩家', True, COLORS['player'])
        screen.blit(player_name, (start_x + 10, player_row_y))

        npc_name = FONT_SMALL.render('电脑', True, COLORS['npc'])
        screen.blit(npc_name, (start_x + 10, npc_row_y))

        player_score = rules.get_score_display(player=True)
        npc_score = rules.get_score_display(player=False)

        score_text_player = FONT_MEDIUM.render(player_score, True, COLORS['player'])
        score_text_npc = FONT_MEDIUM.render(npc_score, True, COLORS['npc'])

        screen.blit(score_text_player, 
                   (start_x + col_widths[0] + col_widths[1] // 2 - score_text_player.get_width() // 2, 
                    player_row_y - 5))
        screen.blit(score_text_npc, 
                   (start_x + col_widths[0] + col_widths[1] // 2 - score_text_npc.get_width() // 2, 
                    npc_row_y - 5))

        games_player = FONT_MEDIUM.render(str(rules.player_games), True, COLORS['text'])
        games_npc = FONT_MEDIUM.render(str(rules.npc_games), True, COLORS['text'])

        screen.blit(games_player, 
                   (start_x + col_widths[0] + col_widths[1] + col_widths[2] // 2 - games_player.get_width() // 2, 
                    player_row_y - 5))
        screen.blit(games_npc, 
                   (start_x + col_widths[0] + col_widths[1] + col_widths[2] // 2 - games_npc.get_width() // 2, 
                    npc_row_y - 5))

        sets_player = FONT_MEDIUM.render(str(rules.player_sets), True, COLORS['text'])
        sets_npc = FONT_MEDIUM.render(str(rules.npc_sets), True, COLORS['text'])

        screen.blit(sets_player, 
                   (start_x + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3] // 2 - sets_player.get_width() // 2, 
                    player_row_y - 5))
        screen.blit(sets_npc, 
                   (start_x + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3] // 2 - sets_npc.get_width() // 2, 
                    npc_row_y - 5))

        set_history_y = y + 150
        if rules.set_history:
            history_text = "盘分: "
            for i, (p, n) in enumerate(rules.set_history):
                if i > 0:
                    history_text += ", "
                history_text += f"{p}-{n}"
            history_surface = FONT_SMALL.render(history_text, True, COLORS['text'])
            screen.blit(history_surface, (x + scoreboard_width // 2 - history_surface.get_width() // 2, set_history_y))

        serve_indicator_y = y + 45
        if rules.serving == 'player':
            serve_text = FONT_SMALL.render('● 发球', True, COLORS['player'])
            screen.blit(serve_text, (x + scoreboard_width - 70, serve_indicator_y))
        else:
            serve_text = FONT_SMALL.render('● 发球', True, COLORS['npc'])
            screen.blit(serve_text, (x + scoreboard_width - 70, serve_indicator_y))

        if not rules.first_serve and not rules.match_winner:
            second_serve = FONT_SMALL.render('二发', True, (255, 200, 0))
            screen.blit(second_serve, (x + scoreboard_width - 70, serve_indicator_y + 25))

    def draw_controls(self, screen, game_state, rules):
        controls_y = SCREEN_HEIGHT - 35
        bg_surface = pygame.Surface((SCREEN_WIDTH, 30), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, (0, 0, 0, 120), bg_surface.get_rect())
        screen.blit(bg_surface, (0, SCREEN_HEIGHT - 30))

        if game_state == 'start':
            text = FONT_SMALL.render('按任意键开始比赛 | WASD/方向键移动 | 空格击球 | 长按蓄力 | R重新开始', True, COLORS['text'])
        elif game_state == 'serve' and rules.serving == 'player' and rules.can_start_serve():
            text = FONT_SMALL.render('按空格发球 | WASD/方向键移动 | 长按蓄力击球 | R重新开始', True, COLORS['player'])
        elif rules.match_winner:
            winner = "你赢了！" if rules.match_winner == 'player' else "你输了！"
            text = FONT_SMALL.render(f'{winner} 按R重新开始', True, COLORS['text'])
        else:
            text = FONT_SMALL.render('WASD/方向键移动 | 空格击球 | 长按蓄力 | R重新开始', True, COLORS['text'])
        
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, controls_y))

    def draw_start_screen(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = FONT_LARGE.render('网球对战', True, COLORS['text'])
        subtitle = FONT_MEDIUM.render('TENNIS MATCH', True, (100, 200, 255))
        
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, SCREEN_HEIGHT // 2 - 40))

        instructions = [
            '操作说明:',
            'WASD / 方向键 - 移动',
            '空格键 - 击球 (长按蓄力)',
            '发球时按空格 - 发球',
            'R键 - 重新开始',
            '',
            '按任意键开始比赛'
        ]

        for i, line in enumerate(instructions):
            text = FONT_SMALL.render(line, True, COLORS['text'])
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 20 + i * 28))

    def draw_point_indicator(self, screen, rules):
        if rules.point_winner and not rules.violation:
            x = SCREEN_WIDTH // 2
            y = COURT_TOP + COURT_HEIGHT // 2
            
            winner = "玩家" if rules.point_winner == 'player' else "电脑"
            color = COLORS['player'] if rules.point_winner == 'player' else COLORS['npc']
            
            pulse = 1.0 + 0.2 * abs(pygame.time.get_ticks() % 400 - 200) / 200
            text = FONT_LARGE.render(f'{winner}得分！', True, color)
            text = pygame.transform.scale(text, 
                (int(text.get_width() * pulse), int(text.get_height() * pulse)))
            
            text_bg = pygame.Surface((text.get_width() + 40, text.get_height() + 20), pygame.SRCALPHA)
            pygame.draw.rect(text_bg, (0, 0, 0, 150), text_bg.get_rect(), border_radius=10)
            text_bg.blit(text, (20, 10))
            
            screen.blit(text_bg, (x - text_bg.get_width() // 2, y - text_bg.get_height() // 2))

    def update(self):
        pass
