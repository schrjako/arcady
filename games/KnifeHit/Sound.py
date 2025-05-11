#   Main background music track "BackgrounTrack1.mp3" made by Nabeel (Discord: zeuz.0) for the GMTK24 "Built to scale" game jam

import pygame

import random

class SoundManager():
    def __init__(self, musicVolume, soundVolume):
        self.musicVolume = musicVolume
        self.soundVolume = soundVolume

        pygame.mixer.init()

        pygame.mixer.music.load('./Sounds/backgroundTrack1.mp3')
        pygame.mixer.music.set_volume(self.musicVolume)
        pygame.mixer.music.play(-1)

        self.knifeThrow1_sfx = pygame.mixer.Sound('./Sounds/throw1.mp3')
        self.knifeThrow2_sfx = pygame.mixer.Sound('./Sounds/throw2.mp3')
        self.knifeThrowSfx = [self.knifeThrow1_sfx, self.knifeThrow2_sfx]

        self.knifeHit1_sfx = pygame.mixer.Sound('./Sounds/hit1.mp3')
        self.knifeHit2_sfx = pygame.mixer.Sound('./Sounds/hit2.mp3')
        self.knifeHit3_sfx = pygame.mixer.Sound('./Sounds/hit3.mp3')
        self.knifeHit4_sfx = pygame.mixer.Sound('./Sounds/hit4.mp3')
        self.knifeHitSfx = [self.knifeHit1_sfx, self.knifeHit2_sfx, self.knifeHit3_sfx, self.knifeHit4_sfx]

        self.knifeBreak1_sfx = pygame.mixer.Sound('./Sounds/break1.mp3')
        self.knifeBreakSfx = [self.knifeBreak1_sfx]

        self.fruitSlice1_sfx = pygame.mixer.Sound('./Sounds/slice1.mp3')
        self.fruitSlice2_sfx = pygame.mixer.Sound('./Sounds/slice2.mp3')
        self.fruitSlice3_sfx = pygame.mixer.Sound('./Sounds/slice3.mp3')
        self.fruitSliceSfx = [self.fruitSlice1_sfx, self.fruitSlice2_sfx, self.fruitSlice3_sfx]

        self.lose_sfx = pygame.mixer.Sound('./Sounds/lose1.mp3')
        self.loseSfx = [self.lose_sfx]

        #settings toggle
        self.doMusic = True
        self.doSound = True

        #load images
        self.musicOnImage = pygame.image.load('./Sprites/MusicIcon.png').convert_alpha()
        self.musicOffImage = pygame.image.load('./Sprites/MusicOffIcon.png').convert_alpha()
        self.musicShadowImage = pygame.image.load('./Sprites/MusicIconShadow.png').convert_alpha()

        self.soundOnImage = pygame.image.load('./Sprites/SoundIcon.png').convert_alpha()
        self.soundOffImage = pygame.image.load('./Sprites/SoundOffIcon.png').convert_alpha()
        self.soundShadowImage = pygame.image.load('./Sprites/SoundIconShadow.png').convert_alpha()

        self.returnImage = pygame.image.load('./Sprites/ReturnIcon.png').convert_alpha()
        self.returnShadowImage = pygame.image.load('./Sprites/ReturnIconShadow.png').convert_alpha()

        #scale images
        self.musicShadowImage = pygame.transform.scale(self.musicShadowImage, (25, 25))
        self.soundShadowImage = pygame.transform.scale(self.soundShadowImage, (25, 25))

        self.musicOnImage = pygame.transform.scale(self.musicOnImage, (25, 25))
        self.musicOffImage = pygame.transform.scale(self.musicOffImage, (25, 25))
        self.soundOnImage = pygame.transform.scale(self.soundOnImage, (25, 25))
        self.soundOffImage = pygame.transform.scale(self.soundOffImage, (25, 25))

        self.returnImage = pygame.transform.scale(self.returnImage, (30, 25))
        self.returnShadowImage = pygame.transform.scale(self.returnShadowImage, (30, 25))

    def toggleMusic(self):
        self.doMusic = not self.doMusic

        if self.doMusic:
            pygame.mixer.music.set_volume(self.musicVolume)
        else:
            pygame.mixer.music.set_volume(0)

    def stopMusic(self):
        pygame.mixer.music.stop()

    def toggleSound(self):
        self.doSound = not self.doSound

    def displayIcons(self, screen):
        #draw shadows
        musicShadowRect = self.musicShadowImage.get_rect(center=(17.5, 17.5 + 7))
        soundShadowRect = self.soundShadowImage.get_rect(center=(17.5*2 + 15, 17.5 + 7))

        screen.blit(self.musicShadowImage, musicShadowRect)
        screen.blit(self.soundShadowImage, soundShadowRect)

        sWidth, sHeight = screen.get_size()
        returnShadowRect = self.returnShadowImage.get_rect(center=(sWidth - 20, 17.5 + 7))

        screen.blit(self.returnShadowImage, returnShadowRect)

        #draw on/off images
        if self.doMusic:
            musicImage = self.musicOnImage
            musicRect = musicImage.get_rect(center=(17.5, 17.5))
        else:
            musicImage = self.musicOffImage
            musicRect = musicImage.get_rect(center=(17.5, 17.5))
        screen.blit(musicImage, musicRect)
        
        if self.doSound:
            soundImage = self.soundOnImage
            soundRect = soundImage.get_rect(center=(17.5*2 + 15, 17.5))
        else:
            soundImage = self.soundOffImage
            soundRect = soundImage.get_rect(center=(17.5*2 + 15, 17.5))
        screen.blit(soundImage, soundRect)

        returnRect = self.returnImage.get_rect(center=(sWidth - 20, 17.5))
        screen.blit(self.returnImage, returnRect)

    def playFromSounds(self, sounds):
        sound = sounds[random.randint(0, len(sounds) - 1)]

        if self.doSound:
            sound.set_volume(self.soundVolume)
        else:
            sound.set_volume(0)

        sound.play()