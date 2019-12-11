#!/usr/bin/env python
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import json
import re
import numpy as np
import os
import uuid
import math
import random
import pickle
#import selection_defs as defs
from array import array
from pprint import pprint
from uncertainties import ufloat
from collections import defaultdict
from FitManager import FitManager
from DrawConfig import DrawConfig
from SampleManager import SampleManager
from argparse import ArgumentParser

parser = ArgumentParser()
#parser.add_argument('--baseDirMuG',      default=None,           dest='baseDirMuG',         required=False, help='Path to muon base directory')
parser.add_argument('--baseDirElG',      default=None,           dest='baseDirElG',         required=False, help='Path to electron base directory')
parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')
parser.add_argument('--step',           default=None,           dest='step',                type=int,        help='select fitting procedures')
parser.add_argument('--batch',           default=False,     action='store_true',      dest='batch',               help='submit batch jobs')
parser.add_argument('--binlow',           default=None,           dest='binlow',               help='lower bin')
parser.add_argument('--binhigh',          default=None,           dest='binhigh',              help='upper bin')
parser.add_argument('--region',          default=None,           dest='region',              help='control/ signal regions')
parser.add_argument('--data',           default=False,      action='store_true',         dest='data',          required=False, help='Use data or MC')
options = parser.parse_args()
ROOT.TVirtualFitter.SetMaxIterations( 100000 )
ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)


_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon16.py'
_LUMI     = 36000
_BASEPATH = '/home/jkunkle/usercode/Plotting/LimitSetting/'
_SAMPCONF = 'Modules/Resonance2016_efake.py'


ROOT.gStyle.SetPalette(ROOT.kBird) 
ROOT.gROOT.SetBatch(True)
if options.outputDir is None :
    options.outputDir = "Plots/" + __file__.rstrip(".py")
if options.outputDir is not None :
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

base = 'ph_n==1 && el_n==1'
baseeta = base + ' && ph_IsEB[0]'# + "&& ph_pt[0]>80"
passpix = '&& ph_hasPixSeed[0]==0'  #Pixel seed
failpix = '&& ph_hasPixSeed[0]==1'
ltmet = '&&met_pt<40'
gtmet = '&&met_pt>40'
phpt50 = "&&ph_pt[0]>50"
UNBLIND = "ph_hasPixSeed[0]==1 || met_pt<40"
phtight = "&& ph_passTight[0]"
phmedium = "&& ph_passMedium[0]"
elpt40 = "&&el_pt[0]>40"
eleta2p1 = "&&abs(el_eta[0])<2.1"
#weight = "PUWeight*NLOWeight"
weight = "NLOWeight"


fitrange = {0   :((40,195),(70,150)),
            -1  :((40,195),(75,170)),
            30  :((40,195),(70,170)),
            40  :((40,195),(70,170)),
            50  :((40,195),(70,170)),
            60  :((40,195),(75,170)),
            70  :((40,195),(75,170)),
            80  :((40,195),(75,170)),
            100 :((40,195),(75,150)),
            150 :((40,195),(75,150)),
            }
fitrange1 = {-1 :((45,180),),    ## -1 default
              0 :((65,170),),
              #30:((45,180),),
              #40:((45,180),),
              50:((55,180),),
              60:((55,180),),
              80:((55,195),),
            }
fitrange2 = {-1 :((60,170),),    ## -1 default
              0 : ((75,170),),
             30 : ((75,170),),
              }
fitrange3 = {-1 :((70,140),),}    ## -1 default; for two gaussians
fitrange4 = {-1 :((70,170),)*5,     ## -1 default; for expo bkgd
            #  0 :((75,180),),
            # 30 :((80,180),),
             }
fitrange5 = {-1 :((70,100),),    ## -1 default; for zgamma fits
              0 :((50,95),),
             30 :((70,95),),
             }
parmrange = { "dcb_mass"  :(85,97),
              "dcb_sigma" :(0 ,5 ),
              "dcb_alpha1":(0 ,5) ,
              "dcb_power1":(0 ,110),
              "dcb_alpha2":(0 ,5) ,
              "dcb_power2":(0 ,10)}

