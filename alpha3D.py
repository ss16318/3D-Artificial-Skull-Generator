import numpy as np
import SimpleITK as sitk

from display import display

def getAlpha3D():

    #builds path to alpha3D and loads image array
    alpha3D_path = '/home/sebastian'
    alpha3D = np.load(alpha3D_path+'/alpha3D_array.npy')
    
    #adjusts image for registration (via numpy package)
    alpha3D = np.rot90( alpha3D, 1, (2,1))                 #rotate Alpha3D rot90(array,#times,plane of rotation)
    alpha3D = np.flip(alpha3D,axis=1)                      #flips image to match input data
    alpha3D -= 1480                                        #roughly transforms [m s^-1] to [HU]
    default_value = -1000                                  #HU for air = -1000
    alpha3D[alpha3D==0] = default_value    
    
    #adjusts image for registration (via SITK package)
    alpha3D_image = sitk.GetImageFromArray(alpha3D)        #create image from array
    alpha3D_image.SetOrigin((0,0,0))                      
    target_spacing = (0.5, 0.5, 0.5)
    alpha3D_image.SetSpacing(target_spacing)
    
    return alpha3D_image 
                      

        







