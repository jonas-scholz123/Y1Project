import numpy as np
from random import randint
from testgrid import makegrid

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
    return count

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
count = 0

grid, head_y, head_x = makegrid(y_width, x_width)
best_direction = best_dir(grid, head_y, head_x)

print(grid)
print('best direction: ', best_direction)
