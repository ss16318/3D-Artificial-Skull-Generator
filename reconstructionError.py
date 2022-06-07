## MODELLING
import numpy as np
from defMatrix import createMatrix
from sklearn.metrics import mean_squared_error

from newTP import newTP
from reconstruct import reconstruct
from display import *
from globalReg import rigidReg
from check import compare
import matplotlib.pyplot as plt


# Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations

# Split Train/Test Data
split = int(defMatrix.shape[0]*0.6)

trainDef = defMatrix[0:split,:]
testDef = defMatrix[split:defMatrix.shape[0],:]

# Perform SVD on matrix
dm = trainDef.T                                 #transposes matrix
average = np.mean(dm,axis=1)                    #finds average of each column
X = dm - np.tile(average,(dm.shape[1],1)).T     #subtracts average to get a zero mean

#performs SVD on zero mean deformation matirx (U are eigenvectors & S singular values)
U , S , VT = np.linalg.svd(X,full_matrices=0)

L = np.square(S)/(S.shape[0]-1)     #Convert singular values to Eigenvalues

# 4. Perform PCA Modelling
totalVar = sum(L)                   #sum of eigenvalues (which represent variance)

# % explained variance for increasing number of eigenmodes
CumulativeExplainedVariance = 100*np.cumsum(L)/totalVar       

# finds number of principal components that account for up to 90% of variance
numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<95])  

defEst = np.transpose(np.zeros(testDef.shape))  #initialize matrix to save CPDs estimates  
    
for x in range(testDef.shape[0]):   #loop through each test skull
    
    # estimate model parameters 
    b = np.matmul( np.transpose(U[:,0:numPC]) , np.transpose(testDef[x,:]) - average )
    # esimate CPD errors
    defEst[:,x] = average + np.matmul( U[:,0:numPC] , b )

#Quantitaive Estimate
error = np.sqrt( ( (np.transpose(testDef) - defEst) ** 2 ).mean(axis=0) )   #RMSE per test skull
error = error * np.sqrt(3) / 2                                              #convert error to mm
        
averageError = np.mean(error)
varianceError = np.var(error)

#plot error for test skulls with statistics
plt.bar(np.arange(1,len(error)+1),error)
ax = plt.gca() 
ax.set_ylabel("Root Mean Squared Error (mm) ")                 
ax.set_xlabel(" Skulls ")
plt.axhline(y=averageError, color='r', linestyle='-')
plt.axhline(y=averageError+np.sqrt(varianceError),color='r' , linestyle='--' )
plt.axhline(y=averageError-np.sqrt(varianceError),color='r' , linestyle='--' )
plt.legend(['Average RMSE','+/-1 standard deviation of RMSE'],loc='lower left',framealpha=1)
plt.show()


#Qualatative Representation
skull = 10                              #choose a skull               

newTP(testDef[skull,:])                 #recreate original skull   
originalSkull = reconstruct()

newTP(defEst[:,skull])                  #generate skull estimate
estimateSkull = reconstruct()

compare(originalSkull,estimateSkull,'') #compare the original and estimate
    





    
    
    
