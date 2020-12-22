# EvoNoodles

EvoNoodles is a natural selection simulator that looks at creatures, known as noodles, as they evolve in a competitive environment. which looks at how creatures, known as noodles, evolve their attributes in a competitive environment as they compete for resources. 


## Simulation

 - To run the simulation simply run main.py
 - There are two settings in main.py, `SIMULATE` and `SAVE`, which can be set to `true`
  - `SIMULATE` will rapidly jump through generations of evolution, speeding up the sim and infrequently redrawing the Pygame window, the console will continue to log the epoch and population to keep track of time
  - `SAVE` will output the creature and attribute statistics in a CSV file, with noodle and pred staistics saved to `data/noodle_output.csv` and `data/pred_output.csv` by default 
 - The starting parameters can be found in sim/settings.py, where starting numbers of noodles, preds, food, as well as width and height for the pygame display and environment size can be edited


## Noodles

Noodles are simple, (mainly) vegetarian creatures which search for food in their nearby enviornment. They attempt to find food at all times to replenish their health, with the goal of reproducing. Food appears regularly in their environment, or at the location of a dead noodle, which they will also eat. 

<img src='/images/nood2.PNG' width='250' height='250'/>

They have a chance at reproducing after a certain number of timesteps, where they produce a genetically similar offspring that potentially has a mutation in their DNA to differ in a single trait from their parent. 

All noodles start with these attributes, which are random attributes, in the following ranges:

Attribute | Description | Range
------|------|------
Size | size, max health | 6 - 10
Speed | increases velocity | 1 - 4
Sight | range of vision | 30 - 200
View | degree angle of vision | 40 - 240
Reproduction | % chance of reproducing | 15 - 35

These attributes all contribute to the loss function of a noodle, or how much energy they consume per timestep. The function can be edited to favor attributes over others, but the default function that allows for stable populations is: 

> loss = size\**2 + speed\**3 + sight/2 + sight/3


## Preds

<img src='/images/pred1.PNG' width='250' height='250'/>

Preds are the predators of the environment, with their prey being the noodles. Preds are also smart creatures, which gives them two distinct advantages: 
 - Preds will chase the closest noodle to them, even if they already have a target, improving their hunting efficiency
 - Preds will only hunt noodles if their health drops below half, to reduce overeating and wasting resources

Their default starting attributes are also slightly different, with greater size, speed, and range of vision, with a much narrower vision angle. 


## Development

I started with green, circular blobs that I called noodles. The noodles started by moving around a map looking for food, which I implemented with a simple food-seeking algorithm where noodles moved towards the closest food with a certain velocity. When they reach the food, they would "eat" it by removing it from the list of foods, and a new food would be added in a random location. 

<img src='/images/demo1.gif' width='500' height='500'/>

Next came giving the noodles the gift of sight; I planned on them competing for food and evolving their attributes, sight included. The first step was to give noodles a range (variable: sight) of how far they can see food. Then they are assigned a viewing angle (variable: view) which dictates the angle they can see with relation to their velocity. This was implemented by calculating the points on an arc given a noodle's range and view and rotating that arc with respect to the noodle velocity. 

A boundary detection method was added to noodle movements to constrain the map limits. Noodles will move in a random direction away from boundaries to help make noodles not get stuck. 

<img src='/images/demo2.gif' width='500' height='500'/>

A smooth turning function was added to give the noodles more realistic movements. Their sight, view, and other attributes of size and speed can all be randomized to give a hetergeneous starting population. 

<img src='/images/demo3.gif' width='500' height='500'/>

Finally, an energy loss function was added. This can be changed to give greater importance to certain attributes, but the default is:

> loss = size\**2 + speed\**3 + sight/2 + sight/3

Noodles will die when they run out of health and leave behind a new food object which is proportional to their size. A noodle's size also affects its health since their maximum health is their size*20. A noodle who is size 4 will only have a maximum of 80 health compared with a size 10 noodle with 200 health, but the smaller noodle will also lose health less quickly. 

A health color function was added which shows noodles turn from green to red the closer they get to losing all health. 

<img src='/images/demo4.gif' width='500' height='500'/>

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

<img src='/images/demo6.gif' width='500' height='500'/>

The other important difference is that they are "smart" creatures, since they are hunters and a smaller population. This means they
 - will chase the closest noodle to them, even if they already have a target, improving their hunting efficiency
 - will only hunt noodles if their health drops below half, to reduce overeating and wasting resources 

<img src='/images/demo8.gif' width='500' height='500'/>


## Summary 

There is an attached Jupyter notebook, *summary.ipynb*, which has various methods for reading CSV files into Pandas dataframes and plotting relevant statistics. 

