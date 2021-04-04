''' 
Project: Clicker game
Author: Cole Miller
Date: 2021-04-01

#Commands to help configure VS Code with Python using a virtual environment
py -m venv venv  #Creates a folder for the virtual envirmont 
"terminal.integrated.shellArgs.windows": ["-ExecutionPolicy", "Bypass"]  #Used to allow Powershell to run these scripts
py -m pip install pygame  #Install the pygame module
'''

#Import Modules
try:
    import pygame
    from pygame.locals import *
    from pygame.math import Vector2
    import os
    import sys
    from Entity import Entity, Enemy
except ImportError as error:
    print("Couldn't load module.")
    print(error)
    sys.exit(2)

#Center game window
os.environ['SDL_VIDEO_CENTERED'] = '1'

class GameLoop:
    def __init__(self):
        self.running = True
        self.FPS = 60

        #Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        #Window
        self.worldSize = Vector2(10,10)
        self.cellSize = Vector2(64,64)

        self.windowSize = self.worldSize.elementwise() * self.cellSize  # ie. A board of 10 x 10 tiles multiplied by the cellSize
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))
        self.windowCaption = 'Clicker Game'

        #Init the pygame
        pygame.init()
        pygame.display.set_caption(self.windowCaption)

        # Creates a Clock class
        self.clock = pygame.time.Clock()

        #Testing-----------------------------------------------------
        p1 = Entity(self.cellSize)
        p2 = Enemy(self.cellSize, (5, 5))

    def processInput(self):
        # Event Checker
        for event in pygame.event.get():
            # If the user has clicked on the 'X' box, close the game
            if event.type == pygame.QUIT:
                self.running = False
            # If the user has pressed down on the keyboard, handle the input
            elif event.type == pygame.KEYDOWN:
                pass
            else:
                pass

    def update(self):
        pass

    def render(self):
        # Reset background
        self.window.fill(self.black)

        #Draw Enemies

        # Update Display screen
        pygame.display.update()


    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()

            # Set the game FPS
            self.clock.tick(self.FPS)    

# Main Game Loop
game = GameLoop()
game.run()

# Quits the game and frees resources
pygame.quit()
sys.exit()