import numpy as np
import SimpleITK as sitk

def getAlpha3D():

    #builds path to alpha3D and loads image array
    alpha3D_path = '/home/sebastian'
    alpha3D = np.load(alpha3D_path+'/alpha3D_array.npy')
    
    #adjusts image for registration (via numpy package)
    alpha3D = np.rot90( alpha3D, 1, (2,1))                 # rotate Alpha 3D rot90(array,#times,plane of rotation)
    alpha3D -= 1480                                        # roughly transforms [m s^-1] to [HU]
    default_value = -1000                                  # HU for air = -1000
    alpha3D[alpha3D==0] = default_value    
    
    #adjusts image for registration (via SITK package)
    alpha3D_image = sitk.GetImageFromArray(alpha3D)        # get Simple ITK image from numpy array
    alpha3D_image.SetOrigin((0,0,0))                      
    target_spacing = (0.5, 0.5, 0.5)
    alpha3D_image.SetSpacing(target_spacing)
    
    return alpha3D_image 


# PASTE IDEA
    # base_im = sitk.GetImageFromArray(np.ones((600,600,600)))      # Create the output image space
    # base_im.SetSpacing(target_spacing)                            # set spacing of points
    # base_im.SetDirection(alpha3D_image.GetDirection())            # set direction of image and resamp to match

    # alpha3D_im = sitk.PasteImageFilter(base_im,alpha3D_image)
    
# RESAMPLE IDEA
    #from resample import resample
    # return resample(alpha3D_image,3,target_spacing)
    
# PAD ARRAY IDEA
        #dims = np.shape(alpha3D)
        #size = 600
        #alpha3D = np.lib.pad(alpha3D, ((0,size-dims[0]),(0,size-dims[1]),(0,size-dims[2])) , 'constant', constant_values=(-1000))                        

        







