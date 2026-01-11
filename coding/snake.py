import pygame
import random
import sys

pygame.init()

# ======================
# SETUP
# ======================
WIDTH, HEIGHT = 1000, 600
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Grid Game - pygame-ce")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# ======================
# COLORS
# ======================
BG = (18, 18, 18)
GRID = (40, 40, 40)
SNAKE = (0, 200, 0)
FOOD = (220, 50, 50)
TEXT = (255, 255, 255)

# ======================
# FUNCTIONS
# ======================
def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

def random_food():
    return (
        random.randint(0, COLS - 1) * CELL,
        random.randint(0, ROWS - 1) * CELL
    )

def reset_game():
    global snake, direction, food, score
    snake = [(300, 300), (280, 300), (260, 300)]
    direction = (CELL, 0)
    food = random_food()
    score = 0

# ======================
# INIT
# ======================
reset_game()

# ======================
# GAME LOOP
# ======================
while True:
    clock.tick(10)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != (0, CELL):
                direction = (0, -CELL)
            if event.key == pygame.K_s and direction != (0, -CELL):
                direction = (0, CELL)
            if event.key == pygame.K_a and direction != (CELL, 0):
                direction = (-CELL, 0)
            if event.key == pygame.K_d and direction != (-CELL, 0):
                direction = (CELL, 0)

    # ======================
    # MOVE SNAKE
    # ======================
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # TELEPORT MAP
    new_head = (
        new_head[0] % WIDTH,
        new_head[1] % HEIGHT
    )

    # COLLISION SELF
    if new_head in snake:
        reset_game()
        continue

    snake.insert(0, new_head)

    # EAT FOOD
    if new_head == food:
        score += 1
        food = random_food()
    else:
        snake.pop()

    # ======================
    # DRAW
    # ======================
    draw_grid()

    pygame.draw.rect(screen, FOOD, (*food, CELL, CELL))

    for part in snake:
        pygame.draw.rect(screen, SNAKE, (*part, CELL, CELL))

    score_text = font.render(f"Score: {score}", True, TEXT)
    screen.blit(score_text, (5, 5))

    pygame.display.flip()

