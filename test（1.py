import pygame
import random
import sys
from pygame.locals import *

# 初始化
pygame.init()

# 游戏常量
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30
TILE_SIZE = 64
GRID_WIDTH, GRID_HEIGHT = WINDOW_WIDTH // TILE_SIZE, WINDOW_HEIGHT // TILE_SIZE
TILE_TYPES = 5
TIME_LIMIT = 60  # seconds
LAYERS = 3  # 定义图层数量

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 设置窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("消除游戏")

# 加载图像
tiles = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f'd:\\study\\软件工程\\第二次个人作业\\pattern\\pattern_{i}.png').convert_alpha()  # 确保图像文件在当前工作目录
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tiles.append(img)

# 加载字体
font_path = 'simhei.ttf'  # 确保字体文件在当前工作目录
try:
    font = pygame.font.Font(font_path, 36)
except IOError as e:
    print(f"Error loading font: {e}")
    font = pygame.font.SysFont(None, 36)  # 回退到系统默认字体

# 游戏类
class Game:
    def __init__(self):
        self.layers = [[random.randint(0, TILE_TYPES - 1) for _ in range(GRID_WIDTH * GRID_HEIGHT)] for _ in range(LAYERS)]
        self.selected = []
        self.score = 0
        self.time_left = TIME_LIMIT
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.combos = 0  # 连续消除次数

    def check_match(self):
        if len(self.selected) == 2:
            x1, y1 = self.selected[0]
            x2, y2 = self.selected[1]
            for layer in self.layers:
                if y1 * GRID_WIDTH + x1 < len(layer) and y2 * GRID_WIDTH + x2 < len(layer):
                    if layer[y1 * GRID_WIDTH + x1] == layer[y2 * GRID_WIDTH + x2] and layer[y1 * GRID_WIDTH + x1] != -1:
                        layer[y1 * GRID_WIDTH + x1] = layer[y2 * GRID_WIDTH + x2] = -1
                        self.selected = []
                        self.score += 10  # 基本消除得分
                        self.combos += 1  # 增加连续消除次数
                        print(f"Match found and removed at ({x1}, {y1}) and ({x2}, {y2})")
                        return True
        self.combos = 0  # 重置连续消除次数
        return False

    def draw_grid(self):
        for layer_index, layer in enumerate(self.layers):
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    tile_type = layer[y * GRID_WIDTH + x]
                    if layer_index == 0 or self.is_visible(x, y, layer_index):
                        window.blit(tiles[tile_type], (x * TILE_SIZE, y * TILE_SIZE))

    def is_visible(self, x, y, layer_index):
        # 检查指定位置的图案是否可见
        for i in range(layer_index):
            if self.layers[i][y * GRID_WIDTH + x] != -1:
                return False
        return True

    def draw_timer(self):
        timer_text = font.render(f"Time Left: {self.time_left:.1f}", True, WHITE)
        window.blit(timer_text, (10, 10))

    def draw_score(self):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        window.blit(score_text, (WINDOW_WIDTH - 150, 10))

    def draw_start_screen(self):
        window.fill(BLACK)
        title_text = font.render("消除游戏", True, WHITE)
        start_text = font.render("点击任意键开始", True, WHITE)
        title_text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        start_text_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        window.blit(title_text, title_text_rect)
        window.blit(start_text, start_text_rect)
        pygame.display.flip()

    def draw_end_screen(self):
        window.fill(BLACK)
        end_text = font.render("游戏结束!", True, RED)
        time_text = font.render(f"剩余时间: {self.time_left:.1f}", True, WHITE)
        score_text = font.render(f"得分: {self.score}", True, WHITE)
        end_text_rect = end_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        time_text_rect = time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        window.blit(end_text, end_text_rect)
        window.blit(time_text, time_text_rect)
        window.blit(score_text, score_text_rect)
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if self.state == 'start':
                        self.state = 'playing'
                    elif self.state == 'playing':
                        x, y = event.pos
                        x //= TILE_SIZE
                        y //= TILE_SIZE
                        if (x, y) in self.selected:
                            self.selected.remove((x, y))
                        else:
                            if len(self.selected) < 2:
                                self.selected.append((x, y))
                                if len(self.selected) == 2:
                                    if self.check_match():
                                        self.score += 5 if self.combos > 0 else 0  # 连续消除奖励
                                    else:
                                        self.selected.pop()

            window.fill(BLACK)
            if self.state == 'start':
                self.draw_start_screen()
            elif self.state == 'playing':
                self.draw_grid()
                self.draw_timer()
                self.draw_score()
                pygame.display.flip()
                self.time_left -= self.clock.get_time() / 1000
                if self.time_left <= 0:
                    self.state = 'end'
            elif self.state == 'end':
                self.draw_end_screen()

            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()