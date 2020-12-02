import math
import random
import numpy as np
import pygame
from pygame import gfxdraw
from sim.settings import WIDTH, HEIGHT, GREEN, BLUE
from sim.helpers import fill_pie, circularize

# Creature is the parent class for a creature in the simulation, 
# with attributes such as health, speed, sight, and view angle 
class Creature:

    def __init__(self, x, y, size, speed, sight, view, rep, color):
        # positioning and velocity
        self.pos = np.array([x,y], dtype='float64')
        self.vel = np.array([0,0], dtype='float64')
        self.theta = 0

        # age, generation, parent, color
        self.age = 1
        self.gen = 0
        self.parent = None
        self.creature_color = color
        self.color = color
        
        # creature attributes
        self.health = size*10
        self.max_health = self.health*2
        self.size = size
        self.speed = speed
        self.sight = sight
        self.view = view
        self.rep = rep
        self.dna = [self.size, self.speed, self.sight, self.view, self.rep]
        # loss function for energy consumption
        self.loss = math.floor((self.size**2 + self.speed**3 + self.sight//3 + self.view//2)/10)

        # turning away from boundaries 
        self.turn_theta = 0
        self.turning_time = 0
        # turning smoothly to food
        self.smooth_counter = 0
        self.smooth_points = []
        self.food_target = None
        # smart creatures will move to closer food sources even if a food target is already found
        self.smart = False

    # draw the sightline of a creature
    def percept(self, window):
        # find current theta
        if np.all((self.vel != 0)):
            theta = math.degrees(math.atan2(self.vel[1], self.vel[0]))
        else:
            theta = 0
        theta = circularize(theta)
        self.theta = theta
        # find points defining creature's view wrt theta
        points = fill_pie((int(self.pos[0]), int(self.pos[1])), self.sight, theta-self.view, theta+self.view, 20)
        # draw transparent sightline
        s = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        gfxdraw.filled_polygon(s, points, (0,255,255,150))
        window.blit(s,(0,0))

    # change  position to seek towards  target position
    def seek(self, target):
        vector = target - self.pos
        norm = (vector[0]**2 + vector[1]**2)**0.5
        output = vector/norm * self.speed
        self.vel = output
        self.pos += self.vel

    # handle aging, health loss
    def step(self):
        self.age += 1
        self.health -= self.loss/100
        # creature has a maximum health so it can't hoard food
        self.health = min(self.health, self.max_health)
        # change color based on health (same color when over half max_health)
        if self.health <= self.max_health/2:
            if self.creature_color == GREEN:
                self.color = (max(min((1-self.health/100)*255,255),0), max(min(self.health/100*255,255),0), 0)
            elif self.creature_color == BLUE:
                self.color = (max(min((1-self.health/100)*255,255),0), 0, max(min(self.health/100*255,255),0))
        else:
            self.color = self.creature_color

    # given a list of foods, turn smoothly to the closest one, and eat if reaching it
    def eat(self, foods): 
        # find closest food
        closest_pos, closest_i = self.find_food(foods)

        # at start, assign random start
        if np.all((self.vel==0)):
            random_start = np.array([random.uniform(0,WIDTH), random.uniform(0,HEIGHT)], dtype='float64')
            self.seek(random_start)

        # if smart creature, only seek food if less than 1/2 health, otherwise continue in last direction
        elif self.smart and self.health > self.max_health/2:
            self.boundary_check()
            self.pos += self.vel
            return

        # if no food found, continue in last direction
        elif closest_i == -1:
            # check for boundaries and navigate away 
            self.boundary_check()
            self.pos += self.vel
            return

        # if no current food target and food found, assign as target and turn smoothly 
        elif self.food_target is None:
            closest_food = foods[closest_i]
            closest_dist = math.hypot(self.pos[0]-closest_food.pos[0], self.pos[1]-closest_food.pos[1])
            self.food_target = foods[closest_i]

            # calculate smooth points
            food_vector = [closest_pos[0]-self.pos[0], closest_pos[1]-self.pos[1]]
            alpha = (self.vel[0]*food_vector[0] + self.vel[1]*food_vector[1]) / ((self.vel[0]**2+self.vel[1]**2)**0.5 * (food_vector[0]**2+food_vector[1]**2)**0.5)
            if alpha > 1:
                alpha = 1
            elif alpha < -1:
                alpha = -1
            alpha = math.degrees(math.acos(alpha))
            curr_theta = math.degrees(math.atan2(self.vel[1], self.vel[0]))
            cross = food_vector[0]*self.vel[1] - food_vector[1]*self.vel[0]
            if cross > 0:
                alpha *= -1
            self.smooth_points = fill_pie((int(self.pos[0]), int(self.pos[1])), closest_dist, curr_theta, curr_theta+alpha, 5)[1:]

            # seek first smooth point, increment smooth counter
            self.seek(self.smooth_points[self.smooth_counter])
            self.smooth_counter += 1

        # else if there is any food target, continue the smooth turn
        elif self.smooth_counter < 5:
            self.seek(self.smooth_points[self.smooth_counter])
            self.smooth_counter += 1

        # else if finished smooth turn, closest food is same as current target, continue towards current target
        elif self.food_target == foods[closest_i]:
            self.seek(closest_pos)

        # else if closer food found now that turned, still continue to old food but assign closer food as target
        elif not foods[closest_i].ate and self.smart:
            closest_food = foods[closest_i]
            closest_dist = math.hypot(self.pos[0]-closest_food.pos[0], self.pos[1]-closest_food.pos[1])
            self.food_target = foods[closest_i]
            self.smooth_counter = 0

            # calculate smooth points
            food_vector = [closest_pos[0]-self.pos[0], closest_pos[1]-self.pos[1]]
            alpha = (self.vel[0]*food_vector[0] + self.vel[1]*food_vector[1]) / ((self.vel[0]**2+self.vel[1]**2)**0.5 * (food_vector[0]**2+food_vector[1]**2)**0.5)
            if alpha > 1:
                alpha = 1
            elif alpha < -1:
                alpha = -1
            alpha = math.degrees(math.acos(alpha))
            curr_theta = math.degrees(math.atan2(self.vel[1], self.vel[0]))
            cross = food_vector[0]*self.vel[1] - food_vector[1]*self.vel[0]
            if cross > 0:
                alpha *= -1
            self.smooth_points = fill_pie((int(self.pos[0]), int(self.pos[1])), closest_dist, curr_theta, curr_theta+alpha, 5)[1:]

            # seek first smooth point, increment smooth counter
            self.seek(self.smooth_points[self.smooth_counter])
            self.smooth_counter += 1

        # else if food still isn't closest, but isn't eaten, continue towards it
        elif not self.food_target.ate:
            self.seek(self.food_target.pos)

        # if a different target, reset smooth_counter and assign new food target
        else:
            self.food_target = foods[closest_i]
            self.smooth_counter = 0
            self.pos += self.vel

        # if reaching food, eat it, reset targets
        closest_food = foods[closest_i]
        closest_dist = math.hypot(self.pos[0]-closest_food.pos[0], self.pos[1]-closest_food.pos[1])
        if closest_dist < self.size:
            self.health += closest_food.nut
            closest_food.ate = True
            self.food_target = None
            self.smooth_counter = 0

    # find the closest food and return its position and index
    def find_food(self, foods):
        # get the creatures view angles
        start_a = circularize(self.theta - self.view)
        end_a = circularize(self.theta + self.view)

        # get foods within circle of creature sight
        view_foods = []
        for food in foods[:]:
            dist = math.hypot(self.pos[0]-food.pos[0], self.pos[1]-food.pos[1])
            if dist < self.sight:
                # then get foods within creature view angles
                food_a = circularize(math.degrees(math.atan2(food.pos[1]-self.pos[1], food.pos[0]-self.pos[0])))
                if start_a < end_a:
                    if food_a > start_a and food_a < end_a:
                        view_foods.append(food)
                else:
                    if food_a > start_a:
                        view_foods.append(food)
                    elif food_a < end_a:
                        view_foods.append(food)

        # find the closest of the foods within view
        closest_dist = max(WIDTH, HEIGHT)
        closest_i = -1
        closest_pos = np.array([0,0], dtype='float64')
        for food in view_foods[:]:
            dist = math.hypot(self.pos[0]-food.pos[0], self.pos[1]-food.pos[1])
            if dist < closest_dist:
                closest_dist = dist
                closest_i = foods.index(food)
                closest_x = food.pos[0]
                closest_y = food.pos[1]
        if closest_i > -1:
            closest_pos = np.array([closest_x, closest_y], dtype='float64')

        # return position, index of closest food
        return closest_pos, closest_i

    # use age/reproduction chance to reproduce a genetically similar offspring
    def reproduce(self, creatures, creature):
        trait_violation = True
        rep_mutation = False
        if self.age % 1000 == 0:
            if random.random()*100 < self.rep:
                # make sure offspring has traits within bounds
                while trait_violation:
                    if rep_mutation:
                        random_trait = random.randint(0,4)
                    else:
                        random_trait = random.randint(0,3)
                    offspring_traits = [self.size, self.speed, self.sight, self.view, self.rep] 
                    if random_trait == 0:
                        mut_val = random.randint(-5,5)
                    elif random_trait == 1:
                        mut_val = random.randint(-1,1)
                    elif random_trait == 2 or random_trait == 3:
                        mut_val = random.randint(-20, 20)
                    elif random_trait == 4:
                        mut_val = random.randint(-5,5)
                    offspring_traits[random_trait] += mut_val

                    if offspring_traits[0]>3 and offspring_traits[0]<20 and offspring_traits[1]>0 and offspring_traits[2]>5 and offspring_traits[3]>5 and offspring_traits[3]<180 and offspring_traits[4]<100:
                        trait_violation = False

                # create new offspring with mutated traits
                offspring = creature(self.pos[0]+self.size*2, self.pos[1]+self.size*2, offspring_traits[0], offspring_traits[1], offspring_traits[2], offspring_traits[3], offspring_traits[4], self.creature_color)
                offspring.gen = self.gen+1
                offspring.parent = self
                random_start = np.array([random.uniform(0,WIDTH), random.uniform(0,HEIGHT)], dtype='float64')
                offspring.seek(random_start)
                creatures.append(offspring)

    # checks if the noodle is within a tolerance of the boundary, turn in random direction away
    def boundary_check(self):
        # tolerance, potential turning angles
        tol = 10
        turns = [50, -50, 75, -75]

        # find the current next position
        next_x = self.pos[0]+self.vel[0]
        next_y = self.pos[1]+self.vel[1]

        # if outside tolerance of boundaries, use turning theta for a new velocity vector
        if next_x-tol < 0 or next_x+tol>WIDTH or next_y-tol<0 or next_y+tol>HEIGHT:
            # if no turning angle, assign a random one, start turn counter
            if self.turn_theta == 0:
                self.turn_theta = random.choice(turns)
            else:
                self.turning_time += 1
            x_prime = self.vel[0]*math.cos(self.turn_theta) - self.vel[1]*math.sin(self.turn_theta)
            y_prime = self.vel[0]*math.sin(self.turn_theta) + self.vel[1]*math.cos(self.turn_theta)
            self.vel = [x_prime, y_prime]

        # if within boundaries, reset
        else:
            self.turn_theta = 0
            self.turning_time = 0

        # if it has been turning for more than some number of loops, change theta
        if self.turning_time > random.randint(25,40):
            self.turn_theta *= -1
            self.turning_time = 0