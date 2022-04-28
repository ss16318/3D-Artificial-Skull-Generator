##CREATE DEFORMATION MATRIX

import os
import numpy as np

def createMatrix():
    
    path = '/home/sebastian/.config/spyder-py3/Parameters3'
    
    files = os.listdir(path)  #lists files in directory
    numIms = len(files)                                                  #counts files in list
    
    for x in range(numIms):                   #loops through each parameter file
    
        name = path+'/'+files[x]
        #Extract data from parameter map
        with open (name , 'rt') as pm:                  #opens parameter file for reading
            for ln in pm:                               #reads each line to a string
                
                    
                if "(TransformParameters" in ln:                         #gets line with control pt def data
                    df = ln.split("(TransformParameters",1)[1]
                    df = df.split(")",1)[0]
                    deformations = np.array(df.split(), dtype=np.float)
                    
        #row = np.concatenate((origin,size,spacing,deformations))   #combines transform data into 1D array
        
        if x ==0:
            defMatrix = np.zeros((numIms,len(deformations)))    #in the first loop the matrix must be instantiated
        
        defMatrix[x,:] = deformations                          #sticks each 1D array of data into row of defMatrix
    
    print("Deformation Created")
    
    return defMatrix

