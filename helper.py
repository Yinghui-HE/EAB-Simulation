import numpy as np
from numpy import savetxt
import random


def generate_random_grid(num_rows, num_cols):
    # create a sparse grid (with less trees)
    grid_rand = np.random.choice(2, size=(num_rows, num_cols), p=[0.7, 0.3])
    return grid_rand


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


def store_grid_to_file(grid_rand, filename = "grid.csv"):
    savetxt(filename, grid_rand, delimiter=',')

def store_start_location_to_file(location_list, filename = "start_point.csv"):
    savetxt(filename, location_list, delimiter=',')


def main():
    num_rows = 50
    num_cols = 50
    grid_rand = generate_random_grid(num_rows, num_cols)
    store_grid_to_file(grid_rand)
    start_x, start_y = generate_random_start_location(num_rows, num_cols)
    while grid_rand[start_x, start_y] != 1:
        start_x, start_y = generate_random_start_location(num_rows, num_cols)
    store_start_location_to_file(np.array([start_x, start_y]))

main()