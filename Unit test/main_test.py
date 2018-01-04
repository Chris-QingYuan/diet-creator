import os

os.chdir("..")

import main as m
import random
import numpy as np

# m.display_breakfast_ingresients()
# print("variable : supported_protein_names \n" + m.supported_protein_names)
# print(random.choice([0,1,2,3]))
# vector_a = np.array(
#     [[0, 39, 14],
#      [31, 5, 15],
#      [3.6, 0.5, 65]])
# vector_b = np.array([80.8, 47.1, 17.96])
# print(np.append(np.linalg.solve(vector_a, vector_b),[1]))
#
print(random.choices([0, 1, 2, 3, 4, 5, 6], k=3))
