from alpha3D import getAlpha3D
import SimpleITK as sitk
import numpy as np
from display import *

def skullVol(skull,threshold):
    
    skull = sitk.GetArrayFromImage(skull)
    
    voxels = np.sum( skull > threshold ) 
    
    # skull[skull<threshold] = -1000                      #sets all array values less than 0 to -1000
    # declutIm = sitk.GetImageFromArray(skull)
    # display(declutIm,'Only Skull')
    
    volume = voxels * pow(0.05,3)
    
    
    return volume

