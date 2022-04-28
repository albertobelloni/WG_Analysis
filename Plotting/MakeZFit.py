#!/usr/bin/env python3
#import ROOT
#ROOT.PyConfig.IgnoreCommandLineOptions = True
#ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000 )

def addparser(parser):
    ### FIXME use a parent argparser
    parser.add_argument('--step',    default=None,    type=int,
                                     help='select fitting procedures (1,2,11)')
    parser.add_argument('--binlow',  default=None,
                                     help='lower bin')
    parser.add_argument('--binhigh', default=None,
                                     help='upper bin')
    parser.add_argument('--region',  default=None,
                                     help='control/ signal regions')
    parser.add_argument('--quality', default=None,
                                     help='detector qualty regions')
    parser.add_argument('--condor',  default=False,  action='store_true',
                                     help='submit batch jobs')
    parser.add_argument('--test',    default=False,  action='store_true',
                                     help='flag for temporary test feature')
    parser.add_argument('--cache',   help='READ|WRITE: hist in/to temp file')

exec(compile(open("MakeBase.py", "rb").read(), "MakeBase.py", 'exec'))

import json
import re
import numpy as np
import os
import uuid
import random
import pickle
from array import array
from pprint import pprint
from uncertainties import ufloat
from collections import defaultdict
from FitManager import FitManager

_SAMPCONF = 'Modules/Resonance%i_efake.py' %options.year
ROOT.gStyle.SetPalette(ROOT.kBird)

if options.year == 2016:
    metcorr=1.02
if options.year == 2017:
    metcorr=1.04
if options.year == 2018:
    metcorr=1.04
base = 'ph_n==1 && el_n==1'
baseeta = base + ' && ph_IsEB[0]'# + "&& ph_pt[0]>80"
ltmet = '&&met_pt<40'
gtmet = '&&met_pt>40'
ltmetfail = '&&met_pt*%g<40' %metcorr
gtmetfail = '&&met_pt*%g>40' %metcorr
phpt50 = "&&ph_pt[0]>50"
phmedium = "&& ph_passMedium[0]"
weight = "NLOWeight"


