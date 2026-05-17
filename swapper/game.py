import pygame
import random
from constants import *
from particle import Particle
from gate import Gate
from effects import CollapseEffect, ScorePopup, DynamicBackground


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("量子纠缠交换")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        self.reset()

    def reset(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.time_left = GAME_DURATION
        self.last_spawn_time = 0
        self.spawn_interval = BASE_SPAWN_INTERVAL
        self.particles = []
        self.gates = []
        self.effects = []
        self.score_popups = []
        self.dragged_particle = None
        self.game_over = False
        self.game_started = False
        self.start_time = 0
        self.background = DynamicBackground()
        
        self.setup_gates()
        self.spawn_initial_particles()

    def setup_gates(self):
        gate_positions = [
            (150, SCREEN_HEIGHT - 100),
            (350, SCREEN_HEIGHT - 100),
            (550, SCREEN_HEIGHT - 100),
            (750, SCREEN_HEIGHT - 100),
            (250, SCREEN_HEIGHT - 200),
            (650, SCREEN_HEIGHT - 200),
        ]
        
        for i, gate_type in enumerate(GATE_TYPES):
            x, y = gate_positions[i]
            self.gates.append(Gate(gate_type, x, y))

    def spawn_initial_particles(self):
        for _ in range(3):
            self.spawn_particle()

    def spawn_particle(self):
        gate_type = random.choice(GATE_TYPES)
        particle = Particle(gate_type)
        self.particles.append(particle)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset()
                    self.game_started = True
                    self.start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_SPACE and not self.game_started:
                    self.game_started = True
                    self.start_time = pygame.time.get_ticks()
            
            if self.game_started and not self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for particle in reversed(self.particles):
                        if particle.contains_point(event.pos):
                            self.dragged_particle = particle
                            particle.start_drag(event.pos)
                            self.particles.remove(particle)
                            self.particles.append(particle)
                            break
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragged_particle:
                        self.dragged_particle.update_drag(event.pos)
                        self.update_gate_highlight(event.pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dragged_particle:
                        self.dragged_particle.stop_drag()
                        self.check_matching()
                        self.dragged_particle = None
                        for gate in self.gates:
                            gate.highlight = False
        
        return True

    def update_gate_highlight(self, pos):
        for gate in self.gates:
            if gate.contains_point(pos):
                gate.highlight = True
            else:
                gate.highlight = False

    def check_matching(self):
        if not self.dragged_particle:
            return
        
        for gate in self.gates:
            if gate.contains_point((self.dragged_particle.x, self.dragged_particle.y)):
                if gate.check_match(self.dragged_particle):
                    self.handle_successful_match(gate)
                else:
                    self.handle_failed_match()
                return
        
        self.combo = 0
        self.spawn_interval = BASE_SPAWN_INTERVAL

    def handle_successful_match(self, gate):
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        
        score_gain = BASE_SCORE + (self.combo - 1) * COMBO_BONUS
        self.score += score_gain
        
        gate.trigger_match()
        
        effect = CollapseEffect(self.dragged_particle.x, self.dragged_particle.y, gate.color)
        self.effects.append(effect)
        
        popup = ScorePopup(self.dragged_particle.x, self.dragged_particle.y - 30, score_gain, self.combo)
        self.score_popups.append(popup)
        
        self.particles.remove(self.dragged_particle)
        
        self.spawn_interval = max(MIN_SPAWN_INTERVAL, int(self.spawn_interval * COMBO_MULTIPLIER))

    def handle_failed_match(self):
        self.combo = 0
        self.spawn_interval = BASE_SPAWN_INTERVAL

    def update(self):
        current_time = pygame.time.get_ticks()
        
        if self.game_started and not self.game_over:
            elapsed = (current_time - self.start_time) / 1000
            self.time_left = max(0, GAME_DURATION - int(elapsed))
            
            if self.time_left <= 0:
                self.game_over = True
            
            if current_time - self.last_spawn_time > self.spawn_interval:
                self.spawn_particle()
                self.last_spawn_time = current_time
        
        for particle in self.particles:
            if particle != self.dragged_particle:
                particle.update(current_time)
        
        for gate in self.gates:
            gate.update()
        
        self.effects = [e for e in self.effects if e.active]
        for effect in self.effects:
            effect.update()
        
        self.score_popups = [p for p in self.score_popups if p.active]
        for popup in self.score_popups:
            popup.update()
        
        self.background.update()

    def draw(self):
        self.background.draw(self.screen)
        
        for gate in self.gates:
            gate.draw(self.screen)
        
        for particle in self.particles:
            if particle != self.dragged_particle:
                particle.draw(self.screen)
        
        if self.dragged_particle:
            self.dragged_particle.draw(self.screen)
        
        for effect in self.effects:
            effect.draw(self.screen)
        
        for popup in self.score_popups:
            popup.draw(self.screen)
        
        self.draw_ui()
        
        if not self.game_started:
            self.draw_start_screen()
        elif self.game_over:
            self.draw_game_over_screen()
        
        pygame.display.flip()

    def draw_ui(self):
        ui_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, (20, 20, 50, 200), ui_rect)
        pygame.draw.line(self.screen, (100, 150, 255), (0, 80), (SCREEN_WIDTH, 80), 2)
        
        score_text = self.font_large.render(f"分数: {self.score}", True, (255, 255, 100))
        self.screen.blit(score_text, (30, 20))
        
        time_color = (255, 100, 100) if self.time_left <= 10 else (100, 255, 100)
        time_text = self.font_large.render(f"时间: {self.time_left}s", True, time_color)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(time_text, time_rect)
        
        combo_color = (255, 100, 100) if self.combo >= 3 else (255, 255, 255)
        combo_text = self.font_medium.render(f"连击: {self.combo}x", True, combo_color)
        combo_rect = combo_text.get_rect(right=SCREEN_WIDTH - 30, centery=40)
        self.screen.blit(combo_text, combo_rect)

    def draw_start_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("量子纠缠交换", True, (100, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title, title_rect)
        
        instructions = [
            "将飘浮的纠缠粒子（太极符号）拖拽到匹配的量子门中",
            "连续正确匹配会加速粒子生成，获得更多分数！",
            "",
            "按空格键开始游戏"
        ]
        
        for i, line in enumerate(instructions):
            text = self.font_small.render(line, True, (255, 255, 255))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20 + i * 30))
            self.screen.blit(text, rect)

    def draw_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        title = self.font_large.render("游戏结束!", True, (255, 100, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(title, title_rect)
        
        final_score = self.font_large.render(f"最终得分: {self.score}", True, (255, 255, 100))
        score_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(final_score, score_rect)
        
        max_combo_text = self.font_medium.render(f"最高连击: {self.max_combo}x", True, (100, 255, 100))
        combo_rect = max_combo_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(max_combo_text, combo_rect)
        
        restart_text = self.font_medium.render("按空格键重新开始", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
