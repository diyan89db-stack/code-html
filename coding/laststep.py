import pygame
import sys

pygame.init()

# ======================
# SETUP
# ======================
WIDTH, HEIGHT = 640, 480
CELL = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LAST STEP")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 42)

# ======================
# COLORS
# ======================
BG = (15, 15, 15)
WALL = (60, 60, 60)
PLAYER = (80, 180, 255)
DOOR = (180, 80, 80)
TEXT = (230, 230, 230)

# ======================
# MAP
# ======================
MAP = [
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

# ======================
# STORY STATE
# ======================
SCENE_DIALOG = "dialog"
SCENE_PLAY = "play"
SCENE_CHOICE = "choice"
SCENE_ENDING_A = "ending_a"
SCENE_ENDING_B = "ending_b"

scene = SCENE_DIALOG
story_progress = 0
choice = None

# ======================
# DIALOG
# ======================
dialog = [
    "......",
    "Kepalaku terasa berat.",
    "Aku tidak ingat bagaimana bisa sampai di sini.",
    "Ruangan ini sunyi.",
    "Ada satu pintu di depan.",
    "Entah kenapa, aku ragu melangkah."
]

typing_index = 0
typing_speed = 2

# ======================
# OBJECT
# ======================
door_rect = pygame.Rect(9 * CELL, 1 * CELL, CELL * 2, CELL)

# ======================
# FUNCTIONS
# ======================
def draw_map():
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile == "1":
                pygame.draw.rect(screen, WALL, (x * CELL, y * CELL, CELL, CELL))

def draw_dialog(text):
    box = pygame.Rect(20, HEIGHT - 100, WIDTH - 40, 80)
    pygame.draw.rect(screen, (0, 0, 0), box)
    pygame.draw.rect(screen, TEXT, box, 2)
    render = font.render(text, True, TEXT)
    screen.blit(render, (box.x + 10, box.y + 30))

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

        if scene == SCENE_DIALOG and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if typing_index < len(dialog[story_progress]):
                    typing_index = len(dialog[story_progress])
                else:
                    story_progress += 1
                    typing_index = 0
                    if story_progress >= len(dialog):
                        scene = SCENE_PLAY

        if scene == SCENE_CHOICE and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                scene = SCENE_ENDING_A
            if event.key == pygame.K_2:
                scene = SCENE_ENDING_B

    keys = pygame.key.get_pressed()

    # ======================
    # SCENE: PLAY
    # ======================
    if scene == SCENE_PLAY:
        if keys[pygame.K_w]: player_vel.y -= ACCEL
        if keys[pygame.K_s]: player_vel.y += ACCEL
        if keys[pygame.K_a]: player_vel.x -= ACCEL
        if keys[pygame.K_d]: player_vel.x += ACCEL

        player_vel *= FRICTION
        if player_vel.length() > MAX_SPEED:
            player_vel.scale_to_length(MAX_SPEED)

        player_pos += player_vel
        player_rect.topleft = player_pos

        if player_rect.colliderect(door_rect):
            scene = SCENE_CHOICE

    # ======================
    # DRAW WORLD
    # ======================
    draw_map()
    pygame.draw.rect(screen, DOOR, door_rect)
    pygame.draw.rect(screen, PLAYER, player_rect)

    # ======================
    # DIALOG SCENE
    # ======================
    if scene == SCENE_DIALOG:
        if typing_index < len(dialog[story_progress]):
            typing_index += typing_speed
        draw_dialog(dialog[story_progress][:typing_index])

    # ======================
    # CHOICE SCENE
    # ======================
    if scene == SCENE_CHOICE:
        screen.fill((0, 0, 0))
        screen.blit(big_font.render("APA YANG AKAN KAMU LAKUKAN?", True, TEXT), (80, 120))
        screen.blit(font.render("1. Masuk dan hadapi semuanya", True, TEXT), (180, 200))
        screen.blit(font.render("2. Pergi dan lupakan", True, TEXT), (180, 240))

    # ======================
    # ENDINGS
    # ======================
    if scene == SCENE_ENDING_A:
        screen.fill((0, 0, 0))
        screen.blit(big_font.render("ENDING: MENGHADAPI", True, TEXT), (120, 180))
        screen.blit(font.render("Kamu melangkah maju.", True, TEXT), (220, 240))
        screen.blit(font.render("Dan menerima kebenaran.", True, TEXT), (200, 270))

    if scene == SCENE_ENDING_B:
        screen.fill((0, 0, 0))
        screen.blit(big_font.render("ENDING: MELARIKAN DIRI", True, TEXT), (80, 180))
        screen.blit(font.render("Kamu pergi.", True, TEXT), (260, 240))
        screen.blit(font.render("Tapi pertanyaan itu tetap ada.", True, TEXT), (180, 270))

    pygame.display.flip()
