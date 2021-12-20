## LOCAL REGISTRATION

import SimpleITK as sitk

from display import display
from check import compare

# Non-rigid Registration 1
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
    parameterMap['GridSpacingSchedule'] = ('16.0' , '16.0' , '16.0' , '16.0' , '16.0' , '16.0')
    parameterMap.asdict()

    elastixImageFilter = sitk.ElastixImageFilter()                                                   #does the registration
    elastixImageFilter.SetParameterMap(parameterMap)
    elastixImageFilter.SetFixedImage(alpha3D)
    elastixImageFilter.SetMovingImage(im)
    elastixImageFilter.LogToFileOn()
    elastixImageFilter.Execute()
    
    elasticRegIm = elastixImageFilter.GetResultImage()
    
    display(elasticRegIm)
    
    transformixImageFilter = sitk.TransformixImageFilter()
    transformixImageFilter.SetMovingImage(im)  
    transformixImageFilter.SetTransformParameterMap(elastixImageFilter.GetTransformParameterMap())
    transformixImageFilter.ComputeDeformationFieldOn()
    transformixImageFilter.LogToConsoleOn()
    #transformixImageFilter.SetOutputDirectory("/home/sebastian/Documents/Deformations/")
    transformixImageFilter.Execute()
    #sitk.WriteImage(transformixImageFilter.GetDeformationField(), "/home/sebastian/Documents/Deformations/transformix_rigid_affine_bspline.dcm.gz")
    deformationField = transformixImageFilter.GetDeformationField()
    display(deformationField)
    
    
    warper = sitk.WarpImageFilter()
    warper.SetOutputParameteresFromImage(deformationField)
    out = warper.Execute(im,deformationField)

    display(out)
    compare(out,elasticRegIm)
    
    
    return deformationField

