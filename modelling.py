## MODELLING

import os
import numpy as np

from defMatrix import createMatrix
from newTP import newTP
from reconstruct import reconstruct
from display import *
from check import *
from alpha3D import getAlpha3D


# 1. Create deformation matrix 

files = os.listdir('/home/sebastian/.config/spyder-py3/Parameters')  #lists files in directory
num = len(files)                                                     #counts files in list

defMatrix = createMatrix(num)   #outputs matrix of deformations


# 2. Perform PCA on matrix

dm = defMatrix.T                                #transposes matrix
average = np.mean(dm,axis=1)                    #finds average of each column
X = dm - np.tile(average,(dm.shape[1],1)).T     #subtracts average to get a zero mean

#performs SVD on zero mean deformation matirx (U are eigenvectors & S eigenvalues)
U , S , VT = np.linalg.svd(X,full_matrices=0)

totalVar = sum(S)   #sum of eigenvalues (which represent variance)


# 3. Create transform parameter file

pcaSkull = average + U[:,0]

explainedVar = int( (S[0] / totalVar)*100 )

newTP(pcaSkull)  #function creates transform paramter file with new control pt deformations


# 4. Artificial skull reconstruction 

artificialSkull = reconstruct()   #deforms model image using DFM reconstruction from new pm

newTP(average)
avg = reconstruct()

display(artificialSkull,"Reconstruction " + str(explainedVar) + "%  "  )

alpha3D = getAlpha3D()

compare(artificialSkull,alpha3D, "Compare")
compare(artificialSkull,avg, "Compare 2")





