
#IDENTIFYING SKULL

import numpy as np
import SimpleITK as sitk 
from alpha3D import getAlpha3D

def findSkull(im):
    
    array = sitk.GetArrayFromImage(im)      #converts image to array
    locations = np.nonzero(array > 500)     #stores locations of skull

    numDataPts = 1000
    jump = np.floor(len(locations)/numDataPts).astype(int)
    
    points = np.array([3,numDataPts])
    
    n = 0
    
    for i in range (1,len(locations),jump):
       
        points[0,n] = locations[0,i]
        points[1,n] = locations[1,i]
        points[2,n] = locations[2,i]
        n = n+1
       
    return points

im = getAlpha3D()
loc = findSkull(im)

