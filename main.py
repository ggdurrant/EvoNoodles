import random
import pygame
from sim.noodle import Noodle
from sim.pred import Pred
from sim.food import Food
from sim.settings import HEIGHT, WIDTH, BLACK, STARTING_NOODLES, STARTING_PREDS, TOTAL_FOOD
from sim.helpers import get_ancestors, log_attributes, log_history

# if simulate, greatly speeds up sim to get mutation of multiple generations
SIMULATE = False
# if save, will save output of noodles and preds in csv file
SAVE = False

# method to run simulation
def main():

    # initialize pygame
    pygame.init()
    game_display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    # redraw the display, noodles, and food
    def redraw_window():
        # draw background
        game_display.fill(BLACK)
        # draw foods, noodles, preds
        for food in foods[:]:
            food.draw(game_display)
        for noodle in noodles[:]:
            noodle.draw(game_display)
            noodle.percept(game_display)
        for pred in preds[:]:
            pred.draw(game_display)
            pred.percept(game_display)
        #update display
        pygame.display.update()

    # lists of objects
    noodles = []
    foods = []
    dead_noodles = []
    preds = []
    noodle_history = {}
    pred_history = {}

    # timers
    total_steps = 0
    food_timer = 0
    fps = 30

    # initialize noodles, foods, preds
    for i in range(STARTING_NOODLES):
        noodles.append(Noodle(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10), random.randint(6,10), random.randint(1,4), random.randint(30,200), random.randint(20,120), random.randint(15,35)))
    for i in range(STARTING_PREDS):
        preds.append(Pred(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10), random.randint(8,12), random.randint(3,5), random.randint(200,400), random.randint(10,40), random.randint(25,45)))
    for i in range(TOTAL_FOOD):
        foods.append(Food(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10)))

    # main loop
    while running:
        # if simulate, speed up, else run at set FPS
        if SIMULATE:
            clock.tick(1080)
            if total_steps%480 == 0:
                redraw_window()
        else:
            clock.tick(fps)
            redraw_window()

        # if exited, quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # noodle updates
        for noodle in noodles[:]:
            # if eaten by pred, kill
            if noodle.ate:
                noodle.kill(noodles, dead_noodles, foods)
            else:
                noodle.eat(foods)
                noodle.step()
                noodle.reproduce(noodles, Noodle)
                noodle.kill(noodles, dead_noodles, foods)

        # pred updates
        for pred in preds[:]:
            pred.eat(noodles)
            pred.step()
            pred.reproduce(preds, Pred)
            pred.kill(preds, foods)
        
        # food updates
        for food in foods[:]:
            # check if any foods have been eaten and remove them
            if food.ate:
                for noodle in noodles[:]:
                    # reset any noodles that have that food as their target
                    if noodle.food_target == food:
                        noodle.food_target = None
                        noodle.smooth_counter = 0
                foods.remove(food)
                # food_timer += 3
                food_timer += 0
        # if a food recently eaten, don't add a food until timer goes down
        if food_timer > 0:
            food_timer -= 1
        elif len(foods)<TOTAL_FOOD:
            foods.append(Food(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10)))
        # every 500 steps, make sure we go back to full food
        if total_steps%500 == 0:
            while len(foods)<TOTAL_FOOD:
                foods.append(Food(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10)))

        # potential immigrant noodle every 5000 steps, immigrant pred every 20000 steps
        if total_steps%5000 == 0 and total_steps > 0 and random.random() < 0.8:
            noodles.append(Noodle(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10), random.randint(4,12), random.randint(1,5), random.randint(30,200), random.randint(20,140), random.randint(15,35)))
        if total_steps%20000 == 0 and total_steps > 0 and random.random() < 0.8:
            preds.append(Pred(random.randint(10, WIDTH-10), random.randint(10, HEIGHT-10), random.randint(8,12), random.randint(3,5), random.randint(200,400), random.randint(10,40), random.randint(25,45)))

        # update total system age
        total_steps += 1

        # print steps, noodles for observation
        if total_steps%500 == 0 and len(noodles) is not 0:
            print('Epoch: '+str(int(total_steps/500))+'   Noodles: '+str(len(noodles))+'   Preds: '+str(len(preds)))

        # add to historical log if save
        if total_steps%500 == 0 and SAVE:
            noodle_history[int(total_steps/500)] = log_attributes(noodles)
            pred_history[int(total_steps/500)] = log_attributes(preds)

        # save checkpoint log every 10000 steps if save
        if total_steps%25000 == 0 and SAVE:
            ancs = []
            for noodle in noodles[:]:
                ancs.append(get_ancestors(noodle))
            noodle_history[max(noodle_history.keys())] = log_attributes(noodles, ancs)
            pancs = []
            for pred in preds[:]:
                pancs.append(get_ancestors(pred))
            pred_history[max(pred_history.keys())] = log_attributes(preds, pancs)
            log_history('data/noodle_checkpoint.csv', noodle_history)
            log_history('data/pred_checkpoint.csv', pred_history)
            print('checkpoint saved...')

        # quit if all creatures dead
        if len(noodles)==0 and len(preds)==0:
            print('all creatures extinct...')
            running = False
        
    # log the history to csv
    if SAVE and total_steps>500:
        ancs = []
        for noodle in noodles[:]:
            ancs.append(get_ancestors(noodle))
        noodle_history[max(noodle_history.keys())] = log_attributes(noodles, ancs)
        pancs = []
        for pred in preds[:]:
            pancs.append(get_ancestors(pred))
        pred_history[max(pred_history.keys())] = log_attributes(preds, pancs)

        log_history('data/noodle_output.csv', noodle_history)
        log_history('data/pred_output.csv', pred_history)
        print('history saved...')

    # end game
    pygame.quit()
    quit()

if __name__ == "__main__":  
    main()