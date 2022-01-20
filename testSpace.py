## LOCAL REGISTRATION

import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

from display import display
from check import compare

from alpha3D import *
from resample import *
from globalReg import *


alpha3D = getAlpha3D() 

path = '/home/sebastian/CQ500-CT-436/CQ500CT436_CQ500CT436/Unknown_Study/CT_PLAIN_THIN'

reader = sitk.ImageSeriesReader()                   #creates reader for image series
dicom_names = reader.GetGDCMSeriesFileNames(path)      #gets dicom image series
reader.SetFileNames(dicom_names)
im = reader.Execute()                               #creates images from DICOM file

im.SetOrigin((0, 0, 0))                             #set the origin 
dimension = 3                                  #parameter (dimension of image)
target_spacing = np.array([0.5,0.5,0.5])       #parameter (spacing of resampled image)
resampled_im = resample(im, dimension, target_spacing)  #calls resample function
 
rigid_reg_im = rigidReg(resampled_im, alpha3D)

#FFD
parameterMap = sitk.GetDefaultParameterMap("bspline")                                            #FFD registration

parameterMap['Registration'] = ("MultiMetricMultiResolutionRegistration",)
parameterMap['FixedImagePyramid'] = ('FixedShrinkingImagePyramid',)                              #applies registration at different resolutions (only downsampling applied)
parameterMap['MovingImagePyramid'] = ('MovingShrinkingImagePyramid',)                            
parameterMap['Metric'] = ("AdvancedNormalizedCorrelation", "AdvancedMattesMutualInformation")    #cross-correlation & probability distribution metrics
parameterMap['MaximumNumberOfIterations'] = ('1500','350','350','350','350','350')               #number of iterations at each pyramid resolution
parameterMap['NumberOfResolutions'] = ("6",)                                                     #number of resolutions (pyramid levels)
parameterMap["DefaultPixelValue"] = ["-1000"]
parameterMap['NumberOfSpatialSamples'] = [str((alpha3D.GetSize()[0]*alpha3D.GetSize()[1]*alpha3D.GetSize()[2])/5000)] #downsamples model by 5000
parameterMap['GridSpacingSchedule'] = ('16.0' , '16.0' , '8.0' , '8.0' , '4.0' , '4.0')           #control point spacing
parameterMap.asdict()                                                                            #the rest of map will follow preset settings

elastixImageFilter = sitk.ElastixImageFilter()      #creates a filter for registration                                                
elastixImageFilter.SetParameterMap(parameterMap)    #defines what filter should do
elastixImageFilter.SetFixedImage(rigid_reg_im)                #input image is fixed
elastixImageFilter.SetMovingImage(alpha3D)          #model image is moving
elastixImageFilter.LogToFileOn()                    #logs processing in terminal
elastixImageFilter.Execute()                        #performs registration

FFDIm = elastixImageFilter.GetResultImage()         #resulting image from FFD

# #EXTRACTING DFMs

# transformixImageFilter = sitk.TransformixImageFilter()                                           #creates filter for transform
# transformixImageFilter.SetMovingImage(alpha3D)                                                   #maintains that model image is moving
# transformixImageFilter.SetTransformParameterMap(elastixImageFilter.GetTransformParameterMap())   #gets paramter map used for FFD
# transformixImageFilter.ComputeDeformationFieldOn()                                               #allows DFM to be computed during transform
# transformixImageFilter.LogToConsoleOn()                                                          #logs processing in terminal
# transformixImageFilter.Execute()                                                                 #performs transform
# DFM = transformixImageFilter.GetDeformationField()                                               #gets DFM of transform


pm = 'TransformParameters.0.txt'

with open ('TransformParameters.0.txt' , 'rt') as pm:  # Open lorem.txt for reading
    for ln in pm:                              # For each line, read to a string,
        
        if "GridOrigin" in ln:
            origin = ln.split("GridOrigin",1)[1]
            origin = origin.split(")",1)[0]
            start = np.array(origin.split(), dtype=np.float)
            
        if "GridSize" in ln:
            size = ln.split("GridSize",1)[1]
            size = size.split(")",1)[0]
            n_el = np.array(size.split(), dtype=np.int)

        if "GridSpacing" in ln:
            spacing = ln.split("GridSpacing",1)[1]
            spacing = spacing.split(")",1)[0]
            spacing = np.array(spacing.split(), dtype=np.float).astype(int)
            spacing = spacing*2
            
        if "(TransformParameters" in ln:
            df = ln.split("(TransformParameters",1)[1]
            df = df.split(")",1)[0]
            deformations = np.array(df.split(), dtype=np.float)
            

deformations = deformations.reshape(3, int(deformations.shape[0]/3))

U = deformations[0,:].reshape(n_el[0], n_el[1], n_el[2])
V = deformations[1,:].reshape(n_el[0], n_el[1], n_el[2])

#### Create deformation grid
X, Y, Z = np.meshgrid(np.linspace(start[0], (n_el[0]*spacing[0])-start[0], int(n_el[0])),
                      np.linspace(start[1], (n_el[1] * spacing[1]) - start[1], int(n_el[1])),
                      np.linspace(start[2], (n_el[2]*spacing[2])-start[2], int(n_el[2])))

#### Create image grid
im_array = sitk.GetArrayFromImage(im)
X_im, Y_im, Z_im = np.meshgrid(np.linspace(0, im_array.shape[0]-1, im_array.shape[0]),
                               np.linspace(0,  im_array.shape[1]-1,  im_array.shape[1]),
                               np.linspace(0,  im_array.shape[2]-1,  im_array.shape[2]))

#### Plot image with arrow overlay

alpha3D_array = sitk.GetArrayFromImage(alpha3D)
slice_id = int(alpha3D_array.shape[2]/2)
plt.figure()
plt.imshow((alpha3D)[slice_id*int(spacing[0]/2),:,:])
X, Y =np.meshgrid(np.linspace(start[1], (n_el[1]*spacing[1])-start[1], int(n_el[1])),
                  np.linspace(start[2], (n_el[2]*spacing[2])-start[2], int(n_el[2])))
X = X.reshape(X.size)
Y = Y.reshape(Y.size)
plt.quiver(X, Y, U[slice_id,:,:], V[slice_id,:,:])

plt.figure()
plt.imshow((alpha3D)[:,slice_id*int(spacing[0]/2),:])
X, Y =np.meshgrid(np.linspace(start[0], (n_el[0]*spacing[0])-start[0], int(n_el[0])),
                  np.linspace(start[2], (n_el[2]*spacing[2])-start[2], int(n_el[2])))
X = X.reshape(X.size)
Y = Y.reshape(Y.size)
plt.quiver(X, Y, U[:,slice_id,:], V[:,slice_id,:])

plt.figure()
plt.imshow((alpha3D)[:,:,slice_id*int(spacing[0]/2)])
X, Y =np.meshgrid(np.linspace(start[0], (n_el[0]*spacing[0])-start[0], int(n_el[0])),
                  np.linspace(start[1], (n_el[1]*spacing[1])-start[1], int(n_el[1])))
X = X.reshape(X.size)
Y = Y.reshape(Y.size)
plt.quiver(X, Y, U[:,:,slice_id], V[:,:,slice_id])  