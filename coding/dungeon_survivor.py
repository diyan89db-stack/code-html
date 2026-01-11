import pygame
import random
import math
import sys

# ================== INIT ==================
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Survivor")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 22)

# ================== COLORS ==================
WHITE = (255, 255, 255)
RED   = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE  = (50, 150, 255)
GRAY  = (40, 40, 40)
BLACK = (0, 0, 0)

# ================== PLAYER ==================
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 15
        self.speed = 5
        self.hp = 100

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.radius)

# ================== BULLET ==================
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 10
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.radius = 4

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

# ================== ENEMY ==================
class Enemy:
    def __init__(self, level):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.x = random.randint(0, WIDTH)
            self.y = -20
        elif side == "bottom":
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + 20
        elif side == "left":
            self.x = -20
            self.y = random.randint(0, HEIGHT)
        else:
            self.x = WIDTH + 20
            self.y = random.randint(0, HEIGHT)

        self.radius = 14
        self.speed = 1.5 + level * 0.1
        self.hp = 30 + level * 2

    def update(self, player):
        angle = math.atan2(player.y - self.y, player.x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

# ================== GAME ==================
def main():
    player = Player()
    bullets = []
    enemies = []

    score = 0
    level = 1
    spawn_timer = 0
    game_over = False

    while True:
        clock.tick(60)
        screen.fill(GRAY)

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx, my = pygame.mouse.get_pos()
                angle = math.atan2(my - player.y, mx - player.x)
                bullets.append(Bullet(player.x, player.y, angle))

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    main()

        keys = pygame.key.get_pressed()

        if not game_over:
            # -------- UPDATE --------
            player.move(keys)

            spawn_timer += 1
            if spawn_timer > max(20, 60 - level * 3):
                enemies.append(Enemy(level))
                spawn_timer = 0

            for bullet in bullets[:]:
                bullet.update()
                if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
                    bullets.remove(bullet)

            for enemy in enemies[:]:
                enemy.update(player)

                # collision with player
                dist = math.hypot(enemy.x - player.x, enemy.y - player.y)
                if dist < enemy.radius + player.radius:
                    player.hp -= 10
                    enemies.remove(enemy)
                    if player.hp <= 0:
                        game_over = True

                # collision with bullet
                for bullet in bullets[:]:
                    dist = math.hypot(enemy.x - bullet.x, enemy.y - bullet.y)
                    if dist < enemy.radius + bullet.radius:
                        enemy.hp -= 20
                        bullets.remove(bullet)
                        if enemy.hp <= 0:
                            enemies.remove(enemy)
                            score += 10
                            if score % 100 == 0:
                                level += 1
                        break

        # -------- DRAW --------
        player.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()

        # UI
        hp_text = FONT.render(f"HP: {player.hp}", True, WHITE)
        score_text = FONT.render(f"Score: {score}", True, WHITE)
        level_text = FONT.render(f"Level: {level}", True, WHITE)

        screen.blit(hp_text, (10, 10))
        screen.blit(score_text, (10, 40))
        screen.blit(level_text, (10, 70))

        if game_over:
            over = FONT.render("GAME OVER - Press R to Restart", True, WHITE)
            screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

# ================== RUN ==================
main()
