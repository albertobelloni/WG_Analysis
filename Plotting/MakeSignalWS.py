#!/usr/bin/env python
execfile("MakeBase.py")
ROOT.PyConfig.IgnoreCommandLineOptions = True
import re
import uuid
import pickle
from uncertainties import ufloat
from collections import OrderedDict
ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)

_XMIN_M = 60
_XMAX_M = 4000
_DEFAULTDATADIR = 'data/sigfit/'

if options.dataDir is None :
    options.dataDir = _DEFAULTDATADIR
if options.dataDir is not None :
    if not os.path.isdir( options.dataDir ) :
        os.makedirs( options.dataDir )
        os.makedirs( options.dataDir+ "/2016" )
        os.makedirs( options.dataDir+ "/2017" )
        os.makedirs( options.dataDir+ "/2018" )
fitmlist = []

def main() :
    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

#    sel_base_mu = 'mu_pt30_n==1 && mu_n==1'
#    sel_base_el = 'el_pt30_n==1 && el_n==1'
#
#    sel_jetveto_mu = sel_base_mu + ' && jet_n == 0 '
#    sel_jetveto_el = sel_base_el + ' && jet_n == 0 '


    workspaces_to_save = {}

    bin_width_m = 20

    xmin_pt = _XMIN_M/2
    if xmin_pt < 50 :
        xmin_pt = 50
    xmax_pt = _XMAX_M/2
    bin_width_pt = bin_width_m/2.

    #binning_m = ((_XMAX_M-_XMIN_M)/bin_width_m, _XMIN_M, _XMAX_M)

    #binning_pt = ( (xmax_pt - xmin_pt )/bin_width_pt, xmin_pt, xmax_pt )

    #xvar_m = ROOT.RooRealVar( 'x_m', 'x_m',_XMIN_M , _XMAX_M)

    #xvar_pt = ROOT.RooRealVar( 'x_pt', 'x_pt', xmin_pt, xmax_pt )

    signal_binning_m_width1 = {
                         200 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         250 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         300 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         350 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         400 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         450 : ( (_XMAX_M)/5 , 0, _XMAX_M ),
                         500 : ( (_XMAX_M)/8 , 0, _XMAX_M ),
                         600 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         700 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         800 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         900 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                        1000 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                        1200 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1400 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1600 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1800 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        2000 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        2200 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        2400 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        2600 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        2800 : ( int((_XMAX_M)/25), 0, _XMAX_M ),
                        3000 : ( int((_XMAX_M)/25), 0, _XMAX_M ),
                        3500 : ( int((_XMAX_M)/40), 0, _XMAX_M ),
                        4000 : ( int((_XMAX_M)/40), 0, _XMAX_M ),
                       }

    signal_binning_m_width2 = {
                         200 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         250 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         300 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         350 : ( (_XMAX_M)/5 , 0, _XMAX_M ),
                         400 : ( (_XMAX_M)/5 , 0, _XMAX_M ),
                         450 : ( (_XMAX_M)/8 , 0, _XMAX_M ),
                         500 : ( (_XMAX_M)/8 , 0, _XMAX_M ),
                         600 : ( (_XMAX_M)/8 , 0, _XMAX_M ),
                         700 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         800 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         900 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1000 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1200 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        1400 : ( (_XMAX_M)/25, 0, _XMAX_M ),
                        1600 : ( (_XMAX_M)/25, 0, _XMAX_M ),
                        1800 : ( int((_XMAX_M)/30), 0, _XMAX_M ),
                        2000 : ( int((_XMAX_M)/30), 0, _XMAX_M ),
                        2200 : ( int((_XMAX_M)/30), 0, _XMAX_M ),
                        2400 : ( int((_XMAX_M)/30), 0, _XMAX_M ),
                        2600 : ( int((_XMAX_M)/35), 0, _XMAX_M ),
                        2800 : ( int((_XMAX_M)/35), 0, _XMAX_M ),
                        3000 : ( int((_XMAX_M)/35), 0, _XMAX_M ),
                        3500 : ( int((_XMAX_M)/40), 0, _XMAX_M ),
                        4000 : ( int((_XMAX_M)/40), 0, _XMAX_M ),
                       }

    signal_binning_m = [ signal_binning_m_width1, signal_binning_m_width2 ]

    ### pT binning is just mass binning divided by two, with floor of 50 GeV
    signal_binning_pt = {}
    for mass, binning in signal_binning_m_width1.iteritems() :
        pt_min = binning[1]/2.
        if pt_min < 50 :
            pt_min = 50
        signal_binning_pt[mass] = ( binning[0]/2., pt_min, binning[2]/2. )



    kine_vars = { #'mt_incl_lepph_z' : { 'var' : 'mt_lep_met_ph'   , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'m_incl_lepph_z'  : { 'var' : 'm_lep_met_ph'    , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  ##'mt_rotated'      : { 'var' : 'mt_rotated'      , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
               'mt_res' : { 'var' : 'mt_res' , 'signal_binning' : signal_binning_m },
                  #'mt_constrwmass'  : { 'var' : 'recoM_lep_nu_ph' , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'ph_pt'           : { 'var' : 'ph_pt[0]'        , 'xvar' : xvar_pt , 'binning' : binning_pt, 'signal_binning' : signal_binning_pt },
                }

