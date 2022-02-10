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


# 1. Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations


# 2. Perform SVD on matrix

dm = defMatrix.T                                #transposes matrix
average = np.mean(dm,axis=1)                    #finds average of each column
X = dm - np.tile(average,(dm.shape[1],1)).T     #subtracts average to get a zero mean

#performs SVD on zero mean deformation matirx (U are eigenvectors & S eigenvalues)
U , S , VT = np.linalg.svd(X,full_matrices=0)


# 3. Perform PCA Modelling

totalVar = sum(S)   #sum of eigenvalues (which represent variance)

# % explained variance for increasing number of eigenmodes
CumulativeExplainedVariance = 100*np.cumsum(S)/totalVar       

displayCEV(CumulativeExplainedVariance)

# finds number of principal components that account for up to 90% of variance
numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<90])   

numIms = 5 #number of artificial images to be created

# create a random parameter vector w/ elements set at 1000
b = np.full((numPC,numIms),1000)     

for i in range(numIms):
    for x in range(numPC):  #loops through each element of random parameter vector 
    
        # imposes that element lies within 3 std dev of eigenvector variation
        while abs(b[x,i]) > 3*np.sqrt(S[x]):    
            # element set to value from Gaussian distribution w/ eigenvalue variance          
            b[x,i] = np.random.normal( 0 , S[x] )        
        
#multiplies random parameter vector with principal eigenvectors
newDeformations = np.matmul(U[:,0:numPC],b)  


# 3. Create transform parameter file

for x in range(numIms):
    newTP(newDeformations[:,x])  #function creates transform paramter file with new control pt deformations

    # 4. Artificial skull reconstruction 
    
    artificialSkull= reconstruct()   #deforms model image using DFM reconstruction from new pm

    display(artificialSkull, "Artificial Skull ")
    
newTP(average)
averageSkull = reconstruct()
display(averageSkull, "Average Skull ")



    





