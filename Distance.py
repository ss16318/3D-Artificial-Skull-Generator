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

# Perform PCA Modelling
totalVar = sum(L)                   #sum of eigenvalues (which represent variance)

# % explained variance for increasing number of eigenmodes
CumulativeExplainedVariance = 100*np.cumsum(L)/totalVar       

# finds number of principal components that account for up to 90% of variance
numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<95]) 

#Initialize correspondence and dissimilarity arrays
C = np.ones(testDef.shape[0])    
D = np.zeros(testDef.shape[0]) 
    
for x in range(testDef.shape[0]):   #loop through each test skull
    #calculate the model parameters
    b = np.matmul( np.transpose(U[:,0:numPC]) , np.transpose(testDef[x,:]) - average )
            
    for PC in range(b.shape[0]):    #loop through each model parameter of a test skull
        #calculate correspodence
        C[x] = C[x] * np.exp( -0.5 * np.square(b[PC]) / L[PC] )
    #calculate dissimialrity
    D[x] = np.sum( np.square(b)  /  L[0:numPC] )

#plot histograms of both metrics
plt.hist(C)
plt.xlabel("Correspodence")
plt.ylabel("Frequency")
plt.title("(a)")
plt.show()

plt.hist(D)
plt.xlabel("Dissimilarity")
plt.ylabel("Frequency")
plt.title("(b)")
plt.show()



