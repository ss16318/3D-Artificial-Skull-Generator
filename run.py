import os
import os.path                          # allows script to read paths
import gc                               # allows computer to handle memory (gc = garbage collector)
import numpy as np
import SimpleITK as sitk

#Functions from other scripts
from display import * 
from resample import resample
from globalReg import *
from localReg import elasticReg
from alpha3D import getAlpha3D
from check import *
from declutter import declutter


# 1. Builds paths to images of interest

core_path = '/home/sebastian/'

file_list = []              #creates a list of paths to heads

#current heads of interest
#file_list.append( core_path + 'CQ500-CT-436/CQ500CT436_CQ500CT436/Unknown_Study/CT_PLAIN_THIN' )
file_list.append( core_path + 'CQ500-CT-309/CQ500CT309_CQ500CT309/Unknown_Study/CT_PLAIN_THIN' )
file_list.append( core_path + 'CQ500-CT-135/CQ500CT135_CQ500CT135/Unknown_Study/CT_PLAIN_THIN' )
file_list.append( core_path + 'CQ500-CT-268/CQ500CT268_CQ500CT268/Unknown_Study/CT_Thin_Plain' )
#file_list.append( core_path + 'CQ500-CT-38/CQ500CT38_CQ500CT38/Unknown_Study/CT_PLAIN_THIN' )
#file_list.append( core_path + 'CQ500-CT-436/CQ500CT436_CQ500CT436/Unknown_Study/CT_Plain' )
#file_list.append( core_path + 'CQ500-CT-0/CQ500CT0_CQ500CT0/Unknown_Study/CT_Plain' )
#file_list.append( core_path + 'CQ500-CT-391/CQ500CT391_CQ500CT391/Unknown_Study/CT_Plain_3mm' )

files = dict()                              #stores list of paths to images in a dictionary
files['path_list'] = file_list


# 2. Store images in vector

vectorOfImages = sitk.VectorOfImage()       #container for multiple ims

for x in list(file_list):

    reader = sitk.ImageSeriesReader()                   #creates reader for image series
    dicom_names = reader.GetGDCMSeriesFileNames(x)      #gets dicom image series
    reader.SetFileNames(dicom_names)
    im = reader.Execute()                               #reads dicom image

    im.SetOrigin((0, 0, 0))                             #set the origin
    vectorOfImages.push_back(im)                        #adds image to container

# 3. Resample image  

vectorOfResamp = sitk.VectorOfImage()          #creates container to save resampled images
dimension = 3                                  #parameter (dimension of image)
target_spacing = np.array([0.5,0.5,0.5])       #parameter (spacing of resampled image)

for n in range (1):
#for n in range (len(vectorOfImages)):
    im = vectorOfImages[n]
    resampled_im = resample(im, dimension, target_spacing)  #calls resample function
    vectorOfResamp.push_back(resampled_im)

declutter(resampled_im, "Decluttered Rigid")
    
# size = np.shape(sitk.GetArrayFromImage(vectorOfResamp[0]))
# rows = size[0]*size[1]*size[2]*3
# model = np.zeros((rows, len(vectorOfImages)))
    
# 5. Global registration

alpha3D = getAlpha3D()                               #gets alpha3D template model

vectorOfRigidReg = sitk.VectorOfImage()              #creates a container to save rigid registered images

for n in range (1):
#for n in range (len(vectorOfImages)):
    im = vectorOfResamp[n]
    rigid_reg_im = affineReg(im, alpha3D)            #calls rigid registration function
    vectorOfRigidReg.push_back(rigid_reg_im)

# # 4. Declutter Image

# vectorOfDeclut = sitk.VectorOfImage()              #creates a container to save locally registered images

# for n in range (1):
# #for n in range (len(vectorOfImages)):
#     im = vectorOfRigidReg[n] 
#     display(im)
#     declutIm = declutter(im)
#     vectorOfDeclut.push_back(declutIm)
    

# 6. Local Registration

vectorOfLocalReg = sitk.VectorOfImage()              #creates a container to save locally registered images

for n in range (1):
#for n in range (len(vectorOfImages)):
    im = vectorOfRigidReg[n]
    deformField = elasticReg(im, alpha3D)           #calls elastic registration function
    vectorOfLocalReg.push_back(deformField)

print('Hello')

# 7. Saving deformation field

# size = np.shape(sitk.GetArrayFromImage(vectorOfLocalReg[0]))

# model = np.zeros((size[0]*size[1]*size[2]*size[3], len(vectorOfImages)))

# #for n in range (1):
# for n in range (len(vectorOfImages)):
#     df = vectorOfLocalReg[n]
#     df = sitk.GetArrayFromImage(df)                 #converts deformation field image to 4D array
#     model[:,n] = df.ravel()                         #converts 4D array to 1D column
    
# np.save("sample.npy", model)

# #loaded_array = np.load("sample.npy")
#print(loaded_array)









