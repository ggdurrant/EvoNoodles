import math
import csv

# Helper functions
# make an angle always positive
def circularize(theta):
    if theta < 0:
        theta += 360
    elif theta > 360:
        theta -= 360
    return theta

# get points along an arc, and the center at index 0
def fill_pie(center, radius, start, stop, divs):
    x0, y0 = center
    dtheta = (stop-start)/divs
    angles = [start + i*dtheta for i in range(divs+1)]

    points = [(x0,y0)] + [(x0 + radius*math.cos(math.radians(theta)), y0 + radius*math.sin(math.radians(theta))) for theta in angles]
    return points

# write log of noodle history to csv
def log_history(name, log):
    with open(name, 'w', newline='') as f:
        c = csv.writer(f)
        c.writerow(['Epoch', 'Living', 'Age', 'Gen', 'Health', 'Size', 'Speed', 'Sight', 'View', 'Rep', 'Loss', 'Ancestors'])
        for key, value in log.items():
            c.writerow([key]+value)

# get new log of all attributes for all current noodles
def log_attributes(noodles, ancs=[]):
    ages, gens, healths, sizes, speeds, sights, views, reps, losses = ([] for i in range(9))
    for noodle in noodles:
        ages.append(noodle.age)
        gens.append(noodle.gen)
        healths.append(noodle.health)
        sizes.append(noodle.size)
        speeds.append(noodle.speed)
        sights.append(noodle.sight)
        views.append(noodle.view)
        reps.append(noodle.rep)
        losses.append(noodle.loss)
    entry = [len(noodles), ages, gens, healths, sizes, speeds, sights, views, reps, losses, ancs]
    return entry

def average(lst):
    if len(lst)!=0:
        return sum(lst)/len(lst)
    else:
        return 0

def get_ancestors(noodle, output=[]):
    if noodle is None:
        return output
    else:
        return get_ancestors(noodle.parent)+[noodle.dna]