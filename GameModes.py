import pygame
import random
from pygame.locals import *
from pygame.math import Vector2

#My modules
from Entity import Entity, Enemy, Player, FastEnemy
    
class GameMode():
    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self):
        raise NotImplementedError()

    def quitGame(self):
        pass

class MenuGameMode(GameMode):
    def __init__(self, UI):
        super().__init__() #Inherit all the properties and methods of the parent class
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
                'menuItemName': 'Settings', 
                'action': lambda: self.ui.showSettings()
            },
            {
                'menuItemName': 'Quit', 
                'action': lambda: self.ui.quitGame()
            }
        ]

        self.currentMenuItem = 0
        self.menuItem = None
        self.menuCursor = pygame.font.SysFont('rubik', self.fontSize)
        self.menuName = "Clicker Game"

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
                self.menuItem = None
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
        surface = self.font.render(self.menuName, True, (200, 0, 0))
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
        self.fastEnemyCounter = 0

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
            else:
                pass

    def update(self):
        #If there are less than the max amount of enemies on screen, spawn one
        if len(self.enemiesList) < self.maxEnemies:
            #Spawn a new fast enemy
            if self.fastEnemyCounter == 3:
                self.enemiesList.append(FastEnemy(self.ui.cellSize, self.ui.worldSize))
                self.fastEnemyCounter = 0

            #Spawn a new enemy 
            else:
                self.enemiesList.append(Enemy(self.ui.cellSize, self.ui.worldSize))
                self.fastEnemyCounter += 1
 
        #Update all enemies  
        self.enemiesListCopy = self.enemiesList  #Create a copy of the enemies list to prevent iteration errors, change later to a lambda function
        for enemy in self.enemiesListCopy:
            #If the enemy is out of the world bounds delete it, else move it
            if enemy.pos.x >= (self.ui.windowSize.x - self.ui.cellSize.x) or enemy.pos.y >= (self.ui.windowSize.y - self.ui.cellSize.y):
                #Deletes the enemy
                self.enemiesList.remove(enemy) 

            #Check if the player has clicked
            elif self.player1.clickPos != Vector2(0, 0):
                collide = enemy.rectangle.collidepoint(self.player1.clickPos)  #Determines if a collision has happened
                
                #If a collision has occured update player and enemy
                if collide:
                    self.player1.update(enemy.points)
                    self.enemiesList.remove(enemy)
                    enemy.deathSound.play()
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
            Enemy.render(self.ui.window)

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

