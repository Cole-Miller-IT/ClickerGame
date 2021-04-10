
#Import Modules
try:
    import pygame
    from pygame.locals import *
    from pygame.math import Vector2
    import os
    import sys

    #My modules
    from Entity import Entity, Enemy, Player
    from GameModes import MenuGameMode, PlayGameMode, MessageGameMode
except ImportError as error:
    print("Couldn't load module.")
    print(error)
    sys.exit(2)

#Center game window
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Main game class
class UserInterface():
    def __init__(self):
        self.running = True

        #Init Pygame
        pygame.init()

        #Window
        self.worldSize = Vector2(10,10)
        self.cellSize = Vector2(64,64)
        self.windowSize = self.worldSize.elementwise() * self.cellSize  # ie. A board of 10 x 10 tiles multiplied by the cellSize
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))
        self.windowCaption = 'Clicker Game'

        #FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60

    def debug(self):
        pass
    
    def quitGame(self):
        self.running = False

    def run(self, UI):
        #Game mode
        self.currentGameMode = None #Set default gamemode to the menu
        self.overlayGameMode = MenuGameMode(UI)
        self.activeGameMode = 'Overlay'

        #Main game loop
        while self.running == True:
            #Determine what the current gamemode is and display an overlay if active
            if self.activeGameMode == 'Overlay':
                #Only process input from this game mode
                self.overlayGameMode.processInput()
                self.overlayGameMode.update()
            #
            elif self.currentGameMode is not None:
                self.currentGameMode.processInput()
                try:
                    self.currentGameMode.update()
                except  error as er:
                    print('Error updating the current game mode')
                    self.currentGameMode = None

            #Render 
            if self.currentGameMode is not None:
                self.currentGameMode.render()
            else:
                #Draw a black screen
                self.window.fill((0, 0, 0))
            
            if self.activeGameMode == 'Overlay':
                darkSurface = pygame.Surface(self.window.get_size(),flags=pygame.SRCALPHA)
                pygame.draw.rect(darkSurface, (0,0,0,150), darkSurface.get_rect())
                self.window.blit(darkSurface, (0,0))
                self.overlayGameMode.render()


            pygame.display.update()
            self.clock.tick(self.FPS)


UI = UserInterface()
UI.run(UI)

pygame.quit()
sys.exit()
