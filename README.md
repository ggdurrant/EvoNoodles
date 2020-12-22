# EvoNoodles

EvoNoodles is a natural selection simulator that looks at creatures, known as noodles, as they evolve in a environment competing for resources and surviving in the presence of predators. 


## Simulation

 - To run the simulation simply run *main.py*
 - There are two settings in main.py, `SIMULATE` and `SAVE`, which can be set to `true`
  - `SIMULATE` will rapidly jump through generations of evolution, speeding up the sim and infrequently redrawing the Pygame window, the console will continue to log the epoch and population to keep track of time
  - `SAVE` will output the creature and attribute statistics in a CSV file, with noodle and pred staistics saved to *data/noodle_output.csv* and *data/pred_output.csv* by default 
 - The starting parameters can be found in *sim/settings.py*, where starting numbers of noodles, preds, food, as well as width and height for the pygame display and environment size can be edited


## Noodles

<img src='/images/nood2.PNG'/>

Noodles are simple, (mainly) vegetarian creatures which search for food in their nearby enviornment. They attempt to find food at all times to replenish their health, with the goal of reproducing. Food appears regularly in their environment, or at the location of a dead noodle which they will also eat. 

They have a chance at reproducing after a certain number of timesteps, where they produce a genetically similar offspring that potentially has a mutation in their DNA to differ in a single trait from their parent. 

All noodles start with these attributes, which are randomly chosen in the following ranges:

Attribute | Description | Range
------|------|------
Size | size, max health=size*20 | 6 - 10
Speed | how fast they move | 1 - 4
Sight | range of vision | 30 - 200
View | degree angle of vision | 40 - 240
Reproduction | % chance of reproducing | 15 - 35

These attributes all contribute to the loss function of a noodle, or how much energy they consume per timestep. The function can be edited to favor certain attributes over others, but the default function that allows for stable populations is: 

> loss = size\**2 + speed\**3 + sight/2 + view/3


## Preds

<img src='/images/pred1.PNG'/>

Preds are the predators of the environment, with their prey being noodles. Preds are also smart creatures, which gives them two distinct advantages: 
 - Preds will chase the closest noodle to them, even if they already have a target, improving their hunting efficiency
 - Preds will only hunt noodles if their health drops below half, to reduce overeating and wasting resources

Their default starting attributes are also slightly different, with greater size, speed, and range of vision, with a much narrower vision angle. 


## Development

I started with green, circular blobs that I called noodles. The noodles started by moving around a map looking for food, which I implemented with a simple food-seeking algorithm where noodles moved towards the closest food with a certain velocity. When they reach the food, they would "eat" it by removing it from the list of foods, and a new food would be added in a random location. 

<img src='/images/demo1.gif' width='550' height='350'/>

Next came giving the noodles the gift of sight; I planned on them competing for food and evolving their attributes which would include vision. The first step was to give noodles a range (variable: `sight`) of how far they can see food. Then they are assigned a viewing angle (variable: `view`) which dictates the angle they can see with relation to their velocity. This was implemented by calculating the points on an arc given a noodle's range and view and rotating that arc with respect to the noodle velocity. 

A boundary detection method was added to noodle movements to constrain them to the environment limits. Noodles will move in a random direction away from boundaries to help make noodles not get stuck. 

<img src='/images/demo2.gif' width='550' height='350'/>

A smooth turning function was added to give the noodles more realistic movements. Their sight, view, and other attributes of size and speed are now all be randomized to give a hetergeneous starting population. There is a countdown for adding new food if multiple foods are consumed within a short timespan, which helps prevent population explosions. There is also a chance of a new, random noodle immigrating to the local environment every few thousand timesteps, to introduce more diversity. 

<img src='/images/demo3.gif' width='550' height='350'/>

An energy loss function was added which can be changed to give greater importance to certain attributes, but the default is:

> loss = size\**2 + speed\**3 + sight/2 + view/3

Noodles will die when they run out of health and leave behind a new food object which is proportional to their size. A noodle's size also affects its health - their maximum health is size*20. A noodle who is size 4 will only have a maximum of 80 health compared with a size 10 noodle with 200 health, but the smaller noodle will also lose health less quickly. 

A health color function was added which shows noodles turn from green to red the closer they get to losing all health. 

<img src='/images/demo4.gif' width='550' height='350'/>

After observing how noodles evolve competing with just each other, the next step was to introduce a predator. Preds are blue triangular hunters, which use the same creature class as the noodles, except they only eat noodles. 

They have been given a slightly different range of starting attributes to encourage a stable but diverse population:

Attribute | Description | Range
------|------|------
Size | size, max health | 8 - 12
Speed | increases velocity | 3 - 5
Sight | range of vision | 200 - 400
View | degree angle of vision | 20 - 80
Reproduction | % chance of reproducing | 25 - 45

Notable differences are that predators are bigger, faster, and can see further but with a greatly reduced range of vision, mimicking the way predators have eyes on the front of their head instead of the side like prey. 

<img src='/images/demo6.gif' width='550' height='350'/>

The other important difference is that they are "smart" creatures, since they are hunters and a smaller population. This means they
 - will chase the closest noodle to them, even if they already have a target, improving their hunting efficiency
 - will only hunt noodles if their health drops below half, to reduce overeating and wasting resources 

<img src='/images/demo8.gif' width='550' height='350'/>


## Summary 

