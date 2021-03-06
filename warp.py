## Warping

import SimpleITK as sitk  # Note that elastix adds some functionality to SimpleITK
import numpy as np

from alpha3D import getAlpha3D
from display import *

def warpGrid(skull,Y):
    
    #Define grid
    grid = sitk.GridSource(outputPixelType=sitk.sitkUInt16, size=(430,496,345),
                                 sigma=(0.1,0.1,0.1), gridSpacing=(100.0,100.0,100.0))

    #Return unwarped grid
    if Y == 0:
    
       return displayGrid(grid,skull,'')
        
    else: 
    
        path = '/home/sebastian/.config/spyder-py3/reconstruction.txt'
        pm = sitk.ReadParameterFile(path)                      #gets parameter map from transform file
    
        #EXTRACTING DFMs
        transformixImageFilter = sitk.TransformixImageFilter() #creates filter for transform
        transformixImageFilter.SetMovingImage(skull)           #model image will be deformed
        transformixImageFilter.SetTransformParameterMap(pm)    #gets paramter map used for FFD
        transformixImageFilter.ComputeDeformationFieldOn()     #allows DFM to be computed during transform
        transformixImageFilter.LogToConsoleOn()                #logs processing in terminal
        transformixImageFilter.Execute()                       #performs deformation
        DFM = transformixImageFilter.GetDeformationField()     #saves DFMs
    
        warper = sitk.WarpImageFilter()                        #creates filter for transform
        warper.SetOutputParameteresFromImage(DFM)              #filter will use a DFM
        warpedGrid = warper.Execute(grid,DFM)                  #applies DFM to model image
    
        return warpedGrid


