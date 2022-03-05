# ARTIFICIAL SKULL RECONSTRUCTION

import SimpleITK as sitk

from alpha3D import getAlpha3D
from display import display4D
from saveToMat import *

    
alpha3D = getAlpha3D()  #gets model image

path = '/home/sebastian/.config/spyder-py3/reconstruction.txt'
pm = sitk.ReadParameterFile(path)    #gets parameter map from transform file

#EXTRACTING DFMs
transformixImageFilter = sitk.TransformixImageFilter() #creates filter for transform
transformixImageFilter.SetMovingImage(alpha3D)         #model image will be deformed
transformixImageFilter.SetTransformParameterMap(pm)    #gets paramter map used for FFD
transformixImageFilter.ComputeDeformationFieldOn()     #allows DFM to be computed during transform
transformixImageFilter.LogToConsoleOn()                #logs processing in terminal
transformixImageFilter.Execute()                       #performs deformation
DFM = transformixImageFilter.GetDeformationField()     #saves DFMs

display4D(DFM, "DFM")

SaveToMat(DFM,"DFM")

warper = sitk.WarpImageFilter()                 #creates filter for transform
warper.SetOutputParameteresFromImage(DFM)       #filter will use a DFM
artificialSkull = warper.Execute(alpha3D,DFM)   #applies DFM to model image

