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

    # vtdf = corr_helper.gen_corrdf(vts)
    
    # print("Running inner loop...", flush=True)

    # initializedcorr = partial(stats.pearsonr, x=v0)
    # res = pool.map(initializedcorr, vts)

    # vtdf.iloc[:,0] = res[:,0]
    # vtdf.iloc[:,1] = res[:,1]
    # count += 1
    # print("Saving file...\n")
    # vtdf.to_csv("./correlations/msc0"+str(subj)+"_sess0"+str(func)+"_L_corrdf_"+str(count)+".csv")

def outer(vlst):
    global pool
    print("Running outer loop...", flush=True)
    pool.map_async(inner, (vlst,))
    print("Called inner loop...", flush=True)


if __name__ == '__main__':
    
    global subj, func, vts, vtn, count

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

            p.apply_async(outer, (vts,))
            
    p.close()

# if main=starmap & 0uter=apply_async:
# (complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool_v2.7.py
# Initializing pool...
# Now running subject 6, session 1
# multiprocessing.pool.RemoteTraceback:
# """
# Traceback (most recent call last):
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 125, in worker
#     result = (True, func(*args, **kwds))
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 51, in starmapstar
#     return list(itertools.starmap(args[0], args[1]))
# TypeError: outer() takes 1 positional argument but 2 were given
# """

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis\corr_msc_w_local_pool_v2.7.py", line 61, in <module>
#     p.starmap(outer, (vts,))
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 375, in starmap
#     return self._map_async(func, iterable, starmapstar, chunksize).get()
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 774, in get
#     raise self._value
# TypeError: outer() takes 1 positional argument but 2 were given
####################################################################
# if main=map & 0uter=apply_async:
# (complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool_v2.7.py
# Initializing pool...
# Now running subject 6, session 1
# Running outer loop...
# multiprocessing.pool.RemoteTraceback:
# """
# Traceback (most recent call last):
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 125, in worker
#     result = (True, func(*args, **kwds))
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 48, in mapstar
#     return list(map(*args))
#   File "C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis\corr_msc_w_local_pool_v2.7.py", line 35, in outer
#     pool.apply_async(inner, (vlst,))
# NameError: name 'pool' is not defined
# """

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis\corr_msc_w_local_pool_v2.7.py", line 61, in <module>
#     p.map(outer, (vts,))
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 367, in map
#     return self._map_async(func, iterable, mapstar, chunksize).get()
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 774, in get
#     raise self._value
# NameError: name 'pool' is not defined
#################################################################
# if main=appy & 0uter=apply_async:
# (complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool_v2.7.py
# Initializing pool...
# Now running subject 6, session 1
# Running outer loop...
# multiprocessing.pool.RemoteTraceback:
# """
# Traceback (most recent call last):
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 125, in worker
#     result = (True, func(*args, **kwds))
#   File "C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis\corr_msc_w_local_pool_v2.7.py", line 35, in outer
#     pool.apply_async(inner, (vlst,))
# NameError: name 'pool' is not defined
# """

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis\corr_msc_w_local_pool_v2.7.py", line 61, in <module>
#     p.apply(outer, (vts,))
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 360, in apply
#     return self.apply_async(func, args, kwds).get()
#   File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 774, in get
#     raise self._value
# NameError: name 'pool' is not defined
###########################################################
# if main=apply_async & 0uter=apply_async:
# (complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool_v2.7.py
# Initializing pool...
# Now running subject 6, session 1
# Now running subject 6, session 2
# Running outer loop...
# Now running subject 7, session 1
# Running outer loop...
# Now running subject 7, session 2
# Running outer loop...
# Now running subject 8, session 1
# Running outer loop...
# Now running subject 8, session 2
# Running outer loop...
##########################################################
# if main=apply_async & 0uter=apply:
# (complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool_v2.7.py
# Initializing pool...
# Now running subject 6, session 1
# Now running subject 6, session 2
# Running outer loop...
# Now running subject 7, session 1
# Running outer loop...
# Now running subject 7, session 2
# Running outer loop...
# Now running subject 8, session 1
# Running outer loop...
# Now running subject 8, session 2
# Running outer loop...
##########################################################
# if main=apply_async & 0uter=map:
# (complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool_v2.7.py
# Initializing pool...
# Now running subject 6, session 1
# Now running subject 6, session 2
# Running outer loop...
# Now running subject 7, session 1
# Running outer loop...
# Now running subject 7, session 2
# Running outer loop...
# Now running subject 8, session 1
# Running outer loop...
# Now running subject 8, session 2
# Running outer loop...
##########################################################
# if main=apply_async & 0uter=map_async:
# (complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool_v2.7.py
# Initializing pool...
# Now running subject 6, session 1
# Now running subject 6, session 2
# Running outer loop...
# Now running subject 7, session 1
# Running outer loop...
# Now running subject 7, session 2
# Running outer loop...
# Now running subject 8, session 1
# Running outer loop...
# Now running subject 8, session 2
# Running outer loop...
##########################################################
