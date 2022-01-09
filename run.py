import os
import os.path                          # allows script to read paths
import gc                               # allows computer to handle memory (gc = garbage collector)
import numpy as np
import SimpleITK as sitk

#Functions from other scripts
from display import * 
from resample import resample
from globalReg import *
from localReg import ffd
from alpha3D import getAlpha3D
from check import *
from declutter import declutter
from reconstruction import reconstruct


# 1. Builds paths to images of interest

core_path = '/home/sebastian/'

file_list = []              #creates a list of paths to heads

#current heads of interest
file_list.append( core_path + 'CQ500-CT-436/CQ500CT436_CQ500CT436/Unknown_Study/CT_PLAIN_THIN' )
file_list.append( core_path + 'CQ500-CT-309/CQ500CT309_CQ500CT309/Unknown_Study/CT_PLAIN_THIN' )
#file_list.append( core_path + 'CQ500-CT-135/CQ500CT135_CQ500CT135/Unknown_Study/CT_PLAIN_THIN' )
file_list.append( core_path + 'CQ500-CT-268/CQ500CT268_CQ500CT268/Unknown_Study/CT_Thin_Plain' )
#file_list.append( core_path + 'CQ500-CT-38/CQ500CT38_CQ500CT38/Unknown_Study/CT_PLAIN_THIN' )
#file_list.append( core_path + 'CQ500-CT-436/CQ500CT436_CQ500CT436/Unknown_Study/CT_Plain' )
#file_list.append( core_path + 'CQ500-CT-0/CQ500CT0_CQ500CT0/Unknown_Study/CT_Plain' )
#file_list.append( core_path + 'CQ500-CT-391/CQ500CT391_CQ500CT391/Unknown_Study/CT_Plain_3mm' )

files = dict()                              #stores list of paths to images in a dictionary
files['path_list'] = file_list


# 2. Store images in vector

vectorOfImages = sitk.VectorOfImage()       #container for original images

for x in list(file_list):

    reader = sitk.ImageSeriesReader()                   #creates reader for image series
    dicom_names = reader.GetGDCMSeriesFileNames(x)      #gets dicom image series
    reader.SetFileNames(dicom_names)
    im = reader.Execute()                               #creates images from DICOM file

    im.SetOrigin((0, 0, 0))                             #set the origin
    vectorOfImages.push_back(im)                        #adds image to container

# 3. Resample image  

vectorOfResamp = sitk.VectorOfImage()          #container for resampled images
dimension = 3                                  #parameter (dimension of image)
target_spacing = np.array([0.5,0.5,0.5])       #parameter (spacing of resampled image)

for n in range (1):
#for n in range (len(vectorOfImages)):
    im = vectorOfImages[n]
    resampled_im = resample(im, dimension, target_spacing)  #calls resample function
    vectorOfResamp.push_back(resampled_im)

display(vectorOfResamp[0],"Resampled Image")
    
# 4. Declutter Image (not ready to use)

# vectorOfDeclut = sitk.VectorOfImage()              

# for n in range (1):
# #for n in range (len(vectorOfImages)):
#     im = vectorOfRigidReg[n] 
#     display(im)
#     declutIm = declutter(im)
#     vectorOfDeclut.push_back(declutIm)
    
# 5. Global registration

alpha3D = getAlpha3D()                              #gets MIDA model

vectorOfRigidReg = sitk.VectorOfImage()             #container for rigidly registered images

for n in range (1):
#for n in range (len(vectorOfImages)):
    im = vectorOfResamp[n]
    rigid_reg_im = rigidReg(im, alpha3D)            #calls rigid registration function
    vectorOfRigidReg.push_back(rigid_reg_im)

display(alpha3D,"Model Image")
display(vectorOfRigidReg[0],"Rigidly Registered Image")
compare(vectorOfRigidReg[0],alpha3D,"Ridigly Registered vs Model")

# 6. Local Registration

vectorOfFFD = sitk.VectorOfImage()             #container for FFD images
vectorOfDFM = sitk.VectorOfImage()             #container for DFMs
listOfDFM = []                                 #list to save DFMs

for n in range (1):
#for n in range (len(vectorOfImages)):
    im = vectorOfRigidReg[n]
    results = ffd(im, alpha3D)           #calls elastic registration function
    vectorOfFFD.push_back(results[0])
    vectorOfDFM.push_back(results[1])
    #listOfDFM.append(sitk.GetArrayFromImage(results[1]))
    #print(n)

display(vectorOfFFD[0],"FFD Result")
display4D(vectorOfDFM[0],"DFM in some direction")
compare(vectorOfFFD[0],vectorOfRigidReg[0],"xxx")

rec = reconstruct(alpha3D, vectorOfDFM[0])

display(rec,"Image reconstruction with DFMs")
compare(rec,vectorOfDFM[0],"FFD registration vs Reconstruction")

#print("1")
#np.save("DFMData.npy", listOfDFM)
#print('2')

# # 7. Matrix of DFMs

# size = np.shape(sitk.GetArrayFromImage(vectorOfDFM[0]))
# cols = size[0]*size[1]*size[2]*size[3]

# defMatrix = np.zeros((len(vectorOfDFM), cols))

# print('2')

# #for n in range (1):
# for n in range (len(vectorOfDFM)):
#      dfm = sitk.GetArrayFromImage(vectorOfDFM[n])    #converts DFM to 4D array
#      print('3')
#      row = np.ravel(dfm)                             #converts 4D array to 1D column
#      print('4')
#      defMatrix[n,:] = row
#      print('5')

# print('6')
# np.save("sample.npy", defMatrix)

# print('7')
# test = np.load("sample.npy")
# print(test)








