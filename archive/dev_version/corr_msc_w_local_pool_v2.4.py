import numpy as np
import pandas as pd
import scipy.stats as stats
import corr_helper
import multiprocessing as mp 
from functools import partial

global subj, func, vts, vtn, count

def inner(v0):
    global pool, subj, func, vts, count
    
    print("Creating empty dataframe...")

    vtdf = corr_helper.gen_corrdf(vts)
    
    print("Running inner loop...")

    initializedcorr = partial(stats.pearsonr, x=v0)
    res = pool.map(initializedcorr, vts)

    vtdf.iloc[:,0] = res[:,0]
    vtdf.iloc[:,1] = res[:,1]
    count += 1
    print("Saving file...\n")
    vtdf.to_csv("./correlations/msc0"+str(subj)+"_sess0"+str(func)+"_L_corrdf_"+str(count)+".csv")

def outer(vlst):
    global pool
    print("Running outer loop...")
    pool.starmap_async(inner, zip(vlst))


if __name__ == '__main__':
    
    global pool, subj, func, vts, vtn, count

    pool = mp.Pool(mp.cpu_count() - 1)

    for subj in range(6,9):
        for func in range(1,3):
            
            print("Now running subject %s, session %s" % (str(subj), str(func)))

            cname = "./msc0"+str(subj)+"_sess0"+str(func)+"_L_dts.csv"
            voxmat, idxlist = corr_helper.get_voxt_mat(cname)
            count = 0

            vts, vtn = corr_helper.gen_voxt_seg(voxmat,idxlist)
            vts = vts[:2] # Keeps things simple; delete after debugging

            print("Initializing pool...")

            result = pool.starmap_async(outer, zip(vts))
            result.get()
            
    p.close()

(complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool_v2.4.py
Now running subject 6, session 1
Initializing pool...
Running outer loop...
Running outer loop...
multiprocessing.pool.RemoteTraceback:
"""
Traceback (most recent call last):
  File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 125, in worker
    result = (True, func(*args, **kwds))
  File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 51, in starmapstar
    return list(itertools.starmap(args[0], args[1]))
  File "C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis\corr_msc_w_local_pool_v2.4.py", line 31, in outer
    pool.starmap_async(inner, zip(vlst))
NameError: name 'pool' is not defined
"""

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis\corr_msc_w_local_pool_v2.4.py", line 55, in <module>
    result.get()
  File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 774, in get
    raise self._value
NameError: name 'pool' is not defined