def main() :

    if options.batch:
        ptbins = [0,30,40,50,60,80,1000]
        #ptbins = np.linspace(0,3.1416*4,37)
        regions = 'aABCD'
        regions = 'AB'
        if options.data: regions = 'ABD'
        with open('condor_template.jdl','r') as file1:
            filedata = file1.read()
        i=0
        for r in regions:
          for binlow,binhigh in zip(ptbins[0:-1],ptbins[1:]):
            pyoption = '%i %g %g %s' %(options.step,binlow,binhigh,r)
            if options.data: pyoption+=" --data"
            filedatawrite= filedata.replace('[REPLACE]',pyoption)
            writefilename = 'log/condor%i.jdl' %i
            with open(writefilename,'w') as file:
                file.write(filedatawrite)
            condor_command = 'condor_submit %s' %writefilename
            os.system(condor_command)
            i+=1
        return

    if options.baseDirElG ==None:
        options.baseDirElG = "/data/users/kakw/Resonances/LepGamma_elg_newblind_2018_09_23_beta/"
        options.baseDirElG = "/data2/users/kakw/Resonances2016/LepGamma_elg_2019_10_28"

    sampManElG= SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElG.ReadSamples( _SAMPCONF )
    #sel_base_el = 'ph_n>=1 && el_n==1 &&!( ph_eta[0]<0&&ph_phi[0]>2.3&&ph_phi[0]<2.7)&&!(ph_phi[0]>1.2&&ph_phi[0]<1.5) '
    #sampManElG.deactivate_all_samples()
    #sampManElG.activate_sample(["Z+jets"])
    #sampManElG.get_samples(name="DYJetsToLL_M-50")[0].scale=1.

    #f1 = ROOT.TFile("%s/output.root"%(options.outputDir),"RECREATE")
#    elefake            = ROOT.RooWorkspace( 'elefake' )
    if options.step == 1:
       sampManElG.deactivate_all_samples()
       #sampManElG.activate_sample(["Z+jets","Zgamma"])
       sampManElG.activate_sample(["Z+jets"])
       sampManElG.get_samples(name="DYJetsToLL_M-50")[0].scale=1.
       #ptbins = np.linspace(0,3.1416*4)
       ptbins = [0,30,40,50,60,80,2000]
       #ptbins = [0,80,2000]
       if options.binlow:
           ptbins = [float(options.binlow), float(options.binhigh)]
       #sampManElG.closure( samp, sel_base_el,'EB', plot_var = 'm_lep_ph',varbins=[20,30,40,50,70,90,110,150,160], mode=1)
       #fitting(sampManElG,(50,80))
       #makevariableplots(sampManElG,[0,0.7,1.0,1.479,3],fitrange,basesel=base+"&&ph_pt[0]>80", tag="etaptgt80",var="abs(ph_sc_eta[0])")
       #makevariableplots(sampManElG,[0,0.7,1.0,1.479,3],fitrange,basesel=base+"&&ph_pt[0]<=80",tag="etaptlt80",var="abs(ph_sc_eta[0])")
       #makevariableplots(sampManElG,ptbins,fitrange,basesel=base+phmedium,tag="phi",var="(ph_phi[0]+3.1416+(ph_eta[0]>0)*3.1416*2)")
       makevariableplots(sampManElG,ptbins,fitrange,basesel=baseeta+phmedium,tag="all")
       #makevariableplots(sampManElG,[0,30,40,50,60,80,1000],fitrange,basesel=baseeta+passpix+ltmet,tag="regA")
       #makevariableplots(sampManElG,[0,30,40,50,60,80,1000],fitrange,basesel=baseeta+failpix+ltmet,tag="regB")
       #makevariableplots(sampManElG,[0,30,40,50,60,80,1000],fitrange,basesel=baseeta+passpix+gtmet,tag="regS")
       #makevariableplots(sampManElG,[0,30,40,50,60,80,1000],fitrange,basesel=baseeta+failpix+gtmet,tag="regD")
    elif options.step == 11:
       sampManElG.deactivate_all_samples()
       sampManElG.activate_sample(["Zgamma"])
       sampManElG.get_samples(name="ZGTo2LG")[0].scale=1.
       makevariableplots_simultaneous_zg(sampManElG,[0,30,40,50,60,80,1000],fitrange5,
               basesel=baseeta+phmedium,tag="zgamma",ic = dict(bkgd="gauszg",ext='simulzg'),dobkgd=False,donorm=False)
    elif options.step == 2:
       print "STEP 2 SIMULTANEOUS FIT"
       bkgd=["expo","gaus"]
       if options.data: doData, tbase = True, "_data"
       else: doData,tbase=False,""
       ic = dict(bkgd=["expo","gaus"],sig="dcbp2",bkgd2="gauszg2",ext="simul2")

       binvar = "ph_pt[0]"
       ptbins = [0,30,40,50,60,80,2000]
       #ptbins = [80,1000]
       ## flattened phi for both forward and backward detector. 10 degree in each bin
       #ptbins = np.linspace(0,3.1416*4,72)
       #binvar = "(ph_phi[0]+3.1416+(ph_eta[0]>0)*3.1416*2)"

       ## batch options
       if options.binlow:
           ptbins = [float(options.binlow), float(options.binhigh)]
           tbase+=options.binlow.replace('.',"p")
       if options.region: 
           doregions = options.region
       else:
           doregions = 'ABCDa'
       print 'DOregions: %s bins %f %f' %(doregions,ptbins[0],ptbins[1])
       #makevariableplots_simultaneous(sampManElG,[0,30,40,50,60,80,1000],fitrange1,basesel=baseeta,tag="all")
       #makevariableplots_simultaneous(sampManElG,[0,30,40,50,60,80,1000],fitrange2,
       #        basesel=baseeta,tag="all",ic = dict(bkgd="gaus"),maxtimes=20)
       if 'A' in doregions: makevariableplots_simultaneous(sampManElG,ptbins,fitrange4,
               basesel=baseeta+passpix+ltmet+phmedium,tag="regA"+tbase,ic = ic,maxtimes=50,doData=doData, var=binvar)
       if 'B' in doregions: makevariableplots_simultaneous(sampManElG,ptbins,fitrange4,
               basesel=baseeta+failpix+ltmet+phmedium,tag="regB"+tbase,ic = ic,maxtimes=50,doData=doData, var=binvar)
       if 'D' in doregions: makevariableplots_simultaneous(sampManElG,ptbins,fitrange4,
               basesel=baseeta+failpix+gtmet+phmedium,tag="regD"+tbase,ic = ic ,maxtimes=50,doData=doData, var=binvar)
       if not doData:
           if 'a' in doregions: makevariableplots_simultaneous(sampManElG,ptbins,fitrange4,
               basesel=baseeta              ,tag="all",ic = ic,maxtimes=50, var= binvar)
           if 'C' in doregions or 'S' in doregions:
             makevariableplots_simultaneous(sampManElG,ptbins,fitrange4,
               basesel=baseeta+passpix+gtmet+phmedium,tag="regS",ic = ic,maxtimes=50, var=binvar)
    return

