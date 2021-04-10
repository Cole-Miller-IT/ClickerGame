''' 
Project: Clicker game
Author: Cole Miller
Date: 2021-04-01 - 2021-04-04

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

    #My modules
    from Entity import Entity, Enemy, Player
    from GameModes import MenuGameMode, PlayGameMode, MessageGameMode
except ImportError as error:
    print("Couldn't load module.")
    print(error)
    sys.exit(2)

#Center game window
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Main class that contains the parts of the game loop in different methods
class GameLoop:
    def __init__(self):
        self.running = True     #Gameloop condition for running
        self.FPS = 60           #Game FPS
        
        #Lists all current fonts 
        '''fonts = pygame.font.get_fonts()
        print(len(fonts))
        for f in fonts:
            print(f)'''

        #Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.gray = (200, 200, 200)

        #Window
        self.worldSize = Vector2(10,10)
        self.cellSize = Vector2(64,64)
        self.windowSize = self.worldSize.elementwise() * self.cellSize  # ie. A board of 10 x 10 tiles multiplied by the cellSize
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))
        self.windowCaption = 'Clicker Game'

        #Init the pygame
        pygame.init()
        pygame.display.set_caption(self.windowCaption)

        #Player
        self.player1 = Player(self.cellSize, self.worldSize)

        #Font
        self.fontSize = 24
        self.font = pygame.font.SysFont('rubik', self.fontSize)

        # Creates a Clock class
        self.clock = pygame.time.Clock()

        #Enemies
        self.enemiesList = []
        self.enemiesListCopy = []
        self.maxEnemies = 4

    def processInput(self):
        # Event Checker
        for event in pygame.event.get():
            # If the user has clicked on the 'X' box, close the game
            if event.type == pygame.QUIT:
                self.running = False
            # If the user has pressed down on the keyboard, handle the input
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player1.processInput()  #Store the mouse click position
                #print(self.player1.clickPos)
                
            else:
                pass

    def update(self):
        #If there are less than the max amount of enemies on screen, spawn one
        if len(self.enemiesList) < self.maxEnemies:
            #Spawn a new enemy
            self.enemiesList.append(Enemy(self.cellSize, self.worldSize))
 
        #Update all enemies  
        self.enemiesListCopy = self.enemiesList  #Create a copy of the enemies list to prevent iteration errors, change later to a lambda function
        for enemy in self.enemiesListCopy:
            #If the enemy is out of the world bounds delete it, else move it
            if enemy.pos.x >= (self.windowSize.x - self.cellSize.x) or enemy.pos.y >= (self.windowSize.y - self.cellSize.y):
                self.enemiesList.remove(enemy)  #Deletes the enemy

            #Check if the player has clicked
            elif self.player1.clickPos != Vector2(0, 0):
                collide = enemy.rectangle.collidepoint(self.player1.clickPos)  #Determines if a collision has happened
                
                #If a collision has occured update player and enemy
                if collide:
                    self.player1.update()
                    self.enemiesList.remove(enemy)

            else:
                enemy.update()     #Moves the enemy
            
        self.player1.clickPos = Vector2(0, 0)  #Reset value

    def render(self):
        # Reset background
        self.window.fill(self.black)

        #Draw Enemies 
        for Enemy in self.enemiesList:
            Enemy.render(self.window, self.red)

        #Draw font/text
        self.fontSurface = self.font.render("FPS: " + str(int(self.clock.get_fps())), True, self.white)  #Convert clock from a float to a int to round off decimal points
        self.window.blit(self.fontSurface, (20, 20))
        self.fontSurface = self.font.render("Score: " + str(self.player1.score), True, self.white)
        self.window.blit(self.fontSurface, (20, 40))

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