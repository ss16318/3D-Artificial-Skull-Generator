## DISPLAYS IMAGES

import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np  

def display( im , Title ):

    im_array = sitk.GetArrayFromImage(im)                     #creates array of image

    plt.figure()                                              #creates figure for plot
    plt.imshow( (im_array)[int(im_array.shape[0]/2), :, :])   #takes halfway slice of transverse view
    plt.clim(-1600, 1600)                                     #sets extremes of color map
    plt.bone()                                                #colormap used
    cbar  = plt.colorbar()                                    #displays colorbar
    ax = plt.gca()                                            #gets plot axis
    ax.invert_yaxis()                                         #flips y-axis for intuitive view
    ax.set_ylabel("Slices")                   #y axis label
    ax.set_xlabel("Slices")                   #x axis label
    cbar.ax.set_ylabel("Intensity (HU)" , fontsize = 10)      #colorbar title
    #plt.title("(a) " + Title + " (Transverse view)")         #adds title to plot                   
    plt.title(Title)      
    
    #same setup for frontal view
    plt.figure()
    plt.imshow((im_array)[:, int(im_array.shape[1]/2) ,:])    
    plt.clim(-1600, 1600)
    plt.bone()
    cbar  = plt.colorbar() 
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_ylabel("Slices")
    ax.set_xlabel("Slices")
    cbar.ax.set_ylabel("Intensity (HU)" , fontsize = 10)
    plt.title("(b) " + Title + " (Frontal view)")
    
    #same setup for saggital view
    plt.figure()
    plt.imshow((im_array)[:, :, int(im_array.shape[2]/2)])
    plt.clim(-1600, 1600)
    plt.bone()
    cbar  = plt.colorbar() 
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_ylabel("Slices")
    ax.set_xlabel("Slices")
    cbar.ax.set_ylabel("Intensity (HU)" , fontsize = 10)
    plt.title("(c) " + Title + " (Sagittal View)")
    
    return plt.show()                                        #displays figures                             

## DISPLAYS DEFORMATION FIELD MAPS
def display4D( im , Title ):

    im_array = sitk.GetArrayFromImage(im) 
    
    plt.figure()
    plt.imshow((im_array)[int(im_array.shape[0]/2), :, : , 0])    #note extra dimension being called
    plt.clim(-20, 25)
    plt.set_cmap('bwr')
    cbar  = plt.colorbar() 
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_ylabel("Pixels (0.5mm spacing)")                   
    ax.set_xlabel("Pixels (0.5mm spacing)")                   
    cbar.ax.set_ylabel("Deformation vector length (Pixels)" , fontsize = 10)       
    plt.title(Title + " (Transverse view)")
    
    plt.figure()
    plt.imshow((im_array)[:, int(im_array.shape[0]/2) ,: , 1])
    cbar  = plt.colorbar() 
    plt.clim(-20, 25)
    plt.set_cmap('bwr')
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_ylabel("Pixels (0.5mm spacing)")                   
    ax.set_xlabel("Pixels (0.5mm spacing)")                   
    cbar.ax.set_ylabel("Deformation vector length (Pixels)" , fontsize = 10)
    plt.title(Title + " (Frontal view)")
    
    plt.figure()
    plt.imshow((im_array)[:, :, int(im_array.shape[0]/2) , 2])
    cbar  = plt.colorbar() 
    plt.clim(-20, 25)
    plt.set_cmap('bwr')
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_ylabel("Pixels (0.5mm spacing)")                   
    ax.set_xlabel("Pixels (0.5mm spacing)")                   
    cbar.ax.set_ylabel("Deformation vector length (Pixels)" , fontsize = 10)
    plt.title(Title + "(f) Saggital View")
    
    return plt.show()

## DISPLAYS Cumulative Exaplained Variance

def displayCEV(CEV):

    modeNum = np.arange(len(CEV))                    # Eigenmode number (just a list) 
    
    plt.plot(modeNum+1, CEV)                          # plot bar of cumulative explained variance
    ax = plt.gca()
    ax.set_ylabel("Cumulative Explained Variance (%)")                 
    ax.set_xlabel("Number of PCs")
    plt.xlim([0,len(CEV)+1])
    plt.title("Cumulaive Explained Variance vs Number of Modes")
    plt.axhline(y=95, color='r', linestyle='-')
    plt.axvline(x=35, color='r', linestyle='--')
    plt.legend(['Cumulative explained variance','95% explained variance cut-off','PC cut-off'])
    plt.show()

    return

## DISPLAYS WARPED IMAGE GRIDS

def displayGrid(Grid,Im,Title):
    

    im = sitk.GetArrayFromImage(Im)                     #creates array of image
    grid = sitk.GetArrayFromImage(Grid)
    
    im_array = grid + im
    
    plt.figure()                                              #creates figure for plot
    plt.imshow( (im_array)[int(im_array.shape[0]/2), :, :])   #takes halfway slice of transverse view
    plt.clim(-1600, 1600)                                     #sets extremes of color map
    plt.bone()                                                #colormap used
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
    plt.clim(-1600, 1600)
    plt.bone()
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
    plt.clim(-1600, 1600)
    plt.bone()
    cbar  = plt.colorbar() 
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_ylabel("Slices")
    ax.set_xlabel("Slices")
    cbar.ax.set_ylabel("Intensity (HU)" , fontsize = 10)
    plt.title(Title)
    
    plt.show()
    
    return

def displayMag( im_array , im2 , Title ):

    plt.figure()                                              #creates figure for plot
    plt.imshow( (im_array)[int(im_array.shape[0]/2), :, :] , cmap='Reds')   #takes halfway slice of transverse view
    cbar  = plt.colorbar() 
    plt.clim(0,8)
    plt.imshow((im2)[int(im2.shape[0]/2), :, :],alpha=0.1)
    ax = plt.gca()                                            #gets plot axis
    ax.invert_yaxis()                                         #flips y-axis for intuitive view
    ax.set_ylabel("Slices")                   #y axis label
    ax.set_xlabel("Slices")                   #x axis label
    plt.title("(a) " + Title + "")              #adds title to plot                        
    
    #same setup for frontal view
    plt.figure()
    plt.imshow((im_array)[:, int(im_array.shape[1]/2) ,:],cmap='Reds')   
    cbar  = plt.colorbar()    
    plt.clim(0,8)
    plt.imshow((im2)[:, int(im2.shape[1]/2), :],alpha=0.1)
    ax = plt.gca()                                            #gets plot axis
    ax.invert_yaxis()                                         #flips y-axis for intuitive view
    ax.set_ylabel("Slices")                   #y axis label
    ax.set_xlabel("Slices")                   #x axis label
    plt.title("(b) " + Title + "")
    
    #same setup for saggital view
    plt.figure()
    plt.imshow((im_array)[:, :, int(im_array.shape[2]/2)],cmap='Reds')
    cbar  = plt.colorbar()    
    plt.clim(0,8)
    plt.imshow((im2)[:, :, int(im2.shape[0]/2)],alpha=0.1)   
    ax = plt.gca()                                            #gets plot axis
    ax.invert_yaxis()                                         #flips y-axis for intuitive view
    ax.set_ylabel("Slices")                   #y axis label
    ax.set_xlabel("Slices")                   #x axis label
    cbar.ax.set_ylabel("Deformation Magnitude (mm)" , fontsize = 10)
    plt.title("(c) " + Title + "")
    
    return plt.show()         