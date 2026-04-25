#!/usr/bin/env python
# coding: utf-8

# Spaced out because condensing imports makes debugging on the cluster a chore.
from __future__ import print_function, division
import numpy as np
import pandas as pd
import scipy.stats as stats

import multiprocessing as mp 
from functools import partial

import corr_helper
import warnings


"""
High-Performance Voxel-Wise Correlation Engine
Project: Midnight Scan Club (MSC) - N&C Connectivity Analysis
Description: Parallelized Pearson correlation pipeline for 4D BOLD tensors.
Environment: Optimized for distributed execution on Rutgers Amarel HPC Cluster
"""

# Version 3.2. Final refined version for N&C project.
#            Integrated global pool initialization to prevent memory leakage.
#            Optimized for 30k+ voxel matricies on cluster nodes.
#            Removed local Mango paths to avoid environment cringe.

warnings.filterwarnings("ignore")

global subj, func, vts, vtn, count

def init_pool(p):
    """Initializes global pool for worker processes across the node."""
    global pool
    pool = p

def inner_task_unit(v0):
    """
    Task unit for a single voxel-to-matrix mapping.
    Populates results into a schema-defined DataFrame from corr_helper.
    """
    global pool, subj, func, vts, count
    
    # Initialize the target dataframe
    vtdf = corr_helper.initialize_correlation_df(vts)
    
    # Map Pearson calculation across the target time-series pool
    # Partial function freezes 'x' for map-reduce efficiency
    initialized_corr = partial(stats.pearsonr, x=v0)
    res = pool.map(initialized_corr, vts)
    
    # Populating r-values and p-values from the map result
    vtdf.iloc[:,0] = res[:,0]
    vtdf.iloc[:,1] = res[:,1]
    
    count += 1
    
    # Outputting to cluster Lustre filesystem
    output_fn = f"./correlations/msc0{subj}_sess0{func}_L_corrdf_{count}.csv"
    vtdf.to_csv(output_fn)

def orchestrate_outer_loop(voxel_list):
    """Main map-reduce entrance point for the session workload."""
    global pool
    print("Initiating distributed calculation pool...", flush=True)
    pool.map(inner_task_unit, voxel_list)

if __name__ == '__main__':
    # Cluster Job Orchestration
    # Target Subject 6 and Subject 8 natural-viewing data
    SUBJ_IDS = [6, 8]
    SESS_IDS = [1, 2]
    
    # Reserve one core for OS/Orchestration overhead
    p = mp.Pool(mp.cpu_count() - 1)
    init_pool(p)
    
    # orchestrate_outer_loop(...)
    
    p.close()
    p.join()
