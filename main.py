import pygame
import random
from pygame import mixer

# Initialize
pygame.init()

# Game Window
screen = pygame.display.set_mode((800, 600))

# title
pygame.display.set_caption("Space Invaders")

# Background
background = pygame.image.load("background.png")

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# player
player_img = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6



# Bullet
bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
show_bullet = False

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over():
    game_over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (200, 250))


def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global show_bullet
    show_bullet = True
    screen.blit(bullet_img, (x + 16, y + 10))


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = ((bulletY - enemyY) ** 2 + (bulletX - enemyX) ** 2) ** (1 / 2)
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            elif event.key == pygame.K_RIGHT:
                playerX_change = 4
            elif event.key == pygame.K_SPACE:
                if show_bullet is False:
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if score == 100:
        num_of_enemies = 10
    if score == 200:
        num_of_enemies = 15
    if score == 300:
        num_of_enemies = 20
    if score == 400:
        num_of_enemies = 25
    if score == 500:
        num_of_enemies = 35
    if score == 600:
        num_of_enemies = 69

    for i in range(num_of_enemies):
        enemy_img.append(pygame.image.load("enemy.png"))
        enemyX.append(random.randint(0, 735))
        enemyY.append(-50)
        enemyX_change.append(5)
        enemyY_change.append(50)

    for i in range(num_of_enemies):

        if enemyY[i] > 420:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collide = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collide:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            show_bullet = False
            score += 10
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = -40

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        show_bullet = False

    if show_bullet:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
