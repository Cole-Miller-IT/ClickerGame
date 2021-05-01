#Import Modules
try:
    import pygame
    from pygame.locals import *
    from pygame.math import Vector2
    import os
    import sys

    #My modules
    from Entity import Entity, Enemy, Player, FastEnemy
    from GameModes import MenuGameMode, PlayGameMode, MessageGameMode, SettingsGameMode
    from GameState import GameState
    from Commands import Command, MoveCommand

except ImportError as error:
    print("Couldn't load module.")
    print(error)
    sys.exit(2)

#Center game window
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Main game class
class UserInterface():
    def __init__(self):
        #Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.gray = (200, 200, 200)

        #Gamestate
        self.gamestate = GameState()

        #Init Pygame
        pygame.init()

        #Window
        self.worldSize = self.gamestate.worldSize
        self.cellSize = self.gamestate.cellSize
        self.windowSize = self.worldSize.elementwise() * self.cellSize  # ie. A board of 10 x 10 tiles multiplied by the cellSize
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))
        self.windowCaption = 'Clicker Game'
        pygame.display.set_caption(self.windowCaption)

        #FPS
        self.clock = pygame.time.Clock()
        self.FPS = self.gamestate.FPS

    def debug(self):
        pass

    def showLevel(self):
        #Init gameplay
        if self.currentGameMode is None:
            self.currentGameMode = PlayGameMode(UI)
            self.overlayGameMode = None
            self.activeGameMode = 'Play'
            
        #Resume gameplay
        else:
            self.overlayGameMode = None
            self.activeGameMode = 'Play'

    def showMessage(self):
        self.overlayGameMode = MessageGameMode(UI)
        self.activeGameMode = 'Overlay'
    
    def showMenu(self):
        self.overlayGameMode = MenuGameMode(UI)
        self.activeGameMode = 'Overlay'

    def showSettings(self):
        self.overlayGameMode = SettingsGameMode(UI)
        self.activeGameMode = 'Overlay'

    def quitGame(self): 
        self.gamestate.running = False

    def run(self, UI):
        #Set default gamemode to the menu
        self.currentGameMode = None 
        self.overlayGameMode = MenuGameMode(UI)
        self.activeGameMode = 'Overlay'
        
        pygame.mixer.music.set_volume(0.3)
        #pygame.mixer.music.load("Assets\MenuMusic(FuckBees).mp3")
        #pygame.mixer.music.play(loops=-1)
        #print(pygame.mixer.music.get_volume())

        #Main game loop
        while self.gamestate.running == True:
            #Determine what the current gamemode is and display an overlay if active
            if self.activeGameMode == 'Overlay':
                #Only process input from this game mode
                self.overlayGameMode.processInput()
                self.overlayGameMode.update()
            
            elif self.currentGameMode is not None:
                self.currentGameMode.processInput()
                try:
                    self.currentGameMode.update()
                except Exception as ex:
                    print('Error updating the current game mode')
                    self.currentGameMode = None
                    self.overlayGameMode = MenuGameMode(UI)
                    self.activeGameMode = 'Overlay'

            #Render 
            #Draw a black screen
            self.window.fill((0, 0, 0))

            #Render the play game mode if set
            if self.currentGameMode is not None:
                self.currentGameMode.render()
            
            #Render the Overlay if it is active
            if self.activeGameMode == 'Overlay':
                darkSurface = pygame.Surface(self.window.get_size(),flags=pygame.SRCALPHA)
                pygame.draw.rect(darkSurface, (0,0,0,150), darkSurface.get_rect())
                self.window.blit(darkSurface, (0,0))
                self.overlayGameMode.render()

            #Draw graphics to the screen
            pygame.display.update()
            self.clock.tick(self.FPS)


UI = UserInterface()
UI.run(UI)

pygame.quit()
sys.exit()
