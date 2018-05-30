import tkinter as tk
import random
import numpy as np
from neural_net import Model

'''
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
'''

class SnakeApp:

    def __init__(self, master, weights, gen, ai=True):

        bgcolor = '#303030'
        self.moved = True
        self.master = master
        self.ai = ai

        # Game size definitions
        self.size_pix = 320, 320                            # Size of game world in pixels
        self.blk_size = 16                                  # Size of one block in pixels
        self.size_blx = (self.size_pix[0] / self.blk_size,  # Size of game world in blocks
                         self.size_pix[1] / self.blk_size)

        # Initialise the window
        self.frame = tk.Frame(self.master)

        # Initialise the game world
        self.world = tk.Canvas(self.frame,
                               width=self.size_pix[0],
                               height=self.size_pix[1],
                               background=bgcolor)
        self.frame.grid(row=2, column=0)
        self.text_frame1 = tk.Frame(self.master)
        self.text_frame1.grid(row=0, column=0)
        self.text_frame2 = tk.Frame(self.master)
        self.text_frame2.grid(row=1, column=0)

        # AI Information
        self.gen_var = tk.StringVar()
        self.gen_var.set('Generation %d' % gen)
        self.gen_label = tk.Label(self.text_frame1, textvariable=self.gen_var)
        self.gen_label.pack(side=tk.LEFT)

        self.itr_var = tk.StringVar()
        self.itr_var.set('Chromosone %d/%d' % (0, len(weights)))
        self.itr_label = tk.Label(self.text_frame1, textvariable=self.itr_var)
        self.itr_label.pack(side=tk.RIGHT)

        self.dat_var = tk.StringVar()
        self.dat_var.set('NN Input: [%d %d %d]' % (0, 0, 0))
        self.dat_label = tk.Label(self.text_frame2, textvariable=self.dat_var)
        self.dat_label.pack(side=tk.LEFT)

        self.mov_var = tk.StringVar()
        self.mov_var.set('NN Move: 0')
        self.mov_label = tk.Label(self.text_frame2, textvariable=self.mov_var)
        self.mov_label.pack(side=tk.RIGHT)

        # Setup speed slider
        self.slider_frame = tk.Frame(self.master)
        self.speed_slider = tk.Scale(self.slider_frame, orient=tk.HORIZONTAL,
                                     from_=1, to=8, resolution=1, showvalue=False)
        if ai:
            self.speed_slider.set(7)
        else:
            self.speed_slider.set(3)
        self.speed_label = tk.Label(self.slider_frame, text='Speed')
        self.speed_label.pack(side=tk.LEFT)
        self.speed_slider.pack(side=tk.LEFT)
        self.slider_frame.grid(row=3, column=0, sticky='N')

        # Setup score display
        self.score = 0
        self.score_var = tk.StringVar()
        self.score_var.set('Score: %d' % self.score)
        self.score_label = tk.Label(self.slider_frame, textvariable=self.score_var)
        self.score_label.pack(side=tk.RIGHT)

        # Initialise the snake
        self.generation = gen
        self.iteration = 0
        self.move_counter = 0
        self.snake = []
        self.direction = []
        self.snake_init()
        self.data = []
        self.food_pos = [0, 0]
        self.food_init()
        self.moves = []
        self.draw_canvas()

        #Initialise the grid
        self.x_width = int(self.size_blx[0])
        self.y_width = int(self.size_blx[1])

        self.grid0 = np.zeros((self.y_width + 2, self.x_width + 2))

        for i in range(len(self.grid0)):
            self.grid0[i][0] = 1
            self.grid0[i][-1] = 1

        for i in range(len(self.grid0[0])):
            self.grid0[0][i] = 1
            self.grid0[-1][i] = 1

        # Initialise the neural network
        self.weights = weights
        self.model = Model()
        self.model.model.set_weights(self.weights[0])

        # Bind the arrow keys to the snake's movement
        self.master.focus_set()
        self.master.bind('<Up>', self.move_up)
        self.master.bind('<Down>', self.move_down)
        self.master.bind('<Left>', self.move_left)
        self.master.bind('<Right>', self.move_right)
        self.master.bind('<space>', lambda a: self.update(a, first_step=True))

    def update(self, event=None, no_draw=False, first_step=False, AI=True):

        # If it's the first step, unbind the spacebar from this function
        if first_step:
            self.master.bind('<space>', '')

        if not no_draw:

            f_check = self.food_check()
            c_check = self.self_collision_check()
            w_check = self.wall_collision_check()
            if f_check:
                self.food_init()

        else:
            f_check = False
            c_check = False
            w_check = False

        if c_check or w_check:
            self.game_over()

        # Save the old snake
        old_snake = self.snake
        prev_h_x, prev_h_y = old_snake[-1]

        # Move the head in the current direction
        if self.direction == 0:
            self.snake[-1] = [prev_h_x, prev_h_y - self.blk_size]
        if self.direction == 2:
            self.snake[-1] = [prev_h_x, prev_h_y + self.blk_size]
        if self.direction == 1:
            self.snake[-1] = [prev_h_x + self.blk_size, prev_h_y]
        if self.direction == 3:
            self.snake[-1] = [prev_h_x - self.blk_size, prev_h_y]

        # Move all pieces into the previous position of the next piece
        for i in range(len(self.snake) - 1):
            self.snake[i] = old_snake[i + 1]

        if f_check:
            self.snake.insert(0, old_snake[0])
            self.score += 10
            self.move_counter = 0
        self.score_var.set('Score: %d' % (self.score ))#+ self.move_counter))

        if not no_draw and not (c_check or w_check):

            # Update the game world after the move
            self.draw_canvas()

            #transcribe the current game into grid:

            mod_grid0 = self.grid0.copy()

            for pos in self.snake:
                pos_x = int(pos[0]/16)
                pos_y = int(pos[1]/16)
                mod_grid0[pos_y][pos_x] = 1

            head_x = int(self.snake[-1][0]/16)
            head_y = int(self.snake[-1][1]/16)

            mod_grid0[head_y, head_x] = 2







            # up_count = self.count_space_up(mod_grid0)
            # right_count = self.count_space_right(mod_grid0)
            # down_count = self.count_space_down(mod_grid0)
            # left_count = self.count_space_left(mod_grid0)

            # if (up_count or right_count or down_count or left_count) == -100:
            # print(up_count, right_count, down_count, left_count)
            # print(head_x, head_y)
            #print(self.snake)
            #print('head: ', self.snake[-1])
            #print(mod_grid0)


            #Collect data about new position

            self.dat_var.set('NN Input: []')
            # self.data = [[self.left_check(), self.front_check(), self.right_check(),\
            #               up_count, right_count, down_count, left_count,
            #               self.food_differential(m)] for m in [-1, 0, 1]]

            # self.data = [[self.count(mod_grid0, m), self.food_differential(m), self.foresight_count(mod_grid0, m) - self.count(mod_grid0, m)] for m in [-1, 0, 1]]
            #self.data = [[self.count(mod_grid0, m), self.food_differential(m)] for m in [-1, 0, 1]]
            self.data = [[self.count(mod_grid0, m), self.food_differential(m), self.check_neighbors(m, mod_grid0)] for m in [-1, 0, 1]]

            # print(self.data[0][2])
            # print(self.data[1][2])
            # print(self.data[2][2])
            self.move_counter += 1

            #print(self.move_counter)
            if self.move_counter > 500:
                self.direction = 2
            #print(self.data)

            # Ask the AI for the next move
            if self.ai:
                self.make_move()

            # Perform the next move
            self.world.after(self.speed_set(), self.update)

    def move_up(self, event):
        if not self.direction == 2:
            self.direction = 0

    def move_down(self, event):
        if not self.direction == 0:
            self.direction = 2

    def move_left(self, event):
        if not self.direction == 1:
            self.direction = 3

    def move_right(self, event):
        if not self.direction == 3:
            self.direction = 1

    def draw_canvas(self):

        # Erase the old snake
        self.world.delete('all')

        # Loop over the pieces of the snake and draw each
        for i, s in enumerate(self.snake[:-1]):
            #colour = 'gray%d' % (99 - (len(self.snake) - i))
            colour = 'gray%d' % (99)
            self.world.create_rectangle(s[0], s[1],
                                        s[0] - self.blk_size,
                                        s[1] - self.blk_size,
                                        fill=colour, outline=colour)

        # Draw the head
        self.world.create_rectangle(self.snake[-1][0], self.snake[-1][1],
                                    self.snake[-1][0] - self.blk_size,
                                    self.snake[-1][1] - self.blk_size,
                                    fill='gray100', outline='gray100')

        # Draw the food
        self.world.create_oval(self.food_pos[0], self.food_pos[1],
                               self.food_pos[0] - self.blk_size,
                               self.food_pos[1] - self.blk_size,
                               fill='SteelBlue1', outline='LightSkyBlue1')

        self.world.pack()

    def snake_init(self):

        self.snake = [[(self.size_blx[0] // 2 - i) * self.blk_size, (self.size_blx[1] // 2) * self.blk_size] for i in range(6)]



        # vertical = (random.randint(0, 1) == 1)
        # prevx, prevy = self.snake[-1]
        #
        # for i in range(3):
        #     if vertical:
        #         pos = [prevx, prevy + self.blk_size * i]
        #     else:
        #         pos = [prevx + self.blk_size * i, prevy]
        #
        #     self.snake.append(pos)
        #
        # hx, hy = self.snake[-1]
        # px, py = self.snake[-2]
        #
        # if vertical:
        #     if hy > py:
        #         self.direction = 2
        #     else:
        #         self.direction = 0
        # else:
        #     if hx > px:
        #         self.direction = 1
        #     else:
        #         self.direction = 3
        #

        self.direction = 1

        for i in range(5):

            self.update(no_draw=True)

    def food_init(self):

        ix, iy = self.snake[-1]

        while any([ix == s[0] and iy == s[1] for s in self.snake]):
            ix = random.randint(1, self.size_blx[0] - 1) * self.blk_size
            iy = random.randint(1, self.size_blx[1] - 1) * self.blk_size

        self.food_pos = ix, iy

    def speed_set(self):

        index = self.speed_slider.get() - 1
        speeds = [1000, 500, 200, 100, 50, 10, 5, 1]

        return speeds[index]

    def game_over(self, event=None):

        self.world.create_text(self.size_pix[0] / 2, self.size_pix[1] / 2,
                               text='Game Over!\nPress Space to Play Again',
                               justify='center', fill='white')

        if not self.ai:
            self.master.bind('<space>', self.restart)
        else:
            self.restart()

    def restart(self, event=None):

        # Close program if we've reached the last iteration
        if self.iteration == len(self.weights):

            self.master.destroy()

        else:

            # Initialise the snake
            if not self.ai:
                self.master.bind('<space>', lambda a: self.update(a, first_step=True))

            self.moves.append(self.score)
            if len(self.moves) % 10 == 0:
                np.save('./moves_%d.npy' % self.generation, self.moves)

            self.move_counter = 0
            self.snake = []
            self.direction = []
            self.snake_init()
            self.food_pos = [0, 0]
            self.food_init()
            self.score = 0
            self.score_var.set('Data: %d' % self.score)
            self.draw_canvas()

            self.itr_var.set('Chromosone %d/%d' % (self.iteration, len(self.weights)))
            self.model.model.set_weights(self.weights[self.iteration])

            self.iteration += 1

            self.update(first_step=True)



    def self_collision_check(self):
        prev_h_x, prev_h_y = self.snake[-1]

        # Move the head in the current direction
        if (self.direction == 0 and
            any([prev_h_x == s[0] and prev_h_y - self.blk_size == s[1] for s in self.snake])):
            check = True
        elif (self.direction == 2 and
              any([prev_h_x == s[0] and prev_h_y + self.blk_size == s[1] for s in self.snake])):
            check = True
        elif (self.direction == 1 and
              any([prev_h_x + self.blk_size == s[0] and prev_h_y == s[1] for s in self.snake])):
            check = True
        elif (self.direction == 3 and
              any([prev_h_x - self.blk_size == s[0] and prev_h_y == s[1] for s in self.snake])):
            check = True
        else:
            check = False

        return check

    def wall_collision_check(self):

        prev_h_x, prev_h_y = self.snake[-1]

        # Move the head in the current direction
        if (self.direction == 0 and
            prev_h_y - self.blk_size == 0):
            check = True
        elif (self.direction == 2 and
              prev_h_y == self.size_pix[1]):
            check = True
        elif (self.direction == 1 and
              prev_h_x == self.size_pix[0]):
            check = True
        elif (self.direction == 3 and
              prev_h_x - self.blk_size == 0):
            check = True
        else:
            check = False

        return check

    def food_check(self):

        prev_h_x, prev_h_y = self.snake[-1]

        # Move the head in the current direction
        if (self.direction == 0 and
            all([prev_h_x == self.food_pos[0], prev_h_y - self.blk_size == self.food_pos[1]])):
            check = True
        elif (self.direction == 2 and
              all([prev_h_x == self.food_pos[0], prev_h_y + self.blk_size == self.food_pos[1]])):
            check = True
        elif (self.direction == 3 and
              all([prev_h_x == self.food_pos[0] + self.blk_size, prev_h_y == self.food_pos[1]])):
            check = True
        elif (self.direction == 1 and
              all([prev_h_x == self.food_pos[0] - self.blk_size, prev_h_y == self.food_pos[1]])):
            check = True
        else:
            check = False

        return check



    def floodfill(self, grid, y, x):
        global count

        x = int(x)
        y = int(y)

        if len(grid) > y and len(grid[0]) > x and x > 0 and y > 0:
            if grid[y][x] == 0:
                grid[y][x] = 3
                count += 1
                if x > 0:
                    self.floodfill(grid, y, x - 1)
                if x < len(grid[y]) - 1:
                    self.floodfill(grid, y, x + 1)
                if y > 0:
                    self.floodfill(grid, y - 1, x)
                if y < len(grid) - 1:
                    self.floodfill(grid, y + 1 , x)
        return count

    def check_neighbors(self, move, mod_grid0):

        prev_h_x, prev_h_y = self.snake[-1]
        prev_h_x = int(prev_h_x/16)
        prev_h_y = int(prev_h_y/16)

        mod_grid = mod_grid0.copy()

        if self.direction == 0:
            if move == -1:
                move_direction = 3
            if move == 0:
                move_direction = 0
            if move == 1:
                move_direction = 1

        if self.direction == 1:
            if move == -1:
                move_direction = 0
            if move == 0:
                move_direction = 1
            if move == 1:
                move_direction = 2

        if self.direction == 2:
            if move == -1:
                move_direction = 1
            if move == 0:
                move_direction = 2
            if move == 1:
                move_direction = 3

        if self.direction == 3:
            if move == -1:
                move_direction = 2
            if move == 0:
                move_direction = 3
            if move == 1:
                move_direction = 0

        if move_direction == 0:
            x, y = prev_h_x, prev_h_y - 2

        elif move_direction == 1:
            x, y = prev_h_x + 2, prev_h_y

        elif move_direction == 2:
            x, y = prev_h_x, prev_h_y + 2

        elif move_direction == 3:
            x, y = prev_h_x - 2, prev_h_y

        if y < len(mod_grid) and x < len(mod_grid[0]):
            if mod_grid[y, x] == 1:
                return - 1
        return 0


    # def foresight_count(self, mod_grid0, move):
    #
    #     head_x, head_y = self.snake[-1]
    #     head_x = int(head_x/16)
    #     head_y = int(head_y/16)
    #     grid_up = mod_grid0.copy()
    #     grid_right = mod_grid0.copy()
    #     grid_down = mod_grid0.copy()
    #     grid_left = mod_grid0.copy()
    #
    #     #print('head coordinates>>>>', head_x, head_y)
    #     if self.direction == 0:
    #         if move == -1:
    #             move_direction = 3
    #         if move == 0:
    #             move_direction = 0
    #         if move == 1:
    #             move_direction = 1
    #
    #     if self.direction == 1:
    #         if move == -1:
    #             move_direction = 0
    #         if move == 0:
    #             move_direction = 1
    #         if move == 1:
    #             move_direction = 2
    #
    #     if self.direction == 2:
    #         if move == -1:
    #             move_direction = 1
    #         if move == 0:
    #             move_direction = 2
    #         if move == 1:
    #             move_direction = 3
    #
    #     if self.direction == 3:
    #         if move == -1:
    #             move_direction = 2
    #         if move == 0:
    #             move_direction = 3
    #         if move == 1:
    #             move_direction = 0
    #
    #     if move_direction == 0:
    #         x, y = head_x, head_y - 1 #these x,y coords are one step further
    #         grid_up[y, x] = 4
    #     elif move_direction == 1:
    #         x, y = head_x + 1, head_y
    #         grid_right[y, x] = 4
    #     elif move_direction == 2:
    #         x, y = head_x, head_y + 1
    #         grid_down[y, x] = 4
    #     elif move_direction == 3:
    #         x, y = head_x - 1, head_y
    #         grid_left[y, x] = 4
    #         #print(grid_left)
    #
    #
    #
    #
    #
    #     up_count = self.count_space_up(grid_up, x, y)
    #     right_count = self.count_space_up(grid_right, x, y)
    #     down_count = self.count_space_up(grid_down, x, y)
    #     left_count = self.count_space_up(grid_left, x, y)
    #
    #     max_area = max(up_count, right_count, down_count, left_count)
    #     print('max area: ', max_area)
    #     return max_area/400


    def count(self, mod_grid0, move):

        if self.direction == 0:
            if move == -1:
                move_direction = 3
            if move == 0:
                move_direction = 0
            if move == 1:
                move_direction = 1

        if self.direction == 1:
            if move == -1:
                move_direction = 0
            if move == 0:
                move_direction = 1
            if move == 1:
                move_direction = 2

        if self.direction == 2:
            if move == -1:
                move_direction = 1
            if move == 0:
                move_direction = 2
            if move == 1:
                move_direction = 3

        if self.direction == 3:
            if move == -1:
                move_direction = 2
            if move == 0:
                move_direction = 3
            if move == 1:
                move_direction = 0


        if move_direction == 0:
            return(self.count_space_up(mod_grid0, int(self.snake[-1][0]/16), int(self.snake[-1][1]/16)))

        if move_direction == 1:
            return(self.count_space_right(mod_grid0, int(self.snake[-1][0]/16), int(self.snake[-1][1]/16)))

        if move_direction == 2:
            return(self.count_space_down(mod_grid0, int(self.snake[-1][0]/16), int(self.snake[-1][1]/16)))

        if move_direction == 3:
            return(self.count_space_left(mod_grid0, int(self.snake[-1][0]/16), int(self.snake[-1][1]/16)))

    def count_space_up(self, mod_grid0, prev_h_x, prev_h_y):
        global count
        mod_grid = mod_grid0.copy()

        if self.direction == 2:
            return 0


        x = prev_h_x
        y = prev_h_y -1 #check that this -1 is right

        up_count = self.floodfill(mod_grid, y, x)
        count = 0

        if up_count == 0:
            return -1

        else:
            return up_count/400

    def count_space_right(self, mod_grid0, prev_h_x, prev_h_y):
        global count
        mod_grid = mod_grid0.copy()

        if self.direction == 3:
            return 0


        x = prev_h_x + 1
        y = prev_h_y

        right_count = self.floodfill(mod_grid, y, x)
        count = 0

        if right_count == 0:
            return -1

        else:
            return right_count/400

    def count_space_down(self, mod_grid0, prev_h_x, prev_h_y):
        global count
        mod_grid = mod_grid0.copy()

        if self.direction == 0:
            return 0

        x = prev_h_x
        y = prev_h_y + 1

        down_count = self.floodfill(mod_grid, y, x)
        count = 0

        if down_count == 0:
            return -1

        else:
            return down_count/400

    def count_space_left(self, mod_grid0, prev_h_x, prev_h_y):
        global count
        mod_grid = mod_grid0.copy()
        if self.direction == 1:
            return 0

        x = prev_h_x - 1
        y = prev_h_y

        left_count = self.floodfill(mod_grid, y, x)
        count = 0

        if left_count == 0:
            return -1

        else:
            return left_count/400



    def left_check(self):

        # Checks for wall or snake directly to left of head
        # Returns 1 if true, 0 if false

        h_x, h_y = self.snake[-1]
        f_x, f_y = self.food_pos

        wall = [int((self.direction == 0) and (h_x // self.blk_size == 1)),
                int((self.direction == 1) and (h_y // self.blk_size == 1)),
                int((self.direction == 2) and (h_x // self.blk_size == self.size_blx[1])),
                int((self.direction == 3) and (h_y // self.blk_size == self.size_blx[0]))]

        self_ = [int(self.direction == 0 and any([(h_x - self.blk_size == s[0] and h_y == s[1]) for s in self.snake])),
                 int(self.direction == 1 and any([(h_x == s[0] and h_y - self.blk_size == s[1]) for s in self.snake])),
                 int(self.direction == 2 and any([(h_x + self.blk_size == s[0] and h_y == s[1]) for s in self.snake])),
                 int(self.direction == 3 and any([(h_x == s[0] and h_y + self.blk_size == s[1]) for s in self.snake]))]

        food = [int((self.direction == 0) and ((h_x - f_x) // self.blk_size == 1 and h_y == f_y)),
                int((self.direction == 1) and ((h_y - f_y) // self.blk_size == 1 and h_x == f_x)),
                int((self.direction == 2) and ((f_x - h_x) // self.blk_size == 1 and h_y == f_y)),
                int((self.direction == 3) and ((f_y - h_y) // self.blk_size == 1 and h_x == f_x))]

        if any(wall) or any(self_):
            return -1
        elif any(food):
            return 1
        else:
            return 0

    def right_check(self):

        # Checks for wall or snake directly to right of head
        # Returns 1 if true, 0 if false

        h_x, h_y = self.snake[-1]
        f_x, f_y = self.food_pos

        wall = [int((self.direction == 0) and (h_x // self.blk_size == self.size_blx[0])),
                int((self.direction == 1) and (h_y // self.blk_size == self.size_blx[1])),
                int((self.direction == 2) and (h_x // self.blk_size == 1)),
                int((self.direction == 3) and (h_y // self.blk_size == 1))]

        self_ = [int(self.direction == 0 and any([(h_x + self.blk_size == s[0] and h_y == s[1]) for s in self.snake])),
                 int(self.direction == 1 and any([(h_x == s[0] and h_y + self.blk_size == s[1]) for s in self.snake])),
                 int(self.direction == 2 and any([(h_x - self.blk_size == s[0] and h_y == s[1]) for s in self.snake])),
                 int(self.direction == 3 and any([(h_x == s[0] and h_y - self.blk_size == s[1]) for s in self.snake]))]

        food = [int((self.direction == 0) and ((f_x - h_x) // self.blk_size == 1 and h_y == f_y)),
                int((self.direction == 1) and ((f_y - h_y) // self.blk_size == 1 and h_x == f_x)),
                int((self.direction == 2) and ((h_x - f_x) // self.blk_size == 1 and h_y == f_y)),
                int((self.direction == 3) and ((h_y - f_y) // self.blk_size == 1 and h_x == f_x))]

        if any(wall) or any(self_):
            return -1
        elif any(food):
            return 1
        else:
            return 0

    def front_check(self):

        # Checks for wall or snake directly in front of head
        # Returns 1 if true, 0 if false

        h_x, h_y = self.snake[-1]
        f_x, f_y = self.food_pos

        wall = [int((self.direction == 0) and (h_y // self.blk_size == 1)),
                int((self.direction == 1) and (h_x // self.blk_size == self.size_blx[0])),
                int((self.direction == 2) and (h_y // self.blk_size == self.size_blx[1])),
                int((self.direction == 3) and (h_x // self.blk_size == 1))]

        self_ = [int(self.direction == 0 and any([(h_x == s[0] and h_y - self.blk_size == s[1]) for s in self.snake])),
                 int(self.direction == 1 and any([(h_x + self.blk_size == s[0] and h_y == s[1]) for s in self.snake])),
                 int(self.direction == 2 and any([(h_x == s[0] and h_y + self.blk_size == s[1]) for s in self.snake])),
                 int(self.direction == 3 and any([(h_x - self.blk_size == s[0] and h_y == s[1]) for s in self.snake]))]

        food = [int((self.direction == 0) and ((h_y - f_y) // self.blk_size == 1 and h_x == f_x)),
                int((self.direction == 1) and ((f_x - h_x) // self.blk_size == 1 and h_y == f_y)),
                int((self.direction == 2) and ((f_y - h_y) // self.blk_size == 1 and h_x == f_x)),
                int((self.direction == 3) and ((h_x - f_x) // self.blk_size == 1 and h_y == f_y))]

        if any(wall) or any(self_):
            return -1
        elif any(food):
            return 1
        else:
            return 0

    def food_differential(self, move):

        # Calculate current distance from head to food
        h_x, h_y = self.snake[-1]
        f_x, f_y = self.food_pos
        current_dist = np.hypot(f_x - h_x, f_y - h_y)

        # Get the new direction
        if self.direction == 0:
            if move == -1:
                move_direction = 3
            if move == 0:
                move_direction = 0
            if move == 1:
                move_direction = 1

        if self.direction == 1:
            if move == -1:
                move_direction = 0
            if move == 0:
                move_direction = 1
            if move == 1:
                move_direction = 2

        if self.direction == 2:
            if move == -1:
                move_direction = 1
            if move == 0:
                move_direction = 2
            if move == 1:
                move_direction = 3

        if self.direction == 3:
            if move == -1:
                move_direction = 2
            if move == 0:
                move_direction = 3
            if move == 1:
                move_direction = 0

        # Calculate head position after the proposed move
        if move_direction == 0:
            new_dist = np.hypot(f_x - h_x, f_y - (h_y - self.blk_size))
        if move_direction == 2:
            new_dist = np.hypot(f_x - h_x, f_y - (h_y + self.blk_size))
        if move_direction == 1:
            new_dist = np.hypot(f_x - (h_x + self.blk_size), f_y - h_y)
        if move_direction == 3:
            new_dist = np.hypot(f_x - (h_x - self.blk_size), f_y - h_y)

        if new_dist < current_dist:
            return 1
        elif new_dist == current_dist:
            return 0
        else:
            return -1

    def make_move(self):

        # Ask the network for the best move to make
        move = self.model.evaluate_move(self.data) # data is input data, need to include area count in data
        self.mov_var.set('NN Move: %d' % move)

        if self.direction == 0:
            if move == -1:
                self.direction = 3
            if move == 0:
                self.direction = 0
            if move == 1:
                self.direction = 1

        elif self.direction == 1:
            if move == -1:
                self.direction = 0
            if move == 0:
                self.direction = 1
            if move == 1:
                self.direction = 2

        elif self.direction == 2:
            if move == -1:
                self.direction = 1
            if move == 0:
                self.direction = 2
            if move == 1:
                self.direction = 3

        else:
            if move == -1:
                self.direction = 2
            if move == 0:
                self.direction = 3
            if move == 1:
                self.direction = 0

count = 0
