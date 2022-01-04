import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

def display( im , Title ):

    im_array = sitk.GetArrayFromImage(im)
    
    plt.figure()
    im0 = (im_array)[int(im_array.shape[0]/2), :, :]
    plt.imshow(im0)
    plt.clim(-1600, 1600)
    plt.colorbar()
    ax = plt.gca()
    ax.invert_yaxis()
    plt.title(Title + " (Transverse view)")
    
    plt.figure()
    plt.imshow((im_array)[:, int(im_array.shape[1]/2) ,:])
    plt.clim(-1600, 1600)
    plt.colorbar()
    ax = plt.gca()
    ax.invert_yaxis()
    plt.title(Title + " (Frontal view)")
    
    plt.figure()
    plt.imshow((im_array)[:, :, int(im_array.shape[2]/2)])
    plt.clim(-1600, 1600)
    plt.colorbar()
    ax = plt.gca()
    ax.invert_yaxis()
    plt.title(Title + " (Saggital view)")
    
    return plt.show()

#allows deformation fields to be displayed
def display4D( im , Title ):

    im_array = sitk.GetArrayFromImage(im) 
    
    plt.figure()
    im0 = (im_array)[int(im_array.shape[0]/2), :, : , 0]
    plt.imshow(im0)
    plt.colorbar()
    plt.clim(-20, 25)
    ax = plt.gca()
    ax.invert_yaxis()
    plt.title(Title + " (Transverse view)")
    
    plt.figure()
    plt.imshow((im_array)[:, int(im_array.shape[1]/2) ,: , 1])
    plt.colorbar()
    plt.clim(-20, 25)
    ax = plt.gca()
    ax.invert_yaxis()
    plt.title(Title + " (Frontal view)")
    
    plt.figure()
    plt.imshow((im_array)[:, :, int(im_array.shape[2]/2) , 2])
    plt.colorbar()
    plt.clim(-20, 25)
    ax = plt.gca()
    ax.invert_yaxis()
    plt.title(Title + " (Saggital view)")
    
    return plt.show()


