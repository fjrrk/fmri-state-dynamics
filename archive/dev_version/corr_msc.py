import numpy as np
import pandas as pd
import scipy.stats as stats
import corr_helper
import multiprocessing as mp 
from functools import partial

def outer(vts):
	global pool
	pool.map(inner, vts)

def inner(v0):
	global pool
	vtdf = corr_helper.gen_corrdf(vts)
	initializedcorr = partial(stats.pearsonr, x=v0)
	res = pool.map(initializedcorr, vts)
	vtdf.iloc[:,0] = res[:,0]
	vtdf.iloc[:,1] = res[:,1]
	#vtdf.iloc[:,2] = res[:,2]
	vtdf.to_csv("./msc0"+str(i)+"_sess0"+str(j)+"_L_corrdf_"+str(count)+".csv")


if __name__ == '__main__':
	
	global pool, vts, vtn

	for subj in range(6,9):
		for func in range(1,3):

			cname = "./msc0"+str(subj)+"_sess0"+str(subj)+"_L_dts.csv"
			voxmat, idxlist = corr_helper.get_voxt_mat(cname)

			vts, vtn = corr_helper.gen_voxt_seg(voxmat,idxlist)

			pool = mp.Pool()
			pool.map(outer, vts)
			pool.close()



			