#    selections = { 'base'    : {
#                                 'mu' : {'selection' : sel_base_mu },
#                                 'el' : { 'selection' : sel_base_el },
#                               },
#                 }


    #for seltag, chdic in selections.iteritems() :
    #    # groups of selection containing dict of channels
    #    print "seltag: ",seltag ,"chdic: ", chdic

    lepg_samps = { 'mu' : sampManMuG, 'el' : sampManElG }

    for ch, man in lepg_samps.iteritems() :
        ## loop channel and sample manager
        for name, vardata in kine_vars.iteritems() :
            ## variables to be fitted
            print "name",name,"vardata", vardata

            ## call fit function
            make_signal_fits( man, workspaces_to_save=workspaces_to_save,
                               suffix='%s%i'%(ch,options.year), **vardata)

    for fileid, ws in workspaces_to_save.iteritems() :
            ws.writeToFile( '%s/%s/%s.root' %( options.dataDir, options.year, fileid ) )




def parsesampname(name):
    res = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_.*', name )
    if res is None :
        print 'Could not interpret path ', name
    else :

        mass = float(res.group(2))
        iwidth = 0
        if name.count( 'width0p01' ) :
            width = 0.0001
            wid = "0p01"
        else :
            res2 = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_width(\d)', name )
            width = float(res2.group(3))/100.
            wid = res2.group(3)
            iwidth = 1
    return mass, width, wid, iwidth

def numtostr(num=0):
    strg = "%g" %num
    return strg.replace(".","p")



def makevar(var, mass):
    xvar = ROOT.RooRealVar( var, var, _XMIN_M , _XMAX_M)
    fit_max = mass * 1.20
    fit_min = max ( mass * 0.50,  200.0 )
    ## set the fit range
    xvar.setMin( fit_min )
    xvar.setMax( fit_max )
    return xvar


def make_signal_fits( sampMan, suffix="", workspaces_to_save=None, var="mt_res",  signal_binning=[]):

    sampMan.clear_hists()

    ## decide which channel it is
    assert "mu" in suffix or "el" in suffix, \
            "suffix %s must contain the mu or el channel" %suffix

    if 'mu' in suffix:
       extra_label = "Muon channel"
       ch="mu"
    else:
       extra_label = "Electron channel"
       ch="el"


    ### now loop over all samples to fit each of them
    for samp in sampMan.get_samples(isSignal=True ) :

        print 'Sample = ', samp.name
        mass, width, wid, iwidth = parsesampname(samp.name)

        ### exclude certain samples
        if samp.name.count( 'MadGraph' ) == 0:
           continue
        if mass > 2000 or mass < 300:
           continue
        if iwidth >=len(signal_binning):
           print "exclude", iwidth,signal_binning
           continue
        if mass not in signal_binning[iwidth]:
           print "exclude mass", mass, signal_binning[iwidth]
           continue

        ## make full suffix
        full_suffix = "_".join(['MG', "M%d"%mass, 'W%s'%wid, suffix])

        ## make full selection string
        binning = signal_binning[iwidth][mass]
        addition = " (%s > %d && %s < %d )" %(var, binning[1], var ,binning[2])
        cuttag, full_sel_sr = defs.selectcutstring( mass , ch, addition )
        print full_sel_sr

        ## make RooRealVar for fit variable

        xvar = makevar(var, mass)

        sample_params = {'mass' : mass, 'width' : width}

        workspace  = ROOT.RooWorkspace( 'wssignal_M%d_W%s_%s'%(mass, wid, ch) )

        lconf = {"labelStyle":str(options.year),
                 "extra_label":"%i %s" %(options.year, extra_label),
                 "extra_label_loc":(.12,.82)}

        ## make histogram
        sampMan.create_hist( samp, var, full_sel_sr, signal_binning[iwidth][mass] )
        print "Integral: ", samp.hist.Integral()

        ## fit histogram
        fit_sample( samp.hist, xvar, workspace, full_suffix, sample_params, lconf)

        ## save result
        #workspaces_to_save.update( { workspace.GetName() : workspace} )
        assert workspaces_to_save.get(workspace.GetName())==None, workspace.GetName()
        workspaces_to_save[ workspace.GetName() ] = workspace


def fit_sample( hist, xvar,  workspace , suffix, sample_params, label_config ):

    fitManager = FitManager( 'dscb',  hist=hist,  xvardata = xvar,
                            sample_params=sample_params, label = suffix)

    fitManager.setup_fit()
    #fitManager.fit_histogram(workspace )
    #fitManager.run_fit_minuit( fitrange = (fit_min, fit_max) ,debug = True)
    fitManager.run_fit_minuit( fitrange = xvar, debug = True)
    fitManager.get_results( workspace )
    #fitManager.save_fit( sampMan, workspace, stats_pos='left',
    #                     extra_label = extra_label , plotParam =True)
    canv = fitManager.draw( subplot = "pull", paramlayout = (0.12,0.5,0.78),
                            useOldsetup = True, label_config = label_config)

    canv.Print("%s/%s.pdf" %(options.outputDir, suffix) )
    canv.Print("%s/%s.png" %(options.outputDir, suffix) )
    canv.Print("%s/%s.C"   %(options.outputDir, suffix) )

    print "************"
    print " RooFitResult Status: %d"%fitManager.fitresult.status()
    print "************"

    fitmlist.append(fitManager)


def fit_pol1( hist, xmin, xmax ) :

    lin_func = ROOT.TF1( 'lin_func', '[0] + [1]*x', xmin, xmax )

    lin_func.SetParameter( 0, 0.5 )
    lin_func.SetParameter( 1, 0 )

    hist.Fit( lin_func, 'R' )

    hist.Draw()
    lin_func.Draw('same')


def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True )
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

main()












