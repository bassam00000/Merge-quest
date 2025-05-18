import pygame
import random
import sys

# إعداد Pygame
pygame.init()
WIDTH, HEIGHT = 500, 600
ROWS, COLS = 5, 5
CELL_SIZE = 80
PADDING = 10
TOP_OFFSET = 100
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Merge Quest")

FONT = pygame.font.SysFont("Arial", 24)
BIG_FONT = pygame.font.SysFont("Arial", 32, bold=True)

# الألوان والعناصر
COLORS = [(200, 200, 200), (100, 200, 100), (100, 100, 200), (200, 100, 100), (255, 215, 0)]
ELEMENTS = [1, 2, 3, 4, 5]

# الشبكة
grid = [[random.choice(ELEMENTS[:3]) for _ in range(COLS)] for _ in range(ROWS)]
score = 0
goal_score = 100

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            val = grid[row][col]
            color = COLORS[val-1] if val else (50, 50, 50)
            pygame.draw.rect(SCREEN, color, (col*CELL_SIZE + PADDING, row*CELL_SIZE + TOP_OFFSET, CELL_SIZE - PADDING, CELL_SIZE - PADDING))
            if val:
                txt = FONT.render(str(val), True, (0, 0, 0))
                SCREEN.blit(txt, (col*CELL_SIZE + 30, row*CELL_SIZE + TOP_OFFSET + 25))

def get_clicked_cell(pos):
    x, y = pos
    if y < TOP_OFFSET:
        return None
    col = x // CELL_SIZE
    row = (y - TOP_OFFSET) // CELL_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None

def merge_neighbors():
    global score
    merged = False
    for row in range(ROWS):
        for col in range(COLS):
            val = grid[row][col]
            if val == 0:
                continue
            neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
            match = [(r, c) for r, c in neighbors if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] == val]
            if len(match) >= 2:
                grid[row][col] = min(val + 1, len(ELEMENTS))
                for r, c in match:
                    grid[r][c] = 0
                score += 10 * val
                merged = True
    return merged

def refill_grid():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 0:
                grid[row][col] = random.choice(ELEMENTS[:3])

def draw_ui():
    title = BIG_FONT.render("Merge Quest", True, (0, 0, 0))
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    scr_txt = FONT.render(f"Score: {score} / {goal_score}", True, (0, 0, 0))
    SCREEN.blit(scr_txt, (20, HEIGHT - 40))

# اللعبة الرئيسية
clock = pygame.time.Clock()
running = True
selected = None

while running:
    SCREEN.fill((240, 240, 240))
    draw_grid()
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cell = get_clicked_cell(pygame.mouse.get_pos())
            if cell:
                if not selected:
                    selected = cell
                else:
                    r1, c1 = selected
                    r2, c2 = cell
                    # تبديل عنصرين متجاورين فقط
                    if abs(r1 - r2) + abs(c1 - c2) == 1:
                        grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
                        if not merge_neighbors():
                            # التراجع إذا لم يحدث دمج
                            grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]
                        else:
                            refill_grid()
                    selected = None

    if score >= goal_score:
        win_text = BIG_FONT.render("You Win!", True, (0, 128, 0))
        SCREEN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
