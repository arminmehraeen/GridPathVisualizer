import pygame
import time

pygame.init()

# رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
LIGHT_BLUE = (40, 50, 70)
GREEN = (80, 220, 180)
RED = (255, 120, 120)
PATH_COLOR = (255, 190, 60)
BUTTON_COLOR = (60, 140, 255)
TEXT_COLOR = (240, 240, 240)

# صفحه
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("All Paths Visualizer")

# فونت
font = pygame.font.SysFont("Segoe UI", 22)
big_font = pygame.font.SysFont("Segoe UI", 28, bold=True)

# شروع
start = (0, 0)
grid_size = 5  # پیش‌فرض

def draw_grid():
    cell_size = WIDTH // grid_size
    for x in range(grid_size):
        for y in range(grid_size):
            rect = pygame.Rect(x * cell_size + 1, y * cell_size + 1, cell_size - 2, cell_size - 2)
            pygame.draw.rect(screen, GRAY, rect, border_radius=4)

def draw_points(end):
    cell_size = WIDTH // grid_size
    pygame.draw.rect(screen, GREEN, (start[0]*cell_size+2, start[1]*cell_size+2, cell_size-4, cell_size-4), border_radius=4)
    pygame.draw.rect(screen, RED, (end[0]*cell_size+2, end[1]*cell_size+2, cell_size-4, cell_size-4), border_radius=4)

def draw_path(path):
    cell_size = WIDTH // grid_size
    for (x, y) in path:
        pygame.draw.rect(screen, PATH_COLOR, (x*cell_size+2, y*cell_size+2, cell_size-4, cell_size-4), border_radius=4)
        pygame.display.update()
        pygame.time.delay(80)

def reset_board(end):
    screen.fill(LIGHT_BLUE)
    draw_grid()
    draw_points(end)
    pygame.display.update()

def get_neighbors_right_down(x, y, size):
    neighbors = []
    if x + 1 < size:
        neighbors.append((x + 1, y))
    if y + 1 < size:
        neighbors.append((x, y + 1))
    return neighbors

def find_all_paths(start, end, size):
    paths = []

    def dfs(current, path):
        if current == end:
            paths.append(path.copy())
            return
        for neighbor in get_neighbors_right_down(*current, size):
            if neighbor not in path:
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()

    dfs(start, [start])
    return paths

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))

def draw_text(text, x, y, color=TEXT_COLOR, center=True, big=False):
    f = big_font if big else font
    label = f.render(text, True, color)
    if center:
        screen.blit(label, (x - label.get_width() // 2, y))
    else:
        screen.blit(label, (x, y))

def choose_grid_size():
    choosing = True
    selected_size = None

    while choosing:
        screen.fill(LIGHT_BLUE)
        draw_text("Choose Grid Size", WIDTH // 2, 50, big=True)

        for i in range(3, 11):
            x = 60 + ((i - 3) % 4) * 130
            y = 150 + ((i - 3) // 4) * 100
            draw_button(f"{i} x {i}", x, y, 100, 60, BUTTON_COLOR)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i in range(3, 11):
                    x = 60 + ((i - 3) % 4) * 130
                    y = 150 + ((i - 3) // 4) * 100
                    if x <= mx <= x + 100 and y <= my <= y + 60:
                        selected_size = i
                        choosing = False
                        break
    return selected_size

def main():
    global grid_size

    grid_size = choose_grid_size()
    cell_size = WIDTH // grid_size
    end = (grid_size - 1, grid_size - 1)

    running = True
    show_paths = False
    total_paths = 0

    while running:
        screen.fill(LIGHT_BLUE)
        draw_grid()
        draw_points(end)
        draw_button("Show All Paths", 200, 620, 200, 50, BUTTON_COLOR)

        if total_paths:
            draw_text(f"Total Paths: {total_paths}", WIDTH // 2, 580, color=(200, 255, 200), big=False)

        pygame.display.update()

        if show_paths:
            paths = find_all_paths(start, end, grid_size)
            total_paths = len(paths)
            for path in paths:
                reset_board(end)
                draw_path(path)
                time.sleep(0.3)
            show_paths = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 200 <= mx <= 400 and 620 <= my <= 670:
                    show_paths = True

    pygame.quit()

if __name__ == "__main__":
    main()
