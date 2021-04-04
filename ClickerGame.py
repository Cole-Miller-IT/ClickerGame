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
    from Entity import Entity, Enemy, Player
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
        self.red = (255, 0, 0)

        #Window
        self.worldSize = Vector2(10,10)
        self.cellSize = Vector2(64,64)

        self.windowSize = self.worldSize.elementwise() * self.cellSize  # ie. A board of 10 x 10 tiles multiplied by the cellSize
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))
        self.windowCaption = 'Clicker Game'
        print(self.windowSize)

        #Init the pygame
        pygame.init()
        pygame.display.set_caption(self.windowCaption)

        # Creates a Clock class
        self.clock = pygame.time.Clock()

        #Enemies
        self.enemiesList = []
        self.enemiesListCopy = []
        self.maxEnemies = 2

        #Player
        self.player1 = Player(self.cellSize, self.worldSize)

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
                print(self.player1.clickPos.x)
                
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
                #print(enemy.pos.x)

            #If the player clicks on a enemy delete it, add to the player's score, and reset clickPos
            elif self.player1.clickPos.x > enemy.pos.x:
                self.player1.update()

            else:
                enemy.update()     #Moves the enemy

    def render(self):
        # Reset background
        self.window.fill(self.black)

        #Draw Enemies 
        for Enemy in self.enemiesList:
            Enemy.render(self.window, self.red)

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