def get_param(filename, ptlist=None):
    js = json.loads(open(filename).read())
    print ptlist, js['ptlist']
    #assert ptlist==js['ptlist']
    parm = js['parm']
    print "imported parmameters: "; pprint(parm)
    return parm

def makevariableplots_simultaneous_zg(samp,ptlist,fitrange,basesel="1",tag="",ic = None, dobkgd=True, donorm=False, maxtimes=5, doData=False):
    """ extended pdf fit for zgamma peak """
    if ic is None: ic = dict(sig="dcbp",bkgd="gaus", ext="simul")
    if "icparm" not in ic: ic["icparm"] = dict()
    parmufloats, parmvals, parmerrs = defaultdict(list),defaultdict(list),defaultdict(list)
    parmnames = FitManager.ParamDCB
    #parmnames2 = ["gauszg_mean","gauszg_sig"]
    #parm ,parm2= get_param("data/dcbparms.txt",ptlist), get_param("data/zgparms.txt",ptlist)
    parm = get_param("data/dcbparms_all.txt",ptlist)
    fm = FitManager("dcbexpo", xvardata = (0,200,"GeV"))
    iconddcb = {pt:[(n,parm[n][ipt]) for n in parmnames] for ipt,pt in enumerate(ptlist[:-1])}
    #icondgzg = {pt:[(n,parm2[n][ipt]) for n in parmnames2] for ipt,pt in enumerate(ptlist[:-1])}
    print "iconddcb"; pprint (iconddcb)
    #print "icondgzg"; pprint (icondgzg)
    for ptrange in zip(ptlist[:-1],ptlist[1:]):
        ptrange = tuple(ptrange)
        #xp.append(ptrange)
        ic['icparm']['dcbp'] = [("x",20,200)]+iconddcb[ptrange[0]] # FIXME: move up a fx level
        #ic['icparm']['gauszg'] = [("x",20,200)]+icondgzg[ptrange[0]] # FIXME: move up a fx level
        ### fitting step
        ptfitrange = fitrange.get(ptrange[0],fitrange[-1]) # get default if entry doesnt exist
        values, stackcount = fitting_simultaneous(samp, fm, ptrange, ptfitrange, basesel=basesel,
                tag=tag, ic = ic, xbins=(200,0,200), dobkgd =dobkgd, maxtimes = maxtimes, doData=doData, donorm=donorm)
        if donorm: make_normalization_comparison(fm,values,stackcount,ptrange,tag)
        for name,val in values.items():
            if val is None: #for case of non-initiated variable
                parmvals[name].append(-1)
                parmerrs[name].append(-1) 
            elif val.s>0: #check if the value is fitted
                parmvals[name].append(val.n) #value
                parmerrs[name].append(val.s) #uncertainty
            parmufloats[name].append(val)
    # dealing with width of overflow/last bin
    #xpoints, xerrs = xp.output()
    print "values:"; pprint(parmufloats.items())
    f = lambda p: {x:y for x,y in p.iteritems()}
    data = {'ptlist':ptlist,'parm':f(parmvals),'error':f(parmerrs)}
    with open('data/parms_%s.txt' %tag,'w') as outfile:
        json.dump(data,outfile)

