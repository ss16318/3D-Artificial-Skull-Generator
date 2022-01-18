## DECLUTTER IMAGE

import numpy as np
import SimpleITK as sitk
from alpha3D import getAlpha3D

from display import display

def declutter(im, Title):

    imArray = sitk.GetArrayFromImage(im)            #converts image to array
    imArray[imArray<750] = -1000                      #sets all array values less than 0 to -1000
    declutIm = sitk.GetImageFromArray(imArray)      #reconstructs image
    display(declutIm, Title)                        #displays images for comparison
   # display(im, Title)
    
    return declutIm

im = getAlpha3D()
declutter(im,"Test")