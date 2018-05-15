import numpy as np
from random import randint
from testgrid import makegrid

y_width = 15
x_width = 15

grid, head_y, head_x = makegrid(y_width, x_width)

# total number of nonzero elements in the grid; i.e. wall and snake's entire body
wall_and_snake = np.count_nonzero(grid)

length = wall_and_snake-57

print(grid)

print ("This is the length of the snake's body:",length )
#print(length)