fitrange = {0   :((60,195),(70,150)),
            -1  :((60,195),(75,170)),
            30  :((60,195),(70,170)),
            40  :((60,195),(70,170)),
            50  :((60,195),(70,170)),
            60  :((60,195),(75,170)),
            70  :((60,195),(75,170)),
            80  :((60,165),(75,120)),
            100 :((60,195),(75,150)),
            150 :((60,195),(75,150)),
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
fitrange4 = {-1 :((70,150),)*3,     ## -1 default; for expo bkgd
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



### ---------------------------------------------------------------------------


def main() :

    if options.condor:

        ptbins = [0,30,40,50,60,80,1000]
        ptbins = [40,80,1000]
        #ptbins = np.linspace(0,3.1416*4,37)

        regions = 'aABCD'
        regions = 'ABD'
        if options.data: regions = 'ABD'

        with open('condor_template.jdl','r') as file1:
            filedata = file1.read()

        i=0
        quality = ["normal","badonly","worstonly"]
        if options.year == 2016: quality = ["normal","badonly"]
        for r in regions:
          for q in quality:
            for binlow,binhigh in zip(ptbins[0:-1],ptbins[1:]):

              pyoptionbase = '%i %g %g %s' %(options.step,binlow,binhigh,r)
              pyoption =" --batch"
              pyoption +=" --quality %s" %q

              if options.data: pyoption+=" --data"
              if options.year: pyoption+=" --year %i" %options.year

              pyoption = " '%s'" %pyoption.strip(" ")
              pyoption = '"%s %s"' %(pyoptionbase,pyoption)

              filedatawrite= filedata.replace('[REPLACE]',pyoption)

              writefilename = 'log/condor%i.jdl' %i

              with open(writefilename,'w') as file:
                  file.write(filedatawrite)

              condor_command = 'condor_submit %s' %writefilename
              os.system(condor_command)

              i+=1

        return


    ### for non-condor-batch usage
    sampManElG.ReadSamples( _SAMPCONF )

    if options.step == 1:

       sampManElG.deactivate_all_samples()
       name = "DYJetsToLL_M-50-amcatnloFXFXPhOlap"
       sampManElG.activate_sample([name])
       sampManElG.get_samples(name=name)[0] .scale=1.

       #ptbins = [0,30,40,50,60,80,2000]
       ptbins = [40,80,1000]

       if options.binlow:
           ptbins = [float(options.binlow), float(options.binhigh)]

       makevariableplots(sampManElG,ptbins,fitrange,basesel=baseeta+phmedium,
                          tag="all%i" %options.year)

    elif options.step == 11:

       #### Zg fit

       sampManElG.deactivate_all_samples()
       sampManElG.activate_sample(["Zgamma"])
       sampManElG.get_samples(name="ZGTo2LG")[0].scale=1.

       makevariableplots_simultaneous_zg(sampManElG, [0,30,40,50,60,80,1000],
               fitrange5, basesel = baseeta+phmedium, tag = "zgamma",
               ic = dict(bkgd="gauszg",ext='simulzg'),
               dobkgd=False,donorm=False)

    elif options.step == 2:


       print("STEP 2 MULTIPLE PDF FIT")

       ##  first remove samples with bad scales
       sampManElG["GJets"].groupsampleNames = ['GJets_HT-200To400',
                          'GJets_HT-400To600', 'GJets_HT-600ToInf']

       bkgd=["expo","gaus"]

       if options.data: doData, tbase = True, "_data"
       else: doData,tbase=False,""

       if options.year: tbase+="%i"%options.year

       ic = dict(bkgd=["expo","gaus"],sig="dcbp",ext="simul")
       #ic = dict(bkgd=["expo","gaus"],sig="dcbp",bkgd2="gauszg",ext="simul2")

       badstring = defs.build_bad_efake_sector_string(options.year, options.quality)
       tbase+=options.quality
       add="&&(%s)" %badstring

       base = baseeta
       if options.test: base="Entry$%10==0" ## NOTE for quick test

       binvar = "ph_pt[0]"
       #ptbins = [0,30,40,50,60,80,2000]
       ptbins = [80,1000]

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


       print('DOregions: %s bins %f %f' %(doregions,ptbins[0],ptbins[1]))

       fitconfig = dict( maxtimes=20, doData=doData, ic = ic, var=binvar,
                         useparms = True )

       if 'A' in doregions:
           makevariableplots_simultaneous( sampManElG, ptbins, fitrange4,
                                 basesel=base+passpix+ltmet+phmedium+add,
                                 tag="regA"+tbase,  **fitconfig )

       if 'B' in doregions:
           makevariableplots_simultaneous( sampManElG, ptbins, fitrange4,
                                 basesel=base+failpix+ltmetfail+phmedium+add,
                                 tag="regB"+tbase,  **fitconfig )

       if 'D' in doregions:
           makevariableplots_simultaneous( sampManElG, ptbins, fitrange4,
                                 basesel=base+failpix+gtmetfail+phmedium+add,
                                 tag="regD"+tbase,  **fitconfig )

       if not doData:
           if 'a' in doregions:
               makevariableplots_simultaneous( sampManElG, ptbins, fitrange4,
                  basesel=base ,tag="all",   **fitconfig )

           if 'C' in doregions or 'S' in doregions:
               makevariableplots_simultaneous( sampManElG, ptbins, fitrange4,
                                basesel=base+passpix+gtmet+phmedium,
                                tag="regS",  **fitconfig )
    return




### ---------------------------------------------------------------------------


def get_param(filename):
    js = json.loads(open(filename).read())
    parm = js['parm']
    print("imported parmameters: "); pprint(parm)
    return parm


### ---------------------------------------------------------------------------


def get_ic( parmfn, parmnames, ptlist ):
    parm = get_param(parmfn)
    parmptlist = json.loads( open(parmfn).read() ) ['ptlist']
    return { pt: [(n,parm[n][parmptlist.index(pt)] ) for n in parmnames ] \
                                                    for pt in ptlist[:-1]}


### ---------------------------------------------------------------------------


def makevariableplots_simultaneous( samp, ptlist, fitrange, basesel = "1",
        tag = "", ic = None, dobkgd = True, donorm = True, maxtimes = 5,
        doData = False, var = "ph_pt[0]", useparms = True):
    """ extended pdf fit """

    if ic is None: ic = dict(sig="dcbp",bkgd="gaus", ext="simul")
    if "icparm" not in ic: ic["icparm"] = dict()

    parmufloats = defaultdict(list)
    parmvals, parmerrs = defaultdict(list),defaultdict(list)
    parmnames = FitManager.ParamDCB
    parmnames2 = ["gauszg_mean","gauszg_sig"]

    ## Get Z+jet/ Zg shape from parameter files
    parm2fn = "data/efake/%i/parms_zgamma.txt"%options.year
    icondgzg = get_ic( parm2fn, parmnames2, ptlist )
    print("icondgzg"); pprint (icondgzg)

    parmfn = "data/efake/%i/dcbparms_all%i.txt" %((options.year,)*2)
    iconddcb = get_ic( parmfn, parmnames, ptlist )
    print("iconddcb"); pprint (iconddcb)

    ## set up fit manager
    fm = FitManager("dcbexpo", xvardata = (50,250,"GeV"))

    for ptrange in zip(ptlist[:-1],ptlist[1:]):
        ptrange = tuple(ptrange)
        ptname = tuple([str(x).replace('.','p') for x in ptrange])
        #xp.append(ptrange)
        if useparms:
            ## do some operations here
            icdcbtemp = iconddcb[ptrange[0]]

            for p in ["dcb_sigma","dcb_mass"]:
                re_parm = getparm( FitManager.setuparray["dcbp"], p )
                replaceparm( icdcbtemp, re_parm )
            ic['icparm']['dcbp']   = [("x",50,250)]+icdcbtemp

            ic['icparm']['gauszg'] = [("x",50,250)]+icondgzg[ptrange[0]]

        ### NOTE fitting step
        # get default if entry doesnt exist
        ptfitrange = fitrange.get(ptrange[0],fitrange[-1])
        values, stackcount = fitting_simultaneous(samp, fm, ptrange, ptfitrange,
                              basesel = basesel, var = var, tag = tag, ic = ic,
                              #xbins=(20,50,250),
                              xbins=[50,]+list(range(75,85,5)) + list(range(85,95,1)) + list(range(95,110,5))+list(range(110,250,10)) +[250,],
                              #xbins = range(50, 251, 1),
                              dobkgd = dobkgd,
                              maxtimes = maxtimes,
                              doData = doData,
                              donorm = donorm)

        if donorm: make_normalization_comparison(fm,values,stackcount,ptname,tag)

        for name,val in list(values.items()):
            if val is None: #for case of non-initiated variable
                parmvals[name].append(-1)
                parmerrs[name].append(-1)
            elif val.s>0: #check if the value is fitted
                parmvals[name].append(val.n) #value
                parmerrs[name].append(val.s) #uncertainty
            parmufloats[name].append(val)

    # dealing with width of overflow/last bin
    #xpoints, xerrs = xp.output()
    print("values:"); pprint(list(parmufloats.items()))
    f = lambda p: {x:y for x,y in p.items()}

    ## output values in json file
    data = {'ptlist':ptlist,'parm':f(parmvals),'error':f(parmerrs)}
    with open('data/efake/%i/parms_%s.txt' %(options.year,tag),'w') as outfile:
        json.dump(data,outfile)




### ---------------------------------------------------------------------------


def fitting_simultaneous( samples, fm, ptrange, fitranges=((50,180)), var="ph_pt[0]",
                        basesel = "1", tag="", ic = None,
                        maxtimes =5, xbins  =(200,0,200), dobkgd=True, doData = False, donorm=False):
    """ Simulatnous fit of signal and background distribution """
    """ icond : input initial condition or choose the preset """
    if ic is None: ic = dict(iconddcb = None, sig = "dcbp", bkgd = "gaus", ext = 'simul')

    ## replace decimal point with p
    ptname = tuple([str(x).replace('.','p') for x in ptrange])

    readcache=writecache=False
    if options.cache == "READ":
        readcache=True
    elif options.cache == "WRITE":
        writecache=True
    elif options.cache:
        raise RuntimeError("What to do with the cache again?")
    if readcache:  f = ROOT.TFile("data/efake/zfitcache.root")
    if writecache: f = ROOT.TFile("data/efake/zfitcache.root", "RECREATE")



    if readcache:

        if doData:
            h1=f.Get("hdata")
            if not dobkgd:
                h0=f.Get("hallbkgd")
        else:
            h1 = f.Get("hallbkgd")

        if dobkgd:
            ### get non-DY contribution
            h0 = f.Get("hallnonzee")
            fm.addhist(h0,"bkgdhist_pt_%s_%s" %ptname,bkgd = "nonzee")

    else:

        ## set up histogram config (set unblind if we use data)
        hconf_data = { "weight": weight, "logy": 1, "ymin": 10, 'ymax': 1e6,
                       "unblind": UNBLIND, "doratio": True, "rmax": 3,
                       "overflow": False }
        hconf_blind = { "weight": weight ,"logy" : 1, "ymin": 10, 'ymax': 1e6,
                        "overflow": False }
        hconf = hconf_data if doData else hconf_blind
        sel = "%s&&%s>%g&&%s<%g" %( basesel, var, ptrange[0], var, ptrange[1])

        ## fill histogram
        sampframe = samples.Draw("m_lep_ph", sel, xbins, hconf)
        samples.print_stack_count( includeData = doData )

        ## save figure
        savename = "thstack_mlepph%s" %("_data" if doData else "")+ \
                     "_%s_%s" %ptname +tag

        samples.SaveStack(savename+".pdf", options.outputDir, "base")
        samples.SaveStack(savename+".png", options.outputDir, "base")

        ## obtain distribution for fitting
        ## EGamma/SingleElectron for data and stack sum for MC
        if doData:
            dataname = "EGamma" if options.year ==2018 else "SingleElectron"
            h1 = samples.get_samples(name=dataname)[0].hist.Clone("hdata")
        else:
            h1 = samples.get_samples(name='__AllStack__')[0]\
                        .hist.Clone("hallbkgd")
            #regulate(h1,10)

        if doData and not dobkgd:
            ## if dobkgd is not toggled, we use whole background
            ## for visualization in data-based fits
            h0 = samples.get_samples(name='__AllStack__')[0]\
                        .hist.Clone("hallbkgd")
            fm.addhist(h0,"mchist_pt_%s_%s" %ptname, bkgd="allmc")
            if writecache: h0.Write()

        if dobkgd:
            ## plot non-Zee contribution
            samples.deactivate_sample(["Z+jets"])

            sampframe.Draw("m_lep_ph", sel , xbins, hconf_blind)
            samples.print_stack_count()
            if not options.batch: input("continue")

            h0 = samples.get_samples(name='__AllStack__')[0]\
                        .hist.Clone("hallnonzee")
            fm.addhist(h0,"bkgdhist_pt_%s_%s" %ptname,bkgd = "nonzee")

            if writecache: h0.Write()

            samples.activate_sample(["Z+jets"])

        ### draw again for correct weight normalization
        if isinstance(xbins, list):
            hconf["normalize"] = "Width"
            sampframe .Draw("m_lep_ph", sel, xbins, hconf)

            ## save figure
            savename = "thstack_mlepph%s" %("_data" if doData else "")+ \
                         "_%s_%s_varwidth" %ptname +tag

            samples.SaveStack(savename+".pdf", options.outputDir, "base")
            samples.SaveStack(savename+".png", options.outputDir, "base")

    fm.addhist(h1,"datahist_pt_%s_%s" %ptname)
    if writecache:
        h1.Write()

    ## get stack count
    if readcache:

        # from cache file
        hstack = f.Get("stackcount")
        fx = lambda h, i: (h[i], h.GetBinError(i))
        stackcount = {"Z+jets":                 fx(hstack,1),
                      "NonEleFake":             fx(hstack,2),
                      "OtherEleFakeBackground": fx(hstack,3)}
    else:
        samples.print_stack_count( fitranges[-1])
        stackcount = samples.get_stack_count(fitranges[-1])

        if writecache:
            ## write stack count to cache file
            htemp=ROOT.TH1F("stackcount","stackcount",10,0,10)
            sethbin(htemp,1,stackcount["Z+jets"])
            sethbin(htemp,2,stackcount["NonEleFake"])
            sethbin(htemp,3,stackcount["OtherEleFakeBackground"])
            htemp.Write()

    ## decide range based on count
    fx = lambda x,y: (x,round(y[0]),0,round(y[0]*10)+1e4)
    if donorm: ic['icparm']['simul2']  =\
                             [ fx("Nsig", stackcount["Z+jets"]),
                               fx("Nbkg", stackcount["NonEleFake"]),
                               fx("Nzg" , stackcount["OtherEleFakeBackground"])]

    ## close file after getting stack count (the hist are attached to current file)
    if writecache or readcache:
        f.Close()

    #### NOTE NOTE fitting step
    corefitting_simultaneous( fm, ptrange, fitranges, tag = tag, ic = ic,
                             maxtimes = maxtimes )
    c=fm.draw(" ",logy=0,paramlayout=(0.55,0.9,0.82),subplot="pull", component=True)
    c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_final" %ptname + tag+ ".pdf")
    c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_final" %ptname + tag+ ".png")
    c=fm.draw(" ",(1,1e6),logy=1,paramlayout=(0.55,0.9,0.82),subplot="pull", component=True)
    c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_finallog" %ptname + tag+ ".pdf")
    c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_finallog" %ptname + tag+ ".png")

    #samples.curr_canvases["top"].cd()
    #fm.func_pdf.asTF(ROOT.RooArgList(fm.xvardata)).Draw("L same")
    #samples.SaveStack("thstack_postfit_mlepph_%s_%s.pdf" %ptrange,
    #                    outputDir = "temp/", canname ="top")
    c = fm.get_correlations()
    if c: ## if no fit result
        c.SaveAs(options.outputDir+"/simult_correlations_%s_%s_" %ptname+tag+".pdf")
        c.SaveAs(options.outputDir+"/simult_correlations_%s_%s_" %ptname+tag+".png")

    values = fm.get_parameter_values()
    print("VALUES")
    pprint(values)
    print("STACKCOUNT")
    pprint(stackcount)
    return values, stackcount



### ---------------------------------------------------------------------------


def corefitting_simultaneous(fm, ptrange,fitranges=((50,180)),
            tag="", ic=None, maxtimes =5):
    """
        Helper function of fitting_simultaneous
        Provide Core Fitting functionality
        Hard-coded retries and break out of loops using return
    """
    bestchi = 1000000
    chi=200
    ptname = tuple([str(x).replace('.','p') for x in ptrange])
    for itry in range(maxtimes):
        print("*** TRIAL %i ***" %itry)
        print()
        ##### setup fit manager #####
        # replace lists in ic with alteratives at each try
        iclocal = {key:item[itry%len(item)] if isinstance(item, list) else item for key,item in ic.items()}
        print(iclocal)
        if chi >5 or fm.func_pdf is None: froo_dcb = fm.setup_fit(**iclocal) # pass down initial condition settings
        c=fm.draw(" ",(1,1e6),logy=1,paramlayout=(0.55,0.9,.82), component = True)
        c.SaveAs(options.outputDir+"/simult_prefit_mlepph_%s_%s_" %ptname + tag+ ".pdf")
        c.SaveAs(options.outputDir+"/simult_prefit_mlepph_%s_%s_" %ptname + tag+ ".png")
        chi = fm.getchisquare()
        print("\nCHI ORIGINAL: ", chi)
        for fr in fitranges:
            #fr = tuple(round(x+random.normalvariate(0,5)) for x in fr)
            #print fr
            #fr = (max(50,min(90,fr[0])), max(100,min(195,fr[1])))
            #print fr
            fr = (50,190)


            print("NOW FITTING mass range %g to %g" %fr + " for pT bin of %g,%g" %ptrange)
            froo_dcb = fm.run_fit(fr)
            #froo_dcb = fm.run_fit_chi2(fr)
            print("FINISH fitting range %g to %g"%fr + " for pT bin of %g,%g" %ptrange)
            #fm.fitresult.Print()
            fm.frame.Print()
            ## draw result
            #c=fm.draw(" ",(1,1e6),logy=1,paramlayout=(0.55,0.9,0.82),subplot="pull", component=True)
            c=fm.draw(" ",paramlayout=(0.55,0.9,0.82),subplot="pull", component=True)
            c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_try%s%s.pdf" %(ptname +(itry, tag)) )
            c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_try%s%s.png" %(ptname +(itry, tag)) )
            chi = fm.getchisquare()
            print("\nCHI: ", chi)
            sigerrtoval = fm.defs['Nsig'].getError()/ fm.defs['Nsig'].getVal()
            print("Nsig : %g +- %g" %(fm.defs['Nsig'].getVal(),fm.defs['Nsig'].getError()))
            if not options.batch: input("continue")
            if (chi*2<itry and sigerrtoval<.5) or (itry>maxtimes/2 and chi<bestchi*2 and sigerrtoval<.5):
                print("\n *** FINISH TRIALS AT %i-TH TRY W/ CHI2 OF %g *** \n" %(itry, chi))
                c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_finalfit%s.pdf" %(ptname +(tag,)) )
                c.SaveAs(options.outputDir+"/simult_postfit_mlepph_%s_%s_finalfit%s.png" %(ptname +(tag,)) )
                if not options.batch: input("finishing")
                return
            bestchi = min(bestchi,chi)
            print("\nbestchi: ",bestchi)



### ---------------------------------------------------------------------------


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

    minvalue = [s[0] for s in list(stackcount.values())]+[values['Nsig'].n,values['Nbkg'].n]
    print("MINVALUES: ",minvalue)
    minvalue = max(min(minvalue),10)
    print("MINVAL: ",minvalue)
    #h2.SetMinimum(0.1*min(map(lambda x:max(1, x.GetMinimum()),[h1,h2]))) #doesnt work
    leg = ROOT.TLegend(0.55,0.7,0.9,0.9)
    leg.AddEntry(h1, "# MC", "PL")
    leg.AddEntry(h2, "Predicted", "PL")
    hratio = h2.Clone()
    hratio.Divide(h1)
    h2.SetMaximum(300*max([x.GetMaximum() for x in [h1,h2]]))
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
    yAxs.SetRangeUser(0,2)
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




### ---------------------------------------------------------------------------


def makevariableplots_simultaneous_zg( samp, ptlist, fitrange, basesel="1",
                                       tag="", ic = None, dobkgd=True,
                                       donorm=False, maxtimes=5, doData=False):
    """ 
        extended pdf fit for zgamma peak
    """

    if ic is None: ic = dict(sig="dcbp",bkgd="gaus", ext="simul")
    if "icparm" not in ic: ic["icparm"] = dict()
    parmufloats = defaultdict(list)
    parmvals    = defaultdict(list)
    parmerrs    = defaultdict(list)
    parmnames   = FitManager.ParamDCB

    parm = get_param("data/efake/%i/dcbparms_all%i.txt"%((options.year,)*2))
    fm = FitManager("dcbexpo", xvardata = (0,200,"GeV"))
    iconddcb = {pt:[(n,parm[n][ipt]) for n in parmnames] \
                    for ipt,pt in enumerate(ptlist[:-1])}

    for ptrange in zip(ptlist[:-1],ptlist[1:]):
        ptrange = tuple(ptrange)
        #xp.append(ptrange)
        ic['icparm']['dcbp'] = [("x",50,200)]+iconddcb[ptrange[0]] # FIXME: move up a fx level
        #ic['icparm']['gauszg'] = [("x",20,200)]+icondgzg[ptrange[0]] # FIXME: move up a fx level
        ### fitting step
        ptfitrange = fitrange.get(ptrange[0],fitrange[-1]) # get default if entry doesnt exist
        values, stackcount = fitting_simultaneous(samp, fm, ptrange, ptfitrange, basesel=basesel,
                tag=tag, ic = ic, xbins=(200,0,200), dobkgd =dobkgd, maxtimes = maxtimes, doData=doData, donorm=donorm)
        if donorm: make_normalization_comparison(fm,values,stackcount,ptrange,tag)
        for name,val in list(values.items()):
            if val is None: #for case of non-initiated variable
                parmvals[name].append(-1)
                parmerrs[name].append(-1)
            elif val.s>0: #check if the value is fitted
                parmvals[name].append(val.n) #value
                parmerrs[name].append(val.s) #uncertainty
            parmufloats[name].append(val)
    # dealing with width of overflow/last bin
    #xpoints, xerrs = xp.output()
    print("values:"); pprint(list(parmufloats.items()))
    f = lambda p: {x:y for x,y in p.items()}
    data = {'ptlist':ptlist,'parm':f(parmvals),'error':f(parmerrs)}
    with open('data/efake/%i/parms_%s.txt' %(options.year,tag),'w') as outfile:
        json.dump(data,outfile)


### ---------------------------------------------------------------------------


def sethbin(h,i,value):
    if value is None: return
    if isinstance(value,tuple):
        value = ufloat(*value)
    h.SetBinContent(i,value.n)
    h.SetBinError  (i,value.s)




### ---------------------------------------------------------------------------


def getparm(ic, parmname):
    """ Return parm of a certain name """
    index = findparmindex(ic, parmname)
    return ic[index]

def findparm(ic, parmname):
    """ Return array of matching parameter names """
    return [i[0] == parmname for i in ic]

def findparmindex(ic, parmname):
    """ Return index of parm array matching a parameter name. Helper function """

    found = findparm(ic, parmname)

    if sum(found) > 1:
        print("WARNING: more than one parm found at replaceparm()")
    if sum(found) == 0:
        print(ic, parm)
        raise IndexError

    return found.index(True)

def replaceparm(ic, parm):
    """
        Replace an item in initial condition list
        Because the order is fixed, we cannot use dict
    """

    ### NOTE the same parameter could appear twice
    ###      only the first one is selected here

    index = findparmindex(ic, parm[0])


    ic[index] = parm

    return


### ---------------------------------------------------------------------------


def setlinestyle(t,width=2,color=2):
        """ works with TH1 and TGraph"""
        t.SetLineColor(color)
        t.SetLineWidth(width)



### ---------------------------------------------------------------------------


def regulate(h1, scale = 1):
    """  add uncertainty to non-zero bin and remove negative bins """
    for i in range(1,h1.GetNbinsX()+1):
        y=h1.GetBinContent(i)
        ye=h1.GetBinError(i)
        ye_new = math.sqrt(ye*ye+scale*scale)
        if y<0: h1.SetBinContent(i,0)
        if y>0: h1.SetBinError(i,ye_new)
        print(i, y, ye, ye_new)



### ---------------------------------------------------------------------------


def addline(graph,y):
    left_edge  = graph.GetXaxis().GetXmin()
    right_edge = graph.GetXaxis().GetXmax()

    print(left_edge, right_edge, y)
    oneline = ROOT.TLine(left_edge, y, right_edge, y)
    oneline.SetLineStyle(3)
    oneline.SetLineWidth(2)
    oneline.SetLineColor(ROOT.kRed)
    return oneline



### ---------------------------------------------------------------------------


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
        parmdict = fitting( samp, fm, ptrange,
                            fitrange.get(ptrange[0],fitrange[-1]),
                            basesel=basesel, tag=tag, var=var )

        for name,val in list(parmdict.items()):
            parmvals[name].append(val.n) #value
            parmerrs[name].append(val.s) #uncertainty
            parmufloats[name].append(val)

    # dealing with width of overflow/last bin
    xpoints[-1] = ptlist[-2] + xerrs[-2]
    xerrs[-1]   = xerrs[-2]

    print("values:")
    pprint(parmufloats)
    print("xpoints: \n", xpoints)
    print("xerrors: \n", xerrs)

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

    for name, tgraph in list(parmgraph.items()):
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
                print(name," ", ylimit[2])

            if (ylimit[1]>yplot[0]):
                lline = addline(tgraph,ylimit[1])
                lline.Draw()
                print(name," ", ylimit[1])
        c1.SaveAs(options.outputDir+"/tge_dcb_%s_%s.pdf" %(name,tag))
        c1.SaveAs(options.outputDir+"/tge_dcb_%s_%s.png" %(name,tag))

    data = {'ptlist':ptlist,'parm':parmvals,'error':parmerrs}

    ## save to json format
    ofname = 'data/efake/%i/dcbparms_%s.txt' %(options.year,tag)
    with open( ofname, 'w' ) as outfile:
        json.dump(data,outfile)



### ---------------------------------------------------------------------------


def fitting(samples,fm, ptrange,fitranges=((50,180)),var="ph_pt[0]",basesel = "1",tag=""):
    froo_dcb = fm.setup_fit((50,195))

    selection  = "%s&&%s>%g&&%s<%g" %(basesel,var,ptrange[0],var,ptrange[1])
    samples.Draw( "m_lep_ph", selection, (100,0,200),
            { "weight": weight, "overflow":False , "onthefly": False} )

    h1 = samples.get_samples(name='__AllStack__')[0].hist.Clone()
    #regulate(h1)
    #h1.Scale(1./h1.Integral())

    ptrange = tuple([str(x).replace('.','p') for x in ptrange])
    fm.addhist(h1,"datahist_pt_%s_%s" %ptrange)

    # setup fit manager
    c=fm.draw(" ",(1,1e6),logy=1,paramlayout=(0.55,0.9,.82))
    c.SaveAs(options.outputDir+"/prefit_mlepph_%s_%s_" %ptrange + tag+ ".pdf")
    c.SaveAs(options.outputDir+"/prefit_mlepph_%s_%s_" %ptrange + tag+ ".png")

    for fr in fitranges:
        print("NOW FITTING mass range %g to %g" %fr)
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



### ---------------------------------------------------------------------------


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


