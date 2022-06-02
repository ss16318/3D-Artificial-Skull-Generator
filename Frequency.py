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

# finds number of principal components that account for up to 90% of variance
numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<95])   


centredTest = testDef.T - np.tile(average,(testDef.T.shape[1],1)).T     #subtracts average to get a zero mean

params = np.zeros( (numPC , centredTest.shape[1] ))
# params = np.zeros( (numPC , X.shape[1] ))

PC = np.zeros((np.shape(params)))

for x in range(centredTest.shape[1]):
    params[:,x] = np.matmul( np.transpose( U[:,0:numPC]) , X[:,x] )
    
    for n in range(params.shape[0]):
    
        # if n > 4:
        
        #     params[n,x] = params[n,x] / (3*(np.sqrt(L[n])))
            
        # elif n >= 1 :
        #     params[n,x] = params[n,x] / ((np.sqrt(L[n])))
            
        # else:
        #     params[n,x] = params[n,x] / (0.5*(np.sqrt(L[n])))

        params[n,x] = params[n,x] / (np.sqrt(L[n]))
            
        PC[n,x] = n+1
        
for n in range(params.shape[0]):
    
    plt.hist(params[n,:])
    plt.title('PC '+str(n+1))
    plt.show()
    
    
x = np.ravel(params)
y = np.ravel(PC)

insideRange = np.sum( abs(x) <= 3)
proportionIn = insideRange*100 / len(x)

plt.scatter(x,y,s=1)
plt.ylabel("Principal Component")
plt.xlabel("Standardized model parameters")
plt.title("(a)" )
plt.show()



plt.hist(x)
plt.xlabel("Standardized Model Parameter")
plt.ylabel("Frequency")
plt.title("(b)" )
plt.show()


