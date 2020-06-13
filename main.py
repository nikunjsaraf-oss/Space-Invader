import pygame
import random
import math
from pygame import mixer

# initiaizing PYGAME
pygame.init()

# Setting up Screen
screen = pygame.display.set_mode((800, 600))  # 800*600 is the resolution

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("background.png")
# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load("Player.png")
# Coordinates of player
playerX = 170
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
# Coordinates of enemy
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numberOfEnemies = 6
for i in range(numberOfEnemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    # Coordinates of enemy
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
# Coordinates of player
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

# score
score_valiue = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)


def score_display(x, y):
    score = font.render("Score: " + str(score_valiue), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (200, 250))


def player(x, y):
    # blit -> draw
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # blit -> draw
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 12, y + 10))


def isCollide(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance <= 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # DISPLAY COLOR
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # Quiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # To check whether key is pressed or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Creating our player
    playerX += playerX_change

    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0

    # SETTING BOUNDARY FOR ENEMY
    for i in range(numberOfEnemies):
        if enemyY[i] > 440:
            for j in range(numberOfEnemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 716:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        collide = isCollide(bulletX, bulletY, enemyX[i], enemyY[i])
        if collide:
            collision = mixer.Sound('explosion.wav')
            collision.play()
            bulletY = 480
            bullet_state = "ready"
            score_valiue += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Firing Bullet
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    score_display(textX, textY)
    pygame.display.update()
