import os
import random
import sys
import time

import pygame
from pygame.locals import *


##All drawable objects include this class
##Responsible for maintianing animations and sprites
class Drawable:
    # Initializer
    def __init__(self, sprites, x, y):
        self.sprites = sprites
        self.sprite = sprites[0]
        self.rect = self.sprite.get_bounding_rect()
        self.rect.x = x
        self.rect.y = y
        self.sprite_index = 0
        self.countdown = 0
        self.duration = 0

    # Assign sprites to this drawable object
    def set_sprites(sprites):
        self.sprites = sprites
        sprite = sprites[sprite_index]

    # Set initial conditions for animation
    def initialize_animation(self, duration, start_time):
        self.duration = duration
        self.countdown = start_time

    # Iterate through sprites in array
    def animate(self):
        atEnd = False
        if self.countdown > 0:
            self.countdown -= 1
        else:
            if self.sprite_index < len(self.sprites) - 1:
                self.sprite_index += 1

            else:
                self.sprite_index = 0
                atEnd = True
            self.sprite = self.sprites[self.sprite_index]
            self.countdown = self.duration

        return atEnd


##Handles enemy-specific functions like health and alternate sprites
class Enemy:
    def __init__(self, drawable, health, type, sprite_alt):
        self.drawable = drawable
        self.default_sprite = self.drawable.sprite
        self.sprite_alt = sprite_alt
        self.health = health
        self.type = type
        # Each enemy type has different point values
        if self.type == "red":
            self.points = 20
        elif self.type == "blue":
            self.points = 30
        elif self.type == "green":
            self.points = 50
        elif self.type == "yellow":
            self.points = 200
        else:
            self.points = 20

    # Defines what happens to an enemy when the player shoots them
    def hit(self):
        self.health -= 1
        if self.type == "yellow" and self.health == 1:
            self.drawable.sprites = self.sprite_alt


##Non-interactable elements that are drawn under all other sprites
class Effect:
    def __init__(self, drawable, x, y, type):
        self.drawable = drawable
        self.drawable.rect.centerx = x
        self.drawable.rect.centery = y
        self.type = type
        if self.type == "explosion":
            self.drawable.initialize_animation(2, 2)
        if self.type == "player_explosion":
            self.drawable.initialize_animation(5, 5)

    # Apply animations to effects
    def animate_effect(self):
        answer = False
        if self.type == "star":
            self.drawable.rect.y += 3
        else:
            answer = self.drawable.animate()
        return answer


# direction should be +1 (down) or -1 (up)
class Bullet:
    def __init__(self, rect, direction):
        self.drawable = Drawable(BULLETSPRITE, rect.centerx, rect.centery)
        self.direction = direction

    def update_bullet(self):
        self.drawable.rect.y += BULLETSPEED * self.direction


# create all lists that will hold objects
bullets = []
drawables = []
enemies = []
effects = []

# Static assignments
FORMATIONS = [
    "0,0,0,Y,0,0,Y,0,0,0",
    "0,0,G,G,G,G,G,G,0,0",
    "0,R,R,R,R,R,R,R,R,0",
    "B,B,B,B,B,B,B,B,B,B",
    "B,B,B,B,B,B,B,B,B,B",
    "B,B,B,B,B,B,B,B,B,B",
]

