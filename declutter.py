## DECLUTTER IMAGE

import numpy as np
import SimpleITK as sitk

from display import display

def declutter(im):

    imArray = sitk.GetArrayFromImage(im)
    imArray[imArray<0] = -1000
    declutIm = sitk.GetImageFromArray(imArray)
    display(declutIm)
    
    return declutIm
