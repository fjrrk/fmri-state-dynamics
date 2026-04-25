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
    pool.starmap(inner, zip(vlst,[pool]*len(vlst)))

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
            vts = vts[:2] # delete after debugging

            print("Initializing pool...")
            pool.starmap(outer, zip(vts,[pool]*len(vts)))
    pool.close() # I took this out of the for loops because I don't want pool to close right after the first iteration


(complexity) PS C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis> python .\corr_msc_w_local_pool_v2.1.py
Now running subject 6, session 1
Initializing pool...
Traceback (most recent call last):
  File "C:\Users\Mango\Documents\Complexity\Midterm_Project\analysis\corr_msc_w_local_pool_v2.1.py", line 45, in <module>
    pool.starmap(outer, zip(vts,[pool]*len(vts)))
  File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 375, in starmap
    return self._map_async(func, iterable, starmapstar, chunksize).get()
  File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 774, in get
    raise self._value
  File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 540, in _handle_tasks
    put(task)
  File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\connection.py", line 206, in send
    self._send_bytes(_ForkingPickler.dumps(obj))
  File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\reduction.py", line 51, in dumps
    cls(buf, protocol).dump(obj)
  File "C:\Users\Mango\anaconda3\envs\complexity\lib\multiprocessing\pool.py", line 643, in __reduce__
    raise NotImplementedError(
NotImplementedError: pool objects cannot be passed between processes or pickled