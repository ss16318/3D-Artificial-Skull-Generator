import numpy as np
import matplotlib.pyplot as plt
from defMatrix import createMatrix
from display import *
from sklearn.cluster import KMeans

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

# initialize arrays to store reporjected CPDs and model parameters
reproj = np.zeros( (trainDef.shape[0] , numPC ))
params = np.zeros( (trainDef.shape[0] , numPC ))

for x in range(trainDef.shape[0]):  #loop through each training skull
    
    #estimate model parameters
    params[x,:] = np.transpose(np.matmul( np.transpose(U[:,0:numPC]) , X[:,x]))
    
    for j in range(numPC):
        #reproject each CPD by each PC
        reproj[x,j] = np.matmul (trainDef[x,:] , U[:,j] ) 

C = 5   #number of clusters chosen

#cluster and label the raw CPD data
kmeansRaw = KMeans(n_clusters=C, random_state=0).fit(trainDef)
labelsRaw = kmeansRaw.fit_predict(trainDef)

#count number of data points in a cluster
count = np.where(labelsRaw==0)
 
centres = kmeansRaw.cluster_centers_    #get location of centroids   

distance = centres[0,:] - centres[2,:]  #measure distances between centroids

theta = np.zeros(numPC)     #initialize array that stores angle between distance vector and eigenvectors

for x in range (numPC):     #loops through all PCs
    
    #take inner product between the distance vector and each eigenvector
    theta[x] = np.abs( np.inner(distance,U[:,x]) / np.sqrt(np.sum(np.square(distance)) ) )

#plot the distance between inner products
plt.bar(range(1,37),theta)
ax = plt.gca()
ax.set_ylabel("Dot Product")
ax.set_xlabel("Principal Component")
plt.show()

#cluster and label the estimated CPD data
kmeansPCA = KMeans(n_clusters=C, random_state=0).fit(reproj)
labelsPCA = kmeansPCA.fit_predict(reproj)

#count number of data points in a cluster
count = np.where(labelsPCA==2)






                




        

    
    