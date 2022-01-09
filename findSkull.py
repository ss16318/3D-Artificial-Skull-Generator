
#IDENTIFYING SKULL

import numpy as np
import SimpleITK as sitk 

def findSkull(im):
    
    array = sitk.GetArrayFromImage(im)      #converts image to array
    locations = np.argwhere(array > 100)    #stores locations of skull
    
    return locations