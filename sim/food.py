import numpy as np
import pygame
from sim.settings import YELLOW

# Food objects are edible by Noodles, with a default nutrition value of 25, 
# they spawn randomly or when a creature dies, which are worth more nutrition
class Food:
    
    # set default nutrition, coordinates
    def __init__(self, x, y, nut=25):
        self.pos = np.array([x,y], dtype='float64')
        self.nut = nut
        self.ate = False

    # draw circle of size 3
    def draw(self, window):
        pygame.draw.circle(window, YELLOW, (int(self.pos[0]), int(self.pos[1])), int(self.nut/7))