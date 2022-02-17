import SimpleITK as sitk

from alpha3D import getAlpha3D
from display import *
from resample import resample
from globalReg import rigidReg
from localReg import ffd

alpha3D = getAlpha3D()

alphaArray = sitk.GetArrayFromImage(alpha3D)

display(alpha3D,'Model ')

alphaArray[alphaArray<500] = -1000                      #sets all array values less than 0 to -1000

decluttered = sitk.GetImageFromArray(alphaArray)

display(decluttered,'Decluttered')

x = '/media/sebastian/Data1/CQ500-CT-2/CQ500CT2 CQ500CT2/Unknown Study/CT 0.625mm' 

reader = sitk.ImageSeriesReader()                   #creates reader for image series
dicom_names = reader.GetGDCMSeriesFileNames(x)      #gets dicom image series
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


parameterMap.GetTransformDomainMeshSize()