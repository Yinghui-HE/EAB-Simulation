# Class of tree

class Tree(object):
    def __init__(self, x, y):
        self.health_level = 5
        self.infected = False
        self.infected_months = 0
        self.infected_start_time = -1
        self.beetle_list = []
        self.neighbor_list = []
        self.x = x
        self.y = y

    def is_infected(self):
        return self.infected

    def update_infected_time(self, curr_time):
        if self.health_level != 0 and self.infected_months != curr_time - self.infected_start_time:
            self.infected_months = curr_time - self.infected_start_time
            self.update_health_level(self.infected_months / 12)

    def update_health_level(self, infected_years):
        # TODO: how many beetles on the tree
        #  depends on the eating rate
        # shape of a function
        curr_health_level = self.health_level
        num_beetles = len(self.beetle_list)
        #


        if 0 < infected_years <= 2:
            self.health_level = 5
        elif 2 < infected_years <= 4: # 3 or 4 years
            self.health_level = 4
        elif 4 < infected_years <= 6: # 5 ot 6 years
            self.health_level = 3
        elif 6 < infected_years <= 8: # 7 or 8 years
            self.health_level = 2
        elif 8 < infected_years <= 10: # 9 or 10 years
            self.health_level = 1
        else: # greater than 10 years, the tree dies
            self.health_level = 0

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
            pass

    def add_neighbor(self, neighbor_tree):
        self.neighbor_list.append(neighbor_tree)

    def get_neighbors(self):
        return self.neighbor_list

    def __str__(self):
        msg = "Tree Info: \n\thealth_level: " + str(self.health_level) + "\n\tInfected: " + str(self.infected) \
              + "\n\tYears of being infected: " + str(self.infected_months / 12) + "\n\tx: " + str(self.x) + "\n\ty: " \
              + str(self.y)
        return msg