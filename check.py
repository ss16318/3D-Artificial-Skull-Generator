import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt


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
    
    im_array = sitk.GetArrayFromImage(diffIm)                 #creates array of image
    
    plt.figure()                                              #creates figure for plot
    plt.imshow( (im_array)[int(im_array.shape[0]/2), :, :])   #takes halfway slice of transverse view
    plt.clim(-500, 500) 
    plt.set_cmap('bwr')                                       #colormap used
    cbar  = plt.colorbar()                                    #displays colorbar
    ax = plt.gca()                                            #gets plot axis
    ax.invert_yaxis()                                         #flips y-axis for intuitive view
    ax.set_ylabel("Slices")                   #y axis label
    ax.set_xlabel("Slices")                   #x axis label
    cbar.ax.set_ylabel("Intensity (HU)" , fontsize = 10)      #colorbar title
    plt.title(Title)                 #adds title to plot                   
    
    #same setup for frontal view
    plt.figure()
    plt.imshow((im_array)[:, int(im_array.shape[1]/2) ,:])    
    plt.clim(-500, 500) 
    plt.set_cmap('bwr')
    cbar  = plt.colorbar() 
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_ylabel("Slices")
    ax.set_xlabel("Slices")
    cbar.ax.set_ylabel("Intensity (HU)" , fontsize = 10)
    plt.title(Title)
    
    #same setup for saggital view
    plt.figure()
    plt.imshow((im_array)[:, :, int(im_array.shape[2]/2)])
    plt.clim(-500, 500) 
    plt.set_cmap('bwr')
    cbar  = plt.colorbar() 
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_ylabel("Slices")
    ax.set_xlabel("Slices")
    cbar.ax.set_ylabel("Intensity (HU)" , fontsize = 10)
    plt.title(Title)
    
    return plt.show()     









         
