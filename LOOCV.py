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
bestEstimation = np.zeros(np.shape(defMatrix)) 

for t in range(len(defMatrix)): 

    test = defMatrix[t,:]
    
    dm = np.delete(defMatrix, t, 0)

    # 2. Perform SVD on matrix
    dm = dm.T                                       #transposes matrix
    average = np.mean(dm,axis=1)                    #finds average of each column
    X = dm - np.tile(average,(dm.shape[1],1)).T     #subtracts average to get a zero mean
    
    #performs SVD on zero mean deformation matirx (U are eigenvectors & S eigenvalues)
    U , S , VT = np.linalg.svd(X,full_matrices=0)
    
    if t == 0 :
        avg = average
    
    # 3. Perform PCA Modelling
    
    totalVar = sum(S)   #sum of eigenvalues (which represent variance)
    
    # % explained variance for increasing number of eigenmodes
    CumulativeExplainedVariance = 100*np.cumsum(S)/totalVar       
    
    
    # finds number of principal components that account for up to 90% of variance
    numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<60])   
    
    numIter = 100 #number of artificial images to be created
    
    # create a random parameter vector w/ elements set at 1000
    b = np.full((numPC),1000)     
    
    for i in range(numIter):
        for x in range(numPC):  #loops through each element of random parameter vector 
        
            # imposes that element lies within 3 std dev of eigenvector variation
            while abs(b[x]) > 3*np.sqrt(S[x]):    
                # element set to value from Gaussian distribution w/ eigenvalue variance          
                b[x] = np.random.uniform(-2*np.sqrt(S[x]) , 2*np.sqrt(S[x]) )#np.random.normal( 0 , S[x] )        
            
        #multiplies random parameter vector with principal eigenvectors
        residualDef = np.matmul(U[:,0:numPC],b)  
        
    
        newDef = average + residualDef
    
        MSE = mean_squared_error(test, newDef)
    
        if error[t] < 0 or error[t] > MSE:
            error[t] = MSE
            bestEstimation[t,:] = newDef
        
averageError = np.mean(error)
varianceError = np.var(error)

for x in range(1):
    
    newTP(bestEstimation[x,:])  #function creates transform paramter file with new control pt deformations

    # 4. Artificial skull reconstruction 
    
    estimatedSkull = reconstruct()   #deforms model image using DFM reconstruction from new pm

    display( estimatedSkull, "Estimated Skull ")
    
    newTP(avg)
    average = reconstruct()
    compare(estimatedSkull,average,'Compare')
    
    
    newTP( defMatrix[x,:] )

    realSkull= reconstruct()   #deforms model image using DFM reconstruction from new pm

    display(realSkull, "Real Skull ")
    
    compare(estimatedSkull,realSkull, "Comparison 1")
    
    alignedSkull = rigidReg(estimatedSkull, realSkull)
    
    compare(alignedSkull,realSkull, "Comparison 2")
    
    
    
    
    

        

    
    
    


