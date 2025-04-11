
#by default not on gimvic computers
import pygame
import numpy as np
#extra lib
import math
import random
import time
#project scripts
#import ExtraMath
from . import OrderedSprites
from . import GameObjects
from . import Sound

#game management classes and functions and some UI that doesnt realy fit anywhere else
class GameState():
    def __init__(self, screen, screenWidth, screenHeight, musicVolume, soundVolume):

        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.musicVolume = musicVolume
        self.soundVolume = soundVolume

        #initialize everything for all scenes
        self.soundMngr = Sound.SoundManager(self.musicVolume, self.soundVolume)

        self.highScore = 0
        self.score = 0

        self.font = pygame.font.Font('./Sprites/SuperMario256.ttf', 40)

        #initialize all objects for one scene

        #initialize transition
        self.transition = gameSceneTransition(self)

        self.orderedSprites = []
        self.knives = []
        self.apples = []

        self.particles = []

        #initialize objects
        self.log = GameObjects.Log(self, 200, 200)

        #spawn apples, get number of available knives
        self.numOfApples = random.randint(2, 5)
        for i in range(self.numOfApples):
            newApple = GameObjects.Apple(self)

        #initialize knife bar
        self.knifeBar = KnifeBar(self, 200, 700, int(self.numOfApples * 1.5))

        #spawn initial knife 
        self.knifeThrowForce = (0, -0.7)
        newKnife = GameObjects.Knife(self, 200, 600)

    def restartScene(self):
        #re initialize all objects for new scene

        #initialize transition
        self.transition = gameSceneTransition(self)

        self.orderedSprites = []
        self.knives = []
        self.apples = []

        self.particles = []

        #initialize objects
        self.log = GameObjects.Log(self, 200, 200)

        #spawn apples, get number of available knives
        self.numOfApples = random.randint(2, 5)
        for i in range(self.numOfApples):
            newApple = GameObjects.Apple(self)

        #initialize knife bar
        self.knifeBar = KnifeBar(self, 200, 700, int(self.numOfApples * 1.5))

        #spawn initial knife 
        self.knifeThrowForce = (0, -0.7)
        newKnife = GameObjects.Knife(self, 200, 600)

    def updateScore(self):
        if self.score > self.highScore:
            self.highScore = self.score

        #blit score text
        highScoreText_top = self.font.render(str(self.highScore), True, (255, 255, 0))
        highScoreText_bottom = self.font.render(str(self.highScore), True, (155, 100, 0))
        highScoreText_shadow = self.font.render(str(self.highScore), True, (0, 0, 0))

        scoreText_top = self.font.render(str(self.score), True, (255, 255, 255))
        scoreText_bottom = self.font.render(str(self.score), True, (155, 155, 155))
        scoreText_shadow = self.font.render(str(self.score), True, (0, 0, 0))

        self.screen.blit(highScoreText_shadow, (self.screenWidth - 15 - highScoreText_shadow.get_width(), 30 + self.screenHeight/2 - highScoreText_shadow.get_width()/2))
        self.screen.blit(scoreText_shadow, (self.screenWidth - 15 - scoreText_shadow.get_width(), 30 + self.screenHeight/2 - scoreText_shadow.get_width()/2 + 45))

        self.screen.blit(highScoreText_bottom, (self.screenWidth - 15 - highScoreText_bottom.get_width(), 18 + self.screenHeight/2 - highScoreText_bottom.get_width()/2))
        self.screen.blit(scoreText_bottom, (self.screenWidth - 15 - scoreText_bottom.get_width(), 18 + self.screenHeight/2 - scoreText_bottom.get_width()/2  + 45))

        self.screen.blit(highScoreText_top, (self.screenWidth - 15 - highScoreText_top.get_width(), 15 + self.screenHeight/2 - highScoreText_top.get_width()/2))
        self.screen.blit(scoreText_top, (self.screenWidth - 15 - scoreText_top.get_width(), 15 + self.screenHeight/2 - scoreText_top.get_width()/2 + 45))

class gameSceneTransition():
    def __init__(self, gs):
        self.gs = gs
        
        self.a = 255
        self.ta = 0

        self.overlaySurface = pygame.Surface((self.gs.screenWidth, self.gs.screenHeight), pygame.SRCALPHA)
        self.overlaySurface.fill((0, 0, 0, self.a))  # RGBA: black with 50% opacity

    def updateOverlay(self):
        #interpolate towards target a
        self.a = self.a + 0.01*(self.ta - self.a) + 0.1

        if self.a > 255:
            self.a = 255
        if self.a < 0:
            self.a = 0

        self.overlaySurface.fill((0, 0, 0, int(self.a)))  # RGBA: black with 50% opacity
        self.gs.screen.blit(self.overlaySurface, (0, 0))

    def outTransition(self):
        #set target a to black
        self.ta = 255

        #restart scene
        if self.a == self.ta:
            self.gs.restartScene()