def makevariableplots_simultaneous(samp,ptlist,fitrange,basesel="1",tag="",ic = None, dobkgd=True, donorm=True, maxtimes=5, doData=False, var = "ph_pt[0]"):
    """ extended pdf fit """
    if ic is None: ic = dict(sig="dcbp",bkgd="gaus", ext="simul")
    if "icparm" not in ic: ic["icparm"] = dict()
    parmufloats, parmvals, parmerrs = defaultdict(list),defaultdict(list),defaultdict(list)
    parmnames = FitManager.ParamDCB
    parmnames2 = ["gauszg_mean","gauszg_sig"]
    parm ,parm2= get_param("data/dcbparms_all.txt",ptlist), get_param("data/parms_zgamma.txt",ptlist)
    parmptlist = json.loads(open("data/dcbparms_all.txt").read())['ptlist']
    parm2ptlist = json.loads(open("data/parms_zgamma.txt").read())['ptlist']
    fm = FitManager("dcbexpo", xvardata = (0,200,"GeV"))

    ## FIXME: need better ways to obtain fitted parameters
    iconddcb = {pt:[(n,parm[n][parmptlist.index(pt)]  ) for n in parmnames]  for pt in ptlist[:-1]}
    icondgzg = {pt:[(n,parm2[n][parm2ptlist.index(pt)]) for n in parmnames2] for pt in ptlist[:-1]}
    #ieighty = parmptlist.index(80) # search for pt80 parameter
    #iconddcb = {pt:[(n,parm[n][ieighty]) for n in parmnames] for ipt,pt in enumerate(ptlist[:-1])}
    #icondgzg = {pt:[(n,parm2[n][ieighty]) for n in parmnames2] for ipt,pt in enumerate(ptlist[:-1])}
    print "iconddcb"; pprint (iconddcb)
    print "icondgzg"; pprint (icondgzg)
    for ptrange in zip(ptlist[:-1],ptlist[1:]):
        ptrange = tuple(ptrange)
        ptname = tuple(map(lambda x: str(x).replace('.','p'), ptrange))
        #xp.append(ptrange)
        ic['icparm']['dcbp'] = [("x",20,200)]+iconddcb[ptrange[0]] # FIXME: move up a fx level
        ic['icparm']['gauszg'] = [("x",20,200)]+icondgzg[ptrange[0]] # FIXME: move up a fx level
        ### fitting step
        ptfitrange = fitrange.get(ptrange[0],fitrange[-1]) # get default if entry doesnt exist
        values, stackcount = fitting_simultaneous(samp, fm, ptrange, ptfitrange, basesel=basesel, var = var,
                tag=tag, ic = ic, xbins=(200,0,200), dobkgd =dobkgd, maxtimes = maxtimes, doData=doData, donorm=donorm)
        if donorm: make_normalization_comparison(fm,values,stackcount,ptname,tag)
        for name,val in values.items():
            if val is None: #for case of non-initiated variable
                parmvals[name].append(-1)
                parmerrs[name].append(-1) 
            elif val.s>0: #check if the value is fitted
                parmvals[name].append(val.n) #value
                parmerrs[name].append(val.s) #uncertainty
            parmufloats[name].append(val)
    # dealing with width of overflow/last bin
    #xpoints, xerrs = xp.output()
    print "values:"; pprint(parmufloats.items())
    f = lambda p: {x:y for x,y in p.iteritems()}
    data = {'ptlist':ptlist,'parm':f(parmvals),'error':f(parmerrs)}
    with open('data/parms_%s.txt' %tag,'w') as outfile:
        json.dump(data,outfile)

