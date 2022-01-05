import numpy as np
import SimpleITK as sitk
from display import display

# THIS FUNCTION CHECKS THE SHAPE OF THE IMAGES (USEFUL FOR REGISTRATION)

def checkShape( im1 , im2):
    
    array1 = sitk.GetArrayFromImage(im1)    #gets arrays of images
    array2 = sitk.GetArrayFromImage(im2)
    
    shape1 = np.shape(array1)               #finds shapes of arrays
    shape2 = np.shape(array2)
    
    if shape1 == shape2:                    #shapes are the same
        print('All good')
    else:                                   #shapes are not same
        print(shape1)
        print(shape2)
        
        return print('Checked')
    

        
# THIS FUNCTION TAKES THE DIFFERENCE BETWEEN TWO IMAGES AND DISPLAYS
# THE RESULTING IMAGE. IT CAN BE USED TO MEASURE DIFFERENCE TO MODEL OR
# THE DIFFERENCES PRE AND POST TRANSFORMATION

def compare(im1, im2 , Title):

    diffIm = im1 - im2  #note im2 is subtracted!

    return display(diffIm , Title)







         
