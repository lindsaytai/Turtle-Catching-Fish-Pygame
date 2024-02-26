#copyright 2021 Lindsay Cheng 1/2/2021
#This game uses the Pygame library for graphics. The library can be downloaded at pygame.org 
#Users can use the keyboard arrow keys to position the turtle and the space bar to challenge the fish. 

import os
import math
import random
import time

import pygame
from pygame import mixer

agentX = 200
screenRefresh = True
spriteGroup = pygame.sprite.OrderedUpdates()
textboxGroup = pygame.sprite.OrderedUpdates()
background = None

def showSprite(sprite):
    spriteGroup.add(sprite)
    if screenRefresh:
        updateDisplay()

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#junk
def changeSpriteImage(sprite, index):
    sprite.changeImage(index)

def player(player_object, x, y):
    #screen.blit(player_object, (x, y))
    moveSprite(agent, x, y)
    showSprite(agent)
    #pass
    
def enemy(my_image, x, y, i):
    screen.blit(my_image, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyPositionX, enemyPositionY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyPositionX - bulletX, 2) + (math.pow(enemyPositionY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

#-----------------from https://github.com/StevePaget/Pygame_Functions/blob/master/pygame_functions.py

def makeSprite(filename, frames=1):
    thisSprite = newSprite(filename, frames)
    return thisSprite

def addSpriteImage(sprite, image):
    sprite.addImage(image)

def moveSprite(sprite, x, y, centre=False):
    sprite.move(x, y, centre)
    if screenRefresh:
        updateDisplay()

def updateDisplay():
    global background
    spriteRects = spriteGroup.draw(screen)
    textboxRects = textboxGroup.draw(screen)
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_ESCAPE]):
        pygame.quit()
        sys.exit()
    pygame.sprite.OrderedUpdates().clear(screen, background.surface)
    textboxGroup.clear(screen, background.surface)

def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")

