import pygame
import random
from pygame.locals import *
from pygame.math import Vector2

#--------------------------------------------------------------------------------------------
class Entity:
    def __init__(self, cellSize):
        #Position of the Entity
        self.pos = Vector2()  

        self.status = "Alive"

        #Entity's pygame surface
        self.surf = pygame.Surface((cellSize.x, cellSize.y))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def processInput(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def debug(self):
        print("Entity")


#Basic enemy class--------------------------------------------------------------------------------------------
class Enemy(Entity):
    def __init__(self, cellSize, worldSize):
        # Inherits all methods and attributes of the parent class
        super().__init__(cellSize)  

        self.cellSize = cellSize
        self.worldSize = worldSize
        self.moveSpeed = 1     
        self.color = (255, 0, 0)     
        self.points = 1
        self.deathSound = pygame.mixer.Sound("Assets\OwenWilson.mp3")

        # Generates a random start location
        self.spawnPosY = 0  #Spawn at the top of the map
        self.spawnPosX = random.randint(0, (worldSize.x - 1)) #Spawn at a random location on the x-axis
        self.spawnPos = Vector2(self.spawnPosX, self.spawnPosY)

        self.pos = Vector2(self.spawnPos).elementwise() * self.cellSize
        self.surf.fill((100, 0, 0))

        self.rectangle = pygame.Rect(self.pos.x, self.pos.y, self.cellSize.x, self.cellSize.y)
        
    #Moves the enemy
    def update(self):
        self.pos = Vector2(self.pos.x, self.pos.y + self.moveSpeed)

    #Draw the enemy to a surface (ie. window)
    def render(self, window):
        self.rectangle = pygame.Rect(self.pos.x, self.pos.y, self.cellSize.x, self.cellSize.y)
        pygame.draw.rect(window, self.color, self.rectangle)

    def debug(self):
        print(self.pos)

#An enemy class that moves faster than the basic one --------------------------------------------------------------------------------------------
class FastEnemy(Enemy):
    def __init__(self, cellSize, worldSize):
        Enemy.__init__(self, cellSize, worldSize)  # Inherits all methods and attributes of the parent class
        self.moveSpeed = 3
        self.color = (0, 255, 0)
        self.points = 5

    def debug(self):
        print("Fast enemy")

#A class that stores all variables and methods related to the player--------------------------------------------------------------------------------------------
class Player(Entity):
    def __init__(self, cellSize, worldSize):
        super().__init__(cellSize)  # Inherits all methods and attributes of the parent class
        self.cellSize = cellSize
        self.worldSize = worldSize
        self.score = 0
        self.clickPos = Vector2()

    def processInput(self):
        self.clickPos = Vector2(pygame.mouse.get_pos())

    def update(self, points):
        self.score = self.score + points
        #print(self.score)