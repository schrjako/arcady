import pygame
import random

import LevelBuilder as bldr

#------------------------------------------------------------------------------------------------------

pygame.init()
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Edge Case')

#remove window icon
transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 0))
pygame.display.set_icon(transparent_surface)

FILE_NAME = "levels.json"

#------------------------------------------------------------------------------------------------------

class Block:
    def __init__(self, x, y, size, life):
        self.x = x
        self.y = y
        self.size = size

        self.life = life

        self.bottomColor = (150, 150, 150)
        self.topColor = (255, 255, 255)

        self.updateColorByLife()

    def updateColorByLife(self):
        match self.life:
            case 1:
                self.bottomColor = (187, 227, 255)
                self.topColor = (255, 255, 255)
            case 2:
                self.bottomColor = (92, 152, 255)
                self.topColor = (136, 201, 255)
            case 3:
                self.bottomColor = (72, 95, 225)
                self.topColor = (92, 152, 255)
            case 4:
                self.bottomColor = (72, 45, 255)
                self.topColor = (72, 95, 225)
        

    def drawShadow(self):
        pygame.draw.rect(screen, (0, 0, 0), pygame.rect.Rect(self.x - self.size/2 + 20, self.y - self.size/2 + 25, self.size, self.size), 0, 7)

    def drawBottom(self):
        pygame.draw.rect(screen, self.bottomColor, pygame.rect.Rect(self.x - self.size/2, self.y - self.size/2 + 3, self.size, self.size), 0, 7)

    def drawTop(self):
        pygame.draw.rect(screen, self.topColor, pygame.rect.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size), 0, 7)

class BlockGrid:
    def __init__(self, gs, centerX, centerY, width, height, size, margin):
        self.gs = gs

        self.grid = [[None for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height

        self.size = size
        self.margin = margin

        #get total width and height
        totalWidth = width * size + width * margin
        totalHeight = height * size + height * margin

        self.topLeftX = centerX - totalWidth/2 + size/2
        self.topLeftY =  centerY - totalHeight/2 + size/2

    def drawBlocks(self):
        #draw all shadows
        for y in range(self.height):
            for x in range(self.width):
                #draw block if it exists
                if self.grid[y][x] != None:
                    self.grid[y][x].drawShadow()

        #draw all bottoms
        for y in range(self.height):
            for x in range(self.width):
                #draw block if it exists
                if self.grid[y][x] != None:
                    self.grid[y][x].drawBottom()

        #draw all tops
        for y in range(self.height):
            for x in range(self.width):
                #draw block if it exists
                if self.grid[y][x] != None:
                    self.grid[y][x].drawTop()
    
class Player:
    def __init__(self, gs):
        self.gs = gs
        
        self.gx = 1
        self.gy = 1

        self.x = self.gs.blockGrid.topLeftX + self.gx * self.gs.blockGrid.size + self.gx * self.gs.blockGrid.margin
        self.y = self.gs.blockGrid.topLeftY + self.gy * self.gs.blockGrid.size + self.gy * self.gs.blockGrid.margin

        self.size = 25

    def move(self, dir, movements):
        #move for number of movements
        for i in range(movements):
            #checks not required as they were executed in finding the number of movements

            #remove 1 lif from previous or delete
            if self.gs.blockGrid.grid[self.gy][self.gx].life > 1:
                self.gs.blockGrid.grid[self.gy][self.gx].life -= 1
                #update color
                self.gs.blockGrid.grid[self.gy][self.gx].updateColorByLife()
            else:
                self.gs.blockGrid.grid[self.gy][self.gx] = None

            #move to new
            self.gx += dir[0]
            self.gy += dir[1]
            #update world position
            self.x = self.gs.blockGrid.topLeftX + self.gx * self.gs.blockGrid.size + self.gx * self.gs.blockGrid.margin
            self.y = self.gs.blockGrid.topLeftY + self.gy * self.gs.blockGrid.size + self.gy * self.gs.blockGrid.margin

    def findFurthestBlock(self, dir):
        #count how many times the player can move in dir until they reach an empty block
        movements = 0
        igx = self.gx
        igy = self.gy
        #move igx and igy in dir direction until next tile is either out of array or none
        while (igy + dir[1] >= 0 and igy + dir[1] < self.gs.blockGrid.height) and (igx + dir[0] >= 0 and igx + dir[0] < self.gs.blockGrid.width):
            if self.gs.blockGrid.grid[igy + dir[1]][igx + dir[0]] != None:
                igx += dir[0]
                igy += dir[1]
                movements += 1
            else:
                break
        
        #return number of times they can move
        return movements

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), pygame.rect.Rect(self.x - self.size/2, self.y - self.size/2 + 3, self.size + 5, self.size), 0, 7)
        pygame.draw.rect(screen, (100, 0, 200), pygame.rect.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size), 0, 7)
        pygame.draw.rect(screen, (100, 100, 255), pygame.rect.Rect(self.x - self.size/2, self.y - self.size/2 - 4, self.size, self.size), 0, 7)

