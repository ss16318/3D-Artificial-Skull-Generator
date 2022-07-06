# 3D Artificial Skull Generator

For my final year masters project at Imperial College London, I worked with a group that is trying to make brain imaging using ultrasound possible. 
Unfortunately, the skull causes complex ultrasound wave interactions, making image resolution a challenging task. Therefore, I built a generative model
of the human skull that can improve starting model selection (initial estimates) for the wave inversion algorithm and guide convergence of the algorithm 
through explicit regularization. The type of generative model I chose to build is called a statistical deformation model (SDM) as it is farily intuitive to interpret,
can be trained automatically and does not require a large dataset for training.



[SDM Report.pdf](https://github.com/ss16318/3D-Artificial-Skull-Generator/files/9054549/SDM.Report.pdf)