def fitting_simultaneous(samples,fm, ptrange,fitranges=((50,180)),var="ph_pt[0]",
                        basesel = "1",tag="", ic = None,
                        maxtimes =5, xbins  =(200,0,200), dobkgd=True, doData = False, donorm=False):
    """ Simulatnous fit of signal and background distribution """
    """ icond : input initial condition or choose the preset """
    if ic is None: ic = dict(iconddcb = None, sig = "dcbp", bkgd = "gaus", ext = 'simul')

    ## replace decimal point with p
    ptname = tuple(map(lambda x: str(x).replace('.','p'), ptrange))

    if dobkgd:
        samples.deactivate_sample(["Z+jets"])
        samples.Draw("m_lep_ph","%s&&%s>%g&&%s<%g" %(basesel,var,ptrange[0],var,ptrange[1]),
                xbins, { "weight": weight ,"logy":1,"ymin":10,'ymax':1e6})
        h1 = samples.get_samples(name='__AllStack__')[0].hist.Clone()
        fm.addhist(h1,"bkgdhist_pt_%s_%s" %ptname,bkgd = "nonefake")
        samples.activate_sample(["Z+jets"])

    if doData:
        samples.Draw("m_lep_ph","%s&&%s>%g&&%s<%g" %(basesel,var,ptrange[0],var,ptrange[1]),
                xbins, { "weight": weight ,"logy":1,"ymin":10,'ymax':1e6, "unblind":UNBLIND, "doratio":True, "rmax":3})
        samples.SaveStack("thstack_mlepph_data_%s_%s_"%ptname+tag+".pdf" ,outputDir = options.outputDir, canname ="base")
        samples.SaveStack("thstack_mlepph_data_%s_%s_"%ptname+tag+".png" ,outputDir = options.outputDir, canname ="base")
        if not dobkgd:
            h0 = samples.get_samples(name='__AllStack__')[0].hist.Clone()
            fm.addhist(h0,"mchist_pt_%s_%s" %ptname, bkgd="allmc")
        h1 = samples.get_samples(name='SingleElectron')[0].hist.Clone()

    else:
        samples.Draw("m_lep_ph","%s&&%s>%g&&%s<%g" %(basesel,var,ptrange[0],var,ptrange[1]),
                xbins, { "weight": weight ,"logy":1,"ymin":10,'ymax':1e6})
        samples.SaveStack("thstack_mlepph_%s_%s_"%ptname+tag+".pdf" ,outputDir = options.outputDir, canname ="top")
        samples.SaveStack("thstack_mlepph_%s_%s_"%ptname+tag+".png" ,outputDir = options.outputDir, canname ="top")
        h1 = samples.get_samples(name='__AllStack__')[0].hist.Clone()
        #regulate(h1,10)
    fm.addhist(h1,"datahist_pt_%s_%s" %ptname)

    ###NOTE NOTE fitting step
    samples.print_stack_count(fitranges[-1])
    stackcount = samples.get_stack_count(fitranges[-1])
    f = lambda x,y: (x,round(y[0]),0,round(y[0]*4))
    if donorm: ic['icparm']['simul2']  = [ f("Nsig", stackcount["Z+jets"]),
                                f("Nbkg", stackcount["NonEleFake"]),
                                f("Nzg" , stackcount["OtherEleFakeBackground"]),
    #ic['icparm']['simul2']  = [ ("Nsig",stackcount["Z+jets"][0],                  0,  stackcount["Z+jets"][0]*4,),
    #                 ("Nbkg" , stackcount["NonEleFake"][0],                 0,  stackcount["NonEleFake"][0]*4 ),
    #                 ("Nzg", stackcount["OtherEleFakeBackground"][0],     0,  stackcount["OtherEleFakeBackground"][0]*4 ),
                     #("Nzg" , stackcount["NonEleFake"][0]*random.normalvariate(1,0.1),                 0,  stackcount["NonEleFake"][0]*4 ),
                   ]
    #### NOTE NOTE fitting step
    corefitting_simultaneous(fm, ptrange,fitranges,
        tag=tag,ic = ic, maxtimes =maxtimes)
    c=fm.draw(" ",(1,1e6),logy=1,paramlayout=(0.55,0.9,0.82),subplot="pull", component=True)
    #c=fm.draw(" ",logy=0,paramlayout=(0.55,0.9,0.82),subplot="pull", component=True)
    c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_" %ptname + tag+ ".pdf")
    c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_" %ptname + tag+ ".png")

    #samples.curr_canvases["top"].cd()
    #fm.func_pdf.asTF(ROOT.RooArgList(fm.xvardata)).Draw("L same")
    #samples.SaveStack("thstack_postfit_mlepph_%s_%s.pdf" %ptrange,
    #                    outputDir = "temp/", canname ="top")
    c = fm.get_correlations()
    c.SaveAs(options.outputDir+"/simult_correlations_%s_%s_" %ptname+tag+".pdf")
    c.SaveAs(options.outputDir+"/simult_correlations_%s_%s_" %ptname+tag+".png")

    values = fm.get_parameter_values()
    print "VALUES"
    pprint(values)
    print "STACKCOUNT"
    pprint(stackcount)
    return values, stackcount

