# Class of tree

class Tree(object):
    def __init__(self, x, y):
        self.health_level = 0.1
        self.infected = False
        self.infected_months = 0
        self.infected_start_time = -1
        self.beetle_list = []
        self.neighbor_list = []
        self.x = x
        self.y = y
        self.last_time_update_health = 0
        self.old_health_level = self.health_level
        self.removed = False

    def is_infected(self):
        return self.infected

    def update_infected_time(self, curr_time):
        if self.infected_months != curr_time - self.infected_start_time:
            self.infected_months = curr_time - self.infected_start_time

    def update_health_level(self, curr_time):
        CONST = 0.005
        old_health = self.old_health_level
        num_beetles = len(self.beetle_list)
        u = 1 + CONST * num_beetles # u is a function of num_beetles
        self.health_level = (u * old_health) / (1 + (u-1)*old_health)

        if curr_time != self.last_time_update_health:
            self.last_time_update_health = curr_time
            self.old_health_level = self.health_level

        # print("health_level: ", self.health_level, ", curr_time: ", curr_time)
        # print(self)

    def get_health_level(self):
        return self.health_level

    def get_infected(self, infected_start_time):
        self.infected = True
        self.infected_start_time = infected_start_time

    def add_beetle_on_tree(self, beetle, infected_start_time):
        if not self.infected:
            self.get_infected(infected_start_time)
        self.beetle_list.append(beetle)

    def delete_beetle_on_tree(self, beetle):
        try:
            self.beetle_list.remove(beetle)
        except:
            print("Beetle", beetle, "is not in the beetle list of tree", self)

    def get_beetle_list(self):
        return self.beetle_list

    def add_neighbor(self, neighbor_tree):
        self.neighbor_list.append(neighbor_tree)

    def get_neighbors(self):
        return self.neighbor_list

    def remove_tree(self):
        self.removed = True

    def is_removed(self):
        return self.removed

    def __str__(self):
        msg = "Tree Info: \n\t" \
              + "health_level: " + str(self.health_level) \
              + "\n\tInfected: " + str(self.infected) \
              + "\n\tYears of being infected: " + str(self.infected_months / 12) \
              + "\n\tx: " + str(self.x) \
              + "\n\ty: " + str(self.y) \
              + "\n\tNumber of Beetles on the tree: " + str(len(self.beetle_list)) \
              + "\n\tLast time updating health level: " + str(self.last_time_update_health) \
              + "\n\tOld health level: " + str(self.old_health_level)

        return msg