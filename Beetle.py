from Tree import Tree

# larvae: 340 days ~ 11 months
# adults: 2 months (avg 50 eggs)
stages = ["hatch", "larvae", "adults"]

# Beetle class (EAB)
class Beetle(object):
    NUM_EGGS = 5
    def __init__(self, start_tree, birth_time):
        self.age = 0 # in months
        self.curr_tree = start_tree
        self.alive = True
        start_tree.add_beetle_on_tree(self, birth_time)

    def update_age(self, months_increased):
        self.age += months_increased

    # eab lays 5 eggs at a time
    def reproduce(self, birth_time):
        beetle_babies = []
        for i in range(self.NUM_EGGS):
            beetle_babies.append(Beetle(self.curr_tree, birth_time))
        return beetle_babies

    def die(self):
        self.alive = False

    def delete_beetle_on_curr_tree(self, time):
        self.curr_tree.delete_beetle_on_tree(self)
        self.curr_tree.update_health_level(time)

    def get_curr_tree(self):
        return self.curr_tree

    def change_curr_tree(self, new_tree):
        self.curr_tree = new_tree

    def is_alive(self):
        return self.alive
