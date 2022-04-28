
import numpy as np
import os
import SimpleITK as sitk
from alpha3D import getAlpha3D

#Functions from other scripts
from display import * 
from resample import resample
from globalReg import *
from localReg import ffd
from alpha3D import getAlpha3D
from check import *


# Find location of images
path = '/media/sebastian/Data1/AAOscar/Oscar/qure_ai/nii_reorient/'
files = os.listdir(path)

ix = [192,193,199,7,8,21,23,24,28,31,35,37,41,43,45,48,53,55,61,62,63,65,66,68,70,75,77,82,84,88,91,101,103,110,112,113,121,123,126,137,138,141,144,150,154,156,163,170,178,182,185]


alpha3D = getAlpha3D()          # Load model image

for x in range(len(ix)):
    
    # Load each image
    index = ix[x]
    name = path + files[index]
    im = sitk.ReadImage(name)
    # Resample each image
    im.SetOrigin((0,0,0))
    im.SetDirection((1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0))
    
                         
    # 4. Global registration
    rigid_reg_im = rigidReg(im, alpha3D)            #calls rigid registration function

    # 5. Local Registration
    results = ffd(rigid_reg_im, alpha3D, x)           #calls elastic registration function
    display(results,'Test')
    




