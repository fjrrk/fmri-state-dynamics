The files in this directory contain figures (in 
"figs") and data (in "data") generated through the R, 
RMD, and ipynb files contained here. The "workbench" 
directory contains files for the Windows-compatible 
version of HCP's Workbench. All other directories are 
to be ignored.

ROI voxel selection was achieved using R, hence the R 
files seen here. They are all associated with the 
RProject file "analysis." The Rmd file more or less 
follows my thought process and various attempts that 
were either later abandoned or successfully followed
through with. The R scripts contain standalone code 
that accomplish specific tasks. All of this R code 
requires the ./data/relevant_CIFTI files to be dumped 
into this folder (i.e., "./") to run.

The ipython notebooks of interest are the 
"...network_building" files, which require the 
contents of ./data/pickles to run. Unfortunately, I 
did not pay attention to file organization when 
writing, testing, and running my code. The data files 
have been moved to the data directory to organize the 
mess of files that originally described this 
directory, but beware that the code will search for 
required files in "./" and not in "./data/pickles/" or 
in "./data/relevant_CIFTI/" unless their contents are 
dumped here. 

The other ipython notebooks (e.g., Final_Sweep) were 
used to generate the files the "...network_building" 
notebooks use. They can safely be ignored.