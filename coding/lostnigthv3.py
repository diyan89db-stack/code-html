import pygame
import sys
import math

pygame.init()

# ======================
# SETUP
# ======================
WIDTH, HEIGHT = 640, 480
CELL = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost Light - Fixed Version")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 48)

# ======================
# COLORS
# ======================
BG = (10, 10, 10)
WALL = (50, 50, 50)
PLAYER_COLOR = (80, 180, 255)
SHADOW_COLOR = (20, 20, 20)
EXIT_COLOR = (200, 80, 80)
TEXT = (230, 230, 230)

# ======================
# MAPS
# ======================
MAP_MAIN = [
    "11111111111111111111",
    "10000000000000000001",
    "10111111111111111001",
    "10000000000000000001",
    "10001111111111100001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "11111111111111111111",
]

MAP_ROOM = [
    "11111111111111111111",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "10000000000000000001",
    "11111111111111111111",
]

# ======================
# PLAYER
# ======================
player_pos = pygame.Vector2(2 * CELL, 2 * CELL)
player_vel = pygame.Vector2(0, 0)
player_rect = pygame.Rect(player_pos.x, player_pos.y, CELL, CELL)

ACCEL = 0.7
FRICTION = 0.85
MAX_SPEED = 4
battery = 100

# ======================
# SHADOW ENEMY
# ======================
shadow_pos = pygame.Vector2(15 * CELL, 7 * CELL)
shadow_rect = pygame.Rect(shadow_pos.x, shadow_pos.y, CELL, CELL)
shadow_speed = 1.4

exit_door = pygame.Rect(17 * CELL, 1 * CELL, CELL, CELL)

# ======================
# GAME STATE
# ======================
PLAY = "play"
JUMPSCARE = "jumpscare"
ENDING_ESCAPE = "escape"
ENDING_ACCEPT = "accept"

state = PLAY
jumpscare_timer = 0

# ======================
# LIGHTING (FIXED)
# ======================
darkness = pygame.Surface((WIDTH, HEIGHT))
darkness.set_alpha(220)

def draw_light(center, radius):
    darkness.fill((0, 0, 0))
    for r in range(radius, 0, -10):
        pygame.draw.circle(darkness, (0, 0, 0), center, r)

def draw_map(map_data):
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == "1":
                pygame.draw.rect(screen, WALL, (x * CELL, y * CELL, CELL, CELL))

# ======================
# MAIN LOOP
# ======================
while True:
    clock.tick(60)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # ======================
    # GAMEPLAY
    # ======================
    if state == PLAY:
        # Player movement
        if keys[pygame.K_w]: player_vel.y -= ACCEL
        if keys[pygame.K_s]: player_vel.y += ACCEL
        if keys[pygame.K_a]: player_vel.x -= ACCEL
        if keys[pygame.K_d]: player_vel.x += ACCEL

        player_vel *= FRICTION
        if player_vel.length() > MAX_SPEED:
            player_vel.scale_to_length(MAX_SPEED)

        player_pos += player_vel
        player_rect.topleft = player_pos

        # Shadow chase
        direction = player_pos - shadow_pos
        if direction.length() != 0:
            direction = direction.normalize()
        shadow_pos += direction * shadow_speed
        shadow_rect.topleft = shadow_pos

        # Battery drain
        battery -= 0.05
        if battery < 20:
            shadow_speed = 1.8

        # Collision → jumpscare
        if player_rect.colliderect(shadow_rect):
            state = JUMPSCARE
            jumpscare_timer = 0

        # Exit → escape ending
        if player_rect.colliderect(exit_door):
            state = ENDING_ESCAPE

        # Draw world
        draw_map(MAP_MAIN)
        pygame.draw.rect(screen, EXIT_COLOR, exit_door)
        pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

        draw_light(player_rect.center, max(40, int(battery)))
        screen.blit(darkness, (0, 0))

    # ======================
    # JUMPSCARE
    # ======================
    elif state == JUMPSCARE:
        jumpscare_timer += 1
        screen.fill((255, 255, 255))

        size = 200 + jumpscare_timer * 20
        rect = pygame.Rect(
            WIDTH // 2 - size // 2,
            HEIGHT // 2 - size // 2,
            size, size
        )
        pygame.draw.rect(screen, (0, 0, 0), rect)

        if jumpscare_timer > 18:
            state = ENDING_ACCEPT
            player_pos = pygame.Vector2(9 * CELL, 5 * CELL)
            player_rect.topleft = player_pos

    # ======================
    # ENDING ESCAPE
    # ======================
    elif state == ENDING_ESCAPE:
        screen.fill((0, 0, 0))
        screen.blit(big_font.render("ENDING: ESCAPE", True, TEXT), (150, 180))
        screen.blit(font.render("Kamu melarikan diri.", True, TEXT), (200, 240))
        screen.blit(font.render("Tapi bayangan itu tetap ada.", True, TEXT), (170, 270))

    # ======================
    # ENDING ACCEPTANCE
    # ======================
    elif state == ENDING_ACCEPT:
        draw_map(MAP_ROOM)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        screen.blit(big_font.render("ENDING: ACCEPTANCE", True, TEXT), (80, 60))
        screen.blit(font.render("Kamu berhenti melawan.", True, TEXT), (190, 120))
        screen.blit(font.render("Bayangan itu adalah dirimu.", True, TEXT), (170, 150))

    pygame.display.flip()
