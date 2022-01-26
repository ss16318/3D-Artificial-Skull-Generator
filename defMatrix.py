##CREATE DEFORMATION MATRIX

import os
import numpy as np

def createMatrix():
    
    files = os.listdir('/home/sebastian/.config/spyder-py3/Parameters')  #lists files in directory
    numIms = len(files)                                                  #counts files in list
    
    for x in range(numIms):                   #loops through each parameter file
        
        file = "/home/sebastian/.config/spyder-py3/Parameters/tp" + str(x) + ".txt"  #finds path to each parameter file
    
        #Extract data from parameter map
        with open (file , 'rt') as pm:                  #opens parameter file for reading
            for ln in pm:                               #reads each line to a string
                
                if "GridOrigin" in ln:                                  #gets line with origin data
                    origin = ln.split("GridOrigin",1)[1]                #cuts string to only numbers
                    origin = origin.split(")",1)[0]
                    origin = np.array(origin.split(), dtype=np.float)   #saves data as an array type float
                    
                if "GridSize" in ln:                                    #gets line with size data
                    size = ln.split("GridSize",1)[1]
                    size = size.split(")",1)[0]
                    size = np.array(size.split(), dtype=np.int)
        
                if "GridSpacing" in ln:
                    spacing = ln.split("GridSpacing",1)[1]               #gets line with spacing data
                    spacing = spacing.split(")",1)[0]
                    spacing = np.array(spacing.split(), dtype=np.float).astype(int)#saved as int to prevent error
                    #spacing = spacing*2                                  #why?
                    
                if "(TransformParameters" in ln:                         #gets line with control pt def data
                    df = ln.split("(TransformParameters",1)[1]
                    df = df.split(")",1)[0]
                    deformations = np.array(df.split(), dtype=np.float)
                    
        row = np.concatenate((origin,size,spacing,deformations))   #combines transform data into 1D array
        
        if x ==0:
            defMatrix = np.zeros((numIms,len(row)))    #in the first loop the matrix must be instantiated
            
        defMatrix[x,:] = row                           #sticks each 1D array of data into row of defMatrix
    
    print("Deformation Created")
    
    return defMatrix

