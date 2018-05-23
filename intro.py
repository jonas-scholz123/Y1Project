import numpy as np
import itertools as it
import collections
from neural_net import Model
from train import train
import matplotlib.pyplot as plt


score_to_weights = {}

# This gets a copy of the neural network we're using, this is just so we can see
# what shape/size the weights vectors are, saving us from manually coding it
model = Model()

# This is the current set of weights
current_weights = model.get_weights()
#print('weights: ', current_weights)

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


#print(weights)

# Now we call the training function with the weights we've generated
# The training function returns the scores that each set of weights achieved
# (press space bar to start the game once the window is open)







def breeding(weights, scores, species_fertility):

    for i in range(len(weights)):
        score_to_weights[scores[i]] = weights[i]

    sorted_dict = collections.OrderedDict(sorted(score_to_weights.items()))

    surviving_weights = []
    fertilities = []
    sum_of_scores = sum(scores)
    sorted_scores = sorted(scores, reverse = True)

    for score in sorted_scores[0:5]: #top 10
        print(score)
        fertility = round(score/sum_of_scores * len(scores)*species_fertility)
        print('fertility: ', fertility)
        for i in range(fertility):
            surviving_weights.append(sorted_dict[score])
            fertilities.append(fertility)


    list_of_parents = it.combinations(surviving_weights, 2)
    list_of_fertilities = it.combinations(fertilities, 2)
    children = []
    for parents, fs in zip(list_of_parents, list_of_fertilities):
        mother, m_fert = np.array(parents[0]), fs[0]
        father, f_fert = np.array(parents[1]), fs[1]
        p_m, p_f = m_fert/(m_fert + f_fert), f_fert/(m_fert + f_fert)
        child = []
        for m , f in zip(mother, father):
            m_flat = m.flatten()
            f_flat = f.flatten()
            c_flat = [np.random.choice([m_flat[i], f_flat[i]], p =[p_m, p_f]) for i in range(len(m_flat))]
            child.append(np.array(c_flat).reshape(m.shape))

        children.append(child)
    return children

# Generate 100 sets of random weights
#weights = [random_weights(model.get_weights()) for i in range(10)]
weights = [np.load('./weights_3.npy')[36]]

# print(weights[36])

generation = 0
number_of_gens = 4

def evolution(number_of_gens, generation, weights):
    scores = train(generation, weights)
    children = breeding(weights, scores, 0.8)
    generation += 1
    if generation == number_of_gens:
        return
    else:
        evolution(number_of_gens, generation, children)

evolution(number_of_gens, generation, weights)
