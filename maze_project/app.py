import pygame
import random
from collections import deque

# Grid and display setup
WIDTH = 600
ROWS = 20
CELL = WIDTH // ROWS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze Solver using DFS & BFS")

# Create grid
grid = [[0 for _ in range(ROWS)] for _ in range(ROWS)]

# Random walls
for i in range(ROWS):
    for j in range(ROWS):
        if random.random() < 0.3:
            grid[i][j] = 1  # wall

start = (0, 0)
end = (ROWS-1, ROWS-1)
grid[start[0]][start[1]] = 0
grid[end[0]][end[1]] = 0

def draw_grid():
    for i in range(ROWS):
        for j in range(ROWS):
            color = WHITE if grid[i][j] == 0 else BLACK
            pygame.draw.rect(win, color, (j*CELL, i*CELL, CELL, CELL))
    pygame.display.update()

# def bfs(start, end):
#     queue = deque([start])
#     visited = {start: None}
#     while queue:
#         current = queue.popleft()
#         if current == end:
#             break
#         r, c = current
#         for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
#             nr, nc = r+dr, c+dc
#             if 0 <= nr < ROWS and 0 <= nc < ROWS and grid[nr][nc] == 0:
#                 if (nr, nc) not in visited:
#                     visited[(nr, nc)] = current
#                     queue.append((nr, nc))
#         pygame.draw.rect(win, BLUE, (c*CELL, r*CELL, CELL, CELL))
#         pygame.display.update()
#     return visited
def bfs(start, end):
    queue = deque([start])
    visited = {start: None}
    while queue:
        current = queue.popleft()
        if current == end:
            break
        r, c = current
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < ROWS and grid[nr][nc] == 0:
                if (nr, nc) not in visited:
                    visited[(nr, nc)] = current
                    queue.append((nr, nc))
        pygame.draw.rect(win, BLUE, (c*CELL, r*CELL, CELL, CELL))
        pygame.display.update()
        pygame.time.delay(50)  # delay 50 milliseconds for slow animation
    return visited


draw_grid()
visited = bfs(start, end)

# reconstruct path
if end in visited:
    node = end
    while node:
        r, c = node
        pygame.draw.rect(win, GREEN, (c*CELL, r*CELL, CELL, CELL))
        pygame.display.update()
        node = visited[node]

# Keep window open until user closes it
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

