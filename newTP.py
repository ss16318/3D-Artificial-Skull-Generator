#Reconstructs parameter map with PCA values

import shutil

def newTP(X):
    
    #converts array to string
    X.T                                          #transpose col to row
    ls = X.tolist()                              #converts array to list     
    
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
        
    
        # if "GridOrigin" in ln:                                  #gets line with origin data
        #     origin = ls[0:3]                                    #takes first 3 elements
        #     orgVal = ' '.join(str(e) for e in origin)           #converts list to string
        #     new_ln1 = '(GridOrigin ' + orgVal + ')\n'
        #     new_file.write(new_ln1)
            
        # if "GridSize" in ln:                                    #gets line with size data
        #     size = ls[3:6]                                    
        #     szVal = ' '.join(str(e) for e in size)           
        #     new_ln2 = '(GridSize ' + szVal + ')\n'
        #     new_file.write(new_ln2)

        # if "GridSpacing" in ln:                                 #gets line with spacing data
        #     spacing = ls[6:9]                                    
        #     spVal = ' '.join(str(e) for e in spacing)           
        #     new_ln3 = '(GridSpacing ' + spVal + ')\n'
        #     new_file.write(new_ln3)

        if "(TransformParameters" in ln:                        #gets line with control pt def data
            control = ls[9:]                                         
            conVal = ' '.join(str(e) for e in control)      
            new_ln4 = '(TransformParameters ' + conVal + ')\n'
            new_file.write(new_ln4)
            
        else:
            new_file.write(ln)      #otherwise keep line unchanged
    
    new_file.close()            
    
    return