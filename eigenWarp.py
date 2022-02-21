## MODELLING

import os
import numpy as np
import matplotlib as plt

from defMatrix import createMatrix
from newTP import newTP
from reconstruct import reconstruct
from display import *
from check import *
from alpha3D import getAlpha3D
from warp import warpGrid


# 1. Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations


# 2. Perform SVD on matrix

dm = defMatrix.T                                #transposes matrix
average = np.mean(dm,axis=1)                    #finds average of each column
X = dm - np.tile(average,(dm.shape[1],1)).T     #subtracts average to get a zero mean

#performs SVD on zero mean deformation matirx (U are eigenvectors & S eigenvalues)
U , S , VT = np.linalg.svd(X,full_matrices=0)

numPC = 3
residualDef = 0

# create a random parameter vector w/ elements set at 1000
b = np.full((numPC,1),1000)

for x in range(numPC):

    # imposes that element lies within 3 std dev of eigenvector variation
    while abs(b[x]) > 3*np.sqrt(S[x]):
        # element set to value from Gaussian distribution w/ eigenvalue variance          
        b[x] = np.random.normal( 0 , S[x] )        
 
    #multiplies random parameter vector with principal eigenvectors
    residualDef = residualDef + U[:,x] * b[x] 
    
    newDef = average + residualDef
    
    newTP(newDef)  #function creates transform paramter file with new control pt deformations
    
    # 4. Artificial skull reconstruction 
    
    artificialSkull= reconstruct()   #deforms model image using DFM reconstruction from new pm
    
    warpedGrid = warpGrid()
    
    displayGrid(warpedGrid,artificialSkull,"Post-warping")