class SettingsGameMode(MenuGameMode):
    #Overrides the parent class
    def __init__(self, UI):
        #Inherits the methods and attributes of the parent class
        super().__init__(UI) 

        #List of all keybinds
        self.hotkeys = [
            {	
                'menuItemName': 'Move Up',
                'hotkey': 'W', 
                'action': lambda: print('up') #commandMoveUp(Command)
            },
            {
                'menuItemName': 'Move Down',
                'hotkey': 'S', 
                'action': lambda: print('down') #commandMoveDown(Command)
            },
            {
                'menuItemName': 'Move Left',
                'hotkey': 'A', 
                'action': lambda: print('left') #commandMoveLeft(Command)
            },
            {	
                'menuItemName': 'Move Right',
                'hotkey': 'D', 
                'action': lambda: print('right') #commandMoveRight(Command)
            },
            {
                'menuItemName': 'Jump',
                'hotkey': 'Space', 
                'action': lambda: print('space') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'DisplayFPS',
                'hotkey': 'F1', 
                'action': lambda: print('left') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'SpecialAbility',
                'hotkey': 'E', 
                'action': lambda: print('E') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Grenade',
                'hotkey': 'Q', 
                'action': lambda: print('Q') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Shoot',
                'hotkey': 'Mouse1', 
                'action': lambda: print('M1') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Temp',
                'hotkey': 'T', 
                'action': lambda: print('T') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special1',
                'hotkey': 'spec1', 
                'action': lambda: print('spec1') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special2',
                'hotkey': 'spec2', 
                'action': lambda: print('spec2') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special3',
                'hotkey': 'spec3', 
                'action': lambda: print('spec3') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special4',
                'hotkey': 'spec4', 
                'action': lambda: print('spec4') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special5',
                'hotkey': 'Special5', 
                'action': lambda: print('Special5') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special6',
                'hotkey': 'Special6', 
                'action': lambda: print('Special6') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special7',
                'hotkey': 'Special', 
                'action': lambda: print('Special7') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'end',
                'hotkey': 'end', 
                'action': lambda: print('end') #commandMoveLeft(Command)
            },
        ]
        self.hotkeysMaxLen = (len(self.hotkeys) - 1)
		
        self.indexOffset = 0
        self.indexMin = 0
        self.indexMax = None
        self.indexOffsetIncrease = None
        self.indexOffsetDecrease = None
        self.indexOffsetChanged = None
        
        self.cursorIndex = 0
        self.menuName = "Settings"
        self.menuItems = []
        self.menuItemsDisplayed = 0
        self.menuItemsDisplayedChanged = None
        self.moveMenu = None

        self.paddingBottom = 50

    def processInput(self):
        #Event handling 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Exit the loop
                self.ui.quitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.currentMenuItem > self.indexMin:
                        self.moveMenu = 'up'
                        #If the User's cursor is halfway up the screen and the index offset is not 0 lower offset
                        if self.currentMenuItem < self.menuMiddle and self.indexOffset != 0:
                            self.indexOffsetDecrease = True
                        
                elif event.key == pygame.K_s:
                    if self.currentMenuItem < self.indexMax:
                        self.moveMenu = 'down'
			            #If the User's cursor is halfway down the screen and the display list will not exceed the hotkeys master list length
                        if self.currentMenuItem > self.menuMiddle and (self.menuItemsDisplayed + self.indexOffset) <= self.hotkeysMaxLen:
                            self.indexOffsetIncrease = True
                           
                elif event.key == pygame.K_RETURN:
                    #Gets the current menuitems action
                    self.menuItem = self.menuItems[self.currentMenuItem]

                elif event.key == K_ESCAPE:
                    self.ui.showMenu()

    def update(self):
      #Add in update code from menugamemode
        if self.menuItem is not None:
            try:
                #Execute the current menuitems Action lambda function
                self.menuItem['action']() 
                self.menuItem = None
            except Exception as ex:
                print(ex)

        #Adjust indexOffset
        if self.indexOffsetIncrease == True:
            self.indexOffset += 1
            self.indexOffsetChanged = True

        elif self.indexOffsetDecrease == True:
            self.indexOffset -= 1
            self.indexOffsetChanged = True

        #User selection moves up
        #I check to make sure the index has not changed to prevent skipping a value. If the index 
        # changes and we move the menuItem the result is changing two positions instead of one.
        if self.moveMenu == 'up' and self.indexOffsetChanged != True:
            self.currentMenuItem -= 1

        #User selection moves down
        elif self.moveMenu == 'down' and self.indexOffsetChanged != True:
            self.currentMenuItem += 1

        #Clear values
        self.moveMenu = None
        self.indexOffsetIncrease = None
        self.indexOffsetDecrease = None

    def render(self): 
        paddingLeft = 20
        paddingRight = 500
        
        #
        def updateHeight(surface):
            updatedHeight = (120 * surface.get_height()) // 100
            return updatedHeight

        #Determines how many menu items can be displayed
        def itemsDisplayed(y):
            menuItemsDisplayed = 0
            for item in self.hotkeys:
                surface = self.font.render(item['menuItemName'], True, (200, 0, 0))

                #Update y-pos so items are not overlaping
                y += updateHeight(surface)

                menuItemsDisplayed += 1

                if y >= self.ui.windowSize.y - self.paddingBottom:
                    break

            return menuItemsDisplayed

        #Creates a list containing the menu items to display from the master hotkeys list
        def createDisplayList():
            displayList = []
            for index in range(self.menuItemsDisplayed):
                try:
                    displayList.append(self.hotkeys[index + self.indexOffset])
                except:
                    print("Index error in createDisplayList")
                
            return displayList

        #Computes where the x-pos should be to center the font surface
        def centerFontX(surface):
            offset = surface.get_width() // 2 #Take the length of the font divided by 2
            x = (self.ui.window.get_width() // 2) - offset #Take half the window width and the offset to determine where to draw

            return x

        # Initial y
        y = 50

        #Amount of pixels to space out text from the edges of the window
        padding = 20

        # Title
        surface = self.font.render(self.menuName, True, (200, 0, 0))
        x = centerFontX(surface)
        self.ui.window.blit(surface, (x, y))

        y += (200 * surface.get_height()) // 100  #Change the y-pos to draw the menu items

        #If this is the first iteration or the screen size has been changed, recreate the list 
        if self.menuItemsDisplayedChanged == None or self.menuItemsDisplayedChanged == True:
            self.menuItemsDisplayed = itemsDisplayed(y)
            self.menuMiddle = round(self.menuItemsDisplayed / 2)
            self.menuItemsDisplayedChanged = False

	    #If this is the first iteration or the index offset has been changed, recreate the list 
        if self.indexOffsetChanged == None or self.indexOffsetChanged == True:
            self.menuItems = createDisplayList()
            self.indexMax = (len(self.menuItems) - 1)
            self.indexOffsetChanged = False

        #Render list
        for item in self.menuItems:         
            #Draw each menuItem to the screen
            surface = self.font.render(item['menuItemName'], True, (200, 0, 0))
            x = paddingLeft
            self.ui.window.blit(surface, (x, y))

            #Draw each hotkey to the screen
            surface = self.font.render(item['hotkey'], True, (200, 0, 0))
            x = paddingRight
            self.ui.window.blit(surface, (x, y))
            
            #Cursor
            index = self.menuItems.index(item)

            #Render the cursor at the current MenuItem selected
            if index == self.currentMenuItem:
                surface = self.menuCursor.render("-->", True, (200, 0, 0))
                cursorX = x - (surface.get_width() + 10) 
                cursorY = y
                self.ui.window.blit(surface, (cursorX, cursorY))

            #Update y-pos so items are not overlaping
            y += updateHeight(surface)