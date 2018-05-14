import numpy as np
from random import randint

def makegrid(y_width, x_width):
    grid = np.zeros((y_width, x_width))

    for i in range(len(grid)):
        grid[i][0] = 1
        grid[i][x_width-1] = 1

    for i in range(len(grid[0])):
        grid[0][i] = 1
        grid[y_width-1][i] = 1

    head_x = randint(2, x_width - 2)
    head_y = randint(2, y_width - 2)

    grid[head_y, head_x] = 2

    i = 0
    j = 0

    x_coord = head_x
    y_coord = head_y

    print('head x: ', head_x)
    print('head y: ', head_y)

    while i < snake_length and j < 3000:

        j += 1
        dir = randint(0,3) # 0 = up, 1 = left, 2 = down, 3 = right


        if dir == 0 and y_coord - 1 > 1:
            if grid[y_coord - 1, x_coord] == 0:
                #print('step to the top')
                y_coord -= 1
                grid[y_coord, x_coord] = 1
                i += 1

        if dir == 1 and x_coord - 1 > 1:
            if grid[y_coord, x_coord - 1] == 0:
                #print('step to the left')
                x_coord -= 1
                grid[y_coord, x_coord] = 1
                i += 1

        if dir == 2 and y_width > y_coord + 1:
            if grid[y_coord + 1, x_coord] == 0:
                #print('step to the bottom')
                y_coord += 1
                grid[y_coord, x_coord] = 1
                i += 1

        if dir == 3 and x_width > x_coord + 2:
            if grid[y_coord, x_coord + 1] == 0:
                #print('step to the right')
                x_coord += 1
                grid[y_coord, x_coord] = 1
                i += 1

    print('j: ', j)
    return grid, head_y, head_x

snake_length = 30
print(makegrid(15, 15))
