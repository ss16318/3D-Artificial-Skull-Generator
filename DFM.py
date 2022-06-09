import SimpleITK as sitk
import numpy as np
from alpha3D import getAlpha3D    
from numpy import save
from numpy import load
from display import *
import matplotlib.pyplot as plt



## IT TAKES SOME TIME TO RUN THIS SECTION HENCE RESULTS ARE SAVED TO NUMPY ##
## ARRAYS AND THE LOADED, SO THIS SECTION MAY BE COMMENTED OUT. ALSO THE   ##
## MODELLING.PY FILE MUST BE RUN TO CREATE THE DESIRED TRANSFORM PARAMETER ##
## FILE                                                                    ##


# alpha3D = getAlpha3D()  #gets model image
    
# path = '/home/sebastian/.config/spyder-py3/reconstruction.txt'

# pm = sitk.ReadParameterFile(path)    #gets parameter map from transform file

# #EXTRACTING DFMs
# transformixImageFilter = sitk.TransformixImageFilter() #creates filter for transform
# transformixImageFilter.SetMovingImage(alpha3D)         #model image will be deformed
# transformixImageFilter.SetTransformParameterMap(pm)    #gets paramter map used for FFD
# transformixImageFilter.ComputeDeformationFieldOn()     #allows DFM to be computed during transform
# transformixImageFilter.LogToConsoleOn()                #logs processing in terminal
# transformixImageFilter.Execute()                       #performs deformation
# DFM = transformixImageFilter.GetDeformationField()     #saves DFMs

# warper = sitk.WarpImageFilter()                 #creates filter for transform
# warper.SetOutputParameteresFromImage(DFM)       #filter will use a DFM


# im_array = sitk.GetArrayFromImage(DFM)          #convert DFM to numpy array

# save('DFM.npy', im_array)                       #save array

## --- END OF COMMENTED OUT SECTION --- ##

data = load('DFM.npy')                          #load array

# get dimensions of DFM
x = np.arange(data.shape[0])
y = np.arange(data.shape[1])
z = np.arange(data.shape[2])

# create meshgrid and get vector directions for transverse view
X0 , Y0 = np.meshgrid(z,y)
U0 = (data)[int(data.shape[0]/2), :, :,2]
V0 = (data)[int(data.shape[0]/2), :, :,1]

n = 32  #choose downsampling for quiver plots

plt.figure()
plt.quiver(X0[::n,::n],Y0[::n,::n],U0[::n,::n],V0[::n,::n])
ax = plt.gca()   
plt.title("(d)")  
ax.set_ylabel("Slices")
ax.set_xlabel("Slices")
plt.show()

# create meshgrid and get vector directions for frontal view
X1 , Y1 = np.meshgrid(z,x)
U1 = (data)[:, int(data.shape[1]/2), :,2]
V1 = (data)[:, int(data.shape[1]/2), :,0]

plt.figure()
plt.quiver(X1[::n,::n],Y1[::n,::n],U1[::n,::n],V1[::n,::n])
ax = plt.gca() 
ax.set_ylabel("Slices")
ax.set_xlabel("Slices")
plt.title("(e)")                                            
plt.show()

# create meshgrid and get vector directions for sagittal view
X2 , Y2 = np.meshgrid(y,x)
U2 = (data)[:, :, int(data.shape[2]/2), 1]
V2 = (data)[:, :, int(data.shape[2]/2), 0]

plt.figure()
plt.quiver(X2[::n,::n],Y2[::n,::n],U2[::n,::n],V2[::n,::n])
ax = plt.gca()  
ax.set_ylabel("Slices")
ax.set_xlabel("Slices")
plt.title("(f)")                                           
plt.show()

#load alpha3D and convert to numpy array
alpha3D = getAlpha3D()
im2 = sitk.GetArrayFromImage(alpha3D)

#calculate magnitude of deformations and convert to mm
mag = np.sqrt( np.square(data[:,:,:,0])+np.square(data[:,:,:,1])+np.square(data[:,:,:,2]) )
mag = 0.5*mag

# display DFM magnitude and add alpha3D shadow
displayMag(mag,im2,"") 
















