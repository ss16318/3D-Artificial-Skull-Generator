## DECLUTTER IMAGE

import numpy as np
import SimpleITK as sitk
from alpha3D import getAlpha3D
from globalReg import *
from localReg import ffd
from newTP import newTP
from reconstruct import reconstruct
import os

from defMatrix import createMatrix
from sklearn.metrics import mean_squared_error

from display import display

def declutter(im, Title):

    imArray = sitk.GetArrayFromImage(im)            #converts image to array
    imArray[imArray<100] = -1000                      #sets all array values less than 0 to -1000
    declutIm = sitk.GetImageFromArray(imArray)      #reconstructs image
    #display(declutIm, 'Input')                        #displays images for comparison
    
    return declutIm


path = '/media/sebastian/Data1/AAOscar/Oscar/qure_ai/nii_reorient/'

files = os.listdir(path)
ix = [1,7,8,14,17]
name = path + files[ix[0]]

im = sitk.ReadImage(name)
# Resample each image
im.SetOrigin((0,0,0))
im.SetDirection((1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0))

alpha3D = getAlpha3D() 
realIm = rigidReg(im, alpha3D)
display(realIm,'Real')

declutIm = declutter(im,"Test")
alpha3D = declutter(alpha3D, 'Test' )  
           
rigid_reg_im = rigidReg(declutIm, alpha3D)            #calls rigid registration function
display(rigid_reg_im,'Input')


results = ffd(rigid_reg_im, alpha3D, 100)           #calls elastic registration function
#display(results,'Target')


defMatrix = createMatrix()   #outputs matrix of deformations


test = defMatrix[len(defMatrix)-1,:]
dm = np.delete(defMatrix, len(defMatrix)-1 , 0)
dm = np.delete(defMatrix, 0 , 0)

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
numPC = len(CumulativeExplainedVariance[CumulativeExplainedVariance<80])   
    
numIter = 100 #number of artificial images to be created
error = -1
    
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

    if error < 0 or error > MSE:
        error = MSE
        bestEstimation = newDef
        
newTP(bestEstimation)  #function creates transform paramter file with new control pt deformations 
estimatedSkull = reconstruct()   #deforms model image using DFM reconstruction from new pm
display( estimatedSkull, "Estimated Skull ")
display(results,'Target')



    
        
    