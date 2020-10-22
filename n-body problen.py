# N-Body Problem.py
# Denis Titov 29.11.2018

import pygame
from pygame import gfxdraw
import random
from numba import jit
import numpy as np


numParticles = 2000

displaySize = (1000, 1000)

massSpread = (2, 20)

black = (255, 255, 255)
white = (0, 0, 0)


def generate(numParticles, velSpread=100, posSpread=100, massSpread=(2, 8)):
    particleList = []
    for i in range(numParticles):
        # empty list. will be: [yPos, yPos, xVel, yVel, xAcc, yAcc mass]
        particleInfo = []
        # pos according to display size
        xPos = (random.randrange(posSpread)) + 500 - (posSpread / 2)
        yPos = (random.randrange(posSpread)) + 500 - (posSpread / 2)
        # 1 velspread is 1/100 pixel
        xVel = (random.randrange(velSpread) / 100)
        yVel = (random.randrange(velSpread) / 100)
        # mass is random int
        mass = random.randrange(massSpread[0], (massSpread[1] + 1))
        # append to info
        particleInfo.append(xPos)
        particleInfo.append(yPos)
        particleInfo.append(xVel)
        particleInfo.append(yVel)
        particleInfo.append(mass)
        # put info into main list
        particleList.append(particleInfo)

    return particleList

#numpy + numba approach [xPos, yPos, xVel, yVel, mass]
@jit()
def nBodyNumpyNumba(particleList):
    for i in range(len(particleList)):
        xAccList = np.zeros(particleList.shape[0])
        yAccList = np.zeros(particleList.shape[0])
        # for every other particle calculations to get current acc
        for j in range(len(particleList)):
            if not i == j:
                # distance in respective dimension
                xDist = particleList[j, 0] - particleList[i, 0] # otherXPos - thisXPos
                yDist = particleList[j, 1] - particleList[i, 1] # otherYPos - thisYPos
                # pythagorean theorem to get real distance
                dist = ((xDist**2 + yDist**2)**0.5) + 20
                # calc acceleration
                acc = (particleList[i, 4] * particleList[j, 4]) / (dist**2 * particleList[i, 4]) * 0.05
                xAcc = (xDist / dist) * acc
                yAcc = (yDist / dist) * acc

                xAccList[j] = xAcc
                yAccList[j] = yAcc
        
        # sums all elements in AccLists to total acc
        xAccCurrent = np.sum(xAccList)
        yAccCurrent = np.sum(yAccList)

        # adds accs to vels
        particleList[i, 2] += xAccCurrent
        particleList[i, 3] += yAccCurrent

        # adds vels to poss
        particleList[i, 0] += particleList[i, 2]
        particleList[i, 1] += particleList[i, 3]

    # calculate center of mass (mass ignored)
    xMove = 500 - np.sum(particleList[:, 0]) / len(particleList)
    yMove = 500 - np.sum(particleList[:, 1]) / len(particleList)

    particleList[:, 0] += xMove
    particleList[:, 1] += yMove

    return particleList

def draw(XPos, YPos, mass):
    #pygame.gfxdraw.aacircle(gameDisplay, int(XPos), int(YPos), int(mass / 2), black)
    pygame.gfxdraw.filled_circle(gameDisplay, int(XPos), int(YPos), int(mass / 5), black)


gameDisplay = pygame.display.set_mode((displaySize))
pygame.display.set_caption("N-Body Problem")
clock = pygame.time.Clock()

# Particle Init
gameDisplay.fill(white)
particleList = []
# set properties to particle list (xpos, ypos, xvel, yvel, mass)
particleList = np.array(generate(numParticles))


# main loop
closed = False
while not closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True

    # remove old particles
    gameDisplay.fill(white)

    # Loop for particle handling
    nBodyNumpyNumba(particleList)


    for i in range(len(particleList)):
        draw(particleList[i][0], particleList[i][1], particleList[i][4])

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