There is an attached Jupyter notebook, *summary.ipynb*, which has various methods for reading CSV files into Pandas dataframes and plotting relevant statistics. For example the average attributes of noodles by timestep, showing how the population evolves over time: 

<img src='/images/trial13_attributes.png'/>

The variability in random starting populations and immigration means that several simulations can be drastically different even if the values such as environment size, food density, and starting population remain constant. 

Populations usually converge to the set of attributes with the highest fitness for that specific population. So, while one set of attributes may be best to compete for resources against a random selection of other noodles, a more efficient set of attributes may be needed to compete against similar noodles. 

### Examples without Predators

An example simulation without predators shows how the population evolves to increase all of their attributes and loss. The more efficient noodles are also longer living as they evolve, shown in the average age of noodles towards the end, and their reproduction rate is selected as a necessarily beneficial trait. 

The populations size, average age, total deaths, and average health over time:

<img src='/images/trial13_living.png'/>

The populations average attributes:

<img src='/images/trial13_attributes.png'/>

The same exact settings can have a very different outcome, showing the potential diversity. This simulation's noodles ended up evolving to favor fast reproducing noodles with short lifespans. Their average age is around 1/4 of the previous example, but their reproduction rate has been genetically selected by the environment with an average rate 4 times the previous population's. Their attributes and loss are still increasing, showing how they still evolve to be competitive and towards higher fitness, but with the aim to reproduce quickly instead of living long enough to reproduce. 

<img src='/images/trial14_living.png'/>

<img src='/images/trial14_attributes.png'/>

When the environment is expanded and the abundance of food is increased, a larger population forms. These noodles are also living much longer, but with less competitive attributes such as speed and sight. Speed may not be worth the compensation in loss if there is more food around, and sight isn't as important with shorter distances to food. Longer sight ranges may even be detrimental, since the noodle will go for the first food it sees, not the closest. In an environment with more noodles to compete with, it may be beaten to the food more easily. 

<img src='/images/trial16_living.png'/>

<img src='/images/trial16_attributes.png'/>

Over time you can see how attributes converge in a population. In this example reproduction doesn't have a change to mutate, with the other attributes converging despite fluctuations in population size, with a relatively low loss selected for. The average generation of the noodles at the end is over 60, and the standard deviations can also be seen in light blue around the averages in the graphs. 

<img src='/images/trial19_living.png'/>

<img src='/images/trial19_attributes.png'/>


### Examples with Predators

Observing the interaction between preds and noodles is very interesting. This example shows how the populations depend on each other: a large starting noodle population means an abundance of food for predators, who quickly deplete their food source and keep their own population in check. The fluctuation in populations continues in a cycle, with more prey allowing more predators to exist, but the greater number of predators quickly eating up all the prey. 

<img src='/images/trial21_living.png'/>

A large influx of predators around epoch 80 quickly decimates the noodle population and the scarcity of food finishes off the predators. The noodle population recovers, but immigrating predators are unable to establish a foothold in the new noodle population, where the noodles are much faster now and reproduce more quickly. 

<img src='/images/trial21_attributes.png'/>

This cycle can play out several times, seen in this simulation which fluctuating cycles but also eras of stability. 

<img src='/images/trial22_living.png'/>

After epoch 100 when a large number of noodles and predators die off, there is a stable period. This is likely due to more predators coming from a common ancestor. This can be seen by looking at the average generations which shows a dropoff after epoch 100, indicating more creatures in that population are offspring of a new species, instead of the starting species. 

<img src='/images/trial22_gen.png'/>

This predator species is characterized by being slower with a longer range of vision and lesser reproduction rate. These creatures are actually slower than their average prey but can see far enough that they are able to eat enough to survive. They don't frequently reproduce, which limits the chance of a population explosion that would decimate their prey. The noodles eventually get too fast for them though, and they aren't able to survive anymore. 

<img src='/images/trial22_attributes.png'/>

Other tools in the summary notebook allow for exploring statistics of individual epochs. Age and generation of each living noodle in the 298th epoch can be viewed:

<img src='/images/trial22_lastepoch.png'/>

Common ancestors' attributes can be viewed by epoch, showing over 80 living noodles who came from the same set of attributes in the 25th to last epoch. Just a few of the noodles came from ancestors who were much bigger, faster, and with better vision:

<img src='/images/trial22_commonancestor.png'/>

And each noodle can be selected to see how their traits have changed over time through their ancestry tree:

<img src='/images/trial22_evolution.png'/>

These are just a few examples which have CSVs in *data*, but there are countless other simulations showing all sorts of evolution and interaction between species, with lots of interesting insights and sometimes hard to explain phenomena thanks to the intentional randomness. 


## Credit

This was inspired by papers I presented and did related work to in a course I took on probabilistic modeling for computational biology. I was specifically interested in neutral biodiversity theory, looking at Hubbell's work as well as approaches to fit models to species abundance distributions. The interplay between speciation, extinction, and immigration inspired me to develop my own model of evolution on a small scale. 

Relevant papers:
- Etienne, R.S. and Olff, H. (2004). A novel genealogical approach to neutral biodiversity theory. Ecology Letters, 7, 170-175.
- Hubbell, S.P. (2001). The Unified Neutral Theory of Biodiversity and Biogeography. Princeton University Press, Princeton, NJ.

I also took inspiration from Primer Learning and MinuteLabs.io (https://www.youtube.com/primerlearning) and their work on creating evolutionary simulations to demonstrate basic principles of natural selection, and Luke Garbutt's genetic steering algorithm (https://github.com/lukegarbutt).