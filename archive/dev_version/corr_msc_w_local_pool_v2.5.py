import numpy as np
import pandas as pd
import scipy.stats as stats
import corr_helper
import multiprocessing as mp
from functools import partial

global subj, func, vts, vtn, count

def inner(v0,pool):
    global subj, func, vts, count

    print("Creating empty dataframe...")
    vtdf = corr_helper.gen_corrdf(vts)

    print("Running inner loop...")
    initializedcorr = partial(stats.pearsonr, x=v0)
    res = pool.map(initializedcorr, vts)
    vtdf.iloc[:,0] = res[:,0]
    vtdf.iloc[:,1] = res[:,1]
    count += 1
    print("Saving file... \n ")
    vtdf.to_csv("./correlations/msc0"+str(subj)+"_sess0"+str(func)+"_L_corrdf_"+str(count)+".csv")

def outer(vlst,pool):
    print("Running outer loop...")
    pool.starmap(inner, zip(vlst,pool))

if __name__ == '__main__':
    global subj, func, vts, vtn, count

    for subj in range(6,9):
        for func in range(1,3):
            print("Now running subject %s, session %s" % (str(subj), str(func)))
            cname = "./msc0"+str(subj)+"_sess0"+str(func)+"_L_dts.csv"
            voxmat, idxlist = corr_helper.get_voxt_mat(cname)
            count = 0
            vts, vtn = corr_helper.gen_voxt_seg(voxmat,idxlist)
            print("Initializing pool...")
            pool = mp.Pool(mp.cpu_count() - 1)
            pool.starmap(outer, zip(vts[:5],pool))
            pool.close()

Now running subject 6, session 1
Initializing pool...
Traceback (most recent call last):
  File "C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis\corr_msc_w_local_pool_v2.5.py", line 41, in <module>
    pool.starmap(outer, zip(vts[:5],pool))
TypeError: 'Pool' object is not iterable