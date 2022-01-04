## LOCAL REGISTRATION

import SimpleITK as sitk

from display import display
from check import compare

# Non-rigid Registration
def elasticReg ( im , alpha3D):
    parameterMap = sitk.GetDefaultParameterMap("bspline")                                         # parameterMap.items()
    
    parameterMap['Registration'] = ("MultiMetricMultiResolutionRegistration",)
    parameterMap['FixedImagePyramid'] = ('FixedShrinkingImagePyramid',)                              # FixedShrinkingImagePyramid, FixedRecursiveImagePyramid
    parameterMap['MovingImagePyramid'] = ('MovingShrinkingImagePyramid',)                            # MovingShrinkingImagePyramid, MovingRecursiveImagePyramid
    parameterMap['Metric'] = ("AdvancedNormalizedCorrelation", "AdvancedMattesMutualInformation")    # AdvancedNormalizedCorrelation, AdvancedMattesMutualInformation
    parameterMap['MaximumNumberOfIterations'] = ('1500','350','350','350','350','350')
    parameterMap['NumberOfResolutions'] = ("6",)
    parameterMap["DefaultPixelValue"] = ["-1000"]
    parameterMap['NumberOfSpatialSamples'] = [str((alpha3D.GetSize()[0]*alpha3D.GetSize()[1]*alpha3D.GetSize()[2])/5000)]
    parameterMap['GridSpacingSchedule'] = ('16.0' , '8.0' , '8.0' , '4.0' , '2.0' , '1.0')
    parameterMap.asdict()

    elastixImageFilter = sitk.ElastixImageFilter()                                                   #does the registration
    elastixImageFilter.SetParameterMap(parameterMap)
    elastixImageFilter.SetFixedImage(im)
    elastixImageFilter.SetMovingImage(alpha3D)
    elastixImageFilter.LogToFileOn()
    elastixImageFilter.Execute()
    
    elasticRegIm = elastixImageFilter.GetResultImage()
    
    display(elasticRegIm , "FFD of Model Skull")
    compare(elasticRegIm, im , "FFD result - input skull")
    
    # Exctracting deformation field of elastic registration
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetMovingImage(alpha3D)  
    transformixImageFilter.SetTransformParameterMap(elastixImageFilter.GetTransformParameterMap())
    transformixImageFilter.ComputeDeformationFieldOn()
    transformixImageFilter.LogToConsoleOn()
    transformixImageFilter.Execute()
    deformationField = transformixImageFilter.GetDeformationField()
    
    warper = sitk.WarpImageFilter()
    warper.SetOutputParameteresFromImage(deformationField)
    out = warper.Execute(alpha3D,deformationField)

    compare(out,elasticRegIm , "Reconstruction compared to actual image")
    
    
    return deformationField

