import pygame
from pygame.locals import *
from pygame.math import Vector2

class GameState():
    def __init__(self):
        self.gameRunning = True
       
        self.FPS = 30

        self.hotkeys = []
        self.commands = []
        self.entities = []
        self.layers = []
        self.score = 0

        self.worldSize = Vector2(12,10)
        self.cellSize = Vector2(64,64)