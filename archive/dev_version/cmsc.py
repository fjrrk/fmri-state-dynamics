import numpy as np
import pandas as pd
import scipy.stats as stats
import corr_helper
import multiprocessing as mp 
from functools import partial

# def core(a,b):
# 	r, p = stats.pearsonr
# 	f = True if (r>0.7) & (p<0.001) else False
# 	return [r, p, f]

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
	pool.map(inner, vlst)


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

			print("Initializing pool...")

#			poola = mp.Pool() 
			pool.map(outer, vts[:5])
	pool.close()



			