class KnifeBar(pygame.sprite.Sprite):
    def __init__(self, gs, x, y, numOfKnives):
        self.gs = gs
        self.x = x
        self.y = y

        self.maxKnives = numOfKnives
        self.knivesLeft = numOfKnives

        self.angle = 160
        self.dead = False

        #create knife slot images
        self.spacing = 20
        self.emptySlotSprites = []
        self.fullSlotSprites = []
        for i in range(self.maxKnives):
            emptySlot = OrderedSprites.orderedSpirte(self, self.gs, "KnifeShadow.png", 15, self.spacing*i - (self.maxKnives * self.spacing) / 2 + self.spacing / 2, 15, 15  * 3.387, 100)
            self.emptySlotSprites.append(emptySlot)

            fullSlot = OrderedSprites.orderedSpirte(self, self.gs, "Knife.png", 0, self.spacing*i - (self.maxKnives * self.spacing) / 2 + self.spacing / 2, 15, 15  * 3.387, 101)
            self.fullSlotSprites.append(fullSlot)

    def updateSprites(self):
        for sprite in self.emptySlotSprites:
            sprite.update()

        for i in range(self.maxKnives):
            self.fullSlotSprites[i].update()
            
            if i >= self.knivesLeft:
                self.fullSlotSprites[i].doBlit = False

class KnifeHitGame:
    def __init__(self, screen):
        self.screen = screen

        #get original arcady menu dimensions for returning back to menu after quiting knifehit
        self.menuWidth, self.menuHeight = pygame.display.get_surface().get_size()

    def initKnifeHit(self, screen):
        import os

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        self.musicVolume = 0.4
        self.soundVolume = 0.4

        #window initialization
        self.screenWidth = 400
        self.screenHeight = 800

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))

        #remove window icon and set caption
        pygame.display.set_caption('Knife Hit')

        transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        transparent_surface = pygame.image.load('./Sprites/Apple.png').convert_alpha()
        pygame.display.set_icon(transparent_surface)

    def returnToMenu(self):
        #set screen dimensions to original/menu
        self.screen = pygame.display.set_mode((self.menuWidth, self.menuHeight))

    def run(self):

        self.initKnifeHit(self.screen)

        #initialize vars as game state
        self.gs = GameState(self.screen, self.screenWidth, self.screenHeight, self.musicVolume, self.soundVolume)

        #get delta time initial ticks
        prevT = pygame.time.get_ticks()

        running = True
        while running:

            #update delta time
            currT = pygame.time.get_ticks()
            dTms = currT - prevT
            dTs = dTms

            # Fill screen
            self.screen.fill((30, 30, 30))

            # Handle inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.returnToMenu()
                        return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        
                        #get press position and determine if settings pressed or knife thrown
                        mPos = pygame.mouse.get_pos()

                        if mPos[0] < 30 and mPos[1] < 30:
                            #toggle music
                            self.gs.soundMngr.toggleMusic()

                        elif mPos[0] < 75 and mPos[1] < 30:
                            #toggle sound
                            self.gs.soundMngr.toggleSound()

                        else:
                            #throw all not yet thrown knives
                            for knife in self.gs.knives:
                                knife.throw(self.gs.knifeThrowForce)
                                self.gs.soundMngr.playFromSounds(self.gs.soundMngr.knifeThrowSfx)

                            #spawn new knife 
                            self.gs.knifeBar.knivesLeft -= 1
                            if self.gs.knifeBar.knivesLeft > 0:
                                newKnife = GameObjects.Knife(self.gs, 200, 600)

            #update log
            self.gs.log.updateRotation(dTs)
            self.gs.log.updateSprites()

            #update knives
            for knife in self.gs.knives:
                knife.move(dTs)
                knife.collide()
                knife.updateSprites()

            #update apples
            for apple in self.gs.apples:
                apple.move(dTs)
                apple.collide()
                apple.updateSprites()

            #update knife bar UI
            self.gs.knifeBar.updateSprites()

            #remove dead objects
            self.gs.apples = [apple for apple in self.gs.apples if apple.dead == False]
            self.gs.knives = [knife for knife in self.gs.knives if knife.dead == False]
            self.gs.orderedSprites = [ordrdSprt for ordrdSprt in self.gs.orderedSprites if ordrdSprt.parent.dead == False]

            #update score
            self.gs.updateScore()

            #check for win/lose condition, (if statement to allow for close button quiting)
            self.checkForWin()

            #draw ordered sprites (blit everything other than particles)
            OrderedSprites.blitOrderedSprites(self.screen, self.gs)

            #blit particles
            for particle in self.gs.particles:
                particle.update(self.screen)
            self.gs.particles = [particle for particle in self.gs.particles if particle.lifeTime > 0]

            #display music/sound ui
            self.gs.soundMngr.displayIcons(self.screen)

            #update transition animation
            self.gs.transition.updateOverlay()

            # Update the display
            pygame.display.flip()

            #update delta time
            prevT = currT

        # Quit Pygame
        pygame.quit()

    def checkForWin(self):
        #check if any apples left
        if len(self.gs.apples) == 0:
            #Win
            self.gs.transition.outTransition()

        #check if no more knives and all knives have hit the log
        else:
            if self.gs.knifeBar.knivesLeft <= 0:

                hitKnives = 0
                for knife in self.gs.knives:
                    if knife.hasHit == True:
                        hitKnives += 1

                if hitKnives == len(self.gs.knives):
                    #Lose
                    self.gs.score = 0
                    self.gs.transition.outTransition()

def run(screen):
    KnifeHitGame(screen).run()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(400, 800)
    run(screen)
