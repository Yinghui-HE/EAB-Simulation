import numpy as np

leave_tree_probability = 0.9
stay_at_tree_probability = 1 - leave_tree_probability # = 0.1
result = np.random.choice(a=2, p=[leave_tree_probability, stay_at_tree_probability])
print(result)