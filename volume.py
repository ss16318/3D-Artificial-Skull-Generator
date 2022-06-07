
import SimpleITK as sitk
import numpy as np


def skullVol(skull,threshold):
    
    skull = sitk.GetArrayFromImage(skull)
    
    voxels = np.sum( skull > threshold ) 
    
    volume = voxels * pow(0.05,3)
    
    
    return volume
