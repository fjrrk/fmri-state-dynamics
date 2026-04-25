import numpy as np
import pandas as pd
import scipy.stats as stats
import corr_helper

if __name__ == '__main__':
    
    for subj in range(6,9):
        for func in range(1,3):
            
            print("Now running subject %s, session %s" % (str(subj), str(func)), flush=True)

            cname = "./msc0"+str(subj)+"_sess0"+str(func)+"_L_dts.csv"
            voxmat, idxlist = corr_helper.get_voxt_mat(cname)

            vts, vtn = corr_helper.gen_voxt_seg(voxmat,idxlist)
            count = 0
            
            for tsA in vts:
                print("Creating empty dataframe...", flush=True)
                vtdf = corr_helper.gen_corrdf(vtn)

                for i, tsB in enumerate(vts):
                    r, p = stats.pearsonr(tsA, tsB)
                    f = True if (r>0.7) & (p<0.001) else False
                    vtdf.loc[vtn[i], 'r_value'] = r
                    vtdf.loc[vtn[i], 'p_value'] = p
                    vtdf.loc[vtn[i], 'flag'] = f
                    
                vtdf.to_csv("./correlations/msc0"+str(subj)+"_sess0"+str(func)+"_L_corrdf_"+str(count)+"_"+str(i)+".csv")
                count += 1

