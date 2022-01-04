# Modelling

import numpy as np

maps = np.load("sample.npy")

mean_map_vector = np.mean(maps, axis=0 , dtype=np.float32)

mean_maps = mean_map_vector.reshape(345, 430, 496 , 3)



