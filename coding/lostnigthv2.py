import pygame
import sys
import random

pygame.init()

# ======================
# SETUP
# ======================
WIDTH, HEIGHT = 640, 480
CELL = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost Light - Chapter 2")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ======================
# COLORS
# ======================
BG = (10, 10, 10)
WALL = (50, 50, 50)
PLAYER_COLOR = (80, 180, 255)
DOOR_LOCK = (180, 60, 60)
DOOR_OPEN = (80, 200, 120)
GENERATOR = (200, 200, 80)
SHADOW = (30, 30, 30)
TEXT = (230, 230, 230)

# ======================
# MAP
# ======================
game_map = [
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

# ======================
# PLAYER
# ======================
player_pos = pygame.Vector2(2 * CELL, 2 * CELL)
player_vel = pygame.Vector2(0, 0)
PLAYER_SIZE = CELL
ACCEL = 0.6
FRICTION = 0.85
MAX_SPEED = 4
player_rect = pygame.Rect(player_pos.x, player_pos.y, PLAYER_SIZE, PLAYER_SIZE)

# ======================
# OBJECTS
# ======================
generator_rect = pygame.Rect(9 * CELL, 5 * CELL, CELL, CELL)
door_rect = pygame.Rect(17 * CELL, 4 * CELL, CELL, CELL)
generator_on = False

shadow_pos = pygame.Vector2(12 * CELL, 3 * CELL)
shadow_timer = 0

# ======================
# DIALOG
# ======================
dialogs = [
    "Gelap... lagi.",
    "Pintu itu menutup sendiri.",
    "Tempat ini lebih besar dari yang kupikir.",
    "Ada suara... seperti langkah kaki.",
    "Aku tidak sendirian."
]

dialog_index = 0
typing_index = 0
typing_speed = 2
show_dialog = True

# ======================
# LIGHTING
# ======================
darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

def draw_light(center, radius):
    for r in range(radius, 0, -10):
        alpha = int(220 * (1 - r / radius))
        pygame.draw.circle(darkness, (0, 0, 0, alpha), center, r)

# ======================
# FUNCTIONS
# ======================
def draw_map():
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == "1":
                pygame.draw.rect(screen, WALL, (x * CELL, y * CELL, CELL, CELL))

def draw_dialog(text):
    box = pygame.Rect(20, HEIGHT - 90, WIDTH - 40, 70)
    pygame.draw.rect(screen, (0, 0, 0), box)
    pygame.draw.rect(screen, TEXT, box, 2)
    render = font.render(text, True, TEXT)
    screen.blit(render, (box.x + 10, box.y + 25))

# ======================
# GAME LOOP
# ======================
while True:
    clock.tick(60)
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and show_dialog:
            if event.key == pygame.K_SPACE:
                if typing_index < len(dialogs[dialog_index]):
                    typing_index = len(dialogs[dialog_index])
                else:
                    dialog_index += 1
                    typing_index = 0
                    if dialog_index >= len(dialogs):
                        show_dialog = False

    keys = pygame.key.get_pressed()

    # PLAYER MOVEMENT
    if not show_dialog:
        if keys[pygame.K_w]: player_vel.y -= ACCEL
        if keys[pygame.K_s]: player_vel.y += ACCEL
        if keys[pygame.K_a]: player_vel.x -= ACCEL
        if keys[pygame.K_d]: player_vel.x += ACCEL

    player_vel *= FRICTION
    if player_vel.length() > MAX_SPEED:
        player_vel.scale_to_length(MAX_SPEED)

    player_pos += player_vel
    player_rect.topleft = player_pos

    # DRAW WORLD
    draw_map()

    pygame.draw.rect(screen, GENERATOR, generator_rect)
    pygame.draw.rect(screen, DOOR_OPEN if generator_on else DOOR_LOCK, door_rect)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # SHADOW EVENT
    shadow_timer += 1
    if shadow_timer % 120 == 0:
        shadow_pos.x = random.randint(4, 15) * CELL
        shadow_pos.y = random.randint(2, 7) * CELL

    if random.randint(0, 10) > 7:
        pygame.draw.rect(screen, SHADOW, (*shadow_pos, CELL, CELL))

    # GENERATOR CHECK
    if player_rect.colliderect(generator_rect):
        generator_on = True

    # DIALOG
    if show_dialog:
        if typing_index < len(dialogs[dialog_index]):
            typing_index += typing_speed
        draw_dialog(dialogs[dialog_index][:typing_index])

    # LIGHTING
    darkness.fill((0, 0, 0, 220))
    draw_light(player_rect.center, 90 if not generator_on else 140)
    screen.blit(darkness, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    # CHAPTER END
    if generator_on and player_rect.colliderect(door_rect):
        screen.fill((0, 0, 0))
        end = font.render("Chapter 2 selesai - tekan ESC", True, TEXT)
        screen.blit(end, (180, 220))
        pygame.display.flip()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    pygame.display.flip()
