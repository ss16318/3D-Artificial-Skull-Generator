#Reconstructs parameter map with PCA values

import shutil

def newTP(X):
    
    #converts array to string
    X.T                                          #transpose col to row
    ls = X.tolist()                              #converts array to list
    del ls[0:9]                                  #deletes first 8 elements
    strOfval = ' '.join(str(e) for e in ls)      #converts list to string     
    
    #paths to files (original acts as a template for target)
    original = r'/home/sebastian/.config/spyder-py3/Parameters/tp0.txt'
    target = r'/home/sebastian/.config/spyder-py3/reconstruction.txt'
    
    #creates a new paramter file (target is the reconstruction tm)
    shutil.copyfile(original,target)   #copies original data and saves in target
    
    file = open(target, "r")         #opens file to read
    lines = file.readlines()         #reads and copies content line by line
    file.close()                     #closes file
    
    new_file = open(target, "w")     #opens file to write new lines
    
    for ln in lines:                 #loops through each line
        
        #when line of control pt deformations is found change data to eigenvector values
        if "(TransformParameters" in ln:
            new_ln = '(TransformParameters ' + strOfval + ')\n'
            new_file.write(new_ln)
            
        else:
            new_file.write(ln)      #otherwise keep line unchanged
    
    new_file.close()            
    
    return