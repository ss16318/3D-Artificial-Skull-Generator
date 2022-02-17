## MODELLING


import numpy as np

from defMatrix import createMatrix
from sklearn.metrics import mean_squared_error

from newTP import newTP
from reconstruct import reconstruct
from display import *



# 1. Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations

defMatrix = np.delete(defMatrix, 41, 0)

error = np.full((len(defMatrix)),-1)  
estimation = np.zeros(np.shape(defMatrix)) 

for t in range(len(defMatrix)): 

    test = defMatrix[t,:]
    
    dm = np.delete(defMatrix, t, 0)

    # 2. Perform SVD on matrix
    dm = dm.T                                       #transposes matrix
    average = np.mean(dm,axis=1)                    #finds average of each column
    X = dm - np.tile(average,(dm.shape[1],1)).T     #subtracts average to get a zero mean
    
    #performs SVD on zero mean deformation matirx (U are eigenvectors & S eigenvalues)
    U , S , VT = np.linalg.svd(X,full_matrices=0)
    
    
    # 3. Perform PCA Modelling
    
    totalVar = sum(S)   #sum of eigenvalues (which represent variance)
    
    # % explained variance for increasing number of eigenmodes
    CumulativeExplainedVariance = 100*np.cumsum(S)/totalVar       
    
    
    # finds number of principal components that account for up to 90% of variance
    numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<100])   
    
    PC = U[:,0:numPC]
    transPC = np.transpose(PC)
    C = np.linalg.inv(np.matmul(transPC,PC))
    C2 = np.matmul(C,transPC)
    
    residual = test - average
    
    params = np.matmul(C2,residual)
    
    estDef = average + (np.matmul(PC,params))
    
    MSE = mean_squared_error(test, estDef)
    
    error[t] = MSE
    estimation[t,:] = estDef
        
averageError = np.mean(error)
varianceError = np.var(error)

for x in range(1):
    
    newTP(estimation[x,:])  #function creates transform paramter file with new control pt deformations

    # 4. Artificial skull reconstruction 
    
    estimatedSkull = reconstruct()   #deforms model image using DFM reconstruction from new pm

    display( estimatedSkull, "Estimated Skull ")
    
    newTP( defMatrix[x,:] )

    realSkull= reconstruct()   #deforms model image using DFM reconstruction from new pm

    display(realSkull, "Real Skull ")
