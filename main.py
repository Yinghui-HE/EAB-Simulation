# Start of the program

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib import colors
from numpy import loadtxt
import sys

from Tree import Tree
from Beetle import Beetle
# np.set_printoptions(threshold=np.inf)


def plot_colored_grid(grid_health_level, time_in_months, title, text=""):
    num_rows = grid_health_level.shape[0]
    num_cols = grid_health_level.shape[1]

    # create discrete colormap
    # cmap = colors.ListedColormap(['#A41212', '#C52C2C',  '#E14545', '#FD6A6A', '#FEBCBC'])
    cmap = colors.ListedColormap(['green', '#FAD1D1', '#FBBBBB', '#FCA5A5', '#F58282', '#F36565', '#F43333', '#D42121', '#BB1010', '#9A0E0E'])

    cmap.set_under('white')
    cmap.set_over('blue')

    bounds = [0, 0.11, 0.3, 0.4, 0.5, 0.6, 0.8, 0.95, 0.98, 0.99, 1.1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    plt.title("Ash tree population simulation (" + title + ") \nat time = " + str(time_in_months) +
              " months (" + str(time_in_months/12) + " years)")
    plt.text(8, 55, text)
    ax.imshow(grid_health_level, cmap=cmap, norm=norm)

    # draw gridlines
    ax.grid(which='minor', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(0, num_cols+1, 5));
    ax.set_yticks(np.arange(0, num_rows+1, 5));
    # ani = animation.FuncAnimation(fig, update, data_gen, interval=500,
    #                               save_count=50)
    plt.show()
    # plt.draw()

# def generate_random_grid(num_rows, num_cols):
#     # create a sparse grid (with less trees)
#     grid_rand = np.random.choice(2, size=(num_rows, num_cols), p=[0.7, 0.3])
#     return grid_rand

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


def declare_neighbors_for_all_trees(list_tree, radius):
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


def become_adult(leave_tree_probability, stay_at_tree_probability, beetle, time):
    # choose a tree to lay eggs
    # 0: leave the tree
    # 1: stay at the current tree
    move_tree_result = np.random.choice(a=2, p=[leave_tree_probability, stay_at_tree_probability])

    babies = []
    # move to another tree
    if move_tree_result == 0:
        neighbor_list = beetle.get_curr_tree().get_neighbors()
        # if cannot find a neighbor tree within 3 km, eab will die
        if len(neighbor_list) == 0:
            beetle.delete_beetle_on_curr_tree(time)
            beetle.die()
        # fly to a random tree nearby, lay eggs (reproduce), and die
        else:
            # delete the beetle from current tree's beetle_list
            beetle.delete_beetle_on_curr_tree(time)
            # choose a random tree and fly to it
            neighbor_index = random.randrange(len(neighbor_list))
            beetle.change_curr_tree(neighbor_list[neighbor_index])
            # lay eggs at the current tree
            babies = beetle.reproduce(birth_time=time)
            beetle.die()

            # print("\nMove to the the tree", neighbor_list[neighbor_index])
    # lay eggs at the current tree, and die
    else:
        babies = beetle.reproduce(birth_time=time)
        # delete the beetle from current tree's beetle_list
        beetle.delete_beetle_on_curr_tree(time)
        beetle.die()

        # print("\nStay at the tree", beetle.curr_tree)
    return babies


def draw_tree_health_changes(health_change_list, time_range_list):
    plt.plot(time_range_list, health_change_list)
    plt.title("Health levels of the start tree")
    plt.xlabel("time (months)")
    plt.ylabel("health levels")
    plt.show()


def simulate_ash_population(grid_tree, list_tree, num_months, time_step, leave_tree_probability,
                            stay_at_tree_probability, list_of_beetles, start_tree):
    time_range_list = range(1, num_months, time_step)
    start_tree_health_list = []
    for time in range(1, num_months, time_step):
        start_tree_health_list.append(start_tree.get_health_level())
        # at each time step
        beetles_next = []

        for beetle in list_of_beetles:
            beetle.update_age(time_step) # add beetle's age by 1 month
            # the beetle changes from a larvae to an adult
            if beetle.age >= 11:
                babies = become_adult(leave_tree_probability, stay_at_tree_probability, beetle, time)
                beetles_next.extend(babies)
            # the beetle is still a larvae (still alive for the next time step)
            else:
                beetles_next.append(beetle)
        list_of_beetles = beetles_next

        if time % 6 == 0:
            grid_health_level = generate_tree_grid_by_health_level(grid_tree)
            plot_colored_grid(grid_health_level, time, "natural simulation")
            print()

        for tree in list_tree:
            if tree.is_infected():
                tree.update_infected_time(curr_time=time)
                tree.update_health_level(curr_time=time)

    grid_health_level = generate_tree_grid_by_health_level(grid_tree)
    print(grid_health_level)
    np.set_printoptions(threshold=np.inf)
    # plot_colored_grid(grid_health_level)

    draw_tree_health_changes(start_tree_health_list, time_range_list)


def infested_tree_removal(grid_tree, list_tree, num_months, time_step, leave_tree_probability,
                            stay_at_tree_probability, list_of_beetles, health_level_threshold):
    list_of_trees_left = list_tree
    num_trees_removed = 0
    for time in range(1, num_months, time_step):
        # at each time step
        beetles_next = []

        for beetle in list_of_beetles:
            if beetle.get_curr_tree() in list_of_trees_left: # if the tree wasn't removed
                beetle.update_age(time_step) # add beetle's age by 1 month

                # print("\nCurrent tree: ", beetle.get_curr_tree())
                # the beetle changes from a larvae to an adult
                if beetle.age >= 11:
                    babies = become_adult(leave_tree_probability, stay_at_tree_probability, beetle, time)
                    beetles_next.extend(babies)
                # the beetle is still a larvae (still alive for the next time step)
                else:
                    beetles_next.append(beetle)
        list_of_beetles = beetles_next

        if time % 6 == 0:
            grid_health_level = generate_tree_grid_by_health_level(grid_tree)
            # print(grid_health_level)
            plot_colored_grid(grid_health_level, time, "infested tree removal with threshold = "
                        + str(health_level_threshold), text="total number of trees removed = " + str(num_trees_removed))
            print()

        for tree in list_tree:
            if tree.is_infected():
                tree.update_infected_time(curr_time=time)
                tree.update_health_level(curr_time=time)
                # remove the tree if pass the threshold
                if tree.get_health_level() > health_level_threshold:
                    list_of_trees_left.remove(tree)
                    grid_tree[tree.x][tree.y] = None
                    num_trees_removed += 1

        list_tree = list_of_trees_left

    # grid_health_level = generate_tree_grid_by_health_level(grid_tree)
    # print(grid_health_level)
    # np.set_printoptions(threshold=np.inf)
    # # plot_colored_grid(grid_health_level)


def delete_all_neighbors(neighbors, grid_tree, list_of_trees_left, num_trees_removed):
    for neighbor in neighbors:
        if not neighbor.is_removed():
            list_of_trees_left.remove(neighbor)
            grid_tree[neighbor.x][neighbor.y] = None
            neighbor.remove_tree()
            num_trees_removed += 1
    return list_of_trees_left, grid_tree, num_trees_removed


def quarantine(grid_tree, list_tree, num_months, time_step, leave_tree_probability,
                                                stay_at_tree_probability, list_of_beetles, health_level_threshold):
    list_of_trees_left = list_tree
    num_trees_removed = 0
    for time in range(1, num_months, time_step):
        # at each time step
        beetles_next = []

        for beetle in list_of_beetles:
            if beetle.get_curr_tree() in list_of_trees_left:  # if the tree wasn't removed
                beetle.update_age(time_step)  # add beetle's age by 1 month

                # print("\nCurrent tree: ", beetle.get_curr_tree())
                # the beetle changes from a larvae to an adult
                if beetle.age >= 11:
                    babies = become_adult(leave_tree_probability, stay_at_tree_probability, beetle, time)
                    beetles_next.extend(babies)
                # the beetle is still a larvae (still alive for the next time step)
                else:
                    beetles_next.append(beetle)
        list_of_beetles = beetles_next

        if time % 6 == 0:
            grid_health_level = generate_tree_grid_by_health_level(grid_tree)
            # print(grid_health_level)
            plot_colored_grid(grid_health_level, time, "quarantine with threshold = " + str(health_level_threshold),
                              text="total number of trees removed = " + str(num_trees_removed))
            print()

        for tree in list_tree:
            if tree.is_infected():
                tree.update_infected_time(curr_time=time)
                tree.update_health_level(curr_time=time)
                # remove the tree if pass the threshold
                if tree.get_health_level() > health_level_threshold:
                    neighbors = tree.get_neighbors()
                    list_of_trees_left, grid_tree, num_trees_removed = delete_all_neighbors(neighbors, grid_tree,
                                                                                list_of_trees_left, num_trees_removed)

        # print("\nUpdate tree's infected years", tree)
        list_tree = list_of_trees_left


def give_insecticides(list_of_trees, num_bugs_killed, list_of_beetles, time):
    for tree in list_of_trees:
        beetle_list = tree.get_beetle_list()

        num_beetles = len(beetle_list)
        num_bugs_killed_for_tree = min(num_bugs_killed, num_beetles)
        beetle_index_list = np.random.choice(a=num_beetles, size=num_bugs_killed_for_tree, replace=False)
        beetle_list_removal = []
        for index in beetle_index_list:
            beetle_list_removal.append(beetle_list[index])

        for beetle in beetle_list_removal:
            beetle.delete_beetle_on_curr_tree(time)
            list_of_beetles.remove(beetle)

    return list_of_beetles


def insecticides(grid_tree, list_tree, num_months, time_step, leave_tree_probability, stay_at_tree_probability,
                 list_of_beetles, health_level_threshold, insecticides_for_trees_type, num_bugs_killed):
    num_tree_get_insecticide = 0
    for time in range(1, num_months, time_step):
        # at each time step
        beetles_next = []
        for tree in list_tree:
            if tree.is_infected():
                tree.update_infected_time(curr_time=time)
                # give insecticides to certain trees if the current tree's health level passes the threshold
                if len(tree.get_beetle_list())>0 and tree.get_health_level() > health_level_threshold:
                    if insecticides_for_trees_type == "all trees":
                        list_of_beetles = give_insecticides(list_tree, num_bugs_killed, list_of_beetles, time)
                        num_tree_get_insecticide += len(list_tree)
                    elif insecticides_for_trees_type == "neighbors":
                        list_of_beetles = give_insecticides(tree.get_neighbors(), num_bugs_killed, list_of_beetles, time)
                        num_tree_get_insecticide += len(tree.get_neighbors())
                    else:
                        list_of_beetles = give_insecticides([tree], num_bugs_killed, list_of_beetles, time)
                        num_tree_get_insecticide += 1
                else:
                    tree.update_health_level(curr_time=time)

        for beetle in list_of_beetles:
            beetle.update_age(time_step)  # add beetle's age by 1 month

            # print("\nCurrent tree: ", beetle.get_curr_tree())
            # the beetle changes from a larvae to an adult
            if beetle.age >= 11:
                babies = become_adult(leave_tree_probability, stay_at_tree_probability, beetle, time)
                beetles_next.extend(babies)
            # the beetle is still a larvae (still alive for the next time step)
            else:
                beetles_next.append(beetle)
        list_of_beetles = beetles_next

        if time % 6 == 0:
            grid_health_level = generate_tree_grid_by_health_level(grid_tree)
            # print(grid_health_level)
            plot_colored_grid(grid_health_level, time,
                              "insecticide with threshold = " + str(health_level_threshold)
                              + ", \neffective for " + insecticides_for_trees_type +
                              ", killing maximum of \n" + str(num_bugs_killed) + " bugs per tree",
                              text="insecticide on " + str(num_tree_get_insecticide) + " trees")
            print()

def main():
    list_of_beetles = []

    # size of the grid
    num_rows = 50
    num_cols = 50

    # the probabilities of moving to another tree and staying at current tree to lay eggs after eab becomes adult
    leave_tree_probability = 0.6
    stay_at_tree_probability = 1 - leave_tree_probability # = 0.1

    # num_months to simulate
    # time is in the unit of "months" => 108 months(9 years)
    num_months = 108

    # grid_rand: a grid of 0's and 1's representing whether the tree exists or not
    # grid_rand = generate_random_grid(num_rows, num_cols)
    grid_rand = loadtxt('grid.csv', delimiter=',')
    print(grid_rand)
    # grid_tree: a grid of Tree objects
    grid_tree, list_tree = generate_tree_grid(grid_rand)
    print(grid_tree)
    print(list_tree)
    # grid_health_level: a grid of health levels of the tree
    grid_health_level = generate_tree_grid_by_health_level(grid_tree)
    print(grid_health_level)

    # a beetle fly average 3 kilometers => ~10000 ft
    # the size of each cell is (1000ft * 1000ft)
    #   => radius of the circle from a tree: 10 cells => 9 cells in between
    radius = 6

    # declare neighbors for all trees
    print("\nDeclare neighbors for all trees...", end="")
    declare_neighbors_for_all_trees(list_tree, radius)
    print("Successfully\n")

    # generate random location index for the first eab，read the location from file
    location_list = loadtxt('start_point.csv', delimiter=',')
    x = int(location_list[0])
    y = int(location_list[1])
    start_tree = grid_tree[x, y]
    print("Start", start_tree)


    # 1st tree get infected
    start_beetle = Beetle(start_tree, 0)
    list_of_beetles.append(start_beetle)

    # print every 1 months
    time_step = 1

    # natural simulation
    # simulate_ash_population(grid_tree, list_tree, num_months, time_step, leave_tree_probability,
    #                         stay_at_tree_probability, list_of_beetles, start_tree)


    # health_level_threshold: if the health level is greater than this threshold, the tree shows symptoms and
    # we can implement containment strategies
    health_level_threshold = 0.2

    # infested_tree_removal: remove the infested tree as soon as it is recognized as infested (health_level > threshold)
    infested_tree_removal(grid_tree, list_tree, num_months, time_step, leave_tree_probability,
                          stay_at_tree_probability, list_of_beetles, health_level_threshold)

    # quarantine: remove surrounding neighbors once recognized as infested (health_level > threshold)
    # quarantine(grid_tree, list_tree, num_months, time_step, leave_tree_probability,
    #                                             stay_at_tree_probability, list_of_beetles, health_level_threshold)

    # insecticides: give insecticides (remove num_bugs_killed bugs to trees once recognized as infested
    #   (health_level > threshold)
    num_bugs_killed = sys.maxsize
    # insecticides(grid_tree, list_tree, num_months, time_step, leave_tree_probability, stay_at_tree_probability,
    #              list_of_beetles, health_level_threshold, insecticides_for_trees_type="all trees", num_bugs_killed=num_bugs_killed)
    # insecticides(grid_tree, list_tree, num_months, time_step, leave_tree_probability, stay_at_tree_probability,
    #              list_of_beetles, health_level_threshold, insecticides_for_trees_type="neighbors", num_bugs_killed=num_bugs_killed)
    # insecticides(grid_tree, list_tree, num_months, time_step, leave_tree_probability, stay_at_tree_probability,
    #              list_of_beetles, health_level_threshold, insecticides_for_trees_type="current tree", num_bugs_killed=num_bugs_killed)

    # bounds = [0, 0.11, 0.3, 0.4, 0.5, 0.6, 0.8, 0.95, 0.98, 0.99, 1.1]

    health_level_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for tree in list_tree:
        if not tree.is_removed():
            health = tree.get_health_level()
            if health == 0.1:
                health_level_count[0] += 1
            elif 0.1 < health <= 0.2:
                health_level_count[1] += 1
            elif 0.2 < health <= 0.3:
                health_level_count[2] += 1
            elif 0.3 < health <= 0.4:
                health_level_count[3] += 1
            elif 0.4 < health <= 0.5:
                health_level_count[4] += 1
            elif 0.5 < health <= 0.6:
                health_level_count[5] += 1
            elif 0.6 < health <= 0.8:
                health_level_count[6] += 1
            elif 0.8 < health <= 0.95:
                health_level_count[7] += 1
            elif 0.98 < health <= 0.99:
                health_level_count[8] += 1
            elif health > 0.99:
                health_level_count[9] += 1
    print(health_level_count)

main()