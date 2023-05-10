import pygame
import numpy as np
from scene import Scene
from math import sqrt
from animation import Timer

timer = Timer()

class Game:
    def __init__(self, first_scene:Scene, frame_rate:int):
        assert isinstance(first_scene, Scene)
        self.active_scene = first_scene
        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()

        self.last_function = lambda: print("End of the game.")

    def run(self): 
        while self.active_scene is not None:
            # Get user input
            pressed_keys = pygame.key.get_pressed()
            filtered_events = []
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active_scene.terminate()
                    FadeOut(self.active_scene, 40)
                else:
                    filtered_events.append(event)

            # Manage scene
            self.active_scene.process_input(filtered_events, pressed_keys, mouse_pos)
            self.active_scene.update()
            if self.active_scene == self.active_scene.next_scene:
                self.active_scene.render()
            else:
                self.active_scene = self.active_scene.next_scene

            # Update and tick
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

        # Call last function before shutting down the window
        self.last_function()



def FadeIn(scene:Scene, fq:int, alpha=255):
    fade_surface = pygame.Surface((scene.surface.get_width(), scene.surface.get_height()), pygame.SRCALPHA, 32)
    while alpha > 10:
        scene.render()
        fade_surface.fill((0,0,0,alpha))
        scene.surface.blit(fade_surface, (0,0))
        pygame.display.flip()
        alpha -= fq
        pygame.time.wait(10)
    pygame.event.clear()


def FadeOut(scene:Scene, fq:int, alpha=0):
    fade_surface = pygame.Surface((scene.surface.get_width(), scene.surface.get_height()), pygame.SRCALPHA, 32)
    while alpha < 245:
        scene.render()    
        fade_surface.fill((0,0,0,alpha))
        scene.surface.blit(fade_surface, (0,0))
        pygame.display.flip()
        alpha += fq
        pygame.time.wait(10)
    pygame.event.clear()


def HorizontalSlidingIn(scene:Scene, speed:int): #speed = 30 : default
    size = scene.surface.get_size()
    block = pygame.Surface((size[0]/2+50, size[1]))
    right_block_pos_x = -50
    left_block_pos_x = size[0]/2
    while right_block_pos_x > -size[0]/2-50:
        scene.render()
        scene.surface.blit(block, (right_block_pos_x, 0))
        scene.surface.blit(block, (left_block_pos_x, 0))
        right_block_pos_x -= speed
        left_block_pos_x += speed
        speed **= 0.95
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.event.clear()


def HorizontalSlidingOut(scene:Scene, speed:int):
    size = scene.surface.get_size()
    block = pygame.Surface((size[0]/2+50, size[1]))
    right_block_pos_x = -size[0]/2-50
    left_block_pos_x = size[0]
    while right_block_pos_x < 0:
        scene.render()
        scene.surface.blit(block, (right_block_pos_x, 0))
        scene.surface.blit(block, (left_block_pos_x, 0))
        right_block_pos_x += speed
        left_block_pos_x -= speed
        speed **= 0.95
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.event.clear()


def CirclerOut(scene:Scene, speed:int = 30, position:tuple = None, cutting_color = (0, 0, 0, 0)):
    size = scene.surface.get_size()
    circle_surface = pygame.Surface(size, pygame.SRCALPHA, 32)
    radius = max(size[0], size[1]) / 2
    if not position:
        position = (size[0] / 2, size[1] / 2)
    while radius > 1:
        scene.render()
        circle_surface.fill((0, 0, 0, 255))
        pygame.draw.circle(circle_surface, cutting_color, position, radius)
        scene.surface.blit(circle_surface, (0, 0))
        pygame.display.flip()
        radius -= speed
        pygame.time.wait(10)
    pygame.event.clear()

def CirclerIn(scene:Scene, speed:int = 30, position:tuple = None, circle_color = (0, 0, 0, 255)):
    size = scene.surface.get_size()
    circle_surface = pygame.Surface(size, pygame.SRCALPHA, 32)
    radius = max(size[0], size[1]) / 2
    if not position:
        position = (size[0] / 2, size[1] / 2)
    while radius > 1:
        scene.render()
        circle_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(circle_surface, circle_color, position, radius)
        scene.surface.blit(circle_surface, (0, 0))
        pygame.display.flip()
        radius -= speed
        pygame.time.wait(10)
    pygame.event.clear()


### Not finished
def SquareOut(scene:Scene, speed:int = 30, position:tuple = None, cutting_color = (0, 0, 0, 0)):
    size = scene.surface.get_size()
    square_surface = pygame.Surface(size, pygame.SRCALPHA, 32)
    length = int(max(size[0], size[1]) / 2 - 1)
    if not position:
        position = (size[0] / 2, size[1] / 2)
    while length > 1:
        scene.render()
        square_surface.fill((0, 0, 0, 255))
        transparent_rect = (position[0] - length / 2, position[1] - length / 2, length, length)
        pygame.draw.rect(square_surface, cutting_color, transparent_rect)
        square_surface = pygame.transform.rotate(square_surface, speed)
        scene.surface.blit(square_surface, (0, 0))
        pygame.display.flip()
        length -= speed
        pygame.time.wait(10)
    pygame.event.clear()

def SquareIn(scene:Scene, speed:int = 30, position:tuple = None, cutting_color = (0, 0, 0, 255)):
    size = scene.surface.get_size()
    square_surface = pygame.Surface(size, pygame.SRCALPHA, 32)
    length = int(max(size[0], size[1]) / 2 - 1)
    if not position:
        position = (size[0] / 2, size[1] / 2)
    while length > 1:
        scene.render()
        square_surface.fill((0, 0, 0, 0))
        square_rect = (position[0] - length / 2, position[1] - length / 2, length, length)
        pygame.draw.rect(square_surface, cutting_color, square_rect)
        square_surface = pygame.transform.rotate(square_surface, speed)
        scene.surface.blit(square_surface, (0, 0))
        pygame.display.flip()
        length -= speed
        pygame.time.wait(10)
    pygame.event.clear()