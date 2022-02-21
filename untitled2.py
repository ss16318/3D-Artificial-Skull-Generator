## MODELLING


import numpy as np

from defMatrix import createMatrix
from sklearn.metrics import mean_squared_error

from newTP import newTP
from reconstruct import reconstruct
from display import *
from globalReg import rigidReg
from check import compare



# 1. Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations

defMatrix = np.delete(defMatrix, 41, 0)
defMatrix = np.delete(defMatrix, 48, 0)

error = np.full((len(defMatrix)),-1)  

test = defMatrix[1,:]

dm = np.delete(defMatrix, 1, 0)

for t in range(len(dm)): 


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
    numPC = t+1   
    
    numIter = 100 #number of artificial images to be created
    
    # create a random parameter vector w/ elements set at 1000
    b = np.full((numPC),1000)     
    
    for i in range(numIter):
        for x in range(numPC):  #loops through each element of random parameter vector 
        
            # imposes that element lies within 3 std dev of eigenvector variation
            while abs(b[x]) > 3*np.sqrt(S[x]):    
                # element set to value from Gaussian distribution w/ eigenvalue variance          
                b[x] = np.random.normal( 0 , S[x] )        
            
        #multiplies random parameter vector with principal eigenvectors
        residualDef = np.matmul(U[:,0:numPC],b)  
        
    
        newDef = average + residualDef
    
        MSE = mean_squared_error(test, newDef)
    
        if error[t] < 0 or error[t] > MSE:
            error[t] = MSE
          
            
        print(i)
    print(t)
        
averageError = np.mean(error)