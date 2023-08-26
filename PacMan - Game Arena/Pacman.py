######################################################################################################################################################
################################################################ Game Setup ##########################################################################
######################################################################################################################################################
import pygame
import sys
import math
import copy
from board import boards
pygame.init()

################################################################ Window Settings #####################################################################
width = 900
height = 950
screen = pygame.display.set_mode(
    (width, height))
################################################################ Game Settings #####################################################################
clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 20)
level = copy.deepcopy(boards)
lineColour = (0, 0, 255)
pi = math.pi
moving = False
startUpCounter = 0

################################################################ Scoring System #####################################################################
flicker = False
score = 0
powerUp = False
powerCounter = 0
ghostEaten = [False, False, False, False]

gameOver = False

gameWon = False

#  .----------------.
# | .--------------. |
# | |      _       | |
# | |     | |      | |
# | |     | |      | |
# | |     | |      | |
# | |     |_|      | |
# | |     (_)      | |
# | '--------------' |
#  '----------------'
# Draw the player score to the screen

#  .----------------.
# | .--------------. |
# | |      _       | |
# | |     | |      | |
# | |     | |      | |
# | |     | |      | |
# | |     |_|      | |
# | |     (_)      | |
# | '--------------' |
#  '----------------'
# Handle a "you win" event


################################################################ Lives Management #####################################################################
lives = 3


#  .----------------.
# | .--------------. |
# | |      _       | |
# | |     | |      | |
# | |     | |      | |
# | |     | |      | |
# | |     |_|      | |
# | |     (_)      | |
# | '--------------' |
#  '----------------'
# Draw the remaining player lives. Use pictures of the player to indicate how many lives are left, instead of numbers.

#  .----------------.
# | .--------------. |
# | |      _       | |
# | |     | |      | |
# | |     | |      | |
# | |     | |      | |
# | |     |_|      | |
# | |     (_)      | |
# | '--------------' |
#  '----------------'
# Handle a game over event


################################################################ Collision Detection #####################################################################


