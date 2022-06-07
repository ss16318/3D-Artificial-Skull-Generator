import numpy as np
import matplotlib as plt

from defMatrix import createMatrix
from newTP import newTP
from reconstruct import reconstruct
from display import *
from check import *
from alpha3D import getAlpha3D
from warp import warpGrid
from volume import skullVol


# Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations

# Split Train/Test Data
split = int(defMatrix.shape[0]*0.8)

trainDef = defMatrix[0:split,:]
testDef = defMatrix[split:defMatrix.shape[0],:]

# Perform SVD on matrix
dm = trainDef.T                                 #transposes matrix
average = np.mean(dm,axis=1)                    #finds average of each column
X = dm - np.tile(average,(dm.shape[1],1)).T     #subtracts average to get a zero mean

#performs SVD on zero mean deformation matirx (U are eigenvectors & S eigenvalues)
U , S , VT = np.linalg.svd(X,full_matrices=0)

L = np.square(S)/(S.shape[0]-1)     #Convert singular values to Eigenvalues

totalVar = sum(L)                   #sum of eigenvalues (which represent variance)

# % explained variance for increasing number of eigenmodes
CumulativeExplainedVariance = 100*np.cumsum(L)/totalVar       

# finds number of principal components that account for up to 90% of variance
numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<95]) 

newTP(average)                          #prepare TP of average skull
averageSkull = reconstruct()            #warp model to average skull
averageVol = skullVol(averageSkull, 50) #estimate volume of average skull
warpedGrid = warpGrid(averageSkull,0)   #display average skull with un-warped grid

volumeVariation = np.zeros(numPC)

for PC in range(numPC): #loop through PCs
# PC = 1 #or set PCs as this analysis takes time
    
    # create a random parameter vector w/ elements set at 1000
    b = np.full((U.shape[1],1),0)
      
    b[PC] = 3*np.sqrt(L[PC])   #set model parameters to 3stdev
     
    #multiplies random parameter vector with principal eigenvectors
    residualDef = U[:,PC] * b[PC] 
    
    #Positive model paramter case
    newDef1 = average + residualDef     #create new deformation field vector
    
    newTP(newDef1)                      #function creates transform paramter file with new control pt deformations 
    
    artificialSkull1 = reconstruct()    #deforms model image using DFM reconstruction from new pm
    
    warpedGrid1 = warpGrid(artificialSkull1, 1) #overlay grid to skull
    
    displayGrid(warpedGrid1,artificialSkull1,"Principal Component " + str(PC+1) )
    
    #Negative model paramter case
    newDef2 = average - residualDef
    
    newTP(newDef2)  
    
    artificialSkull2 = reconstruct()   
    
    warpedGrid2 = warpGrid(artificialSkull2, 1)
    
    displayGrid(warpedGrid2,artificialSkull2,"Principal Component " + str(PC+1) )
    
    compare(artificialSkull1,artificialSkull2,'Comparison')
    
    #Estimate skull volumes
    vol1 = skullVol(artificialSkull1, 50)
    vol2 = skullVol(artificialSkull2, 50)
    #Convert to volume variation calculation relative to average skull
    volumeVariation[PC] = abs(vol1-vol2)*100 / averageVol
    
    
#plot bar chart of volume variation per component
plt.bar(range(1,37),volumeVariation)
ax = plt.gca()
ax.set_ylabel("Volume Variation (%)")
ax.set_xlabel("Principal Component")

    
    
    