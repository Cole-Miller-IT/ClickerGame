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
    import Color

except ImportError as error:
    print("Couldn't load module.")
    print(error)
    sys.exit(2)

#Main game class
class UserInterface():
    def __init__(self):
        self.gamestate = GameState()

        pygame.init()

        #Create a window of 10 x 10 tiles multiplied by the cellSize
        self.worldSize = self.gamestate.worldSize
        self.cellSize = self.gamestate.cellSize
        self.windowSize = self.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        self.windowCaption = 'Clicker Game'
        pygame.display.set_caption(self.windowCaption)

        #FPS
        self.clock = pygame.time.Clock()
        self.FPS = self.gamestate.FPS

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

    def showMessageOverlay(self):
        self.overlayGameMode = MessageGameMode(UI)
        self.activeGameMode = 'Overlay'
    
    def showMenuOverlay(self):
        self.overlayGameMode = MenuGameMode(UI)
        self.activeGameMode = 'Overlay'

    def showSettingsOverlay(self):
        self.overlayGameMode = SettingsGameMode(UI)
        self.activeGameMode = 'Overlay'

    def quitGame(self): 
        self.gamestate.gameRunning = False

    def run(self, UI):
        #Set default gamemode to the menu
        self.currentGameMode = None 
        self.overlayGameMode = MenuGameMode(UI)
        self.activeGameMode = 'Overlay'
        
        pygame.mixer.music.set_volume(0.3)

        #Main game loop
        while self.gamestate.gameRunning == True:
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