def corefitting_simultaneous(fm, ptrange,fitranges=((50,180)),
            tag="", ic=None, maxtimes =5):
    """ 
        Helper function of fitting_simultaneous
        Provide Core Fitting functionality
        Hard-coded retries and break out of loops using return
    """
    bestchi = 1000000
    chi=200
    ptname = tuple(map(lambda x: str(x).replace('.','p'), ptrange))
    for itry in range(maxtimes):
        print "*** TRIAL %i ***" %itry
        print
        ##### setup fit manager #####
        # replace lists in ic with alteratives at each try
        iclocal = {key:item[itry%len(item)] if isinstance(item, list) else item for key,item in ic.iteritems()}
        if chi >5 or fm.func_pdf is None: froo_dcb = fm.setup_fit(**iclocal) # pass down initial condition settings
        c=fm.draw(" ",(1,1e6),logy=1,paramlayout=(0.55,0.9,.82), component = True)
        c.SaveAs(options.outputDir+"/simult_prefit_mlepph_%s_%s_" %ptname + tag+ ".pdf")
        c.SaveAs(options.outputDir+"/simult_prefit_mlepph_%s_%s_" %ptname + tag+ ".png")
        chi = fm.getchisquare()
        print "\nCHI ORIGINAL: ", chi
        for fr in fitranges:
            fr = tuple(round(x+random.normalvariate(0,5)) for x in fr)
            print fr
            fr = (max(50,min(90,fr[0])), max(100,min(195,fr[1])))
            print fr


            print "NOW FITTING mass range %g to %g" %fr + " for pT bin of %g,%g" %ptrange
            froo_dcb = fm.run_fit(fr)
            print "FINISH fitting range %g to %g"%fr + " for pT bin of %g,%g" %ptrange
            fm.fitresult.Print()
            fm.frame.Print()
            ## draw result
            c=fm.draw(" ",(1,1e6),logy=1,paramlayout=(0.55,0.9,0.82),subplot="pull", component=True)
            c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_try%s%s.pdf" %(ptname +(itry, tag)) )
            c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_try%s%s.png" %(ptname +(itry, tag)) )
            chi = fm.getchisquare()
            print "\nCHI: ", chi
            if chi<itry or (itry>maxtimes/2 and chi<bestchi*1.5):
                print "\n *** FINISH TRIALS AT %i-TH TRY W/ CHI2 OF %g *** \n" %(itry, chi)
                return 
            bestchi = min(bestchi,chi)
            print "\nbestchi: ",bestchi

def make_normalization_comparison(fm,values,stackcount,ptrange,tag):
    ## make normalization comparison plot
    fm.create_standard_ratio_canvas("_norm",500,500)
    h1 = ROOT.TH1F("hpt1%s%s"%ptrange, "photon pt %s to %s" %ptrange,4,0,4)
    h2 = ROOT.TH1F("hpt2%s%s"%ptrange, "photon pt %s to %s" %ptrange,4,0,4)
    h1x,h2x = h1.GetXaxis(), h2.GetXaxis(); i=1
    for name in ["Z+jets", "NonEleFake", "OtherEleFakeBackground"]:
        sethbin(h1,i,stackcount[name]);
        i+=1
    hvalues = [values.get(s) for s in ['Nsig',"Nbkg","Nzg"]]
    for i in range(3):
        sethbin(h2,i+1,hvalues[i])
    sethbin(h2,4,sum([v for v in hvalues if v]))
    h2x.SetBinLabel  (1,"N_{s}/Zee")
    h2x.SetBinLabel  (2,"N_{b}/Non-ee")
    h2x.SetBinLabel  (3,"Z#gamma")
    h2x.SetBinLabel  (4,"Total")
    h2x.SetLabelSize(0.06)
    setlinestyle(h1)
    setlinestyle(h2, color = ROOT.kViolet, width=4)

    minvalue = [s[0] for s in stackcount.values()]+[values['Nsig'].n,values['Nbkg'].n]
    print "MINVALUES: ",minvalue
    minvalue = max(min(minvalue),10)
    print "MINVAL: ",minvalue
    #h2.SetMinimum(0.1*min(map(lambda x:max(1, x.GetMinimum()),[h1,h2]))) #doesnt work
    leg = ROOT.TLegend(0.55,0.7,0.9,0.9)
    leg.AddEntry(h1, "# MC", "PL")
    leg.AddEntry(h2, "Predicted", "PL")
    hratio = h2.Clone()
    hratio.Divide(h1)
    h2.SetMaximum(300*max(map(lambda x: x.GetMaximum(),[h1,h2])))
    h2.SetMinimum(0.1*minvalue)

    #c = ROOT.TCanvas("cparam", "parameters",500,500)
    c=fm.curr_canvases['top_norm']
    c.cd()
    c.SetLogy(1)
    h2.Draw('e ')
    h1.Draw('e same')
    leg.Draw()
    c=fm.curr_canvases['bottom_norm']
    c.cd()
    hratio.Draw()
    hratio.SetTitle(" ")
    xAxs = hratio.GetXaxis()
    yAxs = hratio.GetYaxis()
    xAxs.SetTitleSize(0.085)
    xAxs.SetLabelSize(0.12)
    xAxs.SetTitleOffset(0.9)
    yAxs.SetTitleSize(0.08)
    yAxs.SetLabelSize(0.08)
    yAxs.SetTitleOffset(0.45)
    x=hratio.GetXaxis()
    xlow =  x.GetXmin()
    xhigh = x.GetXmax()
    line = ROOT.TLine(xlow,1,xhigh,1)
    line.SetLineStyle(3)
    line.SetLineWidth(2)
    line.Draw()
    c=fm.curr_canvases['base_norm']
    c.SaveAs(options.outputDir+"/simult_normalizations_%s_%s_" %ptrange+tag+".pdf")
    c.SaveAs(options.outputDir+"/simult_normalizations_%s_%s_" %ptrange+tag+".png")
    return

