## GLOBAL REGISTRATION

import SimpleITK as sitk

## RIGID BODY REGISTRATION

def rigidReg( im , alpha3D):
    
    parameterMap = sitk.GetDefaultParameterMap("rigid")                                              # parameterMap.items()
    
    parameterMap['Registration'] = ("MultiMetricMultiResolutionRegistration",)
    parameterMap['FixedImagePyramid'] = ('FixedShrinkingImagePyramid',)                              # FixedShrinkingImagePyramid, FixedRecursiveImagePyramid
    parameterMap['MovingImagePyramid'] = ('MovingShrinkingImagePyramid',)                            # MovingShrinkingImagePyramid, MovingRecursiveImagePyramid
    parameterMap['Metric'] = ("AdvancedNormalizedCorrelation", "AdvancedMattesMutualInformation")    # AdvancedNormalizedCorrelation, AdvancedMattesMutualInformation
    parameterMap['MaximumNumberOfIterations'] = ('1500','350','350','350','350','350')
    parameterMap['NumberOfResolutions'] = ("6",)
    parameterMap["DefaultPixelValue"] = ["-1000"]
    parameterMap.asdict()                                                                            #saves setup in a dictionary
    
    elastixImageFilter = sitk.ElastixImageFilter()                                                   #does the registration
    elastixImageFilter.SetParameterMap(parameterMap)
    elastixImageFilter.SetFixedImage(alpha3D)
    elastixImageFilter.SetMovingImage(im)
    elastixImageFilter.LogToFileOn()
    elastixImageFilter.Execute()
    
    return elastixImageFilter.GetResultImage()


## AFFINE REGISTRATION

def affineReg( im , alpha3D):

    parameterMap = sitk.GetDefaultParameterMap("affine")                                             # parameterMap.items()
    
    parameterMap['Registration'] = ("MultiMetricMultiResolutionRegistration",)
    parameterMap['FixedImagePyramid'] = ('FixedShrinkingImagePyramid',)                              # FixedShrinkingImagePyramid, FixedRecursiveImagePyramid
    parameterMap['MovingImagePyramid'] = ('MovingShrinkingImagePyramid',)                            # MovingShrinkingImagePyramid, MovingRecursiveImagePyramid
    parameterMap['Metric'] = ("AdvancedNormalizedCorrelation", "AdvancedMattesMutualInformation")    # AdvancedNormalizedCorrelation, AdvancedMattesMutualInformation
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
