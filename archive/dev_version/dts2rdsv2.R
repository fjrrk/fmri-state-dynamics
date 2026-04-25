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

time_lagger <- function(sdts, vxl){
  
  v <- sdts[vxl,]
  d <- length(v)
  expd <- d-(d%%10)
  vmat <- matrix(0,10,(expd^2)+expd)
  
  for (j in seq(d-9)){
    vmat[,j] <- v[j:(j+9)]
  }
  
  return(vmat)
}

for (sid in 1:5){
  subj <- ciftiTools::read_cifti(paste0("../data/surface_pipeline/sub-MSC0",
                                        sid,
                                        "/task_timecourses/ses-func01/sub-MSC0",
                                        sid,
                                        "_ses-func01_task-memory_bold_32k_fsLR.dtseries.nii"))
  subjL <- subj$data$cortex_left
  subjR <- subj$data$cortex_right
  
  subj.diff <- matrix(0,dim(subjL)[1], 
                      dim(subjL)[2]-1)
  
  for (i in seq(dim(subjL)[2]-1)){
    subj.diff[,i] = subjL[,i] - subjL[,i+1]
  }

  
  voxels <- seq(dim(subjL)[1]) %>% as.list()
  
  dt <- partial(time_lagger, sdts=subj.diff)
  
  lt <- partial(time_lagger, sdts=subjL)
  
  diff.mat <- sapply(voxels, lt)
  saveRDS(diff.mat, file = paste0("msc0",sid,"_mat_Ldiff1.rds"))
  
  subj.Lmat <- sapply(voxels, lt)
  saveRDS(subj.Lmat, file = paste0("msc0",sid,"_mat_left.rds"))
  
  ####################################################
  voxels <- seq(dim(subjR)[1]) %>% as.list()

  for (i in seq(dim(subjR)[2]-1)){
    subj.diff[,i] = subjR[,i] - subjR[,i+1]
  }
  
  dt <- partial(time_lagger, sdts=subj.diff)
  
  lt <- partial(time_lagger, sdts=subjR)
  
  diff.mat <- sapply(voxels, dt)
  saveRDS(diff.mat, file = paste0("msc0",sid,"_mat_Rdiff1.rds"))
  
  subj.Rmat <- sapply(voxels, lt)
  saveRDS(subj.Rmat, file = paste0("msc0",sid,"_mat_right.rds"))
}