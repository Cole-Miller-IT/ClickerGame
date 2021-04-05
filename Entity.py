import pygame
import random
from pygame.locals import *
from pygame.math import Vector2

class Entity:
    def __init__(self, cellSize):
        self.pos = Vector2()  #Position of the Entity
        self.status = "Alive"

        #Entity's pygame surface
        self.surf = pygame.Surface((cellSize.x, cellSize.y))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def debug(self):
        print("Entity")



class Enemy(Entity):
    def __init__(self, cellSize, worldSize):
        super().__init__(cellSize)  # Inherits all methods and attributes of the parent class
        self.cellSize = cellSize
        self.worldSize = worldSize
        self.moveSpeed = 1          

        # Generates a random start location
        self.spawnPosY = 0  #Spawn at the top of the map
        self.spawnPosX = random.randint(0, (worldSize.x - 1)) #Spawn at a random location on the x-axis
        self.spawnPos = Vector2(self.spawnPosX, self.spawnPosY)

        self.pos = Vector2(self.spawnPos).elementwise() * self.cellSize
        self.surf.fill((100, 0, 0))

        self.rectangle = pygame.Rect(self.pos.x, self.pos.y, self.cellSize.x, self.cellSize.y)
        
    #Moves the enemy
    def update(self):
        #self.pos.update(self.pos.x, self.pos.y + self.moveSpeed)
        self.pos = Vector2(self.pos.x, self.pos.y + self.moveSpeed)

    #Draw the enemy to a surface (ie. window)
    def render(self, window, color):
        self.rectangle = pygame.Rect(self.pos.x, self.pos.y, self.cellSize.x, self.cellSize.y)
        pygame.draw.rect(window, color, self.rectangle)

    def debug(self):
        print(self.pos)

class Player(Entity):
    def __init__(self, cellSize, worldSize):
        super().__init__(cellSize)  # Inherits all methods and attributes of the parent class
        self.cellSize = cellSize
        self.worldSize = worldSize
        self.score = 0
        self.clickPos = Vector2()
        #self.pos = Vector2()

    def processInput(self):
        self.clickPos = Vector2(pygame.mouse.get_pos())

    def update(self):
        self.score = self.score + 1
        #print(self.score)