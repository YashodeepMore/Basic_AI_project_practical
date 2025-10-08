import pygame
import sys
import time
import copy

pygame.init()

# -----------------------------
# Display settings
# -----------------------------
WIDTH, HEIGHT = 540, 600
CELL = WIDTH // 9
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Sudoku Solver")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
GRAY = (200, 200, 200)

# Fonts
FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 25)

# -----------------------------
# Example Sudoku puzzle (0 = empty)
# -----------------------------
puzzle = [
    [5, 1, 7, 6, 0, 0, 0, 3, 4],
    [2, 8, 9, 0, 0, 4, 0, 0, 0],
    [3, 4, 6, 2, 0, 5, 0, 9, 0],
    [6, 0, 2, 0, 0, 0, 0, 1, 0],
    [0, 3, 8, 0, 0, 6, 0, 4, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 7, 8],
    [7, 0, 3, 4, 0, 0, 5, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

board = copy.deepcopy(puzzle)
selected_cell = None

# -----------------------------
# Utility functions
# -----------------------------
def draw_grid():
    SCREEN.fill(WHITE)
    for i in range(10):
        width = 4 if i % 3 == 0 else 1
        pygame.draw.line(SCREEN, BLACK, (0, i*CELL), (WIDTH, i*CELL), width)
        pygame.draw.line(SCREEN, BLACK, (i*CELL, 0), (i*CELL, WIDTH), width)

def draw_numbers():
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                color = BLUE if puzzle[i][j] == 0 else BLACK
                text = FONT.render(str(board[i][j]), True, color)
                SCREEN.blit(text, (j*CELL + 15, i*CELL + 10))

def select_cell(pos):
    global selected_cell
    x, y = pos
    row = y // CELL
    col = x // CELL
    selected_cell = (row, col)

def is_valid(board, row, col, num):
    if num in board[row]: return False
    if num in [board[i][col] for i in range(9)]: return False
    start_row, start_col = 3*(row//3), 3*(col//3)
    for i in range(3):
        for j in range(3):
            if board[start_row+i][start_col+j] == num:
                return False
    return True

def draw_buttons():
    pygame.draw.rect(SCREEN, GREEN, (50, WIDTH + 10, 150, 40))
    pygame.draw.rect(SCREEN, RED, (WIDTH - 200, WIDTH + 10, 150, 40))
    SCREEN.blit(SMALL_FONT.render("Backtracking", True, WHITE), (60, WIDTH+15))
    SCREEN.blit(SMALL_FONT.render("Branch & Bound", True, WHITE), (WIDTH-190, WIDTH+15))

# -----------------------------
# Solvers with visualization
# -----------------------------
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def solve_backtracking_vis(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1,10):
        if is_valid(board,row,col,num):
            board[row][col] = num
            draw_grid()
            draw_numbers()
            pygame.display.update()
            pygame.time.delay(30)
            if solve_backtracking_vis(board):
                return True
            board[row][col] = 0
            draw_grid()
            draw_numbers()
            pygame.display.update()
            pygame.time.delay(30)
    return False

def solve_branch_bound_vis(board):
    empty_cells = [(i,j) for i in range(9) for j in range(9) if board[i][j]==0]
    if not empty_cells:
        return True

    # select cell with fewest candidates
    min_candidates = 10
    for i,j in empty_cells:
        candidates = [num for num in range(1,10) if is_valid(board,i,j,num)]
        if len(candidates) < min_candidates:
            min_candidates = len(candidates)
            best_cell = (i,j)
            best_candidates = candidates

    if min_candidates == 0:
        return False

    row,col = best_cell
    for num in best_candidates:
        board[row][col] = num
        draw_grid()
        draw_numbers()
        pygame.display.update()
        pygame.time.delay(5)
        if solve_branch_bound_vis(board):
            return True
        board[row][col] = 0
        draw_grid()
        draw_numbers()
        pygame.display.update()
        pygame.time.delay(5)
    return False

# -----------------------------
# Main loop
# -----------------------------
running = True
while running:
    draw_grid()
    draw_numbers()
    draw_buttons()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y < WIDTH:
                select_cell((x,y))
            elif 50 <= x <= 200 and WIDTH+10 <= y <= WIDTH+50:
                # Backtracking solve
                board = copy.deepcopy(puzzle)
                start = time.time()
                solve_backtracking_vis(board)
                print("Backtracking solved in:", round(time.time()-start,2),"s")
            elif WIDTH-200 <= x <= WIDTH-50 and WIDTH+10 <= y <= WIDTH+50:
                # Branch & Bound solve
                board = copy.deepcopy(puzzle)
                start = time.time()
                solve_branch_bound_vis(board)
                print("Branch & Bound solved in:", round(time.time()-start,2),"s")
        if event.type == pygame.KEYDOWN and selected_cell:
            row, col = selected_cell
            if event.key == pygame.K_1: board[row][col]=1
            if event.key == pygame.K_2: board[row][col]=2
            if event.key == pygame.K_3: board[row][col]=3
            if event.key == pygame.K_4: board[row][col]=4
            if event.key == pygame.K_5: board[row][col]=5
            if event.key == pygame.K_6: board[row][col]=6
            if event.key == pygame.K_7: board[row][col]=7
            if event.key == pygame.K_8: board[row][col]=8
            if event.key == pygame.K_9: board[row][col]=9
            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                board[row][col]=0
