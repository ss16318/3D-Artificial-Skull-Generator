import numpy as np
import SimpleITK as sitk
from defMatrix import createMatrix
from display import * 
from check import *
from volume import skullVol

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

## -------- SECTION ONLY NEEDED TO ESTIMATE VOLUMES ONCE AS IT TAKES A WHILE ------ ##
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
    
#     volume[x] = skullVol(im,50)
    
# np.savetxt('volume.txt', volume, fmt='%d')

## ----- END OF ESTIMATION ----- ##

volume = np.loadtxt('volume.txt', dtype=int)    #load skull volumes

# Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations

# Split Train/Test Data
split = int(defMatrix.shape[0]*0.8)

trainDef = defMatrix[0:split,:] #CPD deformations
trainY = volume[0:split]        #volume estimate

testDef = defMatrix[split:defMatrix.shape[0],:] #CPD deformations
testY = volume[split:volume.shape[0]]           #volume estimate

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

numPC = 2                                       #choose number of components for analysis

trainB = np.zeros((trainDef.shape[0],numPC))   #initialize model parameter matrix 
    
for x in range(trainDef.shape[0]):             #loop through each skull
    #estimate model parameters of PCs of interest
    trainB[x,:] = np.matmul( np.transpose(U[:,0:numPC]) , np.transpose(trainDef[x,:]) - average )
    
trainX = trainB                                     #rename variable (not really needed)
    
model = LinearRegression().fit( trainX , trainY )   #build regression model

#get slope and intercept of model
coeff = model.coef_
intercept = model.intercept_

#initilaize model parameter actual array, model parameter estimates from regression and the error
testX = np.zeros((testDef.shape[0],numPC))
estimates = np.zeros((testX.shape))
CPError = np.zeros((testDef.shape[1],testDef.shape[0]))

for x in range(testDef.shape[0]):   #loop through each skull
    #calculate model parameters
    testX[x,:] = np.matmul( np.transpose(U[:,0:numPC]) , np.transpose(testDef[x,:]) - average )
    #estimate model parameters from volume
    estimates[x,:] = (1/coeff) * (testY[x]-intercept) 
    #calculate parameter error
    parameterError = testX[x,:] - estimates[x,:]
    #use parameter error to calculate CPD error
    CPError[:,x] = np.square (np.matmul( (U[:,0:numPC]) , parameterError ) )

#translate error to RMSE in mm
error = np.sqrt( CPError.mean(axis=0) )
error = error * np.sqrt(3) / 2
        
averageError = np.mean(error)
varianceError = np.var(error)

# Reconstruction error of test set plot
plt.bar(np.arange(1,len(error)+1),error)
ax = plt.gca()  
ax.set_ylabel("Root Mean Squared Error (mm) ")                 
ax.set_xlabel(" Skulls ")
plt.axhline(y=averageError, color='r', linestyle='-')
plt.legend(['Average RMSE'],loc='upper right',framealpha=1)
plt.show()

#training data
xline = trainX[:,0]
yline = trainX[:,1]
zline = trainY
#test data
xline1 = testX[:,0]
yline1 = testX[:,1]
zline1 = testY

#3D representation
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(xline, yline, zline, color='red')
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xlabel('PC 1')
ax.set_ylabel('PC 2')
ax.set_zlabel('Volume (cm^3)')
plt.show()

#PC 1 vs volume plot
x = np.array([-800,800])
y = x*coeff[0] + intercept

plt.scatter(xline,zline, color='red', label='Training data')
plt.scatter(xline1,zline1, color='green', label='Test data')
plt.plot(x,y,label='Best Fit line')
plt.axvline(x=3*np.sqrt(L[0]), color='r', linestyle='--', label='+/- 3 standard deviations of component variation')
plt.axvline(x=-3*np.sqrt(L[0]), color='r', linestyle='--')
ax = plt.gca()
ax.set_xlabel('PC 1')
ax.set_ylabel('Volume (cm^3)')
ax.legend(bbox_to_anchor =(0, -0.1))
plt.show()

#PC 2 vs volume plot
x = np.array([-600,600])
y = x*coeff[1] + intercept

plt.scatter(yline,zline, color='red',label='Training data')
plt.scatter(yline1,zline1, color='green' ,label='Test data')
plt.axvline(x=3*np.sqrt(L[1]), color='r', linestyle='--',label='+/- 3 standard deviations of component variation')
plt.axvline(x=-3*np.sqrt(L[1]), color='r', linestyle='--')
plt.plot(x,y,label='Best Fit line')
ax = plt.gca()
ax.set_xlabel('PC 2')
ax.set_ylabel('Volume (cm^3)')
plt.show()

#PC1 vs PC 2
plt.scatter(xline,yline, color='red')
plt.scatter(xline1,yline1, color='green')
ax = plt.gca()
ax.set_xlabel('PC 1')
ax.set_ylabel('PC 2')
plt.show()


    
    
    