#{'Nbkg': 406466.1787981999+/-15031.30652819981,
# 'Nsig': 530039.1884532829+/-2054.2875771209915,
# 'expo_c': -0.0411183904328537+/-0.0007961149745417893}
#STACKCOUNT
#[('Z+jets', 492243.7607275421, 1490.374683416905),
# ('NonEleFake', 56203.184975689976, 1414.9426794880515),
# ('OtherEleFakeBackground', 45502.1026592354, 172.70423583752304),
# ('TOTAL', 593949.0483624678, 2062.3060481613993)]


def sethbin(h,i,value):
    if value is None: return
    if isinstance(value,tuple):
        value = ufloat(*value)
    h.SetBinContent(i,value.n)
    h.SetBinError  (i,value.s)


def setlinestyle(t,width=2,color=2):
        """ works with TH1 and TGraph"""
        t.SetLineColor(color)
        t.SetLineWidth(width)

def regulate(h1, scale = 1):
    """  add uncertainty to non-zero bin and remove negative bins """
    for i in range(1,h1.GetNbinsX()+1):
        y=h1.GetBinContent(i)
        ye=h1.GetBinError(i)
        ye_new = math.sqrt(ye*ye+scale*scale)
        if y<0: h1.SetBinContent(i,0)
        if y>0: h1.SetBinError(i,ye_new)
        print i, y, ye, ye_new

def addline(graph,y):
    left_edge  = graph.GetXaxis().GetXmin()
    right_edge = graph.GetXaxis().GetXmax()

    print left_edge, right_edge, y
    oneline = ROOT.TLine(left_edge, y, right_edge, y)
    oneline.SetLineStyle(3)
    oneline.SetLineWidth(2)
    oneline.SetLineColor(ROOT.kRed)
    return oneline