class GameState:
    def __init__(self):
        self.levelIndex = 1
        self.blockGrid = BlockGrid(self, 400, 300, 9, 9, 50, 5)
        self.player = Player(self)

        #get scene init vars
        self.initDict = bldr.readEntry(FILE_NAME, 0)
        self.numOfLevels = self.initDict["numOfLevels"]

        self.loadLevel(FILE_NAME, self.levelIndex)

    def loadLevel(self, filename, levelIndex):
        level = bldr.readEntry(filename, levelIndex)

        #move player to levels start pos
        self.player.gx = level["playerX"]
        self.player.gy = level["playerY"]

        #update world position
        self.player.x = self.blockGrid.topLeftX + self.player.gx * self.blockGrid.size + self.player.gx * self.blockGrid.margin
        self.player.y = self.blockGrid.topLeftY + self.player.gy * self.blockGrid.size + self.player.gy * self.blockGrid.margin

        #regenerate old grid
        for y in range(self.blockGrid.height):
            for x in range(self.blockGrid.width):
                #get new blocks pos
                newX = self.blockGrid.topLeftX + x * self.blockGrid.size + x * self.blockGrid.margin
                newY = self.blockGrid.topLeftY + y * self.blockGrid.size + y * self.blockGrid.margin
                #generate new block
                self.blockGrid.grid[y][x] = Block(newX, newY, self.blockGrid.size, 1)

        #override grid
        for y in range(self.blockGrid.height):
            for x in range(self.blockGrid.width):

                if level["grid"][y][x] > 0:
                    self.blockGrid.grid[y][x].life = level["grid"][y][x]
                    self.blockGrid.grid[y][x].updateColorByLife()
                else:
                    self.blockGrid.grid[y][x] = None

    def checkForWin(self):
        #check if palyer is on last tile
        tilesLeft = 0
        for y in range(self.blockGrid.width):
            for x in range(self.blockGrid.height):
                if self.blockGrid.grid[y][x] != None:
                    tilesLeft += 1

        if tilesLeft == 1:
            #load next level
            self.levelIndex += 1
            if self.levelIndex > self.numOfLevels:
                self.levelIndex = self.numOfLevels
            self.loadLevel(FILE_NAME, self.levelIndex)

        else:
            #check if player cant move
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            hasWay = False

            for dir in dirs:
                #check if in arrays
                if (self.player.gy + dir[1] >= 0 and self.player.gy + dir[1] < self.blockGrid.height) and (self.player.gx + dir[0] >= 0 and self.player.gx + dir[0] < self.blockGrid.width):
                    #check if tile exists
                    if self.blockGrid.grid[self.player.gy + dir[1]][self.player.gx + dir[0]] != None:
                        hasWay = True
                        break

            if not hasWay:
                #reload same level
                self.loadLevel(FILE_NAME, self.levelIndex)

#------------------------------------------------------------------------------------------------------

prevT = pygame.time.get_ticks()

gs = GameState()

running = True
while running:

    #update delta time
    currT = pygame.time.get_ticks()
    dTms = currT - prevT
    dTs = dTms / 1000.0

    # Fill screen
    screen.fill((30, 30, 30))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            #get direction of movement
            dir = (0, 0)
            if event.key == pygame.K_w:
                dir = (0, -1)
            if event.key == pygame.K_s:
                dir = (0, 1)
            if event.key == pygame.K_a:
                dir = (-1, 0)
            if event.key == pygame.K_d:
                dir = (1, 0)

            #get amount of movements and move
            movements = gs.player.findFurthestBlock(dir)
            gs.player.move(dir, movements)

            #check for win
            gs.checkForWin()

    #draw blocks
    gs.blockGrid.drawBlocks()

    #update player
    gs.player.draw()
    
    # Update the display
    pygame.display.flip()

    #update delta time
    prevT = currT

# Quit Pygame
pygame.quit()
