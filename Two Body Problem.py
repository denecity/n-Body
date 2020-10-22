# Two Body Problem.py
# Denis Titov 20.11.2018

import pygame
from pygame import gfxdraw
import random

displaySize = (800, 800)

spawnAreaX1 = int(displaySize[0] * 7 / 16)
spawnAreaX2 = int(displaySize[0] * 9 / 16)

spawnAreaY1 = int(displaySize[1] * 7 / 16)
spawnAreaY2 = int(displaySize[1] * 9 / 16)

# 2 masses with random mass, velocity and position get spawned
mass1 = random.randrange(2, 25)
mass2 = random.randrange(2, 25)

mass1XPos = random.randrange(spawnAreaX1, spawnAreaX2)
mass1YPos = random.randrange(spawnAreaY1, spawnAreaY2)

mass1XVel = random.randrange(-100, 100) / 100
mass1YVel = random.randrange(-100, 100) / 100

mass1Acc = ()

mass2XPos = random.randrange(spawnAreaX1, spawnAreaX2)
mass2YPos = random.randrange(spawnAreaY1, spawnAreaY2)

mass2XVel = -1 * mass1XVel  # random.randrange(-100, 100) / 100
mass2YVel = -1 * mass1YVel  # random.randrange(-100, 100) / 100

mass2Acc = ()

black = (0, 0, 0)
white = (255, 255, 255)


# acceleration function
def gravityAcc(thisXPos, thisYPos, thisMass, otherXPos, otherYPos, otherMass):

    # calculate distances of masses
    distX = otherXPos - thisXPos
    distY = otherYPos - thisYPos

    # calculate real distance
    dist = ((distX**2 + distY**2)**0.5) + 2

    # implement mass mass
    acc = 5 * thisMass * otherMass / (dist * thisMass**2)

    # create X and Y verctor from total acceleration
    XAcc = acc * (distX / dist) / 2
    YAcc = acc * (distY / dist) / 2

    return (XAcc, YAcc)


# mass graphic function
def drawMass(XPos, YPos, mass):
    pygame.gfxdraw.aacircle(gameDisplay, XPos, YPos, int(mass / 2), black)
    pygame.gfxdraw.filled_circle(gameDisplay, XPos, YPos, int(mass / 2), black)


# setup display
gameDisplay = pygame.display.set_mode((displaySize))
pygame.display.set_caption("Two Body Problem")
clock = pygame.time.Clock()

# main loop
closed = False
while not closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True

    gameDisplay.fill(white)

    # draw masses
    drawMass(XPos=int(mass1XPos), YPos=int(mass1YPos), mass=mass1)
    drawMass(XPos=int(mass2XPos), YPos=int(mass2YPos), mass=mass2)

    # get acceleration based on gravity
    mass1Acc = gravityAcc(mass1XPos, mass1YPos, mass1, mass2XPos, mass2YPos, mass2)
    mass2Acc = gravityAcc(mass2XPos, mass2YPos, mass2, mass1XPos, mass1YPos, mass1)

    # add new acceleration
    mass1XVel += mass1Acc[0]
    mass1YVel += mass1Acc[1]

    # deterioration
    mass1XVel *= 0.9995
    mass1YVel *= 0.9995

    # add new acceleration
    mass2XVel += mass2Acc[0]
    mass2YVel += mass2Acc[1]

    # deterioration
    mass2XVel *= 0.9995
    mass2YVel *= 0.9995

    # calculate position
    mass1XPos += mass1XVel
    mass1YPos += mass1YVel

    mass2XPos += mass2XVel
    mass2YPos += mass2YVel

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()


# def acc(thisXPos, thisYPos, thisMass, otherXPos, otherYPos, otherMass):

# particle list for each particle (xpos, ypos, xvel, yvel, mass)
