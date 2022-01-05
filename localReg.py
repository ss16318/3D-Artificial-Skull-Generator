## LOCAL REGISTRATION

import SimpleITK as sitk

from display import display
from check import compare

# FREE-FORM DEFORMATION & Deformation Field Maps
def ffd ( im , alpha3D):
    
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
    parameterMap['GridSpacingSchedule'] = ('16.0' , '8.0' , '8.0' , '4.0' , '2.0' , '1.0')           #control point spacing
    parameterMap.asdict()                                                                            #the rest of map will follow preset settings

    elastixImageFilter = sitk.ElastixImageFilter()      #creates a filter for registration                                                
    elastixImageFilter.SetParameterMap(parameterMap)    #defines what filter should do
    elastixImageFilter.SetFixedImage(im)                #input image is fixed
    elastixImageFilter.SetMovingImage(alpha3D)          #model image is moving
    elastixImageFilter.LogToFileOn()                    #logs processing in terminal
    elastixImageFilter.Execute()                        #performs registration
    
    FFDIm = elastixImageFilter.GetResultImage()         #resulting image from FFD
    
    #EXTRACTING DFMs
    
    transformixImageFilter = sitk.TransformixImageFilter()                                           #creates filter for transform
    transformixImageFilter.SetMovingImage(alpha3D)                                                   #maintains that model image is moving
    transformixImageFilter.SetTransformParameterMap(elastixImageFilter.GetTransformParameterMap())   #gets paramter map used for FFD
    transformixImageFilter.ComputeDeformationFieldOn()                                               #allows DFM to be computed during transform
    transformixImageFilter.LogToConsoleOn()                                                          #logs processing in terminal
    transformixImageFilter.Execute()                                                                 #performs transform
    DFM = transformixImageFilter.GetDeformationField()                                               #gets DFM of transform
    
    return FFDIm , DFM

