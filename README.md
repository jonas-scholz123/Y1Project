# Training an AI to Play Snake
In this project we'll attempt to train an AI to play the old mobile game _Snake_.

If you're unsure exactly what Snake is it's worth [playing a few games](https://playsnake.org/) to get the hang of it.

#### Download the materials with [this link](https://github.com/conor-or/ai-snake/archive/master.zip)

#### Read the below for an overview of the method.

#### Watch this video [this video](https://www.youtube.com/watch?v=ZX2Hyu5WoFg) for a decent introduction to the general ideas esp. neural networks and genetic algorithms (non-technical discussion)

___

# 1. Introduction

### Snake

<div style="text-align:center"><img src ="/screenshot.png" /></div>

When you play Snake (or any game) you're trying to maximise something like a score within the constraints of a few rules - this is the _classic_ machine learning problem.

In Snake those constraints are quite simple:
1. At each turn you must choose a direction to move the head of the snake.
2. The rest of the snake (the tail) will follow the head.
3. The head cannot touch the walls or the tail.
4. Eating food increases the length of the snake by 1 unit.
5. Your score is the length of the snake at the end (i.e. when rule 3 is violated).

Even without playing, a human player can read the rules and come up with basic ideas about how to progress in the game. For example: if approaching a wall, we should turn to avoid it; if approaching food, we should turn to eat it, etc.

These are simple enough things for us to understand, and maybe even for us to program, e.g.
```
if snake.position == wall.position:
    snake.move_left()
```
Could we ever account for every situation the snake might encounter with a prescriptive instruction? Probably not, and even so that wouldn't be very interesting.

Instead of deterministically programming the snake with instructions for different scenarios, could we give the snake the set of rules and let it _learn on its own_?

# 2. Neural Networks

