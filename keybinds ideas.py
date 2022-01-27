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
                    self.ui.showMenuOverlay()

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
