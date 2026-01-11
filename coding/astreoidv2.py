import pygame
import random
import sys

pygame.init()

# ======================
# SETUP
# ======================
WIDTH, HEIGHT = 1010, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Dodger - TIME HELL")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# ======================
# PLAYER
# ======================
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)
player_speed = 6

# ======================
# OBJECTS
# ======================
asteroids = []
spawn_timer = 0

# ======================
# GAME STATE
# ======================
score = 0
game_over = False
start_time = pygame.time.get_ticks()

# ======================
# FUNCTIONS
# ======================
def draw_text(text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global asteroids, score, game_over, spawn_timer, start_time
    asteroids = []
    score = 0
    spawn_timer = 0
    game_over = False
    start_time = pygame.time.get_ticks()
    player.x = WIDTH // 2 - 25
    player.y = HEIGHT - 80

def spawn_asteroid(time_alive):
    size = random.randint(20, 70)
    x = random.randint(0, WIDTH - size)

    speed_y = random.randint(3, 6) + time_alive // 10
    speed_x = random.randint(-2 - time_alive // 20, 2 + time_alive // 20)

    asteroid = {
        "rect": pygame.Rect(x, -size, size, size),
        "speed_y": speed_y,
        "speed_x": speed_x,
        "color": random.choice([(200,50,50), (255,120,50), (180,0,0)])
    }
    asteroids.append(asteroid)

# ======================
# GAME LOOP
# ======================
while True:
    dt = clock.tick(60)
    screen.fill((10, 10, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    # ======================
    # TIME ALIVE
    # ======================
    time_alive = (pygame.time.get_ticks() - start_time) // 1000

    if not game_over:
        # ======================
        # PLAYER MOVE
        # ======================
        if keys[pygame.K_a] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_d] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_w] and player.top > 0:
            player.y -= player_speed
        if keys[pygame.K_s] and player.bottom < HEIGHT:
            player.y += player_speed

        # ======================
        # SPAWN ASTEROID (TIME BASED)
        # ======================
        spawn_timer += 1

        spawn_delay = max(6, 30 - time_alive)
        spawn_count = 1 + time_alive // 15

        if spawn_timer >= spawn_delay:
            spawn_timer = 0
            for _ in range(spawn_count):
                spawn_asteroid(time_alive)

        # ======================
        # MOVE ASTEROIDS
        # ======================
        for asteroid in asteroids[:]:
            asteroid["rect"].y += asteroid["speed_y"]
            asteroid["rect"].x += asteroid["speed_x"]

            if asteroid["rect"].left < 0 or asteroid["rect"].right > WIDTH:
                asteroid["speed_x"] *= -1

            if asteroid["rect"].top > HEIGHT:
                asteroids.remove(asteroid)
                score += 1

            if asteroid["rect"].colliderect(player):
                game_over = True

    # ======================
    # DRAW
    # ======================
    pygame.draw.rect(screen, (0, 200, 255), player)

    for asteroid in asteroids:
        pygame.draw.rect(screen, asteroid["color"], asteroid["rect"])

    # ======================
    # UI
    # ======================
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Time Alive: {time_alive}s", 10, 35)
    draw_text(f"Asteroids: {len(asteroids)}", 10, 60)

    if game_over:
        draw_text("GAME OVER", WIDTH // 2 - 90, HEIGHT // 2 - 40, (255, 50, 50))
        draw_text("Press R to Restart", WIDTH // 2 - 130, HEIGHT // 2)

    pygame.display.flip()
