import numpy as np
import pandas as pd
import scipy.stats as stats
import corr_helper
import multiprocessing as mp 
from functools import partial

global subj, func, vts, vtn, count, cpu_n

cpu_n = (mp.cpu_count() - 1)//3

def inner(v0):
    global pool, subj, func, vts, count
    
    print("Creating empty dataframe...", flush=True)

    vtdf = corr_helper.gen_corrdf(vts)
    
    print("Running inner loop...", flush=True)

    initializedcorr = partial(stats.pearsonr, x=v0)
    res = pool.map(initializedcorr, vts)

    vtdf.iloc[:,0] = res[:,0]
    vtdf.iloc[:,1] = res[:,1]
    count += 1
    print("Saving file...\n")
    vtdf.to_csv("./correlations/msc0"+str(subj)+"_sess0"+str(func)+"_L_corrdf_"+str(count)+".csv")

def outer(vlst):
    pool = mp.Pool(cpu_n)
    print("Running outer loop...", flush=True)
    pool.map_async(inner, (vlst,))
    print("Called inner loop...", flush=True)
    pool.close()


def main():
    
    global subj, func, vts, vtn, count

    print("Initializing pool...", flush=True)

    # create a pool object with initializer
    cpu_n = (mp.cpu_count() - 1)//3

    for subj in range(6,9):
        for func in range(1,3):
            
            print("Now running subject %s, session %s" % (str(subj), str(func)), flush=True)

            cname = "./msc0"+str(subj)+"_sess0"+str(func)+"_L_dts.csv"
            voxmat, idxlist = corr_helper.get_voxt_mat(cname)
            count = 0

            vts, vtn = corr_helper.gen_voxt_seg(voxmat,idxlist)
            vts = vts[:2] # Keeps things simple; delete after debugging

            p = mp.Pool(cpu_n)
            p.apply_async(outer, (vts,))
            
            p.close()

if __name__ == '__main__':
    
    global subj, func, vts, vtn, count
    main()