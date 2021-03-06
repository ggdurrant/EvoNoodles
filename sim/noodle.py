import pygame.draw
from sim.settings import GREEN
from sim.creature import Creature
from sim.food import Food

# Noodle is a child of Creature class, with prey attributes
class Noodle(Creature):
    
    # initialize noodle with nutrition value and ate attribute 
    def __init__(self, x, y, size, speed, sight, view, rep, color=GREEN):
        super().__init__(x, y, size, speed, sight, view, rep, color)
        self.nut = 150
        self.ate = False

    # draw circular noodle
    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.pos[0]), int(self.pos[1])), self.size)

    # kill and replace with food if health depleted, or just kill if eaten
    def kill(self, noodles, dead_noodles, foods):
        if self.health < 0:
            foods.append(Food(int(self.pos[0]), int(self.pos[1]), self.size*4))
            dead_noodles.append(self)
            noodles.remove(self)
        elif self.ate:
            dead_noodles.append(self)
            noodles.remove(self)