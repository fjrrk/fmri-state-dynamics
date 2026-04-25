import numpy as np
import pandas as pd
import scipy.stats as stats
import corr_helper
import multiprocessing as mp 
from functools import partial

global subj, func, vts, vtn, count

def init_pool(p):
    global pool
    pool = p

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
    global pool
    print("Running outer loop...", flush=True)
    pool.map_async(inner, (vlst,))
    print("Called inner loop...", flush=True)


if __name__ == '__main__':
    
    global subj, func, vts, vtn, count

    # set the start method to 'spawn'
    mp.set_start_method('spawn')

    print("Initializing pool...", flush=True)

    # create a pool object with initializer
    p = mp.Pool(mp.cpu_count() - 1)
    init_pool(p)

    for subj in range(6,9):
        for func in range(1,3):
            
            print("Now running subject %s, session %s" % (str(subj), str(func)), flush=True)

            cname = "./msc0"+str(subj)+"_sess0"+str(func)+"_L_dts.csv"
            voxmat, idxlist = corr_helper.get_voxt_mat(cname)
            count = 0

            vts, vtn = corr_helper.gen_voxt_seg(voxmat,idxlist)
            vts = vts[:2] # Keeps things simple; delete after debugging

            # print("Initializing pool...", flush=True)

            # # create a pool object with initializer
            # p = mp.Pool(mp.cpu_count() - 1)
            # init_pool(p)
            
            # use apply_async without initializer
            p.map_async(outer, (vts,))
            # p.apply_async(outer, args=([(v,) for v in vts],))
            
    p.close()
            # create a pool object with initializer
            # p = mp.Pool(mp.cpu_count() - 1, initializer=init_pool, initargs=(p,))

            # # # create a pool object
            # # p = mp.Pool(mp.cpu_count() - 1)
        
            # # pass the pool object to the init_pool function
            # with p as p:
            #     p.apply_async(outer, args=([(v,) for v in vts],))

            # with p as p:
            #     p.starmap(outer, [(v,) for v in vts], initializer=init_pool, initargs=(p,))
            # with mp.Pool(mp.cpu_count() - 1, initializer=init_pool) as p:
            #     p.starmap(outer, [(v,) for v in vts])



            
# (complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool.py
# Now running subject 6, session 1
# Initializing pool...
# Now running subject 6, session 2
# Running outer loop...
# Initializing pool...
# Now running subject 7, session 1
# Running outer loop...
# Initializing pool...
# Now running subject 7, session 2
# Running outer loop...
# Initializing pool...
# Now running subject 8, session 1
# Running outer loop...
# Initializing pool...
# Now running subject 8, session 2
# Running outer loop...
# Initializing pool...