<img source='/images/trial13_attributes.png'/>

The variability in random starting populations and immigration means that several simulations can be drastically different, even if the remaining values such as map size, food density, and starting population size remain constant. 

Populations usually converge to the set of attributes with the highest fitness for that specific population. So, while one set of attributes may be best to compete for resources against a random selection of other noodles, a more efficient set of attributes may be needed to compete against other noodles who are more similar. 

Several settings were tweaked when doing simulations too, such as having new noodles or preds with random attributes immigrating to the local population, not allowing reproduction rate to mutate, or introducing upper and lower limits on attributes. 


Loss goes up, age goes down: shows how noodles are continually evolving to greater fitness with the expense of much shorter lifetimes. Reproduction goes way up 

<img source='/images/trial14_attributes.png' width='500' height='500'/>


With the same settings, a different situation can emerge. Longer living noodles are selected for, even as all attributes are increasing. 

<img source='/images/trial13_attributes.png' width='500' height='500'/>


When the environment is expanded and the abundance of food is increased, a larger population forms. These noodles are also living a lot longer, but with less competitive attributes such as speed and sight. Speed may not be worth the compensation in greater loss if there is more food around, and sight isn't nearly as important with shorter distances to food. Longer sights may even be detrimental, since the noodle will go for the first food it sees, not the closest, and in an environment with more noodles to compete with, it may be beaten to the food. 

<img source='/images/trial16_attributes.png' width='500' height='500'/>


Over time, you can see how attributes converge in a population. 

<img source='/images/trial19_attributes.png' width='500' height='500'/>


Observing the interaction between preds and noodles is very interesting. In this simulation you can see how the populations depend on each other: a large starting noodle population means an abundance of food for predators, who quickly deplete their food source which keeps their own population in check. The fluctuation in populations continues in a cycle, with more prey allowing more predators to exist, but the greater population of predators quickly eating up all the prey. 

<img source='/images/trial21_living.png' width='500' height='500'/>

A large influx of predators around epoch 80 quickly decimates the noodle population and the scarcity of food finishes off the predators. The noodle population recovers, but immigrating predators are unable to establish a foothold in the new noodle population, where the noodles are much faster now and reproduce more quickly. 

<img source='/images/trial21_attributes.png' width='500' height='500'/>


This cycle can play out many times. In this simulation there are cycles of fluctuation, but also long eras of stability. 

<img source='/images/trial22_living.png' width='500' height='500'/>

You can see how after epoch 100, when a large number of noodles and predators die off, there is a stable period. This is likely due to more predators coming from a certain set of attributes from a common ancestor. This is seen by looking at the generations of creatures which shows a dropoff, indicating more creatures in the current population are offspring of a new species, instead of the starting species. 

<img source='/images/trial22_gen.png' width='500' height='500'/>

This species of pred, for example, is characterized by slower creatures with a long range of vision and a lesser reproduction rate. These creatures are actually slower than their average prey but can see far enough that they are able to eat enough to survive. They don't frequently reproduce, which limits the change of a population explosion that would decimate their prey. The noodles eventually get too fast for them, however, and they aren't able to survive anymore. 

<img source='/images/trial22_attributes.png' width='500' height='500'/>

Other tools in the notebook allow for exploring stats about individual epochs. We can see the age and generation of each living noodle in the 298th epoch:

<img source='/images/trial22_lastepoch.png' width='500' height='500'/>

We can look at look at common ancestors, seeing that over 80 living noodles came from the same set of attributes, with just a few of the noodles coming from ancestors who were much bigger, faster, and with better vision:

<img source='/images/trial22_commonancestor.png' width='500' height='500'/>

And each noodle can be selected to see how their traits have changed over time through their ancestry tree:

<img source='/images/trial22_evolution.png' width='500' height='500'/>


<!-- ## Roadmap -->

<!-- ## Credit
Written by George Durrant, with inspiration from: 
 - Primer Learning: https://www.youtube.com/channel/UCKzJFdi57J53Vr_BkTfN3uQ
 - MinuteLabs.io's Primer expansion: https://labs.minutelabs.io/evolution-simulator/#/s/16/about
 - Luke Garbutt's genetic steering algorithm: https://youtu.be/KMeT2k1ytYs?t=15m11s

Also inspired by neutral biodiversity theory and species abundance distributions, specifically from Hubbell, Etienne, and Olff
Relevant Papers:
 - Etienne, R.S. and Olff, H. (2004). A novel genealogical approach to neutral biodiversity theory. Ecology Letters, 7, 170-175.
 - Hubbell, S.P. (2001). The Unified Neutral Theory of Biodiversity and Biogeography. Princeton University Press, Princeton, NJ. -->