def checkCollision(scor, power, power_count, eaten_ghosts):
    tileHeight = (height - 50) // 32
    tileWidth = width // 30
    if 0 < playerX < 870:
        if level[centerY // tileHeight][centerX // tileWidth] == 1:
            level[centerY // tileHeight][centerX // tileWidth] = 0
            scor += 10
        if level[centerY // tileHeight][centerX // tileWidth] == 2:
            level[centerY // tileHeight][centerX // tileWidth] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts

################################################################ Drawing the board #####################################################################


def drawBoard(level):
    tileHeight = ((height - 50)//32)  # how tall each tile should be
    tileWidth = ((width // 30))  # how wide each tile should be

    # iterates through every row in the level
    for row in range(len(level)):
        # iterates through every element of each row in the level
        for tileType in range(len(level[row])):

            # Small dots
            if level[row][tileType] == 1:
                pygame.draw.circle(screen, 'white', (tileType*tileWidth +
                                   (0.5 * tileWidth), row*tileHeight + (0.5 * tileHeight)), 4)
                # Clarification
                # j*tileWidth = the element in the current row being drawn and its x position
                # (0.5 * tileWidth) = makes sure the dot is drawn in the center of the tile
                # i*tileHeight = the y position
                # (0.5 * tileHeight) = center y position

            # Power Dots
            if level[row][tileType] == 2 and not flicker:
                pygame.draw.circle(
                    screen, 'white', (tileType*tileWidth + (0.5 * tileWidth), row*tileHeight + (0.5 * tileHeight)), 10)

            #  .----------------.
            # | .--------------. |
            # | |      _       | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     |_|      | |
            # | |     (_)      | |
            # | '--------------' |
            #  '----------------'
            # Draw the map with the following conditions
            # Verticle Lines = 3
            # Horizontal Lines = 4
            # Curved Lines (top right quarter of a circle) = 5
            # Curved Lines (top left quarter of a circle) = 6
            # Curved Lines (bottom left quarter of a circle) = 7
            # Curved Lines (bottom right quarter of a circle) = 8
            # Ghost Door = 9


################################################################ Adding the player #####################################################################
playerImages = []
for i in range(1, 5):
    playerImages.append(pygame.transform.scale(
        pygame.image.load(f'Assets/Player/{i}.png'), (45, 45)))

# Starting position
playerX = 450
playerY = 663
direction = 0
counter = 0
playerSpeed = 2
validTurns = [False, False, False, False]
directionCommand = 0


def drawPlayer():

    # Right
    if direction == 0:
        screen.blit(playerImages[counter//5], (playerX, playerY))

    # Left
    if direction == 1:
        screen.blit(pygame.transform.flip(
            playerImages[counter//5], True, False), (playerX, playerY))

    # Up
    if direction == 2:
        screen.blit(pygame.transform.rotate(
            playerImages[counter//5], 90), (playerX, playerY))

    # Down
    if direction == 3:
        screen.blit(pygame.transform.rotate(
            playerImages[counter//5], 270), (playerX, playerY))


def checkPosition(centerx, centery):
    turns = [False, False, False, False]
    tileHeight = (height - 50) // 32
    tileWidth = (width // 30)
    buffer = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // tileHeight][(centerx - buffer) // tileWidth] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // tileHeight][(centerx + buffer) // tileWidth] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + buffer) // tileHeight][centerx // tileWidth] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - buffer) // tileHeight][centerx // tileWidth] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % tileWidth <= 18:
                if level[(centery + buffer) // tileHeight][centerx // tileWidth] < 3:
                    turns[3] = True
                if level[(centery - buffer) // tileHeight][centerx // tileWidth] < 3:
                    turns[2] = True
            if 12 <= centery % tileHeight <= 18:
                if level[centery // tileHeight][(centerx - tileWidth) // tileWidth] < 3:
                    turns[1] = True
                if level[centery // tileHeight][(centerx + tileWidth) // tileWidth] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % tileWidth <= 18:
                if level[(centery + tileHeight) // tileHeight][centerx // tileWidth] < 3:
                    turns[3] = True
                if level[(centery - tileHeight) // tileHeight][centerx // tileWidth] < 3:
                    turns[2] = True
            if 12 <= centery % tileHeight <= 18:
                if level[centery // tileHeight][(centerx - buffer) // tileWidth] < 3:
                    turns[1] = True
                if level[centery // tileHeight][(centerx + buffer) // tileWidth] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


#  .----------------.
# | .--------------. |
# | |      _       | |
# | |     | |      | |
# | |     | |      | |
# | |     | |      | |
# | |     |_|      | |
# | |     (_)      | |
# | '--------------' |
#  '----------------'
# Make the player move

################################################################ Adding the ghosts #####################################################################


redGhostX = width/2
redGhostY = height/2 - 50
redGhostDirection = 0
redDead = False
redBox = False
redGhost = pygame.transform.scale(
    pygame.image.load(f'Assets/Enemies/red.png'), (45, 45))

blueGhostX = width/2 + 50
blueGhostY = height/2 - 70
blueGhostDirection = 0
blueDead = False
blueBox = False
blueGhost = pygame.transform.scale(
    pygame.image.load(f'Assets/Enemies/blue.png'), (45, 45))

orangeGhostX = width/2 - 50
orangeGhostY = height/2 - 50
orangeGhostDirection = 0
orangeDead = False
orangeBox = False
orangeGhost = pygame.transform.scale(
    pygame.image.load(f'Assets/Enemies/orange.png'), (45, 45))

pinkGhostX = width/2 - 100
pinkGhostY = height/2 - 70
pinkGhostDirection = 0
pinkDead = False
pinkBox = False
pinkGhost = pygame.transform.scale(
    pygame.image.load(f'Assets/Enemies/pink.png'), (45, 45))

deadGhostX = 56
deadGhostY = 58
deadGhostDirection = 0
deadGhost = pygame.transform.scale(
    pygame.image.load(f'Assets/Enemies/dead.png'), (45, 45))

ghostSpeeds = [2, 2, 2, 2]
targets = [(playerX, playerY), (playerX, playerY),
           (playerX, playerY), (playerX, playerY)]

threatenedGhostX = 56
threatenedGhostY = 58
threatenedGhostDirection = 0
threatenedGhost = pygame.transform.scale(
    pygame.image.load(f'Assets/Enemies/powerup.png'), (45, 45))


class Ghost:
    def __init__(self, x, y, target, speed, body, direction, dead, box, name):
        self.x = x
        self.y = y
        self.centerX = self.x + 22
        self.centerY = self.y + 22
        self.target = target
        self.speed = speed
        self.body = body
        self.direction = direction
        self.dead = dead
        self.box = box
        self.name = name
        self.turns, self.box = self.checkCollisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerUp and not self.dead) or (ghostEaten[self.name] and powerUp and not self.dead):
            screen.blit(self.body, (self.x, self.y))
        elif powerUp and not self.dead and not ghostEaten[self.name]:
            screen.blit(threatenedGhost, (self.x, self.y))
        else:
            screen.blit(deadGhost, (self.x, self.y))

        # Ghost hitbox
        ghostRectangle = pygame.rect.Rect((
            self.centerX - 18, self.centerY - 18), (36, 36))

        return ghostRectangle

    # Ghost wall collision detection
    def checkCollisions(self):
        tileHeight = ((height - 50) // 32)
        tileWidth = (width // 30)
        buffer = 15
        self.turns = [False, False, False, False]
        if 0 < self.centerX // 30 < 29:
            if level[int((self.centerY - buffer) // tileHeight)][int(self.centerX // tileWidth)] == 9:
                self.turns[2] = True
            if level[int(self.centerY // tileHeight)][int((self.centerX - buffer) // tileWidth)] < 3 \
                or (level[int(self.centerY // tileHeight)][(int(self.centerX - buffer) // tileWidth)] == 9 and (
                    self.box or self.dead)):
                self.turns[1] = True
            if level[int(self.centerY // tileHeight)][int((self.centerX + buffer) // tileWidth)] < 3 \
                    or (level[int(self.centerY // tileHeight)][int((self.centerX + buffer) // tileWidth)] == 9 and (
                    self.box or self.dead)):
                self.turns[0] = True
            if level[int((self.centerY + buffer) // tileHeight)][int(self.centerX // tileWidth)] < 3 \
                    or (level[int((self.centerY + buffer) // tileHeight)][int(self.centerX // tileWidth)] == 9 and (
                    self.box or self.dead)):
                self.turns[3] = True
            if level[int((self.centerY - buffer) // tileHeight)][int(self.centerX // tileWidth)] < 3 \
                    or (level[int((self.centerY - buffer) // tileHeight)][int(self.centerX // tileWidth)] == 9 and (
                    self.box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.centerX % tileWidth <= 18:
                    if level[int((self.centerY + buffer) // tileHeight)][int(self.centerX // tileWidth)] < 3 \
                            or (level[(int(self.centerY + buffer) // tileHeight)][int(self.centerX // tileWidth)] == 9 and (
                            self.box or self.dead)):
                        self.turns[3] = True
                    if level[int((self.centerY - buffer) // tileHeight)][int(self.centerX // tileWidth)] < 3 \
                            or (level[(int(self.centerY - buffer) // tileHeight)][int(self.centerX // tileWidth)] == 9 and (
                            self.box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.centerY % tileHeight <= 18:
                    if level[int(self.centerY // tileHeight)][int((self.centerX - tileWidth) // tileWidth)] < 3 \
                            or (level[int(self.centerY // tileHeight)][int((self.centerX - tileWidth) // tileWidth)] == 9 and (
                            self.box or self.dead)):
                        self.turns[1] = True
                    if level[int(self.centerY // tileHeight)][int((self.centerX + tileWidth) // tileWidth)] < 3\
                            or (level[int(self.centerY // tileHeight)][int((self.centerX + tileWidth) // tileWidth)] == 9 and (
                            self.box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.centerX % tileWidth <= 18:
                    if level[(int(self.centerY + buffer) // tileHeight)][int(self.centerX // tileWidth)] < 3 \
                            or (level[(int(self.centerY + buffer) // tileHeight)][int(self.centerX // tileWidth)] == 9 and (
                            self.box or self.dead)):
                        self.turns[3] = True
                    if level[int((self.centerY - buffer) // tileHeight)][int(self.centerX // tileWidth)] < 3 \
                            or (level[(int(self.centerY - buffer) // tileHeight)][int(self.centerX // tileWidth)] == 9 and (
                            self.box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.centerY % tileHeight <= 18:
                    if level[int(self.centerY // tileHeight)][int((self.centerX - buffer) // tileWidth)] < 3 \
                            or (level[int(self.centerY // tileHeight)][int((self.centerX - buffer) // tileWidth)] == 9 and (
                            self.box or self.dead)):
                        self.turns[1] = True
                    if level[int(self.centerY // tileHeight)][int((self.centerX + buffer) // tileWidth)] < 3 \
                            or (level[int(self.centerY // tileHeight)][int((self.centerX + buffer) // tileWidth)] == 9 and (
                            self.box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True

        # Check whether ghost is in the box or not
        if 350 < self.x < 550 and 370 < self.y < 480:
            self.box = True
        else:
            self.box = False
        return self.turns, self.box

    def moveBlue(self):
        # Moves whenever advantageous

        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x += self.speed

        elif self.direction == 1:
            if self.target[1] > self.y and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                if self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                else:
                    self.x -= self.speed

        elif self.direction == 2:
            if self.target[0] < self.x and self.turns[1]:
                self.direction = 1
                self.x -= self.speed
            elif self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y -= self.speed

        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y += self.speed
        if self.x < -30:
            self.x = width
        elif self.x > width:
            self.x = -30
        return self.x, self.y, self.direction

    def moveRed(self):
        # Changes direction only when hits wall

        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                self.x += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                self.x -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[2]:
                self.y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[3]:
                self.y += self.speed
        if self.x < -30:
            self.x = width
        elif self.x > width:
            self.x = -30
        return self.x, self.y, self.direction

    def moveOrange(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x and self.turns[0]:
                self.x += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
            elif self.turns[0]:
                self.x += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x and self.turns[1]:
                self.x -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[1]:
                self.x -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x and self.turns[1]:
                self.direction = 1
                self.x -= self.speed
            elif self.target[1] < self.y and self.turns[2]:
                self.direction = 2
                self.y -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] > self.y and self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y and self.turns[3]:
                self.y += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.target[1] < self.y and self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x and self.turns[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.target[0] < self.x and self.turns[1]:
                    self.direction = 1
                    self.x -= self.speed
                else:
                    self.y += self.speed
        if self.x < -30:
            self.x = width
        elif self.x > width:
            self.x - 30
        return self.x, self.y, self.direction

    #  .----------------.
    # | .--------------. |
    # | |      _       | |
    # | |     | |      | |
    # | |     | |      | |
    # | |     | |      | |
    # | |     |_|      | |
    # | |     (_)      | |
    # | '--------------' |
    #  '----------------'
    # add a movement algoritham for pink


def getTargets(blueGhostX, blueGhostY, redGhostX, redGhostY,
               orangeGhostX, orangeGhostY, pinkGhostX, pinkGhostY):

    if playerX < 450:
        runawayX = width
    else:
        runawayX = 0

    if playerY < 450:
        runawayY = width
    else:
        runawayY = 0

    returnTarget = (380, 400)

    if powerUp:
        if not blue.dead and not ghostEaten[0]:
            blueTarget = (runawayX, runawayY)
        elif not blue.dead and ghostEaten[0]:
            if 340 < blueGhostX < 560 and 340 < blueGhostY < 500:
                blueTarget = (400, 100)
            else:
                blueTarget = (playerX, playerY)
        else:
            blueTarget = returnTarget

        if not red.dead and not ghostEaten[1]:
            redTarget = (runawayX, playerY)
        elif not red.dead and ghostEaten[1]:
            if 340 < redGhostX < 560 and 340 < redGhostY < 500:
                redTarget = (400, 100)
            else:
                redTarget = (playerX, playerY)
        else:
            redTarget = returnTarget

        if not orange.dead:
            orangeTarget = (playerX, runawayY)
        elif not orange.dead and ghostEaten[2]:
            if 340 < orangeGhostX < 560 and 340 < orangeGhostY < 500:
                orangeTarget = (400, 100)
            else:
                orangeTarget = (playerX, playerY)
        else:
            orangeTarget = returnTarget

        if not pink.dead and not ghostEaten[3]:
            pinkTarget = (450, 450)
        elif not pink.dead and ghostEaten[3]:
            if 340 < pinkGhostX < 560 and 340 < pinkGhostY < 500:
                pinkTarget = (400, 100)
            else:
                pinkTarget = (playerX, playerY)
        else:
            pinkTarget = returnTarget

    else:

        if not blue.dead:
            if 340 < blueGhostX < 560 and 340 < blueGhostY < 500:
                blueTarget = (400, 100)
            else:
                blueTarget = (playerX, playerY)
        else:
            blueTarget = returnTarget

        if not red.dead:
            if 340 < redGhostX < 560 and 340 < redGhostY < 500:
                redTarget = (400, 100)
            else:
                redTarget = (playerX, playerY)
        else:
            redTarget = returnTarget

        if not orange.dead:
            if 340 < orangeGhostX < 560 and 340 < orangeGhostY < 500:
                orangeTarget = (400, 100)
            else:
                orangeTarget = (playerX, playerY)
        else:
            orangeTarget = returnTarget

        if not pink.dead:
            if 340 < pinkGhostX < 560 and 340 < pinkGhostY < 500:
                pinkTarget = (400, 100)
            else:
                pinkTarget = (playerX, playerY)
        else:
            pinkTarget = returnTarget

    return [blueTarget, redTarget, orangeTarget, pinkTarget]


while True:

    for event in pygame.event.get():
        ################################################################ Safe Exit Mechanic ##################################################################
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        ################################################################ Player movement and Orientation ##################################################################
        # When the key is pressed, a command is given to orientate player in the desired way
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                directionCommand = 0

            if event.key == pygame.K_LEFT:
                directionCommand = 1

            if event.key == pygame.K_UP:
                directionCommand = 2

            if event.key == pygame.K_DOWN:
                directionCommand = 3

            #  .----------------.
            # | .--------------. |
            # | |      _       | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     |_|      | |
            # | |     (_)      | |
            # | '--------------' |
            #  '----------------'
            # If the game is over, or the game is won, press the space bar to reset and restart the game

    # A check is made to see if the player can indeed move in that direction.
    # The command will only execute if/when the move is possible.
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT and direction == 0:
            directionCommand = direction

        if event.key == pygame.K_LEFT and direction == 1:
            directionCommand = direction

        if event.key == pygame.K_UP and direction == 2:
            directionCommand = direction

        if event.key == pygame.K_DOWN and direction == 3:
            directionCommand = direction

    for i in range(4):
        if directionCommand == i and validTurns[i]:
            direction = i

    screen.fill(('black'))
    drawBoard(level)
    centerX = playerX + 23
    centerY = playerY + 24
    if powerUp:
        ghostSpeeds = [1, 1, 1, 1]

    else:
        ghostSpeeds = [2, 2, 2, 2]

    if ghostEaten[0]:
        ghostSpeeds[0] = 2

    if ghostEaten[1]:
        ghostSpeeds[1] = 2

    if ghostEaten[2]:
        ghostSpeeds[2] = 2

    if ghostEaten[3]:
        ghostSpeeds[3] = 2

    if blueDead:
        ghostSpeeds[0] = 4

    if redDead:
        ghostSpeeds[1] = 4

    if orangeDead:
        ghostSpeeds[2] = 4

    if pinkDead:
        ghostSpeeds[3] = 4

    gameWon = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            gameWon = False

    playerHitBox = pygame.draw.circle(
        screen, 'black', (centerX, centerY), 15, 1)

    drawPlayer()

    blue = Ghost(blueGhostX, blueGhostY,
                 targets[0], ghostSpeeds[0], blueGhost, blueGhostDirection, blueDead, blueBox, 0)
    red = Ghost(redGhostX, redGhostY,
                targets[1], ghostSpeeds[1], redGhost, redGhostDirection, redDead, redBox, 1)
    orange = Ghost(orangeGhostX, orangeGhostY,
                   targets[2], ghostSpeeds[2], orangeGhost, orangeGhostDirection, orangeDead, orangeBox, 2)
    pink = Ghost(pinkGhostX, pinkGhostY,
                 targets[3], ghostSpeeds[3], pinkGhost, pinkGhostDirection, pinkDead, pinkBox, 3)

    targets = getTargets(blueGhostX, blueGhostY, redGhostX, redGhostY,
                         orangeGhostX, orangeGhostY, pinkGhostX, pinkGhostY)
    validTurns = checkPosition(centerX, centerY)
    if moving:
        playerX, playerY = movePlayer(playerX, playerY)
        blueGhostX, blueGhostY, blueGhostDirection = blue.moveBlue()

        if not redDead and not red.box:
            redGhostX, redGhostY, redGhostDirection = red.moveRed()
        else:
            redGhostX, redGhostY, redGhostDirection = red.moveBlue()

        if not orangeDead and not orange.box:
            orangeGhostX, orangeGhostY, orangeGhostDirection = orange.moveOrange()
        else:
            orangeGhostX, orangeGhostY, orangeGhostDirection = orange.moveBlue()

        if not pinkDead and not pink.box:
            pinkGhostX, pinkGhostY, pinkGhostDirection = pink.movePink()
        else:
            pinkGhostX, pinkGhostY, pinkGhostDirection = pink.moveBlue()

    score, powerUp, powerCounter, ghostEaten = checkCollision(
        score, powerUp, powerCounter, ghostEaten)

    if not powerUp:
        if (playerHitBox.colliderect(blue.rect) and not blueDead) or \
            (playerHitBox.colliderect(red.rect) and not redDead) or \
            (playerHitBox.colliderect(orange.rect) and not orangeDead) or \
                (playerHitBox.colliderect(pink.rect) and not pinkDead):
            if lives > 0:
                # .----------------.
                # | .--------------. |
                # | |      _       | |
                # | |     | |      | |
                # | |     | |      | |
                # | |     | |      | |
                # | |     |_|      | |
                # | |     (_)      | |
                # | '--------------' |
                #  '----------------'
                # the player dies, but still has lives, set everything back up and get ready to play again.
                # no points are to be deducted. balls that were eaten are not to spawn back in

            else:
                gameOver = True
                moving = False
                startupCounter = 0

    if powerUp and playerHitBox.colliderect(blue.rect) and ghostEaten[0] and not blue.dead:
        if lives > 0:
            # .----------------.
            # | .--------------. |
            # | |      _       | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     |_|      | |
            # | |     (_)      | |
            # | '--------------' |
            #  '----------------'
            # the player dies, but still has lives, set everything back up and get ready to play again.
            # no points are to be deducted. balls that were eaten are not to spawn back in

        else:
            gameOver = True
            moving = False
            startupCounter = 0

    if powerUp and playerHitBox.colliderect(red.rect) and ghostEaten[1] and not red.dead:
        if lives > 0:
            # .----------------.
            # | .--------------. |
            # | |      _       | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     |_|      | |
            # | |     (_)      | |
            # | '--------------' |
            #  '----------------'
            # the player dies, but still has lives, set everything back up and get ready to play again.
            # no points are to be deducted. balls that were eaten are not to spawn back in

        else:
            gameOver = True
            moving = False
            startupCounter = 0

    if powerUp and playerHitBox.colliderect(orange.rect) and ghostEaten[2] and not orange.dead:
        if lives > 0:
            # .----------------.
            # | .--------------. |
            # | |      _       | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     |_|      | |
            # | |     (_)      | |
            # | '--------------' |
            #  '----------------'
            # the player dies, but still has lives, set everything back up and get ready to play again.
            # no points are to be deducted. balls that were eaten are not to spawn back in

        else:
            gameOver = True
            moving = False
            startupCounter = 0

    if powerUp and playerHitBox.colliderect(pink.rect) and ghostEaten[3] and not pink.dead:
        if lives > 0:
            # .----------------.
            # | .--------------. |
            # | |      _       | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     | |      | |
            # | |     |_|      | |
            # | |     (_)      | |
            # | '--------------' |
            #  '----------------'
            # the player dies, but still has lives, set everything back up and get ready to play again.
            # no points are to be deducted. balls that were eaten are not to spawn back in

        else:
            gameOver = True
            moving = False
            startupCounter = 0

    if powerUp and playerHitBox.colliderect(blue.rect) and not blueDead and not ghostEaten[0]:
        blueDead = True
        ghostEaten[0] = True
        score += (2 ** ghostEaten.count(True)) * 100

    if powerUp and playerHitBox.colliderect(red.rect) and not redDead and not ghostEaten[1]:
        redDead = True
        ghostEaten[1] = True
        score += (2 ** ghostEaten.count(True)) * 100

    if powerUp and playerHitBox.colliderect(orange.rect) and not orangeDead and not ghostEaten[2]:
        orangeDead = True
        ghostEaten[2] = True
        score += (2 ** ghostEaten.count(True)) * 100

    if powerUp and playerHitBox.colliderect(pink.rect) and not pinkDead and not ghostEaten[3]:
        pinkDead = True
        ghostEaten[3] = True
        score += (2 ** ghostEaten.count(True)) * 100

    drawScore()
    drawLives()
    if gameOver:
        gameOverScreen()

    # This updates only the sections of the screen that have been explicitly marked for updating.
    # pygame.display.flip() could also be used, but it updates the entire screen, instead of just sections of it.
    pygame.display.update()

    # .----------------.
    # | .--------------. |
    # | |      _       | |
    # | |     | |      | |
    # | |     | |      | |
    # | |     | |      | |
    # | |     |_|      | |
    # | |     (_)      | |
    # | '--------------' |
    #  '----------------'
    # Bring the ghosts back to life at an appropriate time

    # .----------------.
    # | .--------------. |
    # | |      _       | |
    # | |     | |      | |
    # | |     | |      | |
    # | |     | |      | |
    # | |     |_|      | |
    # | |     (_)      | |
    # | '--------------' |
    #  '----------------'
    # Allow the player to warp to the other side of the map when going through the portal

    # Limits frame rate to 60 fps
    clock.tick(60)

    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerUp and powerCounter < 600:
        powerCounter += 1
    elif powerUp and powerCounter >= 600:
        powerCounter = 0
        powerUp = False
        ghostEaten = [False, False, False, False]

    if startUpCounter < 180 and not gameOver and not gameWon:
        moving = False
        startUpCounter += 1
    else:
        moving = True
