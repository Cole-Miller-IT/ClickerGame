import pygame
import random
from pygame.locals import *
from pygame.math import Vector2

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
                'action': 1#lambda: load level
            },
            {
                'menuItemName': 'Level 1',
                'action': 2#lambda: throw error no level 2 created
            },
            {
                'menuItemName': 'Quit', #Quit must be the last item in the menuItems list
                'action': 3#lambda: Quit game
            }
        ]

        self.currentMenuItem = 0
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
                    #If the user selects the last menuItem quit the game, this should say "Quit"
                    if self.currentMenuItem == (len(self.menuItems) - 1):
                        #Exit the loop
                        self.ui.quitGame()

    def update(self):
        pass

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
    def __init__(self):

        pygame.init()

        #Window
        self.worldSize = Vector2(10,10)
        self.cellSize = Vector2(64,64)
        self.windowSize = self.worldSize.elementwise() * self.cellSize  # ie. A board of 10 x 10 tiles multiplied by the cellSize
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))
        self.windowCaption = 'Clicker Game'
        
        #Font
        self.fontSize = 24
        self.font = pygame.font.SysFont('rubik', self.fontSize)
        
        #Create a list, each item of the list is a dict[] of all levels and a quit option
        self.menuItems = [
            {
                'title': 'Level 1',
                'action': 1#lambda: load level
            },
            {
                'title': 'Level 2',
                'action': 2#lambda: throw error no level 2 created
            },
            {
                'title': 'Quit',
                'action': 3#lambda: Quit game
            }
        ]

        self.currentMenuItem = 0
        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        #Event handling 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Exit the menu
                print("quit")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_s:
                    if self.currentMenuItem < len(self.menuItems):
                        self.currentMenuItem += 1
                elif event.type == pygame.K_RETURN:
                    try:
                        #Action
                        print("enter works")
                    except error as er:
                        print(er)

    def update(self):
        x = 1
        
    def render(self):
        self.window.fill((0, 0, 0))
        
        #Title
        surfaceTitle = self.font.render("title", True, (0, 255, 255))
        self.window.blit(surfaceTitle, (25, 25))

        pygame.display.update()

class MessageGameMode(GameMode):
    def __init__(self):
        #Init Pygame
        pygame.init()

        #Window
        self.worldSize = Vector2(10,10)
        self.cellSize = Vector2(64,64)
        self.windowSize = self.worldSize.elementwise() * self.cellSize  # ie. A board of 10 x 10 tiles multiplied by the cellSize
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))
        self.windowCaption = 'Clicker Game'
        
        #Font
        self.fontSize = 24
        self.font = pygame.font.SysFont('rubik', self.fontSize)
        
        #Create a list, each item of the list is a dict[] of all levels and a quit option
        self.menuItems = [
            {
                'title': 'Level 1',
                'action': 1#lambda: load level
            },
            {
                'title': 'Level 2',
                'action': 2#lambda: throw error no level 2 created
            },
            {
                'title': 'Quit',
                'action': 3#lambda: Quit game
            }
        ]

        self.currentMenuItem = 0
        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        #Event handling 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Exit the menu
                print("quit")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_s:
                    if self.currentMenuItem < len(self.menuItems):
                        self.currentMenuItem += 1
                elif event.type == pygame.K_RETURN:
                    try:
                        #Action
                        print("enter works")
                    except error as er:
                        print(er)

    def update(self):
        x = 1
        
    def render(self):
        self.window.fill((0, 0, 0))
        
        #Title
        surfaceTitle = self.font.render("title", True, (255, 0, 255))
        self.window.blit(surfaceTitle, (25, 25))

        pygame.display.update()