BULLETSPRITE = [pygame.image.load(os.path.join("Resources", "sprites", "bullet.png"))]
REDENEMY = [
    pygame.image.load(os.path.join("Resources", "sprites", "red enemy.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "red enemy 2.png")),
]
BLUEENEMY = [
    pygame.image.load(os.path.join("Resources", "sprites", "blue enemy.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "blue enemy 2.png")),
]
GREENENEMY = [
    pygame.image.load(os.path.join("Resources", "sprites", "green enemy.png"))
]
YELLOWENEMY = [
    pygame.image.load(os.path.join("Resources", "sprites", "yellow enemy.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "yellow enemy 2.png")),
]
YELLOWALT = [
    pygame.image.load(os.path.join("Resources", "sprites", "yellow alt.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "yellow alt 2.png")),
]
ENEMYEXPLOSION = [
    pygame.image.load(os.path.join("Resources", "sprites", "explosion 1.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "explosion 2.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "explosion 3.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "explosion 4.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "explosion 5.png")),
]
ENEMYEXPLOSIONDRAWBLE = Drawable(ENEMYEXPLOSION, 0, 0)
PLAYEREXPLOSION = [
    pygame.image.load(os.path.join("Resources", "sprites", "player explosion 1.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "player explosion 2.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "player explosion 3.png")),
    pygame.image.load(os.path.join("Resources", "sprites", "player explosion 4.png")),
]
PLAYEREXPLOSIONDRAWABLE = Drawable(PLAYEREXPLOSION, 0, 0)
STARSPRITES = [
    [pygame.image.load(os.path.join("Resources", "sprites", "star blue.png"))],
    [pygame.image.load(os.path.join("Resources", "sprites", "star red.png"))],
    [pygame.image.load(os.path.join("Resources", "sprites", "star green.png"))],
    [pygame.image.load(os.path.join("Resources", "sprites", "star purple.png"))],
    [pygame.image.load(os.path.join("Resources", "sprites", "star dkblue.png"))],
]

STARCOUNTMAX = 100
PLAYERLIVESMAX = 3
PAUSETICKERMAX = 120
SHOOTTICKERMAX = 30
BULLETSPEED = 10
LIVESMAX = 3
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()

DISPLAYFONT = pygame.font.Font(os.path.join("Resources", "fonts", "Emulogic.ttf"), 12)

DISPLAYSURF = pygame.display.set_mode((400, 600))

DISPLAYHEIGHT = DISPLAYSURF.get_height()
DISPLAYWIDTH = DISPLAYSURF.get_width()

pygame.display.set_caption("We have Galaga at home!")

lives = LIVESMAX
points = 0
highscore = 0


def main():
    # get access to global variables
    global lives
    global points
    global highscore

    # Pygame magic to make the main game loop run consistently
    fpsClock = pygame.time.Clock()

    pause = "False"
    pause_ticker = PAUSETICKERMAX
    moveTickerMax = 1
    shoot_ticker = SHOOTTICKERMAX
    move_ticker = moveTickerMax

    # Create GUI text
    create_GUI()

    # Create stars
    for i in range(STARCOUNTMAX):
        star_drawable = Drawable(STARSPRITES[random.randrange(len(STARSPRITES))], 0, 0)
        star = Effect(
            star_drawable,
            random.randrange(DISPLAYWIDTH),
            random.randrange(DISPLAYHEIGHT),
            "star",
        )
        effects.append(star)

    # Set up player
    playerSpeed = 5
    playerSprite = [
        pygame.image.load(os.path.join("Resources", "sprites", "player.png"))
    ]
    playerx = DISPLAYSURF.get_width() / 2 - playerSprite[0].get_width() / 2
    playery = DISPLAYSURF.get_height() * 0.9 - playerSprite[0].get_height()
    player = Drawable(playerSprite, playerx, playery)
    drawables.append(player)

    # Create initial enemy formation
    create_enemies()

    ##This is the "main loop" for the game, will continue until the window is closed
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        ##Fill the frame with black
        DISPLAYSURF.fill(BLACK)
        ##^Try to comment this line out and see what happens

        ##Process and draw effects (explosions, stars)
        for effect in effects:
            DISPLAYSURF.blit(
                effect.drawable.sprite, (effect.drawable.rect.x, effect.drawable.rect.y)
            )
            if effect.animate_effect():
                effects.remove(effect)
            if effect.type == "star" and effect.drawable.rect.y > DISPLAYHEIGHT:
                effect.drawable.rect.x = random.randrange(DISPLAYWIDTH)
                effect.drawable.rect.y = -3

        ##Process information for bullets (hits, offscreen, etc)
        for bullet in bullets:
            if bullet.drawable.rect.y < 0 or bullet.drawable.rect.y > DISPLAYHEIGHT:
                bullets.remove(bullet)
                drawables.remove(bullet.drawable)
            else:
                # process player shots
                if bullet.direction == -1:
                    for enemy in enemies:
                        if (
                            bullet.drawable.rect.colliderect(enemy.drawable.rect)
                            == True
                        ):
                            enemy.hit()
                            if enemy.health <= 0:
                                explosion = Effect(
                                    ENEMYEXPLOSIONDRAWBLE,
                                    enemy.drawable.rect.centerx,
                                    enemy.drawable.rect.centery,
                                    "explosion",
                                )
                                effects.append(explosion)
                                points += enemy.points
                                destroy(enemy)
                            destroy(bullet)
                            if len(enemies) == 0:
                                pause = "Enemies"
                            break
                # process enemy shots
                if bullet.direction == 1:
                    if bullet.drawable.rect.colliderect(player.rect) == True:
                        explosion = Effect(
                            PLAYEREXPLOSIONDRAWABLE,
                            player.rect.centerx,
                            player.rect.centery,
                            "player_explosion",
                        )
                        effects.append(explosion)
                        destroy(player)
                        destroy(bullet)
                        lives -= 1
                        pause = "Player"
                bullet.update_bullet()

        ##Update enemy movements
        if pause == "False":
            update_enemies()

            ##Process keyboard inputs
            keys = pygame.key.get_pressed()

            if (keys[K_a] or keys[K_LEFT]) and move_ticker == 0:
                move_ticker = moveTickerMax
                player.rect.x -= playerSpeed
            if (keys[K_d] or keys[K_RIGHT]) and move_ticker == 0:
                move_ticker = moveTickerMax
                player.rect.x += playerSpeed
            if keys[K_SPACE] and shoot_ticker == 0:
                shoot_ticker = SHOOTTICKERMAX
                shoot(player.rect, -1)

            if move_ticker > 0:
                move_ticker -= 1

            if shoot_ticker > 0:
                shoot_ticker -= 1
        else:
            pause_ticker -= 1

        # The pause ticker is used for 2 cases
        # 1. The player is destroyed
        # 2. All of the enemies are destroyed
        if pause_ticker < 0:
            pause_ticker = PAUSETICKERMAX
            if pause == "Player":
                player.rect.x = DISPLAYWIDTH / 2
                drawables.append(player)
            if pause == "Enemies":
                create_enemies()
            pause = "False"

        ##Update all drawables and draw to the screen
        for drawable in drawables:
            drawable.animate()
            DISPLAYSURF.blit(drawable.sprite, drawable.rect)

        ##Print all GUI elements to the screen
        update_GUI()

        ##Pygame magic
        pygame.display.update()
        fpsClock.tick(FPS)


# Responsible for creating bullets and assigning a movement vector to them
def shoot(rect, direction):
    bullet = Bullet(rect, direction)
    bullets.append(bullet)
    drawables.append(bullet.drawable)


##Creates enemies in the formation specified in the formation array
def create_enemies():
    originX = (DISPLAYWIDTH - 220) * 0.5
    originY = originX

    ycount = 0

    # Create the enemies in formation as shown in FORMATIONS list
    for formation in FORMATIONS:
        xcount = 0
        sprite = 0
        sprite_alt = 0
        health = 0
        type = ""

        for enemy in formation.split(","):
            sprite = 0
            if enemy == "Y":
                sprite = YELLOWENEMY
                sprite_alt = YELLOWALT
                health = 2
                type = "yellow"
            if enemy == "G":
                sprite = GREENENEMY
                health = 1
                type = "green"
            if enemy == "R":
                sprite = REDENEMY
                health = 1
                type = "red"
            if enemy == "B":
                sprite = BLUEENEMY
                health = 1
                type = "blue"

            if sprite != 0:
                # print("new enemy at ", originX + (xcount*20), ", ",originY + (ycount*20))
                # print(originX, "+",xcount,"*20=",originX + (xcount*20))
                enemyDrawable = Drawable(
                    sprite, originX + (xcount * 22), originY + (ycount * 22)
                )
                if xcount % 2 == 0:
                    enemyDrawable.initialize_animation(45, 0)
                else:
                    enemyDrawable.initialize_animation(45, 45)

                newEnemy = Enemy(enemyDrawable, health, type, sprite_alt)
                enemies.append(newEnemy)
                drawables.append(newEnemy.drawable)

            xcount += 1
        ycount += 1


enemyOffset = 0
enemyDirection = "left"
enemyFireCooldown = 30
##Responsible for maintaining enemy movement
def update_enemies():
    global enemyOffset
    global enemyDirection
    global enemyFireCooldown

    # move enemies to the left
    if enemyDirection == "left":
        if enemyOffset > -5:
            enemyOffset -= 0.1
            for enemy in enemies:
                enemy.drawable.rect.x -= 1

        else:
            enemyDirection = "right"
    # move enemies to the right
    elif enemyDirection == "right":
        if enemyOffset < 5:
            enemyOffset += 0.1
            for enemy in enemies:
                enemy.drawable.rect.x += 1

        else:
            enemyDirection = "left"

    ##Enemy firing algorithm
    # if the fire "cooldown" has expired
    # choose a random enemy in the list
    # roll a 7 sided die to determine if the enemy can shoot. If roll > 2, allow the enemy to shoot
    if enemyFireCooldown < 0 and len(enemies) > 0:
        shooting = random.randrange(len(enemies))
        if random.randrange(7) > 2:
            shoot(enemies[shooting].drawable.rect, 1)
        enemyFireCooldown = 30
    else:
        enemyFireCooldown -= 1


def destroy(instance):
    if isinstance(instance, Enemy):
        enemies.remove(instance)
        drawables.remove(instance.drawable)
    elif isinstance(instance, Bullet):
        bullets.remove(instance)
        drawables.remove(instance.drawable)
    else:
        drawables.remove(instance)


livesDisplay = 0
livesDisplayRect = 0
scoreLabelDisplay = 0
scoreLabelDisplayRect = 0
scoreDisplay = 0
scoreDisplayRect = 0
highScoreLabelDisplay = 0
highScoreLabelDisplayRect = 0
highScoreDisplay = 0
highScoreDisplayRect = 0


def create_GUI():
    global livesDisplay
    global livesDisplayRect
    global scoreLabelDisplay
    global scoreLabelDisplayRect
    global scoreDisplay
    global scoreDisplayRect
    global highScoreLabelDisplay
    global highScoreLabelDisplayRect
    global highScoreDisplay
    global highScoreDisplayRect

    livesDisplay = DISPLAYFONT.render("Lives: " + str(lives), True, WHITE, BLACK)
    livesDisplayRect = livesDisplay.get_rect()
    livesDisplayRect.x = 0
    livesDisplayRect.y = DISPLAYHEIGHT - livesDisplayRect.height

    scoreLabelDisplay = DISPLAYFONT.render("SCORE", True, RED, BLACK)
    scoreLabelDisplayRect = scoreLabelDisplay.get_rect()
    scoreLabelDisplayRect.centerx = DISPLAYWIDTH * 0.2
    scoreLabelDisplayRect.y = 0

    scoreDisplay = DISPLAYFONT.render(str(points), True, WHITE, BLACK)
    scoreDisplayRect = scoreDisplay.get_rect()
    scoreDisplayRect.centerx = scoreLabelDisplayRect.centerx
    scoreDisplayRect.y = scoreLabelDisplayRect.height

    highScoreLabelDisplay = DISPLAYFONT.render("HIGH SCORE", True, RED, BLACK)
    highScoreLabelDisplayRect = highScoreLabelDisplay.get_rect()
    highScoreLabelDisplayRect.centerx = DISPLAYWIDTH * 0.7
    highScoreLabelDisplayRect.y = 0

    highScoreDisplay = DISPLAYFONT.render(str(highscore), True, WHITE, BLACK)
    highScoreDisplayRect = highScoreDisplay.get_rect()
    highScoreDisplayRect.centerx = highScoreLabelDisplayRect.centerx
    highScoreDisplayRect.y = highScoreLabelDisplayRect.height


def update_GUI():
    global livesDisplay
    global livesDisplayRect
    global scoreLabelDisplay
    global scoreLabelDisplayRect
    global scoreDisplay
    global scoreDisplayRect
    global highScoreLabelDisplay
    global highScoreLabelDisplayRect
    global highScoreDisplay
    global highScoreDisplayRect
    global points
    global lives
    global highscore

    livesDisplay = DISPLAYFONT.render("Lives: " + str(lives), True, WHITE, BLACK)
    scoreDisplay = DISPLAYFONT.render(str(points), True, WHITE, BLACK)
    highScoreDisplay = DISPLAYFONT.render(str(highscore), True, WHITE, BLACK)
    DISPLAYSURF.blit(livesDisplay, livesDisplayRect)
    DISPLAYSURF.blit(scoreLabelDisplay, scoreLabelDisplayRect)
    DISPLAYSURF.blit(scoreDisplay, scoreDisplayRect)
    DISPLAYSURF.blit(highScoreLabelDisplay, highScoreLabelDisplayRect)
    DISPLAYSURF.blit(highScoreDisplay, highScoreDisplayRect)


main()
