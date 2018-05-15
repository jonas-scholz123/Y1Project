"""

    This is the script for training the AI.
    It loads in the game from the script snake.py

    Use AI=True/False to turn the AI on/off i.e. to play the
    game yourself.

"""

import numpy as np
import tkinter as tk
from sys import argv
from snake import SnakeApp

def train(gen, weights):

    # Save the set of weights for this generation of models
    np.save('./weights_%d.npy' % gen, weights)

    # Open the window
    root = tk.Tk()
    root.title('Snake AI')

    # Start the snake app. The AI will play one game for
    # each set of weights in the weights file
    app = SnakeApp(root, weights, gen, ai=True)
    root.mainloop()

    return app.moves

if __name__ == '__main__':

    train(argv[1])
