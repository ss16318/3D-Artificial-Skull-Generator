
import numpy as np
import SimpleITK as sitk

#Functions from other scripts
from display import * 
from resample import resample

x = ''


reader = sitk.ImageSeriesReader()                   #creates reader for image series
dicom_names = reader.GetGDCMSeriesFileNames(x)      #gets dicom image series
reader.SetFileNames(dicom_names)
im = reader.Execute()                               #creates images from DICOM file
im.SetOrigin((0, 0, 0))                             #set the origin
   
dimension = 3                                  #parameter (dimension of image)
target_spacing = np.array([0.5,0.5,0.5])       #parameter (spacing of resampled image)

resampled_im = resample(im, dimension, target_spacing)  #calls resample function

display(im , "Original")
display(resampled_im,"Resampled " )


#OK List
# /media/sebastian/Data1/CQ500-CT-0/CQ500CT0 CQ500CT0/Unknown Study/CT PLAIN THIN
# /media/sebastian/Data1/CQ500-CT-4/CQ500CT4 CQ500CT4/Unknown Study/CT 0.625mm
# /media/sebastian/Data1/CQ500-CT-14/CQ500CT14 CQ500CT14/Unknown Study/CT Plain THIN
# /media/sebastian/Data1/CQ500-CT-22/CQ500CT22 CQ500CT22/Unknown Study/CT PLAIN THIN
# /media/sebastian/Data1/CQ500-CT-27/CQ500CT27 CQ500CT27/Unknown Study/CT PLAIN THIN
# /media/sebastian/Data1/CQ500-CT-36/CQ500CT36 CQ500CT36/Unknown Study/CT PRE CONTRAST THIN
# /media/sebastian/Data1/CQ500-CT-40/CQ500CT40 CQ500CT40/Unknown Study/CT 0.625mm
# /media/sebastian/Data1/CQ500-CT-53/CQ500CT53 CQ500CT53/Unknown Study/CT Thin Plain
# /media/sebastian/Data1/CQ500-CT-57/CQ500CT57 CQ500CT57/Unknown Study/CT 0.625mm
# /media/sebastian/Data1/CQ500-CT-63/CQ500CT63 CQ500CT63/Unknown Study/CT PRE CONTRAST THIN
# /media/sebastian/Data1/CQ500-CT-72/CQ500CT72 CQ500CT72/Unknown Study/CT PRE CONTRAST THIN
# /media/sebastian/Data1/CQ500-CT-89/CQ500CT89 CQ500CT89/Unknown Study/CT PRE CONTRAST THIN
# /media/sebastian/Data1/CQ500-CT-95/CQ500CT95 CQ500CT95/Unknown Study/CT PRE CONTRAST THIN

#GOOD List
# /media/sebastian/Data1/CQ500-CT-78/CQ500CT78 CQ500CT78/Unknown Study/CT PLAIN THIN
# /media/sebastian/Data1/CQ500-CT-80/CQ500CT80 CQ500CT80/Unknown Study/CT 0.625mm
# /media/sebastian/Data1/CQ500-CT-81/CQ500CT81 CQ500CT81/Unknown Study/CT Thin Plain
# /media/sebastian/Data1/CQ500-CT-82/CQ500CT82 CQ500CT82/Unknown Study/CT PLAIN THIN
# /media/sebastian/Data1/CQ500-CT-84/CQ500CT84 CQ500CT84/Unknown Study/CT PLAIN THIN
# /media/sebastian/Data1/CQ500-CT-85/CQ500CT85 CQ500CT85/Unknown Study/CT PLAIN THIN
# /media/sebastian/Data1/CQ500-CT-86/CQ500CT86 CQ500CT86/Unknown Study/CT Thin Plain
# /media/sebastian/Data1/CQ500-CT-88/CQ500CT88 CQ500CT88/Unknown Study/CT PRE CONTRAST THIN
# /media/sebastian/Data1/CQ500-CT-90/CQ500CT90 CQ500CT90/Unknown Study/CT 0.625mm
# /media/sebastian/Data1/CQ500-CT-93/CQ500CT93 CQ500CT93/Unknown Study/CT PRE CONTRAST THIN
# /media/sebastian/Data1/CQ500-CT-98/CQ500CT98 CQ500CT98/Unknown Study/CT PRE CONTRAST THIN
# /media/sebastian/Data1/CQ500-CT-99/CQ500CT99 CQ500CT99/Unknown Study/CT PRE CONTRAST THIN


#Oscar not good
# file_list.append( core_path + 'CQ500-CT-38/CQ500CT38_CQ500CT38/Unknown_Study/CT_PLAIN_THIN' )
# file_list.append( core_path + 'CQ500-CT-436/CQ500CT436_CQ500CT436/Unknown_Study/CT_Plain' )
# file_list.append( core_path + 'CQ500-CT-0/CQ500CT0_CQ500CT0/Unknown_Study/CT_Plain' )
# file_list.append( core_path + 'CQ500-CT-391/CQ500CT391_CQ500CT391/Unknown_Study/CT_Plain_3mm' )