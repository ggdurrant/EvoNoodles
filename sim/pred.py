import math
import numpy as np
import pygame.draw
from sim.settings import BLUE
from sim.noodle import Noodle
from sim.food import Food
from sim.helpers import circularize, fill_pie

# Pred is a child of Creature class, with additional health and smart predator attributes
class Pred(Noodle):
    
    # initialize pred as smart creature to chase closest prey, only if health below threshold
    def __init__(self, x, y, size, speed, sight, view, rep, color=BLUE):
        super().__init__(x, y, size, speed, sight, view, rep, color)
        self.health = self.health*2
        self.max_health = self.max_health*2
        self.smart = True

    # draw triangular pred
    def draw(self, window):
        if np.all((self.vel != 0)):
            theta = math.degrees(math.atan2(self.vel[1], self.vel[0]))
        else:
            theta = 0
        theta = circularize(theta)
        points = fill_pie((int(self.pos[0]), int(self.pos[1])), self.size*4, theta-160, theta+160, 1)
        pygame.draw.polygon(window, self.color, points)

    # kill pred if health depleted and replace with food
    def kill(self, preds, foods):
        if self.health < 0:
            foods.append(Food(int(self.pos[0]), int(self.pos[1]), self.size*6))
            preds.remove(self)