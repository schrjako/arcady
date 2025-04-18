#-------------------------------------------------------------------------------------------
import json

def initFile(filename):
    """Initialize a json file with the filename name if it doesnt already exist"""
    import os
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, 'w') as file:
            json.dump([], file)

def readData(filename):
    """Read json file contents as an array of dictionaries"""
    with open(filename, "r") as file:
        return json.load(file)
    
def addEntry(filename, entry):
    """When the index dictionary doesnt exist already it appends it, otherwise it replaces the old preexisting one with the new dictionary"""
    data = readData(filename)
    updated = False

    for i, item in enumerate(data):
        if item.get('index') == entry.get('index'):
            data[i] = entry
            updated = True
            break

    if not updated:
        data.append(entry)

    with open(filename, 'w') as file:
        json.dump(data, file)

def removeEntry(filename, index):
    """Deletes existing dictionary"""
    data = readData(filename)
    data = [item for item in data if item["index"] != index]
    with open(filename, "w") as file:
        json.dump(data, file)

def readEntry(filename, index):
    """Reads as dictionary"""
    data = readData(filename)
    for item in data:
        if item["index"] == index:
            return item
        
#-------------------------------------------------------------------------------------------
class Grid:
    def __init__(self, centerX, centerY, width, height, size, margin):
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
        
        self.playerGX = 0
        self.playerGY = 0
        self.playerX = 0
        self.playerY = 0
        
        self.displayLevel = 1
        
        #initial level load
        self.loadLevel()

    def drawBlocks(self):
        for y in range(self.height):
            for x in range(self.width):
                #draw block if it exists
                if self.grid[y][x] != None:
                    self.grid[y][x].draw()

    def drawPlayer(self):
        pygame.draw.rect(screen, (100, 100, 255), pygame.rect.Rect(self.playerX - 25/2, self.playerY - 25/2, 25, 25), 0, 7)
    
    def loadLevel(self):
        level = readEntry(FILE_NAME, self.displayLevel)
        #place player
        self.playerGX = level["playerX"]
        self.playerGY = level["playerY"]
        self.playerX = self.topLeftX + self.playerGX * self.size + self.playerGX * self.margin
        self.playerY = self.topLeftY + self.playerGY * self.size + self.playerGY * self.margin
        
        #regenerate grid
        for y in range(self.height):
            for x in range(self.width):
                #get new blocks pos
                newX = self.topLeftX + x * self.size + x * self.margin
                newY = self.topLeftY + y * self.size + y * self.margin
                #generate new block
                self.grid[y][x] = Block(newX, newY, self.size, 1)

        #override grid
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].life = level["grid"][y][x]
                self.grid[y][x].updateColorByLife()

    def addLevel(self):
        #move all further levels 1 right
        #get all levels
        levels = readData(FILE_NAME)
        
        #sort by levels that are further or equal selected
        furtherLevels = []
        for level in levels:
            if level["index"] >= self.displayLevel:
                furtherLevels.append(level)

        #modify their index to index + 1
        modifiedLevelsToAdd = []
        for level in furtherLevels:
            modifiedLevel = level   #copy level
            modifiedLevel["index"] = modifiedLevel["index"] + 1 #move right in chain of levels
            modifiedLevelsToAdd.append(modifiedLevel)   #append to queue to ovveride the previous levels

        #override previous levels with modified levels
        for modifiedLevel in modifiedLevelsToAdd:
            addEntry(FILE_NAME, modifiedLevel)

        #create empty level as displaylevel
        newLevel = {
            "index": self.displayLevel,
            "playerX": 0,
            "playerY": 0,
            "grid": [[0 for x in range(self.width)] for y in range(self.height)]
        }

        #override previous displaylevel with empty level
        addEntry(FILE_NAME, newLevel)

        #update num of levels
        chainStats = readEntry(FILE_NAME, 0)    #stats of the level chain like num of levels
        chainStats["numOfLevels"] = chainStats["numOfLevels"] + 1
        addEntry(FILE_NAME, chainStats)

        #reload display level
        self.loadLevel()

        print("added level")

    def removeLevel(self):
        #check if display level isnt last level
        chainStats = readEntry(FILE_NAME, 0)

        #if display level isnt last level continue (else log issue)
        if self.displayLevel < chainStats["numOfLevels"]:

            #remove display level
            removeEntry(FILE_NAME, self.displayLevel)

            #move all further levels 1 left
            #get all levels
            levels = readData(FILE_NAME)
            
            #sort by levels that are further or equal selected  (can be only further as equal was just deleted)
            furtherLevels = []
            for level in levels:
                if level["index"] >= self.displayLevel:
                    furtherLevels.append(level)

            #modify their index to index - 1
            modifiedLevelsToAdd = []
            for level in furtherLevels:
                modifiedLevel = level   #copy level
                modifiedLevel["index"] = modifiedLevel["index"] - 1 #move right in chain of levels
                modifiedLevelsToAdd.append(modifiedLevel)   #append to queue to ovveride the previous levels

            #override previous levels with modified levels
            for modifiedLevel in modifiedLevelsToAdd:
                addEntry(FILE_NAME, modifiedLevel)

            #update num of levels
            chainStats["numOfLevels"] = chainStats["numOfLevels"] - 1
            addEntry(FILE_NAME, chainStats)

            #reload display level
            self.loadLevel()

            print("removed level")
            
        else:
            print("Cant remove last level!")

    def saveLevel(self):
        #get grid of health
        healthGrid = [[0 for x in range(self.width)] for y in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                healthGrid[y][x] = self.grid[y][x].life

        #create dictionary
        newDict = {
            "index": self.displayLevel,
            "playerX": self.playerGX,
            "playerY": self.playerGY,
            "grid": healthGrid
        }

        #add entry as dirctionary
        addEntry(FILE_NAME, newDict)

class Block:
    def __init__(self, x, y, size, life):
        self.x = x
        self.y = y
        self.size = size
        self.life = life
        self.color = (0, 255, 0)
    def updateColorByLife(self):
        match self.life:
            case 0:
                self.color = (0, 0, 0)
            case 1:
                self.color = (255, 255, 255)
            case 2:
                self.color = (136, 201, 255)
            case 3:
                self.color = (92, 152, 255)
            case 4:
                self.color = (72, 95, 225)
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.rect.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size), 0, 7)

