## MODELLING

from defMatrix import createMatrix
import os

# 1. Create deformation matrix 
files = os.listdir('/home/sebastian/.config/spyder-py3/Parameters')  #lists files in directory
num = len(files) #counts files in list

defMatrix = createMatrix(num)



