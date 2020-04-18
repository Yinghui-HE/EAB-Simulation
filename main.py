# Start of the program

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.pyplot import plot, ion, show
import matplotlib.animation as animation


from Tree import Tree
from Beetle import Beetle
# np.set_printoptions(threshold=np.inf)

def plot_colored_grid(grid_health_level):
    num_rows = grid_health_level.shape[0]
    num_cols = grid_health_level.shape[1]
    # create discrete colormap
    cmap = colors.ListedColormap(['#A41212', '#C52C2C',  '#E14545', '#FD6A6A', '#FEBCBC'])
    cmap.set_under('white')
    cmap.set_over('green')

    bounds = [0, 1, 2, 3, 4, 5]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(grid_health_level, cmap=cmap, norm=norm)

    # draw gridlines
    ax.grid(which='minor', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(0, num_cols+1, 5));
    ax.set_yticks(np.arange(0, num_rows+1, 5));
    # ani = animation.FuncAnimation(fig, update, data_gen, interval=500,
    #                               save_count=50)
    plt.show()
    # plt.draw()

def generate_random_grid(num_rows, num_cols):
    # create a sparse grid (with less trees)
    grid_rand = np.random.choice(2, size=(num_rows, num_cols), p=[0.7, 0.3])
    return grid_rand

def generate_tree_grid(grid_rand):
    num_rows = grid_rand.shape[0]
    num_cols = grid_rand.shape[1]
    grid_tree = []
    list_tree = []
    for x in range(0, num_rows):
        tree_row = []
        for y in range(0, num_cols):
            tree = None
            if grid_rand[x, y] == 1:
                tree = Tree(x, y)
                list_tree.append(tree)
            tree_row.append(tree)
        grid_tree.append(tree_row)
    return np.array(grid_tree), list_tree

def generate_tree_grid_by_health_level(grid_tree):
    num_rows = grid_tree.shape[0]
    num_cols = grid_tree.shape[1]
    grid_health_level = []
    for x in range(0, num_rows):
        grid_health_level_row = []
        for y in range(0, num_cols):
            tree = grid_tree[x, y]
            health_level = -1
            if tree is not None:
                health_level = tree.health_level
            grid_health_level_row.append(health_level)
        grid_health_level.append(grid_health_level_row)
    return np.array(grid_health_level)


# start location generated is on one of the edges of the grid
def generate_random_start_location(num_rows, num_cols):
    x = num_rows - 1
    y = num_cols - 1

    # edge = 0, on a row; edge = 1, on a col
    edge = random.randint(0, 1)
    if edge == 0:
        # row = 0, on 1st row; row = 1, on last row
        row = random.randint(0, 1)
        if row == 0:
            x = 0
        y = random.randint(0, num_cols-1)
    elif edge == 1:
        # col = 0, on 1st col; col = 1, on last col
        col = random.randint(0, 1)
        if col == 0:
            y = 0
        x = random.randint(0, num_rows-1)

    return x, y


# a beetle fly average 3 kilometers => ~10000 ft
# the size of each cell is (1000ft * 1000ft)
#   => radius of the circle from a tree: 10 cells => 9 cells in between
def declare_neighbors_for_all_trees(list_tree):
    radius = 9
    for i in range(len(list_tree)):
        j = i + 1
        tree = list_tree[i]
        for k in range(j, len(list_tree)):
            neighbor = list_tree[k]
            distance = math.sqrt((neighbor.x - tree.x)**2 + (neighbor.y - tree.y)**2)
            if distance <= radius:
                # in the distance that the beetle can fly to => add neighbors
                tree.add_neighbor(neighbor)
                neighbor.add_neighbor(tree)


def main():
    list_of_beetles = []

    # size of the grid
    num_rows = 50
    num_cols = 50

    # the probabilities of moving to another tree and staying at current tree to lay eggs after eab becomes adult
    leave_tree_probability = 0.9
    stay_at_tree_probability = 1 - leave_tree_probability # = 0.1

    # num_months to simulate
    # time is in the unit of "months" => 120 months(10 years)
    num_months = 150

    # grid_rand: a grid of 0's and 1's representing whether the tree exists or not
    grid_rand = generate_random_grid(num_rows, num_cols)
    print(grid_rand)
    # grid_tree: a grid of Tree objects
    grid_tree, list_tree = generate_tree_grid(grid_rand)
    print(grid_tree)
    print(list_tree)
    # grid_health_level: a grid of health levels of the tree
    grid_health_level = generate_tree_grid_by_health_level(grid_tree)
    print(grid_health_level)

    # declare neighbors for all trees
    print("\nDeclare neighbors for all trees...", end="")
    declare_neighbors_for_all_trees(list_tree)
    print("Successfully\n")

    # generate random location index for the first eab
    x, y = generate_random_start_location(num_rows, num_cols)
    while grid_tree[x, y] is None:
        x, y = generate_random_start_location(num_rows, num_cols)
    start_tree = grid_tree[x, y]
    print("Start", start_tree)


    # 1st tree get infected
    start_beetle = Beetle(start_tree, 0)
    list_of_beetles.append(start_beetle)


    time_step = 1 # print every 1 months
    for time in range(1, num_months, time_step):
        # at each time step
        beetles_next = []
        for tree in list_tree:
            if tree.is_infected():
                tree.update_infected_time(curr_time=time)
                # print("\nUpdate tree's infected years", tree)
        for beetle in list_of_beetles:
            beetle.update_age(time_step) # add beetle's age by 1 month

            # print("\nCurrent tree: ", beetle.get_curr_tree())
            # the beetle changes from a larvae to an adult
            if beetle.age >= 11:
                # choose a tree to lay eggs
                # 0: leave the tree
                # 1: stay at the current tree
                move_tree_result = np.random.choice(a=2, p=[leave_tree_probability, stay_at_tree_probability])

                # move to another tree
                if move_tree_result == 0:
                    neighbor_list = beetle.get_curr_tree().get_neighbors()
                    # if cannot find a neighbor tree within 3 km, eab will die
                    if len(neighbor_list) == 0:
                        beetle.die()
                    # fly to a random tree nearby, lay eggs (reproduce), and die
                    else:
                        # choose a random tree and fly to it
                        neighbor_index = random.randrange(len(neighbor_list))
                        beetle.change_curr_tree(neighbor_list[neighbor_index])
                        # lay eggs at the current tree
                        babies = beetle.reproduce(birth_time=time)
                        beetles_next.extend(babies)
                        beetle.die()

                        # print("\nMove to the the tree", neighbor_list[neighbor_index])
                # lay eggs at the current tree, and die
                else:
                    babies = beetle.reproduce(birth_time=time)
                    beetles_next.extend(babies)
                    beetle.die()
                    # print("\nStay at the tree", beetle.curr_tree)
            # the beetle is still a larvae (still alive for the next time step)
            else:
                beetles_next.append(beetle)

        list_of_beetles = beetles_next
        if time % 4 == 0:
            grid_health_level = generate_tree_grid_by_health_level(grid_tree)
            print(grid_health_level)
            plot_colored_grid(grid_health_level)
            print()
    grid_health_level = generate_tree_grid_by_health_level(grid_tree)
    print(grid_health_level)
    np.set_printoptions(threshold=np.inf)
    plot_colored_grid(grid_health_level)






main()