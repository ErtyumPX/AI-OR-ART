import pygame
from game import *
import defaults, time

#SCENES
from main_scene import MainScene

pygame.init()

pygame.mouse.set_cursor(*defaults.CURSOR)

root = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

defaults.SIZE = size = rootX, rootY = root.get_size()

pygame.display.set_caption(defaults.WINDOW_NAME)

game = Game(MainScene(root), defaults.FRAME_RATE)

game.run()
