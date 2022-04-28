## MODELLING

import numpy as np
import matplotlib.pyplot as plt
from defMatrix import createMatrix
from display import *

# 1. Create deformation matrix 
defMatrix = createMatrix()   #outputs matrix of deformations


# 2. Perform SVD on matrix
dm = defMatrix.T                                       #transposes matrix
average = np.mean(dm,axis=1)                    #finds average of each column
X = dm - np.tile(average,(dm.shape[1],1)).T     #subtracts average to get a zero mean

#performs SVD on zero mean deformation matirx (U are eigenvectors & S eigenvalues)
U , S , VT = np.linalg.svd(X,full_matrices=0)

params = np.zeros( (len(S),len(S)) )
     
for t in range(len(defMatrix)): 

    test = defMatrix[t,:]

    params[t,:] = np.matmul( np.transpose(U) , (test-average) )

component = np.zeros((np.shape(params)))
for n in range(len(params[0])):
    params[:,n] = params[:, n] / (3*np.sqrt(S[n]))
    component[:,n] = n+1
    
    
    plt.hist(params[:,n])
    plt.title("Principal Component " + str(n+1))
    plt.show() 
    
x = np.ravel(params)
y = np.ravel(component)

insideRange = np.sum( abs(x) <= 1)
proportionIn = insideRange*100 / len(x)

plt.scatter(x,y,s=1)
plt.ylabel("Principal Component")
plt.xlabel("Normalized model paramters parameter")
plt.title("Normalized PC values across training skulls - within range " + str(round(proportionIn)) + "%" )
plt.show()



plt.hist(x)
plt.show()


