## MODELLING

import numpy as np
import matplotlib.pyplot as plt
from defMatrix import createMatrix
from display import *

# 1. Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations

# 2. Split Train/Test Data
split = int(defMatrix.shape[0]*0.8)

trainDef = defMatrix[0:split,:]
testDef = defMatrix[split:defMatrix.shape[0],:]


# 3. Perform SVD on matrix
dm = trainDef.T                                 #transposes matrix
average = np.mean(dm,axis=1)                    #finds average of each column
X = dm - np.tile(average,(dm.shape[1],1)).T     #subtracts average to get a zero mean

#performs SVD on zero mean deformation matirx (U are eigenvectors & S eigenvalues)
U , S , VT = np.linalg.svd(X,full_matrices=0)

L = np.square(S)/(S.shape[0]-1)     #Convert singular values to Eigenvalues

totalVar = sum(L)                   #sum of eigenvalues (which represent variance)

# % explained variance for increasing number of eigenmodes
CumulativeExplainedVariance = 100*np.cumsum(L)/totalVar       

displayCEV(CumulativeExplainedVariance)

# finds number of principal components that account for up to 95% of variance
numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<95])   


# 4. Analyze model parameters
centredTest = testDef.T - np.tile(average,(testDef.T.shape[1],1)).T     #subtracts average to get a zero mean

params = np.zeros( (numPC , centredTest.shape[1] ))                     #creates model parameter matrix

PC = np.zeros((np.shape(params)))                                       #PC counter for plot

for x in range(centredTest.shape[1]):
    
    params[:,x] = np.matmul( np.transpose( U[:,0:numPC]) , X[:,x] )     #calculate parameters for each skull
    
    for n in range(params.shape[0]):

        params[n,x] = params[n,x] / (np.sqrt(L[n]))                     #standardize parameters
            
        PC[n,x] = n+1
        
# for n in range(params.shape[0]):
    
    #show paramter distriubtion for each PC
    plt.hist(params[n,:])
    plt.title('PC '+str(n+1) + ' distriubtion of model parameters')
    plt.xlabel("Standardized Model Parameter")
    plt.ylabel("Frequency")
    plt.show()
    

#create 1D arrays of data for scatter
x = np.ravel(params)
y = np.ravel(PC)

#count number of points within 3 standard deviations 
insideRange = np.sum( abs(x) <= 1)
proportionIn = insideRange*100 / len(x)

#component-wise scatter plot
plt.scatter(x,y,s=1)
plt.ylabel("Principal Component")
plt.xlabel("Standardized model parameters")
plt.title("(a)" )
plt.show()

#overall parameter distribution
plt.hist(x)
plt.xlabel("Standardized Model Parameter")
plt.ylabel("Frequency")
plt.title("(b)" )
plt.show()


