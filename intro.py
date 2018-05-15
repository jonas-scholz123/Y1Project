import numpy as np
from neural_net import Model
from train import train
import matplotlib.pyplot as plt

# This gets a copy of the neural network we're using, this is just so we can see
# what shape/size the weights vectors are, saving us from manually coding it
model = Model()

# This is the current set of weights
model.get_weights()

# We can see the structure of the network (kind of) with the following
model.model.summary()

# This just returns vectors the same size as prev_weights filled with random numbers
def random_weights(prev_weights):

    # Take the shapes from the original weights vectors
    shapes = [p.shape for p in prev_weights]
    new_weights = []

    # Loop over each vector
    for i, s in enumerate(shapes):

        # Generate a new vector the same size
        # You can change the distribution [uniform, gaussian, etc] and the
        # range of random numbers (currently [-1, 1])
        new_weights.append(np.random.uniform(-1.0, 1.0, size=s))

    return new_weights

# Generate 100 sets of random weights
weights = [random_weights(model.get_weights()) for i in range(100)]

# Now we call the training function with the weights we've generated
# The training function returns the scores that each set of weights achieved
# (press space bar to start the game once the window is open)
generation = 0
score = train(generation, weights)
