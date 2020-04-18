import numpy as np
from numpy import savetxt


def generate_random_grid(num_rows, num_cols):
    # create a sparse grid (with less trees)
    grid_rand = np.random.choice(2, size=(num_rows, num_cols), p=[0.7, 0.3])
    return grid_rand


# print(generate_random_grid(5, 5))

def store_grid_to_file(grid_rand, filename = "grid.csv"):
    savetxt('data.csv', grid_rand, delimiter=',')


def main():
    grid_rand = generate_random_grid(50, 50)
    store_grid_to_file(grid_rand)

main()