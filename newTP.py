#Reconstructs parameter map with PCA values

import shutil

def newTP(X):
    
    #converts array to string
    X.T                                          #transpose col to row
    ls = X.tolist()                              #converts array to list     
    
    #paths to files (original acts as a template for target)
    original = r'/home/sebastian/.config/spyder-py3/Parameters2/tp10.txt'
    target = r'/home/sebastian/.config/spyder-py3/reconstruction.txt'
    
    #creates a new paramter file (target is the reconstruction tm)
    shutil.copyfile(original,target)   #copies original data and saves in target
    
    file = open(target, "r")         #opens file to read
    lines = file.readlines()         #reads and copies content line by line
    file.close()                     #closes file
    
    new_file = open(target, "w")     #opens file to write new lines
    
    for ln in lines:                 #loops through each line

        if "(TransformParameters" in ln:                        #gets line with control pt def data
            conVal = ' '.join(str(e) for e in ls)      
            new_ln4 = '(TransformParameters ' + conVal + ')\n'
            new_file.write(new_ln4)
            
        else:
            new_file.write(ln)      #otherwise keep line unchanged
    
    new_file.close()            
    
    return