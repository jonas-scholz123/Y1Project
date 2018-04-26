"""

    This is the script for training the AI.
    It loads in the game from the script snake.py
    
    Use AI=True/False to turn the AI on/off i.e. to play the
    game yourself.

"""

import numpy as np
import tkinter as tk
from snake import SnakeApp

# Set generation counter
gen = 0

# Load the set of weights for this generation of models
weights = np.load('./weights_%d.npy' % gen)

# Open the window
root = tk.Tk()
root.title('Snake AI')

# Start the snake app. The AI will play one game for
# each set of weights in the weights file
app = SnakeApp(root, weights, gen, ai=True)
root.mainloop()
