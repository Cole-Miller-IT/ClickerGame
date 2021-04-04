import pygame
from pygame.locals import *
from pygame.math import Vector2

class Entity:
    def __init__(self, cellSize):
        self.pos = Vector2()  #Position of the Entity

        #Entity's pygame surface
        self.surf = pygame.Surface((cellSize.x, cellSize.y))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def debug(self):
        print("Entity")



class Enemy(Entity):
    def __init__(self, cellSize, pos):
        super().__init__(cellSize)  # Inherits all methods and attributes of the parent class
        self.pos = pos
        self.surf.fill((100, 0, 0))
    
    def update(self):
        self.pos = self.pos + 1

    def render(self, window, color):
        test = pygame.Rect(64, 64, 120, 120)
        pygame.draw.rect(window, self.color, test)