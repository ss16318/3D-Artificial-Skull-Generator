## DISPLAYS IMAGES

import SimpleITK as sitk
from scipy.io import savemat


def SaveToMat(im,name):

    im_array = sitk.GetArrayFromImage(im)
    
    savemat(name+".mat", {'image': im_array} )
    
    return