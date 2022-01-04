# FUNCTION RESAMPLES IMAGE IN DEFINED DIMENSIONS USING TARGET SPACING, 
# BSPLINE INTERPOLATION AND FILLING IN NEW VALUES AT -10000 

import numpy as np
import SimpleITK as sitk

# Resample
def resample(image, dimension, target_spacing, default_value = -1000.0):

    resamp_image = sitk.GetImageFromArray(np.ones((500,500,500)))      # Create the output image space
    resamp_image.SetSpacing(target_spacing)                            # set spacing of points
    resamp_image.SetDirection(image.GetDirection())                    # set direction of image and resamp to match

    actual_spacing = np.array(image.GetSpacing())                      # finds spacing of image
    scaleTransform = sitk.ScaleTransform(dimension)                    # creates correct sized variable (2D or 3D)
    scaleTransform.SetScale(target_spacing/actual_spacing)             # sets correct scaling for each dimension

    interpolator = sitk.sitkBSpline                                    # Use the BSpline interpolator
    return sitk.Resample(image, resamp_image, scaleTransform, interpolator, default_value)
