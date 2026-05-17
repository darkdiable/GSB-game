import pygame
import random
import math
from constants import *
from audio import AudioSynth


class Slider:
    def __init__(self, x, y, width, height, color, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.label = label
        self.value = 128
        self.dragging = False
        self.handle_radius = 15

    def get_handle_x(self):
        return self.rect.x + (self.value / 255) * self.rect.width

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_x = self.get_handle_x()
            handle_rect = pygame.Rect(
                handle_x - self.handle_radius,
                self.rect.y - self.handle_radius + self.rect.height // 2,
                self.handle_radius * 2,
                self.handle_radius * 2
            )
            if handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.value = int((x - self.rect.x) / self.rect.width * 255)

    def draw(self, screen, font):
        pygame.draw.rect(screen, DARK_GRAY, self.rect, border_radius=5)
        
        fill_width = (self.value / 255) * self.rect.width
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, self.color, fill_rect, border_radius=5)
        
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=5)
        
        handle_x = self.get_handle_x()
        handle_y = self.rect.y + self.rect.height // 2
        pygame.draw.circle(screen, WHITE, (int(handle_x), handle_y), self.handle_radius)
        pygame.draw.circle(screen, self.color, (int(handle_x), handle_y), self.handle_radius - 3)
        
        label_text = font.render(f"{self.label}: {self.value}", True, WHITE)
        screen.blit(label_text, (self.rect.x, self.rect.y - 35))


class Distractor:
    def __init__(self, safe_zones):
        while True:
            self.x = random.randint(50, SCREEN_WIDTH - DISTRACTOR_SIZE - 50)
            self.y = random.randint(50, SCREEN_HEIGHT - DISTRACTOR_SIZE - 50)
            self.size = DISTRACTOR_SIZE
            distractor_rect = pygame.Rect(self.x, self.y, self.size, self.size)
            
            overlaps = False
            for zone in safe_zones:
                if distractor_rect.colliderect(zone):
                    overlaps = True
                    break
            
            if not overlaps:
                break
        
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        self.alpha = random.randint(100, 200)

    def draw(self, screen):
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surface.fill((*self.color, self.alpha))
        screen.blit(surface, (self.x, self.y))


class ColorSoundGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("颜色听觉 - Color Sound")
        self.clock = pygame.time.Clock()
        
        self.font_large = self._load_font(FONT_SIZE_LARGE)
        self.font_medium = self._load_font(FONT_SIZE_MEDIUM)
        self.font_small = self._load_font(FONT_SIZE_SMALL)
        
        self.audio_synth = AudioSynth()
        
        self.red_slider = Slider(SLIDER_X, SLIDER_START_Y, SLIDER_WIDTH, SLIDER_HEIGHT, RED_SLIDER_COLOR, "R")
        self.green_slider = Slider(SLIDER_X, SLIDER_START_Y + SLIDER_GAP, SLIDER_WIDTH, SLIDER_HEIGHT, GREEN_SLIDER_COLOR, "G")
        self.blue_slider = Slider(SLIDER_X, SLIDER_START_Y + SLIDER_GAP * 2, SLIDER_WIDTH, SLIDER_HEIGHT, BLUE_SLIDER_COLOR, "B")
        
        self.target_color = self.generate_target_color()
        self.score = 0
        self.level = 1
        self.round_time = INITIAL_ROUND_TIME
        self.time_left = self.round_time
        self.last_time = pygame.time.get_ticks()
        self.game_state = "playing"
        self.distractors = []
        self.last_distractor_time = 0
        
        self.submit_button = pygame.Rect(SLIDER_X, SLIDER_START_Y + SLIDER_GAP * 3 + 20, SLIDER_WIDTH, 50)
        
        self.safe_zones = self._init_safe_zones()

    def _load_font(self, size):
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
        for path in font_paths:
            try:
                return pygame.font.Font(path, size)
            except:
                continue
        return pygame.font.Font(None, size)

    def _init_safe_zones(self):
        zones = []
        
        zones.append(pygame.Rect(0, 0, SCREEN_WIDTH, 130))
        zones.append(pygame.Rect(
            TARGET_COLOR_X - 20,
            TARGET_COLOR_Y - 50,
            TARGET_COLOR_SIZE + 40,
            TARGET_COLOR_SIZE + 80
        ))
        zones.append(pygame.Rect(
            CURRENT_COLOR_X - 20,
            CURRENT_COLOR_Y - 50,
            CURRENT_COLOR_SIZE + 40,
            CURRENT_COLOR_SIZE + 80
        ))
        zones.append(pygame.Rect(
            SLIDER_X - 20,
            SLIDER_START_Y - 50,
            SLIDER_WIDTH + 40,
            SLIDER_GAP * 4 + 120
        ))
        return zones

    def generate_target_color(self):
        return (
            random.randint(20, 235),
            random.randint(20, 235),
            random.randint(20, 235)
        )

    def calculate_similarity(self, c1, c2):
        return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)

    def calculate_score(self, diff):
        normalized = 1 - (diff / MAX_COLOR_DIFF)
        return int(BASE_SCORE * max(0, normalized) * self.level)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.game_state == "playing":
                self.red_slider.handle_event(event)
                self.green_slider.handle_event(event)
                self.blue_slider.handle_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.submit_button.collidepoint(event.pos):
                        self.submit_answer()
            elif self.game_state == "gameover":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
        
        return True

    def submit_answer(self):
        current_color = (self.red_slider.value, self.green_slider.value, self.blue_slider.value)
        diff = self.calculate_similarity(current_color, self.target_color)
        round_score = self.calculate_score(diff)
        self.score += round_score
        
        self.level += 1
        self.round_time = max(MIN_ROUND_TIME, INITIAL_ROUND_TIME - (self.level - 1) * TIME_DECREASE_PER_LEVEL)
        self.time_left = self.round_time
        
        self.target_color = self.generate_target_color()
        
        self.red_slider.value = 128
        self.green_slider.value = 128
        self.blue_slider.value = 128

    def update(self):
        if self.game_state != "playing":
            return
        
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_time) / 1000
        self.last_time = current_time
        
        self.time_left -= dt
        
        if self.time_left <= 0:
            self.game_state = "gameover"
            self.audio_synth.stop_all()
            return
        
        current_color = (self.red_slider.value, self.green_slider.value, self.blue_slider.value)
        self.audio_synth.update(*current_color)
        
        if self.level >= 3:
            if current_time - self.last_distractor_time > 2000:
                self.last_distractor_time = current_time
                if len(self.distractors) < min(MAX_DISTRACTORS, self.level - 1):
                    self.distractors.append(Distractor(self.safe_zones))
            
            self.distractors = [d for d in self.distractors if random.random() > 0.005]

    def draw(self):
        self.screen.fill(BLACK)
        
        if self.game_state == "playing":
            for distractor in self.distractors:
                distractor.draw(self.screen)
            
            title = self.font_large.render("颜色听觉", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
            
            score_text = self.font_medium.render(f"得分: {self.score}  关卡: {self.level}", True, WHITE)
            self.screen.blit(score_text, (20, 80))
            
            time_text = self.font_medium.render(f"时间: {self.time_left:.1f}s", True, (255, 100, 100))
            self.screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 80))
            
            target_label = self.font_medium.render("目标颜色", True, WHITE)
            self.screen.blit(target_label, (TARGET_COLOR_X, TARGET_COLOR_Y - 40))
            pygame.draw.rect(
                self.screen, self.target_color,
                (TARGET_COLOR_X, TARGET_COLOR_Y, TARGET_COLOR_SIZE, TARGET_COLOR_SIZE),
                border_radius=10
            )
            pygame.draw.rect(
                self.screen, WHITE,
                (TARGET_COLOR_X, TARGET_COLOR_Y, TARGET_COLOR_SIZE, TARGET_COLOR_SIZE),
                3, border_radius=10
            )
            
            target_rgb = self.font_small.render(f"RGB: {self.target_color}", True, WHITE)
            self.screen.blit(target_rgb, (TARGET_COLOR_X, TARGET_COLOR_Y + TARGET_COLOR_SIZE + 10))
            
            current_label = self.font_medium.render("你的颜色", True, WHITE)
            self.screen.blit(current_label, (CURRENT_COLOR_X, CURRENT_COLOR_Y - 40))
            current_color = (self.red_slider.value, self.green_slider.value, self.blue_slider.value)
            pygame.draw.rect(
                self.screen, current_color,
                (CURRENT_COLOR_X, CURRENT_COLOR_Y, CURRENT_COLOR_SIZE, CURRENT_COLOR_SIZE),
                border_radius=10
            )
            pygame.draw.rect(
                self.screen, WHITE,
                (CURRENT_COLOR_X, CURRENT_COLOR_Y, CURRENT_COLOR_SIZE, CURRENT_COLOR_SIZE),
                3, border_radius=10
            )
            
            current_rgb = self.font_small.render(f"RGB: {current_color}", True, WHITE)
            self.screen.blit(current_rgb, (CURRENT_COLOR_X, CURRENT_COLOR_Y + CURRENT_COLOR_SIZE + 10))
            
            self.red_slider.draw(self.screen, self.font_medium)
            self.green_slider.draw(self.screen, self.font_medium)
            self.blue_slider.draw(self.screen, self.font_medium)
            
            pygame.draw.rect(self.screen, (50, 150, 50), self.submit_button, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, self.submit_button, 2, border_radius=10)
            submit_text = self.font_medium.render("提交答案", True, WHITE)
            self.screen.blit(
                submit_text,
                (self.submit_button.x + self.submit_button.width // 2 - submit_text.get_width() // 2,
                 self.submit_button.y + self.submit_button.height // 2 - submit_text.get_height() // 2)
            )
            
            diff = self.calculate_similarity(current_color, self.target_color)
            similarity = max(0, 1 - diff / MAX_COLOR_DIFF) * 100
            sim_text = self.font_small.render(f"相似度: {similarity:.1f}%", True, WHITE)
            self.screen.blit(sim_text, (SLIDER_X, self.submit_button.y + self.submit_button.height + 15))
            
        elif self.game_state == "gameover":
            game_over_text = self.font_large.render("游戏结束!", True, (255, 100, 100))
            self.screen.blit(
                game_over_text,
                (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100)
            )
            
            final_score = self.font_medium.render(f"最终得分: {self.score}", True, WHITE)
            self.screen.blit(
                final_score,
                (SCREEN_WIDTH // 2 - final_score.get_width() // 2, SCREEN_HEIGHT // 2 - 30)
            )
            
            final_level = self.font_medium.render(f"到达关卡: {self.level}", True, WHITE)
            self.screen.blit(
                final_level,
                (SCREEN_WIDTH // 2 - final_level.get_width() // 2, SCREEN_HEIGHT // 2 + 20)
            )
            
            restart_text = self.font_small.render("按 R 键重新开始", True, LIGHT_GRAY)
            self.screen.blit(
                restart_text,
                (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80)
            )
        
        pygame.display.flip()

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.round_time = INITIAL_ROUND_TIME
        self.time_left = self.round_time
        self.target_color = self.generate_target_color()
        self.red_slider.value = 128
        self.green_slider.value = 128
        self.blue_slider.value = 128
        self.game_state = "playing"
        self.distractors = []
        self.last_time = pygame.time.get_ticks()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        self.audio_synth.stop_all()
        pygame.quit()
