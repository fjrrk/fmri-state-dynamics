# install.packages("tidyverse")
# install.packages("caret")
# install.packages("readr")
# install.packages("ggplot2")

library(tidyverse)
library(caret)
library(readr)
library(ggplot2)
library(ciftiTools)

ciftiTools.setOption('wb_path', './wb/wb_command.exe')

for (sid in 1:5){
  msc1 <- ciftiTools::read_cifti(paste0("../data/surface_pipeline/sub-MSC0",
                                        sid,
                                        "/task_timecourses/ses-func01/sub-MSC0",
                                        sid,
                                        "_ses-func01_task-memory_bold_32k_fsLR.dtseries.nii"))
  
  msc1.diff <- matrix(0,dim(msc1$data$cortex_left)[1], 
                      dim(msc1$data$cortex_left)[2]-1)
  
  for (i in seq(dim(msc1$data$cortex_left)[2]-1)){
    msc1.diff[,i] = msc1$data$cortex_left[,i] - msc1$data$cortex_left[,i+1]
  }
  
  time_lagger <- function(vxl){
    d <- length(vxl)
    if (d-9%%10!=0){
      vmat <- matrix(0,10,d-(d%%10))
    }
    else {
      vmat <- matrix(0,10,d)
    }
    
    for (j in seq(d-9)){
      vmat[,j]= vxl[i,j:j+9]
    }
    return(vmat)
  }
  
  voxels <- seq(dim(msc1$data$cortex_left)[1]) %>% as.list()
  
  diff.mat <- sapply(voxels, function(x) sapply(msc1.diff[x,], time_lagger))
  saveRDS(diff.mat, file = paste0("msc0",sid,"_mat_Ldiff1.rds"))
  
  msc1.Lmat <- sapply(voxels, function(x) sapply(msc1$data$cortex_left[x,], time_lagger))
  saveRDS(msc1.Lmat, file = paste0("msc0",sid,"_mat_left.rds"))
  
  ####################################################
  voxels <- seq(dim(msc1$data$cortex_right)[1]) %>% as.list()
  
  for (i in seq(dim(msc1$data$cortex_right)[2]-1)){
    msc1.diff[,i] = msc1$data$cortex_right[,i] - msc1$data$cortex_right[,i+1]
  }
  
  diff.mat <- sapply(voxels, function(x) sapply(msc1.diff[x,], time_lagger))
  saveRDS(diff.mat, file = paste0("msc0",sid,"_mat_Rdiff1.rds"))
  
  msc1.Rmat <- sapply(voxels, function(x) sapply(msc1$data$cortex_right[x,], time_lagger))
  saveRDS(msc1.Rmat, file = paste0("msc0",sid,"_mat_right.rds"))
}