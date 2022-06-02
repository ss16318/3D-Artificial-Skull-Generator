
import numpy as np
import os
import SimpleITK as sitk
from alpha3D import getAlpha3D
# from sklearn.metrics import mutual_info_score 

#Functions from other scripts
from display import * 
from globalReg import *
from localReg import ffd
from alpha3D import getAlpha3D
from check import *

from reconstruct import reconstruct

from volume import skullVol


# Find location of images
path = '/media/sebastian/Data/AAOscar/Oscar/qure_ai/nii_reorient/'
files = os.listdir(path)

ix = [192,193,199,7,8,21,23,24,28,31,35,37,41,43,45,48,53,55,61,62,63,65,66,68,70,75,77,82,84,88,91,101,103,110,112,113,121,123,126,137,138,141,144,150,154,156,163,170,178,182,185,300,302,306,307,312,315,321,323,328,334,336,338,339,341,342,434,353,364,368,370,374,389,395,396,397,405,407,408,412,413,416,425,430,434,438,444,446,447,450,451,458,460,465,469,470,477,482,492,498,499,506,507,200,206,207,209,211,213,216,218,230,235,236,242,243,246,247,252,259,265,267,268,271,276]

alpha3D = getAlpha3D()          # Load model image


# ix = np.array(ix[100:125])
# volume = np.zeros((ix.shape))

#for x in range(len(ix)):

MI = np.zeros((50,1))    

for x in range(MI.shape[0]):

    # Load each image
    index = ix[x]
    name = path + files[index]
    
    im = sitk.ReadImage(name)

    # # Resample each image
    im.SetOrigin((0,0,0))
    im.SetDirection((1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0))
                 
    # 4. Global registration
    rigid_reg_im = rigidReg(im, alpha3D)            #calls rigid registration function

    # MI[x] = mutual_info_score(alpha3D, rigid_reg_im)
    
    # # 5. Local Registration
    # results = ffd(rigid_reg_im, alpha3D, x)           #calls elastic registration function
    # display(results,'')
    

    
    # # 4. Artificial skull reconstruction 

    # artificialSkull= reconstruct()   #deforms model image using DFM reconstruction from new pm

    # display(artificialSkull, "Extreme Skull 1 " )

    # compare(results,artificialSkull,'')
    
    # volume[x] = skullVol(im,50)
    
    # print(x)

# numSkulls = np.arange(len(ix)) 

# avgSkullVol = np.mean(volume)

# plt.bar(numSkulls+1,volume)                          # plot bar of cumulative explained variance
# ax = plt.gca()
# ax.set_ylabel("Skull Volume (cm^3) ")                 
# ax.set_xlabel("Skulls")
# plt.axhline(y=960, color='r', linestyle='--')
# plt.axhline(y=avgSkullVol,color='r' , linestyle='-' )
# plt.legend(['Average skull volume from literature','Average skull volume of data'],loc='lower right',framealpha=1)
# plt.show()




