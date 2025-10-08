import pygame
import random
import sys

pygame.init()
pygame.mixer.init()  # Initialize mixer for sound

# Screen settings
WIDTH, HEIGHT = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player
player_width, player_height = 50, 50
player_speed = 7
player_lives = 5

# Bullets
bullet_speed = 10
enemy_bullet_speed = 7
bullet_cooldown_max = 12

# Enemies
enemy_width, enemy_height = 50, 50

# Power-ups
powerup_speed = 3
powerup_chance = 0.2

# Load images
player_img = pygame.image.load("images/space_rocket.png")
player_img = pygame.transform.scale(player_img, (player_width, player_height))

enemy_img = pygame.image.load("images/rocket.png")
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))

bullet_img = pygame.image.load("images/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

enemy_bullet_img = pygame.image.load("images/bullet2.png")
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (10, 20))
enemy_bullet_img = pygame.transform.rotate(enemy_bullet_img, -90)

powerup_img = pygame.image.load("images/booster.png")
powerup_img = pygame.transform.scale(powerup_img, (30, 30))

# Load sounds
pygame.mixer.music.load("music/track.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

bullet_sound = pygame.mixer.Sound("music/laser1.mp3")
bullet_sound.set_volume(0.5)

enemy_hit_sound = pygame.mixer.Sound("music/laser2.mp3")
enemy_hit_sound.set_volume(0.5)

powerup_sound = pygame.mixer.Sound("music/laser2.mp3")
powerup_sound.set_volume(0.5)

# Font
font = pygame.font.SysFont("comicsans", 30)

# Game over screen
def game_over_screen(score):
    while True:
        SCREEN.fill(BLACK)
        over_text = font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        SCREEN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//3))
        SCREEN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//3 + 50))
        SCREEN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//3 + 100))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main game
def main():
    player_x = WIDTH//2 - player_width//2
    player_y = HEIGHT - player_height - 10
    lives = player_lives

    bullets = []
    enemy_bullets = []
    bullet_cooldown = 0
    bullets_per_shot = 1
    boost_timer = 0

    enemies = []
    enemy_speed = 3
    spawn_timer = 0
    enemy_spawn_rate = 30

    powerups = []
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        SCREEN.fill(BLACK)
        keys = pygame.key.get_pressed()

        # Player continuous firing
        if keys[pygame.K_SPACE] and bullet_cooldown == 0:
            for i in range(bullets_per_shot):
                offset = i * 10 - (bullets_per_shot-1)*5
                bullets.append([player_x + player_width//2 - 5 + offset, player_y])
            bullet_cooldown = bullet_cooldown_max
            bullet_sound.play()
        if bullet_cooldown > 0:
            bullet_cooldown -= 1

        # Move bullets
        for b in bullets[:]:
            b[1] -= bullet_speed
            if b[1] < 0:
                bullets.remove(b)

        # Spawn enemies
        spawn_timer += 1
        if spawn_timer > enemy_spawn_rate:
            ex = random.randint(0, WIDTH - enemy_width)
            enemies.append([ex, -enemy_height])
            spawn_timer = 0

        # Move enemies and fire bullets
        for e in enemies[:]:
            e[1] += enemy_speed
            if random.random() < 0.02:
                enemy_bullets.append([e[0]+enemy_width//2 - 5, e[1]+enemy_height])
            if e[1] > HEIGHT:
                enemies.remove(e)
                lives -= 1
                if lives <= 0:
                    running = False

        # Move enemy bullets
        for eb in enemy_bullets[:]:
            eb[1] += enemy_bullet_speed
            if eb[1] > HEIGHT:
                enemy_bullets.remove(eb)
            # Collision with player
            if player_x < eb[0] < player_x + player_width and player_y < eb[1] < player_y + player_height:
                enemy_bullets.remove(eb)
                lives -= 1
                if lives <= 0:
                    running = False
            # Collision with player's bullets (cut bullets)
            for b in bullets[:]:
                if (b[0] > eb[0] and b[0] < eb[0]+10) and (b[1] > eb[1] and b[1] < eb[1]+20):
                    bullets.remove(b)
                    enemy_bullets.remove(eb)
                    break

        # Move power-ups
        for p in powerups[:]:
            p[1] += powerup_speed
            if p[1] > HEIGHT:
                powerups.remove(p)

        # Collision detection (enemy hit)
        for e in enemies[:]:
            for b in bullets[:]:
                if (b[0] > e[0] and b[0] < e[0]+enemy_width) and (b[1] > e[1] and b[1] < e[1]+enemy_height):
                    enemies.remove(e)
                    bullets.remove(b)
                    score += 1
                    enemy_hit_sound.play()
                    if random.random() < powerup_chance and bullets_per_shot < 3:
                        powerups.append([e[0]+10, e[1]+10])
                    break

        # Player collects power-ups
        for p in powerups[:]:
            if (player_x < p[0] < player_x + player_width) and (player_y < p[1] < player_y + player_height):
                if bullets_per_shot < 3:
                    bullets_per_shot += 1
                boost_timer = 300
                powerups.remove(p)
                powerup_sound.play()

        # Reduce boost timer
        if bullets_per_shot > 1:
            boost_timer -= 1
            if boost_timer <= 0:
                bullets_per_shot -= 1
                boost_timer = 0

        # Player movement
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Difficulty increase
        if score >= 10:
            enemy_speed = 4
            enemy_spawn_rate = 30
        if score >= 20:
            enemy_speed = 5
            enemy_spawn_rate = 25
        if score >= 30:
            enemy_speed = 6
            enemy_spawn_rate = 20

        # Draw everything
        SCREEN.blit(player_img, (player_x, player_y))
        for b in bullets: SCREEN.blit(bullet_img, (b[0], b[1]))
        for e in enemies: SCREEN.blit(enemy_img, (e[0], e[1]))
        for eb in enemy_bullets: SCREEN.blit(enemy_bullet_img, (eb[0], eb[1]))
        for p in powerups: SCREEN.blit(powerup_img, (p[0], p[1]))

        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        SCREEN.blit(lives_text, (10, 40))
        power_text = font.render(f"Power Level: {bullets_per_shot}", True, WHITE)
        SCREEN.blit(power_text, (10, 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

    game_over_screen(score)

# Start game
main()