def makevariableplots(samp,ptlist,fitrange,basesel="1",tag="",var="ph_pt[0]"):
    parmnames = FitManager.ParamDCB
    parmvals = {name:[] for name in parmnames}
    parmerrs = {name:[] for name in parmnames}
    parmufloats = {name:[] for name in parmnames}
    xpoints, xerrs = [],[]
    fm = FitManager("dcbp", xvardata = (0,200,"GeV"))
    for ptrange in zip(ptlist[:-1],ptlist[1:]):
        xpoints.append((ptrange[1]+ptrange[0])/2)
        xerrs  .append((ptrange[1]-ptrange[0])/2)
        ### NOTE NOTE fitting step  NOTE NOTE
        parmdict = fitting(samp,fm,ptrange,fitrange.get(ptrange[0],fitrange[-1]),basesel=basesel,tag=tag,var=var)
        for name,val in parmdict.items():
            parmvals[name].append(val.n) #value
            parmerrs[name].append(val.s) #uncertainty
            parmufloats[name].append(val)
    # dealing with width of overflow/last bin
    xpoints[-1] = ptlist[-2] + xerrs[-2]
    xerrs[-1]   = xerrs[-2]
    print "values:"
    pprint(parmufloats)
    print "xpoints: \n", xpoints
    print "xerrors: \n", xerrs
    npt = len(ptlist)-1
    tod = lambda x: array("d",x)
    xpoints = tod(xpoints)
    xerrs   = tod(xerrs  )
    #for i in range(npt):
    parmgraph = {name:ROOT.TGraphErrors(npt,
                    xpoints,tod(parmvals[name]),xerrs,tod(parmerrs[name])) \
                    for name in parmnames}
    c1 = ROOT.TCanvas("c1","",800,500)
    parmlimits  = FitManager.setuparray["dcb"]
    parmlimits  ={n[0]:n[1:] for n in parmlimits}
    for name, tgraph in parmgraph.items():
        tgraph.SetTitle(name)
        tgraph.GetXaxis().SetTitle("pt")
        tgraph.GetYaxis().SetTitle(name)
        yplot   = parmrange[name]
        tgraph.SetMaximum(yplot[1])
        tgraph.SetMinimum(yplot[0])
        setlinestyle(tgraph)
        tgraph.Draw('AC*')
        ylimit = parmlimits[name]
        if len(ylimit)==3:
            if (ylimit[2]<yplot[1]): 
                hline = addline(tgraph,ylimit[2])
                hline.Draw()
                print name," ", ylimit[2]
            if (ylimit[1]>yplot[0]): 
                lline = addline(tgraph,ylimit[1])
                lline.Draw()
                print name," ", ylimit[1]
        c1.SaveAs(options.outputDir+"/tge_dcb_%s_%s.pdf" %(name,tag))
        c1.SaveAs(options.outputDir+"/tge_dcb_%s_%s.png" %(name,tag))
    data = {'ptlist':ptlist,'parm':parmvals,'error':parmerrs}
    with open('data/temp/dcbparms_%s.txt' %tag,'w') as outfile:
        json.dump(data,outfile)

def fitting(samples,fm, ptrange,fitranges=((50,180)),var="ph_pt[0]",basesel = "1",tag=""):
    froo_dcb = fm.setup_fit((50,195))
    samples.Draw("m_lep_ph","%s&&%s>%g&&%s<%g" %(basesel,var,ptrange[0],var,ptrange[1]),
    #samples.Draw("m_lep_ph",baseeta+"&&ph_pt[0]>%g&&ph_pt[0]<%g" %ptrange,
                     (200,0,200), { "weight": weight })
    h1 = samples.get_samples(name='__AllStack__')[0].hist.Clone()
    #regulate(h1)
    #h1.Scale(1./h1.Integral())
    ptrange = tuple(map(lambda x: str(x).replace('.','p'), ptrange))
    fm.addhist(h1,"datahist_pt_%s_%s" %ptrange)
    # setup fit manager
    c=fm.draw(" ",(1,1e6),logy=1,paramlayout=(0.55,0.9,.82))
    c.SaveAs(options.outputDir+"/prefit_mlepph_%s_%s_" %ptrange + tag+ ".pdf")
    c.SaveAs(options.outputDir+"/prefit_mlepph_%s_%s_" %ptrange + tag+ ".png")
    for fr in fitranges:
        print "NOW FITTING mass range %g to %g" %fr
        froo_dcb = fm.run_fit(fr)
        fm.fitresult.Print()
    fm.fitresult.Print()
    c=fm.draw(" ",(1,1e6),logy=1,paramlayout=(0.55,0.9,0.82),subplot="pull")
    c.SaveAs(options.outputDir+"/postfit_mlepph_%s_%s_" %ptrange + tag+ ".pdf")
    c.SaveAs(options.outputDir+"/postfit_mlepph_%s_%s_" %ptrange + tag+ ".png")
    c = fm.get_correlations()
    c.SaveAs(options.outputDir+"/correlations_%s_%s_" %ptrange+tag+".pdf")
    c.SaveAs(options.outputDir+"/correlations_%s_%s_" %ptrange+tag+".png")
    values = fm.get_parameter_values()
    return values

class Xpoints:
    def __init__(self):
        self.xpoints, self.xerrs = [],[]

    def append(self,ptrange):
        self.xpoints.append((ptrange[1]+ptrange[0])/2)
        self.xerrs  .append((ptrange[1]-ptrange[0])/2)

    def output(self):
        if len(xerrs)>1:
            self.xpoints[-1] = xpoints[-2] + 2*xerrs[-2]
            self.xerrs[-1]   = xerrs[-2]
        return self.xpoints, self.xerrs

main()

    
