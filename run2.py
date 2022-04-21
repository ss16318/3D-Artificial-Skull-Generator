
import numpy as np
import SimpleITK as sitk

#Functions from other scripts
from display import * 
from resample import resample
from globalReg import *
from localReg import ffd
from alpha3D import getAlpha3D
from check import *


# 1. Builds paths to images of interest

core_path = '/home/sebastian/'

file_list = []              #creates a list of paths to heads

#current heads of interest
# file_list.append( core_path + 'CQ500-CT-436/CQ500CT436_CQ500CT436/Unknown_Study/CT_PLAIN_THIN' )
# file_list.append( core_path + 'CQ500-CT-309/CQ500CT309_CQ500CT309/Unknown_Study/CT_PLAIN_THIN' )
# file_list.append( core_path + 'CQ500-CT-135/CQ500CT135_CQ500CT135/Unknown_Study/CT_PLAIN_THIN' )
# file_list.append( core_path + 'CQ500-CT-268/CQ500CT268_CQ500CT268/Unknown_Study/CT_Thin_Plain' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-2/CQ500CT2 CQ500CT2/Unknown Study/CT 0.625mm' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-3/CQ500CT3 CQ500CT3/Unknown Study/CT PLAIN THIN' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-9/CQ500CT9 CQ500CT9/Unknown Study/CT Thin Plain' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-10/CQ500CT10 CQ500CT10/Unknown Study/CT PLAIN THIN' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-11/CQ500CT11 CQ500CT11/Unknown Study/CT Thin Plain' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-12/CQ500CT12 CQ500CT12/Unknown Study/CT Thin Plain' )

# file_list.append( '/media/sebastian/Data1/CQ500-CT-13/CQ500CT13 CQ500CT13/Unknown Study/CT PRE CONTRAST THIN' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-18/CQ500CT18 CQ500CT18/Unknown Study/CT 0.625mm' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-19/CQ500CT19 CQ500CT19/Unknown Study/CT PLAIN THIN' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-20/CQ500CT20 CQ500CT20/Unknown Study/CT Thin Plain' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-25/CQ500CT25 CQ500CT25/Unknown Study/CT Thin Plain' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-28/CQ500CT28 CQ500CT28/Unknown Study/CT Thin Plain' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-29/CQ500CT29 CQ500CT29/Unknown Study/CT Thin Plain' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-30/CQ500CT30 CQ500CT30/Unknown Study/CT PLAIN THIN' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-32/CQ500CT32 CQ500CT32/Unknown Study/CT 0.625mm' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-34/CQ500CT34 CQ500CT34/Unknown Study/CT PRE CONTRAST THIN')

# file_list.append( '/media/sebastian/Data1/CQ500-CT-35/CQ500CT35 CQ500CT35/Unknown Study/CT Thin Plain')
# file_list.append( '/media/sebastian/Data1/CQ500-CT-37/CQ500CT37 CQ500CT37/Unknown Study/CT PLAIN THIN' )
# file_list.append( '/media/sebastian/Data1/CQ500-CT-39/CQ500CT39 CQ500CT39/Unknown Study/CT PRE CONTRAST THIN' )
# file_list.append('/media/sebastian/Data1/CQ500-CT-47/CQ500CT47 CQ500CT47/Unknown Study/CT PRE CONTRAST THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-48/CQ500CT48 CQ500CT48/Unknown Study/CT PLAIN THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-49/CQ500CT49 CQ500CT49/Unknown Study/CT PRE CONTRAST THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-50/CQ500CT50 CQ500CT50/Unknown Study/CT 0.625mm')
# file_list.append('/media/sebastian/Data1/CQ500-CT-52/CQ500CT52 CQ500CT52/Unknown Study/CT PRE CONTRAST THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-54/CQ500CT54 CQ500CT54/Unknown Study/CT Thin Plain')
# file_list.append('/media/sebastian/Data1/CQ500-CT-55/CQ500CT55 CQ500CT55/Unknown Study/CT 0.625mm')
# file_list.append('/media/sebastian/Data1/CQ500-CT-58/CQ500CT58 CQ500CT58/Unknown Study/CT PRE CONTRAST THIN')

