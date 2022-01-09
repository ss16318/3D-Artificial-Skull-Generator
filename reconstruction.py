# RECONSTRUCTION 

import SimpleITK as sitk

def reconstruct(im , DFM):

    warper = sitk.WarpImageFilter()              #creates filter for transform
    warper.SetOutputParameteresFromImage(DFM)    #filter will use a DFM
    out = warper.Execute(im,DFM)                 #applies DFM to image
    
    return out