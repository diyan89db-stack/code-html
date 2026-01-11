import pygame
import sys
import random

pygame.init()

# ======================
# CONFIG
# ======================
TILE = 40
FPS = 60
PAC_SPEED = 10
GHOST_SPEED = 5

# ======================
# MAP
# ======================
LEVEL = [
"1111111111111111111111111111111",
"1000000000000110000000000000001",
"1011110111110110111110111111101",
"1011110111110110111110111111101",
"1000000000000000000000000000001",
"1011110110111111110110111111101",
"1000000110000110000110000000001",
"1111110111110110111110111111111",
"0000010100000000000000101000000",
"1111010110111111110110101111101",
"0000010100000000000000101000000",
"1111010110111111110110101111101",
"1000000000110000000110000000001",
"1011110111110110111110111111101",
"1000000000000110000000000000001",
"1111111111111111111111111111111",
]

ROWS = len(LEVEL)
COLS = len(LEVEL[0])
WIDTH = COLS * TILE
HEIGHT = ROWS * TILE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Classic (Restart)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# ======================
# COLORS
# ======================
BLACK = (0,0,0)
BLUE = (0,0,200)
YELLOW = (255,255,0)
WHITE = (240,240,240)
GHOST_COLORS = [(255,0,0),(255,105,180),(0,255,255),(255,165,0)]

# ======================
# FUNCTIONS
# ======================
def build_level():
    walls = []
    pellets = []
    for y, row in enumerate(LEVEL):
        for x, tile in enumerate(row):
            if tile == "1":
                walls.append(pygame.Rect(x*TILE, y*TILE, TILE, TILE))
            else:
                pellets.append(
                    pygame.Rect(
                        x*TILE + TILE//2 - 3,
                        y*TILE + TILE//2 - 3,
                        6, 6
                    )
                )
    return walls, pellets

def can_move(rect, dx, dy):
    test = rect.move(dx, dy)
    return not any(test.colliderect(w) for w in walls)

def move(rect, direction, speed):
    if can_move(rect, direction.x * speed, 0):
        rect.x += direction.x * speed
    if can_move(rect, 0, direction.y * speed):
        rect.y += direction.y * speed

def at_center(rect):
    return rect.x % TILE == 0 and rect.y % TILE == 0

def possible_dirs(rect):
    dirs = []
    for d in [pygame.Vector2(1,0), pygame.Vector2(-1,0),
              pygame.Vector2(0,1), pygame.Vector2(0,-1)]:
        if can_move(rect, d.x*GHOST_SPEED, d.y*GHOST_SPEED):
            dirs.append(d)
    return dirs

def ghost_ai(ghost):
    rect = ghost["rect"]
    current = ghost["dir"]

    if not at_center(rect):
        return current

    choices = possible_dirs(rect)
    back = -current
    if len(choices) > 1 and back in choices:
        choices.remove(back)

    best = current
    min_dist = 999999

    for d in choices:
        test = rect.move(d.x*TILE, d.y*TILE)
        dist = abs(test.centerx - pacman.centerx) + abs(test.centery - pacman.centery)
        if dist < min_dist:
            min_dist = dist
            best = d

    return best

def reset_game():
    global pacman, pac_dir, ghosts, walls, pellets, game_over, win

    walls, pellets = build_level()

    pacman = pygame.Rect(1*TILE, 1*TILE, TILE, TILE)
    pac_dir.update(0,0)

    ghosts.clear()
    start_pos = [(15,8),(16,8),(15,9),(16,9)]
    for i in range(4):
        ghosts.append({
            "rect": pygame.Rect(start_pos[i][0]*TILE,
                                start_pos[i][1]*TILE,
                                TILE, TILE),
            "dir": random.choice([
                pygame.Vector2(1,0),
                pygame.Vector2(-1,0),
                pygame.Vector2(0,1),
                pygame.Vector2(0,-1)
            ]),
            "color": GHOST_COLORS[i]
        })

    game_over = False
    win = False

# ======================
# INIT GAME
# ======================
walls, pellets = build_level()
pacman = pygame.Rect(1*TILE, 1*TILE, TILE, TILE)
pac_dir = pygame.Vector2(0,0)
ghosts = []

game_over = False
win = False
reset_game()

# ======================
# GAME LOOP
# ======================
while True:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or win):
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over and not win:
        pac_dir.update(0,0)
        if keys[pygame.K_w]: pac_dir.y = -1
        elif keys[pygame.K_s]: pac_dir.y = 1
        elif keys[pygame.K_a]: pac_dir.x = -1
        elif keys[pygame.K_d]: pac_dir.x = 1

        move(pacman, pac_dir, PAC_SPEED)

        if pacman.x < -TILE: pacman.x = WIDTH
        if pacman.x > WIDTH: pacman.x = -TILE

        for g in ghosts:
            g["dir"] = ghost_ai(g)
            move(g["rect"], g["dir"], GHOST_SPEED)
            if pacman.colliderect(g["rect"]):
                game_over = True

    for p in pellets[:]:
        if pacman.colliderect(p):
            pellets.remove(p)

    if not pellets:
        win = True

    # DRAW
    for w in walls:
        pygame.draw.rect(screen, BLUE, w)

    for p in pellets:
        pygame.draw.circle(screen, WHITE, p.center, 3)

    pygame.draw.circle(screen, YELLOW, pacman.center, TILE//2)

    for g in ghosts:
        pygame.draw.circle(screen, g["color"], g["rect"].center, TILE//2)

    if game_over:
        t1 = font.render("GAME OVER", True, WHITE)
        t2 = font.render("Press R to Restart", True, WHITE)
        screen.blit(t1, (WIDTH//2 - 90, HEIGHT//2 - 20))
        screen.blit(t2, (WIDTH//2 - 120, HEIGHT//2 + 15))

    if win:
        t1 = font.render("YOU WIN!", True, WHITE)
        t2 = font.render("Press R to Play Again", True, WHITE)
        screen.blit(t1, (WIDTH//2 - 80, HEIGHT//2 - 20))
        screen.blit(t2, (WIDTH//2 - 130, HEIGHT//2 + 15))

    pygame.display.flip()
