library(tidyverse)
library(caret)
library(readr)
library(ggplot2)
library(foreach)
library(parallel)
library(ciftiTools)
ciftiTools.setOption('wb_path', './bin_windows64/wb_command.exe')
library(R.matlab)

get_subj <- function(sn, fn){
  # get voxel time series
  subj <- ciftiTools::read_cifti(paste0("../data/surface_pipeline/sub-MSC0",sn,
                                        "/processed_task_timecourses/ses-func0",fn,
                                        "/sub-MSC0",sn,"_ses-func0",fn,
                                        "_task-memory_bold_32k_fsLR.dtseries.nii"))
  
}

get_parcel_verts <- function(parcels, labeln){
  # get RU_KONG parcellations
  # parcels: mat file with labels
  # labeln: target label number
  # p: set of vertices in parcel
  which(parcels$lh.labels==labeln)
}

get_left_cortex_vertices <- function(subj){
  which(subj$meta$cortex$medial_wall_mask$left==TRUE)
}

make_matrix <- function(rois){
  # voxmat <- matrix(data=0, ncol=dim(rois)[1], nrow=dim(rois)[1])
  iteration <- dim(rois)[1]
  vmat <- foreach(vtsx=1:iteration, .combine=cbind
  ) %:% 
    foreach(vtsy=1:iteration
    ) %dopar% {
      as.numeric(cov(rois[vtsx,], rois[vtsy,], method="pearson"))#voxmat[vtsx,vtsy] <- 
    }
  vapply(vmat, FUN=unlist, FUN.VALUE=0.00)
  
}

n.cores <- parallel::detectCores() - 2
#create the cluster
clustmsc <- parallel::makeCluster(
  n.cores, 
  type = "PSOCK"
)

doParallel::registerDoParallel(cl = clustmsc)


for (sn in c(6,8)){
  ind_parc <- R.matlab::readMat(paste0("./5_sess/beta50/Ind_parcellation_MSHBM_sub",
                                       sn-5,"_w20_MRF20_beta50.mat"))
  for (fn in c(1,2)){
    subj <- get_subj(sn, fn)
    
    cortL_vertices <- get_left_cortex_vertices(subj)
    
    parc_rois <- c(125, 36, 187, 198, 199, 190, 201)

    parc_names <- c("p125", "p36", "p187", "p198", "p190", "p199", "p201")

    roi_voxls <- list()
    for (i in 1:length(parc_rois)){
      roi <- get_parcel_verts(ind_parc, parc_rois[i])

      current <- foreach(j = 1:32492
                         ) %dopar% {
                           if (j %in% roi){
                             if (j %in% cortL_vertices){
                               j
                             }
                           }
                         }
      roi_voxls[[parc_names[i]]] <- current
    }
    # names(roi_voxls) <- parc_names
    
    for (k in 1:length(parc_names)){
      # we'll get rid of nulls...
      roi_voxls[[parc_names[k]]][sapply(roi_voxls[[parc_names[k]]], is.null)] <- NULL
      roiv_ts <- subj$data$cortex_left[unlist(roi_voxls[[parc_names[k]]]),]
      
      if (length(roiv_ts) > 0){
      # create a csv file for further analysis...
        ts <- seq(from=0,by=2.2,length.out=dim(roiv_ts)[2])
        colnames(roiv_ts) <- paste("time_step", ts,"s", sep="_")
        write.csv(x = roiv_ts, file = paste0("msc0", sn,
                                             "_sess0", fn,
                                             "_ind_parc_", 
                                             parc_names[k],".csv"))
        
        # now we make a matrix and get covariances between all voxels
        # in the parcel
        voxmat <- matrix(make_matrix(roiv_ts), 
                         nrow=dim(roiv_ts)[1],
                         ncol=dim(roiv_ts)[1],
                         byrow=F)
        
        # create heatmaps and save them!
        col<- colorRampPalette(c("pink", "darkgreen"))(256)
        heatmap(voxmat, col=col)
        ggsave(paste0("msc0", sn, "_sess0", fn, "_ind_parc_", 
                      parc_names[k],"_cov.jpg"), 
               device="jpeg", width=3000, units="px", dpi=300)
      }
    }
    # one-to-one index mapping for voxels and vertices
    
  }
}

parallel::stopCluster(cl = clustmsc)
