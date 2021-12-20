import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

def display( im ):

    im_array = sitk.GetArrayFromImage(im) 
    plt.figure()
    im0 = (im_array)[int(im_array.shape[0]/2), :, :]
    plt.imshow(im0)
    plt.colorbar()
    plt.figure()
    #plt.rotate(180)
    plt.imshow((im_array)[:, int(200), :])
    plt.colorbar()
    plt.figure()
    #plt.rotate(180)
    plt.imshow((im_array)[:, :, int(im_array.shape[2]/2)])
    plt.colorbar()
    
    return plt.show()