# file_list.append('/media/sebastian/Data1/CQ500-CT-60/CQ500CT60 CQ500CT60/Unknown Study/CT 0.625mm')
# file_list.append('/media/sebastian/Data1/CQ500-CT-62/CQ500CT62 CQ500CT62/Unknown Study/CT Thin Plain')
# file_list.append('/media/sebastian/Data1/CQ500-CT-66/CQ500CT66 CQ500CT66/Unknown Study/CT PLAIN THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-67/CQ500CT67 CQ500CT67/Unknown Study/CT PLAIN THIN') 
# file_list.append('/media/sebastian/Data1/CQ500-CT-68/CQ500CT68 CQ500CT68/Unknown Study/CT Thin Plain')
# file_list.append('/media/sebastian/Data1/CQ500-CT-71/CQ500CT71 CQ500CT71/Unknown Study/CT PRE CONTRAST THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-74/CQ500CT74 CQ500CT74/Unknown Study/CT PRE CONTRAST THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-76/CQ500CT76 CQ500CT76/Unknown Study/CT Thin Plain')
# file_list.append('/media/sebastian/Data1/CQ500-CT-78/CQ500CT78 CQ500CT78/Unknown Study/CT PLAIN THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-80/CQ500CT80 CQ500CT80/Unknown Study/CT 0.625mm')

# file_list.append('/media/sebastian/Data1/CQ500-CT-81/CQ500CT81 CQ500CT81/Unknown Study/CT Thin Plain')
# file_list.append('/media/sebastian/Data1/CQ500-CT-82/CQ500CT82 CQ500CT82/Unknown Study/CT PLAIN THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-84/CQ500CT84 CQ500CT84/Unknown Study/CT PLAIN THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-85/CQ500CT85 CQ500CT85/Unknown Study/CT PLAIN THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-86/CQ500CT86 CQ500CT86/Unknown Study/CT Thin Plain')
# file_list.append('/media/sebastian/Data1/CQ500-CT-88/CQ500CT88 CQ500CT88/Unknown Study/CT PRE CONTRAST THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-90/CQ500CT90 CQ500CT90/Unknown Study/CT 0.625mm')
# file_list.append('/media/sebastian/Data1/CQ500-CT-93/CQ500CT93 CQ500CT93/Unknown Study/CT PRE CONTRAST THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-98/CQ500CT98 CQ500CT98/Unknown Study/CT PRE CONTRAST THIN')
# file_list.append('/media/sebastian/Data1/CQ500-CT-99/CQ500CT99 CQ500CT99/Unknown Study/CT PRE CONTRAST THIN')



files = dict()                              #stores list of paths to images in a dictionary
files['path_list'] = file_list

print(len(file_list))

#pre-process each image
for x in list(file_list):

    # 2. Load Images
    
    # reader = sitk.ImageSeriesReader()                   #creates reader for image series
    # dicom_names = reader.GetGDCMSeriesFileNames(x)      #gets dicom image series
    # reader.SetFileNames(dicom_names)
    # im = reader.Execute()                               #creates images from DICOM file
    
    name = '/media/sebastian/Data1/Oscar/Osca/resample_isosCQ500CT96-000140-00001-00001-0.nii'
    im = sitk.ReadImage(name)   
    im.SetOrigin((0, 0, 0))                             #set the origin
    print('Image loaded')

    # 3. Resample image  

    dimension = 3                                  #parameter (dimension of image)
    target_spacing = np.array([0.5,0.5,0.5])       #parameter (spacing of resampled image)
    resampled_im = resample(im, dimension, target_spacing)  #calls resample function
    print('Image resampled')
    
    display(resampled_im,'Test')
    
    
    # 4. Global registration

    alpha3D = getAlpha3D()                          #gets MIDA model
    rigid_reg_im = rigidReg(resampled_im, alpha3D)            #calls rigid registration function
    print('Image rigidly registered')


    # 5. Local Registration

    results = ffd(rigid_reg_im, alpha3D, x)           #calls elastic registration function
    print('FFD Image')



##DISPLAY IMAGES
#display(vectorOfFFD[0],"")
#display4D(vectorOfDFM[0]," (a) Toward Rigidly-Registered Image")
#compare(vectorOfFFD[0],vectorOfRigidReg[0]," (b) FFD of Model vs Rigidly-Registered")
#compare(vectorOfRigidReg[0],alpha3D,"(a) Rigidly-Registered vs Model")
#rec = reconstruct(alpha3D, vectorOfDFM[0])
#compare(rec,vectorOfFFD[0],"FFD of Model vs Model with DFM approximation")
  
