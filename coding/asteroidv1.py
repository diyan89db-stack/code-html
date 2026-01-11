import pygame
import random
import sys

pygame.init()

# ======================
# SETUP
# ======================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Dodger")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# ======================
# PLAYER
# ======================
player = pygame.Rect(WIDTH//2 - 25, HEIGHT - 80, 50, 50)
player_speed = 6

# ======================
# ASTEROID
# ======================
asteroids = []
spawn_timer = 0
asteroid_speed = 4

# ======================
# GAME STATE
# ======================
score = 0
game_over = False

# ======================
# FUNCTIONS
# ======================
def draw_text(text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global asteroids, score, asteroid_speed, game_over
    asteroids = []
    score = 0
    asteroid_speed = 4
    game_over = False
    player.x = WIDTH//2 - 25

# ======================
# GAME LOOP
# ======================
while True:
    clock.tick(60)
    screen.fill((10, 10, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

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
        # SPAWN ASTEROID
        # ======================
        spawn_timer += 1
        if spawn_timer > 30:
            spawn_timer = 0
            size = random.randint(30, 60)
            x = random.randint(0, WIDTH - size)
            asteroids.append(pygame.Rect(x, -size, size, size))

        # ======================
        # ASTEROID MOVE
        # ======================
        for asteroid in asteroids[:]:
            asteroid.y += asteroid_speed
            if asteroid.top > HEIGHT:
                asteroids.remove(asteroid)
                score += 1
                if score % 10 == 0:
                    asteroid_speed += 1

            if asteroid.colliderect(player):
                game_over = True

    # ======================
    # DRAW PLAYER
    # ======================
    pygame.draw.rect(screen, (0, 200, 255), player)

    # ======================
    # DRAW ASTEROIDS
    # ======================
    for asteroid in asteroids:
        pygame.draw.rect(screen, (200, 50, 50), asteroid)

    # ======================
    # UI
    # ======================
    draw_text(f"Score: {score}", 10, 10)

    if game_over:
        draw_text("GAME OVER", WIDTH//2 - 100, HEIGHT//2 - 40, (255, 50, 50))
        draw_text("Press R to Restart", WIDTH//2 - 140, HEIGHT//2)

    pygame.display.flip()
