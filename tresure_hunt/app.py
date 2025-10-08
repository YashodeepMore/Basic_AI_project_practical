import pygame, sys, math, random

pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunt Path Optimizer")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

treasures = []
path = []

FONT = pygame.font.SysFont("comicsans", 25)

def draw():
    SCREEN.fill(WHITE)
    # Draw treasures
    for x, y in treasures:
        pygame.draw.circle(SCREEN, RED, (x, y), 10)
    # Draw path
    for i in range(len(path)-1):
        pygame.draw.line(SCREEN, GREEN, path[i], path[i+1], 3)
    pygame.display.update()

def distance(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def greedy_path(start):
    remaining = treasures.copy()
    current = start
    result = [current]
    total_dist = 0
    while remaining:
        # Find nearest treasure
        nearest = min(remaining, key=lambda t: distance(current, t))
        total_dist += distance(current, nearest)
        current = nearest
        result.append(current)
        remaining.remove(current)
        draw()
        pygame.time.delay(500)
    print("Total distance traveled:", int(total_dist))
    return result

running = True
while running:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y < HEIGHT:
                treasures.append((x, y))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and treasures:
                start = treasures[0]  # Start from first treasure
                path = greedy_path(start)
