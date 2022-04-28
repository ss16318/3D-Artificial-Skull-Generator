import SimpleITK as sitk  # Note that elastix adds some functionality to SimpleITK
import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt

from alpha3D import getAlpha3D
from resample import resample
from globalReg import rigidReg
from localReg import ffd
from display import display

x = '/media/sebastian/Data1/CQ500-CT-2/CQ500CT2 CQ500CT2/Unknown Study/CT 0.625mm' 

reader = sitk.ImageSeriesReader()                   #creates reader for image series
dicom_names = reader.GetGDCMSeriesFileNames(x)      #gets dicom image series
reader.SetFileNames(dicom_names)
im = reader.Execute()                               #creates images from DICOM file

im.SetOrigin((0, 0, 0))                             #set the origin

alpha3D = getAlpha3D()

dimension = 3                                  #parameter (dimension of image)
target_spacing = np.array([0.5,0.5,0.5])       #parameter (spacing of resampled image)
resampled_im = resample(im, dimension, target_spacing)  #calls resample function

rigid_reg_im = rigidReg(resampled_im, alpha3D) 

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
parameterMapElastic = elastixImageFilter.GetTransformParameterMap()

FFDIm = elastixImageFilter.GetResultImage()         #resulting image from FFD

display(FFDIm,"FFD")

file = "/home/sebastian/.config/spyder-py3/TransformParameters.0.txt"

#Extract data from parameter map
with open (file , 'rt') as pm:                  #opens parameter file for reading
    for ln in pm:                               #reads each line to a string
        
        if "GridOrigin" in ln:                                  #gets line with origin data
            origin = ln.split("GridOrigin",1)[1]                #cuts string to only numbers
            origin = origin.split(")",1)[0]
            start = np.array(origin.split(), dtype=np.float)   #saves data as an array type float
            
        if "GridSize" in ln:                                    #gets line with size data
            size = ln.split("GridSize",1)[1]
            size = size.split(")",1)[0]
            n_el = np.array(size.split(), dtype=np.int)

        if "GridSpacing" in ln:
            spacing = ln.split("GridSpacing",1)[1]               #gets line with spacing data
            spacing = spacing.split(")",1)[0]
            spacing = np.array(spacing.split(), dtype=np.float).astype(int)#saved as int to prevent error
            spacing = spacing                                #why?
            
        if "(TransformParameters" in ln:                         #gets line with control pt def data
            df = ln.split("(TransformParameters",1)[1]
            df = df.split(")",1)[0]
            deformations = np.array(df.split(), dtype=np.float)
                

deformations = deformations.reshape(3, int(deformations.shape[0]/3))
U = deformations[0,:].reshape(n_el[0], n_el[1], n_el[2])
V = deformations[1,:].reshape(n_el[0], n_el[1], n_el[2])
                                                                                                                                                                                                                                            

#### Plot image with arrow overlay
im_array = sitk.GetArrayFromImage(alpha3D)
size = np.shape(im_array)

slice_id = int(im_array.shape[2]/(2*spacing[0]))
plt.figure()
plt.imshow( (im_array)[int(im_array.shape[0]/2), :, :])
ax = plt.gca() 
ax.invert_yaxis()
X, Y =np.meshgrid(np.linspace(0, size[2], int(n_el[2])),
                  np.linspace(0, size[1], int(n_el[1])))
X = X.reshape(X.size)
Y = Y.reshape(Y.size)
plt.quiver(X, Y, U[slice_id,:,:], V[slice_id,:,:] , color='r')

plt.figure()
plt.imshow((im_array)[:, int(im_array.shape[1]/2) ,:]) 
ax = plt.gca() 
ax.invert_yaxis()
X, Y =np.meshgrid(np.linspace(0, size[2], int(n_el[2])),
                  np.linspace(0, size[0], int(n_el[0])))
X = X.reshape(X.size)
Y = Y.reshape(Y.size)
plt.quiver(X, Y, U[:,slice_id,:], V[:,slice_id,:], color='r')

plt.figure()
plt.imshow((im_array)[:, :, int(im_array.shape[2]/2)])
ax = plt.gca() 
ax.invert_yaxis()
X, Y =np.meshgrid(np.linspace(0, size[1], int(n_el[1])),
                  np.linspace(0, size[0], int(n_el[0])))
X = X.reshape(X.size)
Y = Y.reshape(Y.size)
plt.quiver(X, Y, U[:,:,slice_id], V[:,:,slice_id] , color='r')


