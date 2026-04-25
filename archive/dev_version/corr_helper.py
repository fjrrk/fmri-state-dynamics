import numpy as np
import pandas as pd

def get_voxt_mat(filen):
	"""
	Takes in a file name and returns an
	ndarray and a list of indices for every
	10 time steps.
	"""
	voxmat = np.genfromtxt(filen, delimiter=",", dtype=float)
	if np.isnan(voxmat[0,0]):
		voxmat = voxmat[1:,:]
	idlst = [*range(0, voxmat.shape[1], 10)]
	return voxmat, idlst

def gen_voxt_seg(vmat, idxs):
	"""
	Takes in a voxel x time matrix and
	list of times at which a new time
	segment begins. Returns a list of 
	time segments for all voxels and
	their names
	"""
	vxt_list = []
	vxt_names = []
	for i in range(1,vmat.shape[0]):
	    for j in range(len(idxs)-2):
	        vxt_list.append(vmat[i,idxs[j]:idxs[j+1]])
	        vxt_names.append("voxel_"+str(i)+"_timestep_"+str(idxs[j])+"_to_"+str(idxs[j+1]))
	return vxt_list, vxt_names

def gen_corrdf(row_names):
	"""
	Takes in a list of row names and
	creates a dataframe with 
	columns: r-value, p-value, flag
	and indices: row_names
	"""
	dummy = {
				'r_value':np.zeros(len(row_names)),
				'p_value':np.zeros(len(row_names)),
				'flag':np.zeros(len(row_names))
			}
	df = pd.DataFrame(dummy, index=row_names)

	return df

