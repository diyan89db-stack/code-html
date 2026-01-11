import pygame
import random
import math

# ================== INIT ==================
pygame.init()
WIDTH, HEIGHT = 960, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 20)

TILE = 32
MAP_W, MAP_H = 40, 40

# ================== COLORS ==================
DARK = (10, 10, 14)
GRAY = (70, 70, 80)
WHITE = (220, 220, 220)
RED = (220, 60, 60)
GREEN = (60, 220, 120)
BLUE = (80, 160, 255)
YELLOW = (255, 210, 80)

# ================== MAP ==================
def gen_map():
    m = [[1 for _ in range(MAP_W)] for _ in range(MAP_H)]
    x, y = MAP_W // 2, MAP_H // 2
    for _ in range(1500):
        m[y][x] = 0
        dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        x = max(1, min(MAP_W-2, x+dx))
        y = max(1, min(MAP_H-2, y+dy))
    return m

world = gen_map()

# ================== PLAYER ==================
player = {
    "x": MAP_W//2,
    "y": MAP_H//2,
    "hp": 100,
    "max_hp": 100,
    "energy": 100,
    "score": 0
}

# ================== ENEMIES ==================
enemies = []
for _ in range(20):
    while True:
        ex, ey = random.randint(1, MAP_W-2), random.randint(1, MAP_H-2)
        if world[ey][ex] == 0:
            enemies.append({"x": ex, "y": ey, "hp": 30})
            break

# ================== ITEMS ==================
items = []
for _ in range(25):
    while True:
        ix, iy = random.randint(1, MAP_W-2), random.randint(1, MAP_H-2)
        if world[iy][ix] == 0:
            items.append({"x": ix, "y": iy, "type": random.choice(["hp","energy","score"])})
            break

# ================== HELPERS ==================
def draw_text(text, x, y, color=WHITE):
    screen.blit(FONT.render(text, True, color), (x, y))

def reset():
    global world, enemies, items, player
    world = gen_map()
    player.update({"x": MAP_W//2, "y": MAP_H//2, "hp": 100, "energy": 100, "score": 0})
    enemies.clear()
    items.clear()
    for _ in range(20):
        while True:
            ex, ey = random.randint(1, MAP_W-2), random.randint(1, MAP_H-2)
            if world[ey][ex] == 0:
                enemies.append({"x": ex, "y": ey, "hp": 30})
                break
    for _ in range(25):
        while True:
            ix, iy = random.randint(1, MAP_W-2), random.randint(1, MAP_H-2)
            if world[iy][ix] == 0:
                items.append({"x": ix, "y": iy, "type": random.choice(["hp","energy","score"])})
                break

# ================== GAME LOOP ==================
running = True
while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
            if e.key == pygame.K_r:
                reset()

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = 1

    if player["energy"] > 0:
        nx, ny = player["x"] + dx, player["y"] + dy
        if 0 <= nx < MAP_W and 0 <= ny < MAP_H and world[ny][nx] == 0:
            player["x"], player["y"] = nx, ny
            if dx or dy:
                player["energy"] -= 0.2

    # Enemy AI
    for en in enemies[:]:
        dist = abs(en["x"] - player["x"]) + abs(en["y"] - player["y"])
        if dist < 8:
            mx = 1 if player["x"] > en["x"] else -1 if player["x"] < en["x"] else 0
            my = 1 if player["y"] > en["y"] else -1 if player["y"] < en["y"] else 0
            if world[en["y"]][en["x"]+mx] == 0:
                en["x"] += mx
            if world[en["y"]+my][en["x"]] == 0:
                en["y"] += my
        if en["x"] == player["x"] and en["y"] == player["y"]:
            player["hp"] -= 0.5

    # Item pickup
    for it in items[:]:
        if it["x"] == player["x"] and it["y"] == player["y"]:
            if it["type"] == "hp":
                player["hp"] = min(player["max_hp"], player["hp"] + 25)
            elif it["type"] == "energy":
                player["energy"] = min(100, player["energy"] + 40)
            else:
                player["score"] += 10
            items.remove(it)

    if player["hp"] <= 0:
        draw_text("PRESS R", WIDTH//2-60, HEIGHT//2)
        pygame.display.flip()
        continue

    # ================== DRAW ==================
    screen.fill(DARK)
    cam_x = player["x"]*TILE - WIDTH//2
    cam_y = player["y"]*TILE - HEIGHT//2

    for y in range(MAP_H):
        for x in range(MAP_W):
            if world[y][x] == 1:
                pygame.draw.rect(
                    screen, GRAY,
                    (x*TILE-cam_x, y*TILE-cam_y, TILE, TILE)
                )

    for it in items:
        color = GREEN if it["type"]=="hp" else BLUE if it["type"]=="energy" else YELLOW
        pygame.draw.circle(
            screen, color,
            (it["x"]*TILE+TILE//2-cam_x, it["y"]*TILE+TILE//2-cam_y),
            6
        )

    for en in enemies:
        pygame.draw.rect(
            screen, RED,
            (en["x"]*TILE-cam_x, en["y"]*TILE-cam_y, TILE, TILE)
        )

    pygame.draw.rect(
        screen, WHITE,
        (player["x"]*TILE-cam_x, player["y"]*TILE-cam_y, TILE, TILE)
    )

    draw_text(f"HP: {int(player['hp'])}", 10, 10)
    draw_text(f"ENERGY: {int(player['energy'])}", 10, 32)
    draw_text(f"SCORE: {player['score']}", 10, 54)

    pygame.display.flip()

pygame.quit()