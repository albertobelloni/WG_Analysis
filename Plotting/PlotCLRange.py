#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
plt.style.use("seaborn-bright")

def process_combine_file(fname) :

    ofile = open( fname, 'r' )

    results = defaultdict(list)

    cllabeldict= { "Expected 50.0%": "exp0",
                   "Expected  2.5%": "exp-2",
                   "Expected 16.0%": "exp-1",
                   "Expected 84.0%": "exp+1",
                   "Expected 97.5%": "exp+2",
                   "Observed Limit": "obs"    }

    for line in ofile :
        rvalue=-1
        if line.count(':') == 1 and ("Expected" in line or "Observed" in line):
            clname, rvstr = line.split(':')
            rvalue = float(rvstr.rstrip('\n').split('<')[1])
            results[cllabeldict[clname]].append(rvalue)

    if results.get("obs") == None or results.get("exp-2") == None:
        print "No observed or expected value"
        print fname

    ofile.close()

    return results


def make_CL_hist(resultfile, savepath):
    results = process_combine_file(resultfile)
    if  len(results)==0:
        return

    fig = plt.figure()
    mincl = np.floor(min([ x for k, v in results.iteritems() for x in v]))
    maxcl = np.ceil(max([ x for k, v in results.iteritems() for x in v]))

    for k, v in results.iteritems():
        plt.hist(v, bins=np.linspace(mincl,maxcl,100), label=k, histtype="step")
    plt.legend()
    plt.savefig("%s.pdf" %savepath)
    plt.savefig("%s.png" %savepath)
    #plt.show()
    plt.close()

#resultfile = "data/higgs//Width5/all/Mass600/results_mt_res_M600_W5_all_range200-1000.txt"
#savepath ="/home/kakw//public_html/hist_CLRange_M600_W5_all_range200-1000"
#make_CL_hist(resultfile,savepath)

for mass in [300,350,400,450,600,700,800,900,1000,1200,1400,1600,1800,2000]:
    for w in ["5","0p01"]:
        for ch in ["all","el2016","el2017","el2018","mu2016","mu2017","mu2018"]:

            resultfile = "data/higgs/Width%s/%s/Mass%i/results_mt_res_M%i_W%s_%s.txt" %(w,ch,mass,mass,w,ch)
            #savepath ="/home/kakw/public_html/plots/hcombplots/CLHist/CLhist_M%i_W%s_%s" %(mass,w,ch)
            savepath ="/home/kakw/public_html/plots/hcombplots/CLHist/CLhist_M%i_W%s_%s_constrained_dijet_toys" %(mass,w,ch)
            make_CL_hist(resultfile,savepath)

