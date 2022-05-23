## LOCAL REGISTRATION

import SimpleITK as sitk
import shutil

# FREE-FORM DEFORMATION & Deformation Field Maps
def ffd ( im , alpha3D, num):
    
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
    parameterMap['GridSpacingSchedule'] = ('16.0' , '8.0' , '8.0' , '4.0' , '4.0' , '2.0')           #control point spacing
    parameterMap.asdict()                                                                            #the rest of map will follow preset settings

    elastixImageFilter = sitk.ElastixImageFilter()      #creates a filter for registration                                                
    elastixImageFilter.SetParameterMap(parameterMap)    #defines what filter should do
    elastixImageFilter.SetFixedImage(im)                #input image is fixed
    elastixImageFilter.SetMovingImage(alpha3D)          #model image is moving
    elastixImageFilter.LogToFileOn()                    #logs processing in terminal
    elastixImageFilter.Execute()                        #performs registration
    
    FFDIm = elastixImageFilter.GetResultImage()         #resulting image from FFD
    
    #Saves each transform parameter text file into Parameter folder
    original = r'TransformParameters.0.txt'
    target = r'/home/sebastian/.config/spyder-py3/Parameters3/tp' + str(num+113) + '.txt'
    
    shutil.copyfile(original,target)   #copies original data and saves in target
                                           
    return FFDIm
  
