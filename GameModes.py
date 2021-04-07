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


class MenuGameMode(GameMode):
    def __init__(self):
        pass

    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self, window):
        raise NotImplementedError()

class PlaeGameMode(GameMode):
    def __init__(self):
        pass
    
    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self, window):
        raise NotImplementedError()