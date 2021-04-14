import pygame
import random
from pygame.locals import *
from pygame.math import Vector2

#My modules
from Entity import Entity, Enemy, Player

class GameMode():
    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self, window):
        raise NotImplementedError()

    def quitGame(self):
        pass

class MenuGameMode(GameMode):
    def __init__(self, UI):
        self.ui = UI
        
        #Font
        self.fontSize = 24
        self.font = pygame.font.SysFont('rubik', self.fontSize)
        
        #Create a list, each item of the list is a dict[] of all levels and a quit option
        self.menuItems = [
            {
                'menuItemName': 'Tutorial Instructions',
                'action': lambda: self.ui.showMessage()
            },
            {
                'menuItemName': 'Level 1',
                'action': lambda: self.ui.showLevel()
            },
            {
                'menuItemName': 'Quit', 
                'action': lambda: self.ui.quitGame()
            }
        ]

        self.currentMenuItem = 0
        self.menuItem = None
        self.menuCursor = pygame.font.SysFont('rubik', self.fontSize)

    def processInput(self):
        #Event handling 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Exit the loop
                self.ui.quitGame()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_s:
                    if self.currentMenuItem < (len(self.menuItems) - 1):
                        self.currentMenuItem += 1
                elif event.key == pygame.K_RETURN:
                    #Gets the current menuitems action
                    self.menuItem = self.menuItems[self.currentMenuItem]

    def update(self):
        if self.menuItem is not None:
            try:
                #Execute the current menuitems Action lambda function
                self.menuItem['action']() 
            except Exception as ex:
                print(ex)

    def render(self):   
        #Computes where the x-pos should be to center the font surface
        def centerFontX(surface):
            offset = surface.get_width() // 2 #Take the length of the font divided by 2
            x = (self.ui.window.get_width() // 2) - offset #Take half the window width and the offset to determine where to draw

            return x

        # Initial y
        y = 50
        
        # Title
        surface = self.font.render("Clicker Game", True, (200, 0, 0))
        x = centerFontX(surface)
        self.ui.window.blit(surface, (x, y))

        y += (200 * surface.get_height()) // 100  #Change the y-pos to draw the menu items
        
        #Iterate through each menuItem
        for item in self.menuItems:
            #Draw each menuItem to the screen
            surface = self.font.render(item['menuItemName'], True, (200, 0, 0))
            x = centerFontX(surface)
            self.ui.window.blit(surface, (x, y))
            
            #Cursor
            #Get the current index number
            index = self.menuItems.index(item)  
            
            #Render the cursor at the current MenuItem selected
            if index == self.currentMenuItem:
                surface = self.menuCursor.render("-->", True, (200, 0, 0))
                cursorX = x - (surface.get_width() + 10) 
                cursorY = y
                self.ui.window.blit(surface, (cursorX, cursorY))

            #Update y-pos so items are not overlaping
            y += (120 * surface.get_height()) // 100  

#---------------------------------------------------------------------------------------
class PlayGameMode(GameMode):
    def __init__(self, UI):
        self.ui = UI

        #Font
        self.fontSize = 24
        self.font = pygame.font.SysFont('rubik', self.fontSize)
        self.message = "play Game mode"

        #Player
        self.player1 = Player(self.ui.cellSize, self.ui.worldSize)

        #Enemies
        self.enemiesList = []
        self.enemiesListCopy = []
        self.maxEnemies = 4

    def processInput(self):
        # Event Handler
        for event in pygame.event.get():
            # If the user has clicked on the 'X' box, close the game
            if event.type == pygame.QUIT:
                self.running = False
            # If the user has pressed down on the keyboard, handle the input
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.ui.showMenu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player1.processInput()  #Store the mouse click position
                #print(self.player1.clickPos)
                
            else:
                pass

    def update(self):
        #If there are less than the max amount of enemies on screen, spawn one
        if len(self.enemiesList) < self.maxEnemies:
            #Spawn a new enemy
            self.enemiesList.append(Enemy(self.ui.cellSize, self.ui.worldSize))
 
        #Update all enemies  
        self.enemiesListCopy = self.enemiesList  #Create a copy of the enemies list to prevent iteration errors, change later to a lambda function
        for enemy in self.enemiesListCopy:
            #If the enemy is out of the world bounds delete it, else move it
            if enemy.pos.x >= (self.ui.windowSize.x - self.ui.cellSize.x) or enemy.pos.y >= (self.ui.windowSize.y - self.ui.cellSize.y):
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
        #surface = self.font.render(self.message, True, (255, 0, 0))
        #self.ui.window.blit(surface, (200, 200))

        # Reset background
        self.ui.window.fill(self.ui.black)

        #Draw Enemies 
        for Enemy in self.enemiesList:
            Enemy.render(self.ui.window, self.ui.red)

        #Draw font/text
        self.fontSurface = self.font.render("FPS: " + str(int(self.ui.clock.get_fps())), True, self.ui.white)  #Convert clock from a float to a int to round off decimal points
        self.ui.window.blit(self.fontSurface, (20, 20))
        self.fontSurface = self.font.render("Score: " + str(self.player1.score), True, self.ui.white)
        self.ui.window.blit(self.fontSurface, (20, 40))

class MessageGameMode(GameMode):
    def __init__(self, UI):
        self.ui = UI

        self.fontSize = 24
        self.font = pygame.font.SysFont('rubik', self.fontSize)
        self.message = "Message Game mode"

        self.returnToMenu = False
     
    def processInput(self):
        #Event handling 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE \
                or event.key == pygame.K_RETURN:
                    #Store the value to be updated later
                    self.returnToMenu = True

    def update(self):
        #Return to the menu
        if self.returnToMenu == True:
            self.ui.showMenu()
        
    def render(self):
        surface = self.font.render(self.message, True, (255, 0, 0))
        self.ui.window.blit(surface, (200, 200))