def screenSize(sizex, sizey, xpos=None, ypos=None, fullscreen=False):
    global screen
    global background
    if xpos != None and ypos != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (xpos, ypos + 50)
    else:
        windowInfo = pygame.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % ((monitorWidth - sizex) / 2, (monitorHeight - sizey) / 2)
    if fullscreen:
        screen = pygame.display.set_mode([sizex, sizey], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([sizex, sizey])
    background = Background()
    screen.fill(background.colour)
    pygame.display.set_caption("Graphics Window")
    background.surface = screen.copy()
    pygame.display.update()
    return screen

class newSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = loadImage(filename)
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pygame.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1

    def addImage(self, filename):
        self.images.append(loadImage(filename))

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pygame.mask.from_surface(self.image)
        if screenRefresh:
            updateDisplay()

class Background():
    def __init__(self):
        self.colour = pygame.Color("black")

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[loadImage(tiles)]]
        elif type(tiles[0]) is str:
            self.tiles = [[loadImage(i) for i in tiles]]
        else:
            self.tiles = [[loadImage(i) for i in row] for row in tiles]
        self.stagePosX = 0
        self.stagePosY = 0
        self.tileWidth = self.tiles[0][0].get_width()
        self.tileHeight = self.tiles[0][0].get_height()
        screen.blit(self.tiles[0][0], [0, 0])
        self.surface = screen.copy()

    def scroll(self, x, y):
        self.stagePosX -= x
        self.stagePosY -= y
        col = (self.stagePosX % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        xOff = (0 - self.stagePosX % self.tileWidth)
        row = (self.stagePosY % (self.tileHeight * len(self.tiles))) // self.tileHeight
        yOff = (0 - self.stagePosY % self.tileHeight)

        col2 = ((self.stagePosX + self.tileWidth) % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        row2 = ((self.stagePosY + self.tileHeight) % (self.tileHeight * len(self.tiles))) // self.tileHeight
        screen.blit(self.tiles[row][col], [xOff, yOff])
        screen.blit(self.tiles[row][col2], [xOff + self.tileWidth, yOff])
        screen.blit(self.tiles[row2][col], [xOff, yOff + self.tileHeight])
        screen.blit(self.tiles[row2][col2], [xOff + self.tileWidth, yOff + self.tileHeight])

        self.surface = screen.copy()

    def setColour(self, colour):
        self.colour = parseColour(colour)
        screen.fill(self.colour)
        pygame.display.update()
        self.surface = screen.copy()

#--------------------end junk

# Intialize the pygame and variables
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)

#variables
score_value = 0
max_horiz = 1600
max_vert = 1200

#junk
screenSize(max_horiz,max_vert)

#functions
def show_debug(txt):
    score = font.render(txt, True, (255, 255, 255))
    screen.blit(score, (50, 50))

# create the screen
screen = pygame.display.set_mode((max_horiz, max_vert))

# Background
mybackground = pygame.image.load('background.png')

# Sound
#mixer.music.load("background.wav") #xxx
#mixer.music.play(-1) #xxx

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImgUp = pygame.image.load('player_up.png')
playerImgDown = pygame.image.load('player_down.png')
player_direction = []
playerX = (max_horiz)/2
playerY = (max_vert)*(2/3)
playerX_change = 0
playerY_change = 0
player_object = playerImgUp 

#sprite sheet
agent = makeSprite("images/player_0.png")
addSpriteImage(agent, "images/player_1.png")

# Enemy
enemyImgR = pygame.image.load('enemyR.png')
enemyImgL = pygame.image.load('enemyL.png')
my_enemy = []

enemyImg = []
enemyPositionX = []
enemyPositionY = []
enemyPositionX_change = []
enemyPositionY_change = []
num_of_enemies = 6

#initialize enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemyR.png'))
    enemyPositionX.append(random.randint(0, max_horiz))
    enemyPositionY.append(random.randint(50, max_vert/2))
    enemyPositionX_change.append(4)
    enemyPositionY_change.append(10)  #was 40
    #show_debug(str(i))

    #creates an array called my_enemy to store images of the fish so that when turtle changes direction, a different image can be stored
    my_enemy.append(enemyImgR)

    #player dirrection array
    player_direction.append(pygame.image.load('player_down.png'))


# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = (max_vert - 100)
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

    
# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(mybackground, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            #move up and down
            if event.key == pygame.K_UP:
                playerY_change = -5
                player_object = playerImgUp
            if event.key == pygame.K_DOWN:
                player_object = playerImgDown
                playerY_change = 5                            

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

                bulletX = playerX
                bulletY = playerY

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX > (max_horiz - 14): #xxx make sure that 14 is correct
        playerX = max_horiz -14

    playerY = playerY + playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY > (max_vert - 14): #xxx make sure that 14 is correct
        playerY = max_vert -14

    # Enemy Movement
    change_dir = 0
    for i in range(num_of_enemies):

        # Game Over
        #if enemyPositionY[i] > 440:
            #for j in range(num_of_enemies):
               #enemyPositionY[j] = 2000
            #game_over_text()
            #break

        if change_dir < 4:
            #time.sleep(1)
            change_dir = change_dir + 1
            #show_debug("aaa")
        else:
            #show_debug("here")
            enemyPositionY[i] = enemyPositionY[i] +  random.randint(-10, 10) #enemyPositionY_change[i] 
            change_dir = 0

        #enemyPositionX[i] += enemyPositionX_change[i]  
        enemyPositionX[i] = enemyPositionX[i] + enemyPositionX_change[i]
       
        if enemyPositionY[i] < 0:
            enemyPositionY[i] = 200

        if enemyPositionY[i] > max_vert:
            enemyPositionY[i] = random.randint(1, 600)

       
        if enemyPositionX[i] <= 0:
            enemyPositionX_change[i] = 2 #was 4
            random.randint(1, 600)
            my_enemy[i] = enemyImgR

            enemyPositionY[i] += enemyPositionY_change[i]
            #enemyPositionY[i] = enemyPositionY[i] +  random.randint(1, 400) #enemyPositionY_change[i] 

        elif enemyPositionX[i] >= (max_horiz - 14): #xxx 
            enemyPositionX_change[i] = -1 #was -4
            my_enemy[i] = enemyImgL

            enemyPositionY[i] = enemyPositionY[i] + enemyPositionY_change[i]
            #enemyPositionY[i] = enemyPositionY[i] +  random.randint(1, 400) #enemyPositionY_change[i] 

        # Collision
        collision = isCollision(enemyPositionX[i], enemyPositionY[i], bulletX, bulletY)
        if collision:
            #explosionSound = mixer.Sound("explosion.wav")
            explosionSound = mixer.Sound("boing.wav")
            explosionSound.play()
            bulletX = playerX
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1

            #spawn new enemy at (0, 0) location
            enemyPositionX[i] = 1000 #max_horiz #random.randint(0, 736)
            enemyPositionY[i] = 1000 #random.randint(50, 150)

        enemy(my_enemy[i], enemyPositionX[i], enemyPositionY[i], i)
        #enemy(enemyImgR, enemyPositionX[i], enemyPositionY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = (max_vert - 150)
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    mytime = time.time()
    #print("mytime", mytime)
    
    bigtime = int(mytime)
    #print("bigtime", bigtime)

    if (bigtime % 2):
        changeSpriteImage(agent, 1)
        playerY = playerY - 0.5
        #print("going up")#; time.sleep(1)
    elif (not bigtime % 7):
        changeSpriteImage(agent, 0)
        playerY = playerY + 1
        #print("going down rare 7")#; time.sleep(1)
    elif (not bigtime % 17):
        changeSpriteImage(agent, 0)
        playerY = playerY + 2
        playerX = playerX + random.randint(-2, 2)
        #print("going down rare 17")#; time.sleep(1)
    else:
        changeSpriteImage(agent, 0)
        playerY = playerY + 0.1
        #print("going down mod 2")#; time.sleep(1)

    player(player_object, playerX, playerY)
    #player(playerX, 100)
    show_score(textX, testY)
    pygame.display.update()
