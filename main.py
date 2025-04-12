import pygame
import time
from collections import deque

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the screen size
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Path Visualization')

# Font for displaying text
font = pygame.font.SysFont('arial', 20)

def draw_grid(n):
    """Draw the grid and label each cell with coordinates."""
    cell_size = screen_width // n
    for x in range(n):
        for y in range(n):
            pygame.draw.rect(screen, WHITE, (x * cell_size, y * cell_size, cell_size, cell_size), 1)
            text = font.render(f"({x},{y})", True, BLACK)
            screen.blit(text, (x * cell_size + 5, y * cell_size + 5))

def draw_path(path, n):
    """Draw the path step by step."""
    cell_size = screen_width // n
    for i in range(len(path)):
        x, y = path[i]
        pygame.draw.rect(screen, GREEN, (x * cell_size, y * cell_size, cell_size, cell_size))
        pygame.display.update()
        time.sleep(0.5)  # Delay between steps to show the path

def find_paths(n):
    """Find all possible paths from the top-left to the bottom-right corner."""
    dp = [[0] * n for _ in range(n)]
    dp[0][0] = 1  # Start point

    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            if i > 0:
                dp[i][j] += dp[i - 1][j]
            if j > 0:
                dp[i][j] += dp[i][j - 1]

    # Collect all paths using backtracking
    paths = []
    find_all_paths(paths, [], n - 1, n - 1, dp)
    return paths

def find_all_paths(paths, current_path, i, j, dp):
    """Backtracking to find all the paths."""
    if i == 0 and j == 0:
        current_path.append((i, j))
        paths.append(list(current_path))
        current_path.pop()
        return

    if i > 0 and dp[i - 1][j] > 0:
        current_path.append((i, j))
        find_all_paths(paths, current_path, i - 1, j, dp)
        current_path.pop()

    if j > 0 and dp[i][j - 1] > 0:
        current_path.append((i, j))
        find_all_paths(paths, current_path, i, j - 1, dp)
        current_path.pop()

def main():
    """Main program that runs the visualization."""
    running = True
    n = int(input("Please enter the grid size: "))
    
    while running:
        screen.fill(BLACK)
        draw_grid(n)

        # Find all possible paths
        paths = find_paths(n)
        
        # Draw each path step by step
        for path in paths:
            draw_path(path, n)
        
        pygame.display.update()

        # Wait for the user to input a new grid size
        running = False
        while not running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        running = True
                        n = int(input("Please enter a new grid size: "))
                        break

# Run the program
if __name__ == "__main__":
    main()
