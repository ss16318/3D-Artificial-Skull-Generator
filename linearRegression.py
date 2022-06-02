
import numpy as np
import os
import SimpleITK as sitk
from defMatrix import createMatrix

#Functions from other scripts
from display import * 
from check import *
from volume import skullVol

from sklearn.linear_model import LinearRegression


# # Find location of images
# path = '/media/sebastian/Data/AAOscar/Oscar/qure_ai/nii_reorient/'
# files = os.listdir(path)

# ix = [192,193,199,7,8,21,23,24,28,31,35,37,41,43,45,48,53,55,61,62,63,65,66,68,70,75,77,82,84,88,91,101,103,110,112,113,121,123,126,137,138,141,144,150,154,156,163,170,178,182,185,300,302,306,307,312,315,321,323,328,334,336,338,339,341,342,434,353,364,368,370,374,389,395,396,397,405,407,408,412,413,416,425,430,434,438,444,446,447,450,451,458,460,465,469,470,477,482,492,498,499,506,507,200,206,207,209,211,213,216,218,230,235,236,242,243,246,247,252,259,265,267,268,271,276]

# volume = np.zeros((len(ix)))

# for x in range(len(ix)):


#     # Load each image
#     index = ix[x]
#     name = path + files[index]
    
#     im = sitk.ReadImage(name)

#     # # Resample each image
#     im.SetOrigin((0,0,0))
#     im.SetDirection((1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0))
    
#     volume[x] = skullVol(im,100)
    
# np.savetxt('volume.txt', volume, fmt='%d')

volume = np.loadtxt('volume.txt', dtype=int)

# 1. Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations

# 2. Split Train/Test Data
split = int(defMatrix.shape[0]*0.8)

trainDef = defMatrix[0:split,:]
trainY = volume[0:split]


testDef = defMatrix[split:defMatrix.shape[0],:]
testY = volume[split:volume.shape[0]]


# 3. Perform SVD on matrix
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
#numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<95]) 

numPC = 2

trainB = np.zeros((trainDef.shape[0],numPC))    
    
for x in range(trainDef.shape[0]):
    
    trainB[x,:] = np.matmul( np.transpose(U[:,0:numPC]) , np.transpose(trainDef[x,:]) - average )
    
trainX = trainB
    
model = LinearRegression().fit( trainX , trainY )


coeff = model.coef_
intercept = model.intercept_

testX = np.zeros((testDef.shape[0],numPC))

estimates = np.zeros((testX.shape))

CPError = np.zeros((testDef.shape[1],testDef.shape[0]))

for x in range(testDef.shape[0]):
    
    testX[x,:] = np.matmul( np.transpose(U[:,0:numPC]) , np.transpose(testDef[x,:]) - average )
    
    estimates[x,:] = coeff.T * (testY[x]-intercept) 
    
    parameterError = testX[x,:] - estimates[x,:]
    
    CPError[:,x] = np.square (np.matmul( (U[:,0:numPC]) , parameterError ) )
    
error = np.sqrt( CPError.mean(axis=0) )

error = error * np.sqrt(3) / 2
        
averageError = np.mean(error)
varianceError = np.var(error)

plt.bar(np.arange(1,len(error)+1),error)
ax = plt.gca()  
ax.set_ylabel("Root Mean Squared Error (mm) ")                 
ax.set_xlabel(" Skulls ")
plt.axhline(y=averageError, color='r', linestyle='-')
# plt.axhline(y=averageError+np.sqrt(varianceError),color='r' , linestyle='--' )
# plt.axhline(y=averageError-np.sqrt(varianceError),color='r' , linestyle='--' )
# plt.legend(['Average RMSE','+/-1 standard deviation of RMSE'],loc='upper right',framealpha=1)
plt.legend(['Average RMSE'],loc='upper right',framealpha=1)
plt.show()
    
    
    
    
    
    
    
    
    
    
    


