# EvoNoodles
EvoNoodles is a natural selection simulator that looks at creatures, known as noodles, as they evolve in a competitive environment. which looks at how creatures, known as noodles, evolve their attributes in a competitive environment as they compete for resources. 

## Noodles
Noodles are simple, (mainly) vegetarian creatures which search for food in their nearby enviornment. They attempt to find food at all times to replenish their health, with the goal of reproducing. 
They have a chance at reproducing after a certain number of timesteps, where they produce a genetically similar offspring that potentially has a mutation in their DNA to differ in a trait from their parent. 
The attributes of all noodles include:
 - Size
 - Speed
 - Range
 - Vision
 - Reproduction Rate

## Preds

## Summary 

## Simulation
To run the simulation simply run main.py. There are two settings in main.py, SIMULATE and SAVE, which if set to TRUE will rapidly jump through generations of evolution and will output the creature and attribute statistics in a CSV file, respectively. The default setting runs the simulation at 30 fps so each creature's movements can be observed, and outputs noodle statistics and pred statistics in noodle_output.csv and pred_output.csv. The starting parameters can be found in sim/settings.py, where starting numbers of noodles, preds, food, as well as width and height for the pygame display, and therefore environment size, can be edited. 

## Development
Started as an OOJ tile based project to refresh

#### Credit
Written by George Durrant, with insipration from: 
 - Primer Learning: https://www.youtube.com/channel/UCKzJFdi57J53Vr_BkTfN3uQ
 - MinuteLabs.io's expansion on Primer's ideas: https://labs.minutelabs.io/evolution-simulator/#/s/16/about
 - Luke Garbutt's genetic steering algorithm: https://youtu.be/KMeT2k1ytYs?t=15m11s

Also inspired by neutral biodiversity theory and species abundance distributions, specifically from Hubbell, Etienne, and Olff
Relevant Papers:
 - Etienne, R.S. and Olff, H. (2004). A novel genealogical approach to neutral biodiversity theory. Ecology Letters, 7, 170-175.
 - Hubbell, S.P. (2001). The Unified Neutral Theory of Biodiversity and Biogeography. Princeton University Press, Princeton, NJ.