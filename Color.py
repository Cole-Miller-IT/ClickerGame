try:
    import pygame
    from pygame.locals import *
    import sys

except ImportError as error:
    print("Couldn't load module.")
    print(error)
    sys.exit(2)

black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
