## GLOBAL REGISTRATION

import SimpleITK as sitk

## RIGID BODY REGISTRATION

def rigidReg( im , alpha3D):
    
    parameterMap = sitk.GetDefaultParameterMap("rigid")                                              #rigid = rotation + translation
    
    parameterMap['Registration'] = ("MultiMetricMultiResolutionRegistration",)
    parameterMap['FixedImagePyramid'] = ('FixedShrinkingImagePyramid',)                              #applies registration at different resolutions (only downsampling applied)
    parameterMap['MovingImagePyramid'] = ('MovingShrinkingImagePyramid',)                            
    parameterMap['Metric'] = ("AdvancedNormalizedCorrelation", "AdvancedMattesMutualInformation")    #cross-correlation & probability distribution metrics
    parameterMap['MaximumNumberOfIterations'] = ('1500','350','350','350','350','350')               #number of registration iterations at each pyramid level
    parameterMap['NumberOfResolutions'] = ("6",)                                                     #number of pyramid levels
    parameterMap["DefaultPixelValue"] = ["-1000"]
    parameterMap.asdict()                                                                            #the rest of map will follow preset settings
    
    elastixImageFilter = sitk.ElastixImageFilter()         #creates a registration filter
    elastixImageFilter.SetParameterMap(parameterMap)       #uses parameter map to define filter
    elastixImageFilter.SetFixedImage(alpha3D)              #model is fixed
    elastixImageFilter.SetMovingImage(im)                  #input is moving
    elastixImageFilter.LogToFileOn()                       #logs process in terminal
    elastixImageFilter.Execute()                           #performs registration

    return elastixImageFilter.GetResultImage()             #returns output image


## AFFINE REGISTRATION

def affineReg( im , alpha3D):

    parameterMap = sitk.GetDefaultParameterMap("affine")  #affine = shear, scale, translation & rotation
    
    parameterMap['Registration'] = ("MultiMetricMultiResolutionRegistration",)
    parameterMap['FixedImagePyramid'] = ('FixedShrinkingImagePyramid',)                              
    parameterMap['MovingImagePyramid'] = ('MovingShrinkingImagePyramid',)                            
    parameterMap['Metric'] = ("AdvancedNormalizedCorrelation", "AdvancedMattesMutualInformation")    
    parameterMap['MaximumNumberOfIterations'] = ('1500','350','350','350','350','350')
    parameterMap['NumberOfResolutions'] = ("6",)
    parameterMap["DefaultPixelValue"] = ["-1000"]
    parameterMap.asdict()
    
    elastixImageFilter = sitk.ElastixImageFilter()
    elastixImageFilter.LogToFileOn()
    elastixImageFilter.SetFixedImage(alpha3D)
    elastixImageFilter.SetMovingImage(im)
    elastixImageFilter.SetParameterMap(parameterMap)
    elastixImageFilter.Execute()
    
    return elastixImageFilter.GetResultImage()