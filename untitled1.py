import numpy as np
import SimpleITK as sitk

from alpha3D import getAlpha3D

## ========================================================================== ##
## ====================== Plot Non-rigid Registration ======================= ##
## ========================================================================== ##

#### Grid parameters

file = "/home/sebastian/.config/spyder-py3/TransformParameters.0.txt"

#Extract data from parameter map
with open (file , 'rt') as pm:                  #opens parameter file for reading
    for ln in pm:                               #reads each line to a string
        
        if "GridOrigin" in ln:                                  #gets line with origin data
            origin = ln.split("GridOrigin",1)[1]                #cuts string to only numbers
            origin = origin.split(")",1)[0]
            start = np.array(origin.split(), dtype=np.float)   #saves data as an array type float
            
        if "GridSize" in ln:                                    #gets line with size data
            size = ln.split("GridSize",1)[1]
            size = size.split(")",1)[0]
            n_el = np.array(size.split(), dtype=np.int)

        if "GridSpacing" in ln:
            spacing = ln.split("GridSpacing",1)[1]               #gets line with spacing data
            spacing = spacing.split(")",1)[0]
            spacing = np.array(spacing.split(), dtype=np.float).astype(int)#saved as int to prevent error
            spacing = spacing*2                                  #why?
            
        if "(TransformParameters" in ln:                         #gets line with control pt def data
            df = ln.split("(TransformParameters",1)[1]
            df = df.split(")",1)[0]
            deformations = np.array(df.split(), dtype=np.float)
                



deformations = deformations.reshape(3, int(deformations.shape[0]/3))
U = deformations[0,:].reshape(n_el[0], n_el[1], n_el[2])
V = deformations[1,:].reshape(n_el[0], n_el[1], n_el[2])

#### Create deformation grid
X, Y, Z = np.meshgrid(np.linspace(start[0], (n_el[0]*spacing[0])-start[0], int(n_el[0])),
                      np.linspace(start[1], (n_el[1] * spacing[1]) - start[1], int(n_el[1])),
                      np.linspace(start[2], (n_el[2]*spacing[2])-start[2], int(n_el[2])))

#### Create image grid

alpha3D = getAlpha3D()

alpha3D_image_array = sitk.GetArrayFromImage(alpha3D)
X_im, Y_im, Z_im = np.meshgrid(np.linspace(0, alpha3D_image_array.shape[0]-1, alpha3D_image_array.shape[0]),
                               np.linspace(0, alpha3D_image_array.shape[1]-1, alpha3D_image_array.shape[1]),
                               np.linspace(0, alpha3D_image_array.shape[2]-1, alpha3D_image_array.shape[2]))

#### Plot image with arrow overlay
im_array_a = sitk.GetArrayFromImage(FFDIm)
slice_id = int(im_array_a.shape[2]/(2*spacing[0]))
plt.figure()
plt.imshow((im_array_a)[slice_id*int(spacing[0]/2),:,:])
X, Y =np.meshgrid(np.linspace(start[1], (n_el[1]*spacing[1])-start[1], int(n_el[1])),
                  np.linspace(start[2], (n_el[2]*spacing[2])-start[2], int(n_el[2])))
X = X.reshape(X.size)
Y = Y.reshape(Y.size)
plt.quiver(X, Y, U[slice_id,:,:], V[slice_id,:,:])

plt.figure()
plt.imshow((im_array_a)[:,slice_id*int(spacing[0]/2),:])
X, Y =np.meshgrid(np.linspace(start[0], (n_el[0]*spacing[0])-start[0], int(n_el[0])),
                  np.linspace(start[2], (n_el[2]*spacing[2])-start[2], int(n_el[2])))
X = X.reshape(X.size)
Y = Y.reshape(Y.size)
plt.quiver(X, Y, U[:,slice_id,:], V[:,slice_id,:])

plt.figure()
plt.imshow((im_array_a)[:,:,slice_id*int(spacing[0]/2)])
X, Y =np.meshgrid(np.linspace(start[0], (n_el[0]*spacing[0])-start[0], int(n_el[0])),
                  np.linspace(start[1], (n_el[1]*spacing[1])-start[1], int(n_el[1])))
X = X.reshape(X.size)
Y = Y.reshape(Y.size)
plt.quiver(X, Y, U[:,:,slice_id], V[:,:,slice_id])