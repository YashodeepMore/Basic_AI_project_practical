import pygame
import sys
import math

# Initialize pygame
pygame.init()
WIDTH = 600
ROWS = 3
CELL = WIDTH // ROWS
LINE_WIDTH = 10
CIRCLE_RADIUS = CELL//3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = CELL//4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

# Create window
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Tic-Tac-Toe with Alpha-Beta AI")
screen.fill(BG_COLOR)

# Initialize board
board = [[" " for _ in range(ROWS)] for _ in range(ROWS)]

# Draw grid lines
def draw_lines():
    for i in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, CELL * i), (WIDTH, CELL * i), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (CELL * i, 0), (CELL * i, WIDTH), LINE_WIDTH)

def draw_figures():
    for row in range(ROWS):
        for col in range(ROWS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * CELL + SPACE, row * CELL + CELL - SPACE),
                                 (col * CELL + CELL - SPACE, row * CELL + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * CELL + SPACE, row * CELL + SPACE),
                                 (col * CELL + CELL - SPACE, row * CELL + CELL - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (col * CELL + CELL//2, row * CELL + CELL//2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_winner():
    for row in range(ROWS):
        if board[row][0] == board[row][1] == board[row][2] != " ":
            return board[row][0]
    for col in range(ROWS):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def is_moves_left():
    return any(" " in row for row in board)

def minimax(is_maximizing, alpha, beta):
    winner = check_winner()
    if winner == "O": return 1
    if winner == "X": return -1
    if not is_moves_left(): return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    eval = minimax(False, alpha, beta)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        return max_eval
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    eval = minimax(True, alpha, beta)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        return min_eval
        return min_eval

def find_best_move():
    best_val = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                move_val = minimax(False, -math.inf, math.inf)
                board[i][j] = " "
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    return best_move

# Game variables
player_turn = True
game_over = False
draw_lines()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over and player_turn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // CELL
                col = x // CELL
                if board[row][col] == " ":
                    board[row][col] = "X"
                    player_turn = False

        if not game_over and not player_turn:
            pygame.time.delay(500)
            move = find_best_move()
            if move:
                board[move[0]][move[1]] = "O"
            player_turn = True

        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        pygame.display.update()

        winner = check_winner()
        if winner:
            print(f"{winner} wins!")
            pygame.time.wait(2000)
            game_over = True
        elif not is_moves_left():
            print("Draw!")
            pygame.time.wait(2000)
            game_over = True
