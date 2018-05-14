#%%
import numpy as np
from random import randint
#%%

count = 0

def floodfill(grid, y, x):
    global count
    if grid[y][x] == 0:
        grid[y][x] = 3
        count += 1
        if x > 0:
            floodfill(grid, y, x - 1)
        if x < len(grid[y]) - 1:
            floodfill(grid , y, x + 1)
        if y > 0:
            floodfill(grid, y - 1, x)
        if y < len(grid) - 1:
            floodfill(grid, y + 1 , x)
    #print(count)
    return count

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


def count_space(grid, direction, head_x, head_y):

    #grid[head_y, head_x] = 1

    if direction == 0 and grid[head_y - 1, head_x] == 0:
        grid[head_y - 1, head_x] = 2

    if direction == 1 and grid[head_y, head_x - 1] == 0:
        grid[head_y, head_x - 1] = 2

    if direction == 2 and grid[head_y + 1 , head_x] == 0:
        grid[head_y + 1, head_x] = 2

    if direction == 3 and grid[head_y, head_x + 1] == 0:
        grid[head_y, head_x + 1] = 2

    else:
        print('Cant move in direction ', direction)

    print(grid)
    counter = 0

    for col in grid:
        for entry in col[1:]:
            if entry == 0:
                counter += 1
            else:
                break

    return counter

def best_dir(grid, head_y, head_x):
    global count
    mod_grid = grid.copy()
    count_up = floodfill(mod_grid, head_y - 1, head_x)
    count = 0
    mod_grid = grid.copy()
    count_left = floodfill(mod_grid, head_y, head_x - 1)
    count = 0
    mod_grid = grid.copy()
    count_down = floodfill(mod_grid, head_y + 1, head_x)
    count = 0
    mod_grid = grid.copy()
    count_right = floodfill(mod_grid, head_y, head_x + 1)
    count = 0

    counts = [count_up, count_left, count_down, count_right]
    print(counts)

    if max(counts) == count_up:
        return 0

    if max(counts) == count_left:
        return 1

    if max(counts) == count_down:
        return 2

    if max(counts) == count_right:
        return 3


y_width = 15
x_width = 15
snake_length = 30

grid, head_y, head_x = makegrid(y_width, x_width)

#%%

best_direction = best_dir(grid, head_y, head_x)




print(grid)
print('best direction: ', best_direction)

#print(count_up)

# count_left = count_space(grid, 1, head_x, head_y)
# print(count_left)
#
# count_down = count_space(grid, 2, head_x, head_y)
# print(count_down)
#
# count_right = count_space(grid, 3, head_x, head_y)
# print(count_right)
#print(grid)
