import os
import os.path                          # allows script to read paths
import gc                               # allows computer to handle memory (gc = garbage collector)
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt

#Functions from other scripts
from resample import resample
from display import display 
from declutter import declutter
from alpha3d import getAlpha3D
from rigid import rigidReg

# 1. Builds paths to images of interest

core_path = 'C:/Users/sebas/Desktop/Project/Code/qure_best_ims/'

file_list = []
file_list.append( core_path + 'CQ500CT309_CQ500CT309/Unknown_Study/CT_PLAIN_THIN/PLAIN_THIN_Tilt.nii' )
file_list.append( core_path + 'CQ500CT135_CQ500CT135/Unknown_Study/CT_PLAIN_THIN/PLAIN_THIN_Tilt.nii' )
file_list.append( core_path + 'CQ500CT38_CQ500CT38/Unknown_Study/CT_Plain/Plain_Tilt.nii' )
file_list.append( core_path + 'CQ500CT268_CQ500CT268/Unknown_Study/CT_Thin_Plain/Thin_Plain.nii' )
file_list.append( core_path + 'CQ500CT436_CQ500CT436/Unknown_Study/CT_Plain/Plain_Tilt.nii' )
#file_list.append( core_path + 'CQ500CT436_CQ500CT436/Unknown_Study/CT_Plain/Plain.nii' )
#file_list.append( core_path + 'CQ500CT0_CQ500CT0/Unknown_Study/CT_Plain/Plain.nii' )
#file_list.append( core_path + 'CQ500CT391_CQ500CT391/Unknown_Study/CT_Plain_3mm/Plain_3mm.nii' )

files = dict()                              #stores list of paths to images in a dictionary
files['path_list'] = file_list


# 2. Store images in vector

vectorOfImages = sitk.VectorOfImage()       #container for multiple ims

for x in list(file_list):
  im = sitk.ReadImage(x)                    #load the image
  im.SetOrigin((0, 0, 0))                   #set the origin
  vectorOfImages.push_back(im)              #adds images to container


im_id = 0                                   #selects image to be displayed from list


# 3. Resample images

vectorOfResampImages = sitk.VectorOfImage()    #creates container to save resampled images
dimension = 3                                  #parameter (dimension of image)
target_spacing = np.array([0.5,0.5,0.5])       #parameter (spacing of resampled image)

for n in range(0, 1):#len(vectorOfImages)):
    im = vectorOfImages[n]
    resampled_im = resample(im, dimension, target_spacing)  #calls resample function
    vectorOfResampImages.push_back(resampled_im)
    
display(vectorOfResampImages,im_id)                         #calls display function to plot resampled image


# 4. Global registration

alpha3D = getAlpha3D()                               #gets alpha3D template model

vectorOfRigidReg = sitk.VectorOfImage()              #creates a container to save rigid registered images

for n in range(0, 1):#len(vectorOfImages)):
    im = vectorOfResampImages[n]
    rigid_reg_im = rigidReg(im, alpha3D)             #calls resample function
    vectorOfResampImages.push_back(rigid_reg_im)

display(vectorOfRigidReg,im_id)








# 4. Declutter images

# vectorOfDCImages = sitk.VectorOfImage()

# for n in range(0, 1):#len(vectorOfImages)):
#     im = vectorOfResampImages[n]
#     declutter_im = declutter(im)                  #calls declutter function
#     vectorOfDCImages.push_back(declutter_im)
