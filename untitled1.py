import SimpleITK as sitk

from alpha3D import getAlpha3D
from display import display

alpha3D = getAlpha3D()


edges = sitk.CannyEdgeDetection(sitk.Cast(alpha3D, sitk.sitkFloat32), lowerThreshold=0.0, 
                                upperThreshold=1500, variance = (5.0,5.0,5.0))

display(edges,'Boundary')