if __name__ == "__main__":

    import pygame

    pygame.init()
    screenWidth = 800
    screenHeight = 600
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption('Edge Case Levle Builder')

    #remove window icon
    transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    transparent_surface.fill((0, 0, 0, 0))
    pygame.display.set_icon(transparent_surface)

    FILE_NAME = "levels.json"

    initFile(FILE_NAME)

    #- - - - - - - - - - - - - -

    grid = Grid(400, 300, 9, 9, 50, 5)

    running = True
    while running:

        screen.fill((30, 30, 30))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    #if can move left
                    if grid.displayLevel - 1 >= 1:
                        #save current level
                        grid.saveLevel()

                        #update display level
                        grid.displayLevel -= 1

                        #load display level
                        grid.loadLevel()

                if event.key == pygame.K_d:
                    if grid.displayLevel + 1 <= readEntry(FILE_NAME, 0)["numOfLevels"]:
                        #save current level
                        grid.saveLevel()

                        #update display level
                        grid.displayLevel += 1

                        #load new display level
                        grid.loadLevel()

                if event.key == pygame.K_1:
                    #before adding level save current
                    grid.saveLevel()

                    grid.addLevel()

                if event.key == pygame.K_2:
                    #before deleting save current
                    grid.saveLevel()

                    grid.removeLevel()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #get mouse pos
                    mPos = pygame.mouse.get_pos()

                    #get mouse grid pos
                    if mPos[0] > grid.topLeftX - grid.size/2 and mPos[0] < grid.topLeftX + grid.size * grid.width + (grid.width - 1) * grid.margin and mPos[1] > grid.topLeftY - grid.size/2 and mPos[1] < grid.topLeftY + grid.size * grid.height + (grid.height - 1) * grid.margin:
                        gridWorldPos = (mPos[0] - grid.topLeftX + grid.size/2, mPos[1] - grid.topLeftY + grid.size/2)

                        gridX = int(gridWorldPos[0] // (grid.size + grid.margin))
                        gridY = int(gridWorldPos[1] // (grid.size + grid.margin))

                        #get block health
                        if gridX < grid.width and gridY < grid.height:
                            blockLife = grid.grid[gridY][gridX].life

                            #adjust new block life
                            blockLife += 1
                            if blockLife > 4:
                                blockLife = 0

                            #apply new block life
                            grid.grid[gridY][gridX].life = blockLife

                            grid.grid[gridY][gridX].updateColorByLife()
                        
                if event.button == 3:
                    #get mouse pos
                    mPos = pygame.mouse.get_pos()

                    #get mouse grid pos
                    if mPos[0] > grid.topLeftX - grid.size/2 and mPos[0] < grid.topLeftX + grid.size * grid.width + (grid.width - 1) * grid.margin and mPos[1] > grid.topLeftY - grid.size/2 and mPos[1] < grid.topLeftY + grid.size * grid.height + (grid.height - 1) * grid.margin:
                        gridWorldPos = (mPos[0] - grid.topLeftX + grid.size/2, mPos[1] - grid.topLeftY + grid.size/2)

                        gridX = int(gridWorldPos[0] // (grid.size + grid.margin))
                        gridY = int(gridWorldPos[1] // (grid.size + grid.margin))

                        #get block health
                        if gridX < grid.width and gridY < grid.height:
                            grid.playerGX = gridX
                            grid.playerGY = gridY
                            grid.playerX = grid.topLeftX + grid.playerGX * grid.size + grid.playerGX * grid.margin
                            grid.playerY = grid.topLeftY + grid.playerGY * grid.size + grid.playerGY * grid.margin

        grid.drawBlocks()
        grid.drawPlayer()

        #switch buffer
        pygame.display.flip()

    pygame.quit()

