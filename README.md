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

A neural network (NN) is essentially just a very complicated function which takes many inputs and produces (usually) one or a small number of outputs. It's used to make predictions based on lots of input data where the functional form of the predictor itself is not clear. For example, classifying the objects in an image (input: 512x512 grid of pixel values, output: text label describing the object).

![NN](https://upload.wikimedia.org/wikipedia/commons/e/e4/Artificial_neural_network.svg)

The NN is made up of nodes or _neurons_ organised into _layers_. Each neuron is really a very simple function (for example: _y_ = _w_ * _X_). It receives some _X_ from the input data and computes _y_ given some constant(s) _w_ called the _weights_. If our input has 4 numbers then all the nodes in the first _layer_ take a vector _X_ of 4 numbers. These nodes might connect to one single node providing an output _y_ or they might again be the input for a second layer. A NN with multiple layers between input and output is called a _deep neural network_ and the layers between input and output are called _hidden layers_.

The __weights__, _w_ tell the network exactly what output to give based on the input and the weights encode all of the information about the data we have. We learn the weights by _training_ the network. At first the weights are random. We then use the network to predict a _y_ value based on some data where we _already know the true outcome_. The network then adjusts its own weights depending on how close it was to the true value.  
