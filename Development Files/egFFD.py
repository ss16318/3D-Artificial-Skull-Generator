import SimpleITK as sitk
import os
import numpy as np
from itertools import count
import matplotlib.pyplot as plt

PATH = 'C:/Users/oscar/PycharmProjects/head_encoding/'

# Load image
reader = sitk.ImageFileReader()
reader.SetFileName(os.path.join(PATH, 'rsna-dataset/examples/', 'frame256.jpg'))
im = reader.Execute()
im_array = sitk.GetArrayFromImage(im).astype(np.float64)
im = sitk.GetImageFromArray(im_array[:, :, 0])

# Output image container
shape = im.GetSize()
im_out = sitk.Image(shape[0], shape[1], sitk.sitkFloat64)
im.CopyInformation(im_out)

# Displacement grids
X1 = np.linspace(1, shape[0], shape[0])-1
X2 = np.linspace(1, shape[1], shape[1])-1
X1X1, X2X2 = np.meshgrid(X1, X2)
X1X1 = X1X1.reshape(shape[0]*shape[1])
X2X2 = X2X2.reshape(shape[0]*shape[1])

# Displacements
direction = np.zeros((shape[0]*shape[1], 2))
for X1, X2, n in zip(X1X1, X2X2, count(0)):
    direction[n] = (-100, 100)  # Uniform displacement transform (x-axis -ve right, y-axis +ve up)
    # direction[n] = (X1, X2) if X1 < X2 else (0, 0)  # Distortion transform
direction = direction.reshape(shape[1], shape[0], 2).transpose(0, 1, 2)
field = sitk.GetImageFromArray(direction, isVector=True)  # Setup the displacement field

# Transform
transform_ffd = sitk.DisplacementFieldTransform(field)
im_out = sitk.Resample(im,
                       im_out,
                       transform_ffd, sitk.sitkLinear, -10.)
# To correct the non-uniform spacing, I can resample in the opposite direction of the spacing error using a FFD field.
# I should check this on the worst spacing error examples.

plt.figure()
plt.imshow(direction[:, :, 0])
plt.figure()
plt.imshow(direction[:, :, 1])
plt.figure()
plt.imshow(sitk.GetArrayFromImage(im_out))
plt.show()

print()