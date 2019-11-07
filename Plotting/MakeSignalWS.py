import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import re
import os
import uuid
import math
import pickle
import selection_defs as defs
from uncertainties import ufloat
from FitManager import FitManager
from collections import OrderedDict
#ROOT.TVirtualFitter.SetMaxIterations( 100000 )
ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)

from SampleManager import SampleManager
from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument('--baseDirMuG',      default=None,           dest='baseDirMuG',         required=False, help='Path to signal samples in muon channel')
parser.add_argument('--baseDirElG',      default=None,           dest='baseDirElG',         required=False, help='Path to signal samples in muon channel')
parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')
parser.add_argument('--useRooFit',       default=False,    action='store_true',      dest='useRooFit', required=False, help='Make fits using roostats' )
parser.add_argument('--doSignal',       default=False,    action='store_true',      dest='doSignal', required=False, help='make signal fits' )
parser.add_argument('--doWGamma',       default=False,    action='store_true',      dest='doWGamma', required=False, help='make wgamma fits' )
parser.add_argument('--doTop',          default=False,    action='store_true',      dest='doTop', required=False, help='make top fits' )
parser.add_argument('--doZGamma',          default=False,    action='store_true',      dest='doZGamma', required=False, help='make ZGamma fits' )
parser.add_argument('--doWJets',       default=False,     action='store_true',     dest='doWJets', required=False, help='make w+jets fits' )
parser.add_argument('--doEleFake',       default=False,     action='store_true',     dest='doEleFake', required=False, help='make electron fake fits' )
parser.add_argument('--doClosure',       default=False,   action='store_true',       dest='doClosure', required=False, help='make closure tests' )

options = parser.parse_args()


_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000
_BASEPATH = '/home/jkunkle/usercode/Plotting/LimitSetting/'
_SAMPCONF = 'Modules/Resonance.py'


ROOT.gROOT.SetBatch(False)
if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

def main() :

    #sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME)
    #sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME)

    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

    sampManMuG.outputs = OrderedDict()
    sampManMuG.fitresults = OrderedDict()
    sampManMuG.chi2= OrderedDict()
    sampManMuG.chi2prob = OrderedDict()

    sampManElG.outputs = OrderedDict()
    sampManElG.fitresults = OrderedDict()
    sampManElG.chi2= OrderedDict()
    sampManElG.chi2prob = OrderedDict()

    sel_base_mu = 'mu_pt30_n==1 && mu_n==1'
    sel_base_el = 'el_pt30_n==1 && el_n==1'

    sel_jetveto_mu = sel_base_mu + ' && jet_n == 0 '
    sel_jetveto_el = sel_base_el + ' && jet_n == 0 '

    #eta_cuts = ['EB', 'EE']
    eta_cuts = ['EB']

    workspaces_to_save = {}

    xmin_m = 60
    xmax_m = 4000
    bin_width_m = 20

    xmin_pt = xmin_m/2
    if xmin_pt < 50 :
        xmin_pt = 50
    xmax_pt = xmax_m/2
    bin_width_pt = bin_width_m/2.

    binning_m = ((xmax_m-xmin_m)/bin_width_m, xmin_m, xmax_m)

    binning_pt = ( (xmax_pt - xmin_pt )/bin_width_pt, xmin_pt, xmax_pt )

    xvar_m = ROOT.RooRealVar( 'x_m', 'x_m',xmin_m , xmax_m)

    xvar_pt = ROOT.RooRealVar( 'x_pt', 'x_pt', xmin_pt, xmax_pt )

    signal_binning_m_width1 = { 
                         200 : ( (xmax_m)/4 , 0, xmax_m ),
                         250 : ( (xmax_m)/4 , 0, xmax_m ),
                         300 : ( (xmax_m)/4 , 0, xmax_m ),
                         350 : ( (xmax_m)/4 , 0, xmax_m ),
                         400 : ( (xmax_m)/4 , 0, xmax_m ),
                         450 : ( (xmax_m)/5 , 0, xmax_m ),
                         500 : ( (xmax_m)/8 , 0, xmax_m ),
                         600 : ( (xmax_m)/10, 0, xmax_m ),
                         700 : ( (xmax_m)/10, 0, xmax_m ),
                         800 : ( (xmax_m)/10, 0, xmax_m ),
                         900 : ( (xmax_m)/10, 0, xmax_m ),
                        1000 : ( (xmax_m)/10, 0, xmax_m ),
                        1200 : ( int((xmax_m)/15), 0, xmax_m ),
                        1400 : ( int((xmax_m)/15), 0, xmax_m ),
                        1600 : ( int((xmax_m)/15), 0, xmax_m ),
                        1800 : ( int((xmax_m)/15), 0, xmax_m ),
                        2000 : ( (xmax_m)/20, 0, xmax_m ),
                        2200 : ( (xmax_m)/20, 0, xmax_m ),
                        2400 : ( (xmax_m)/20, 0, xmax_m ),
                        2600 : ( (xmax_m)/20, 0, xmax_m ),
                        2800 : ( int((xmax_m)/25), 0, xmax_m ),
                        3000 : ( int((xmax_m)/25), 0, xmax_m ),
                        3500 : ( int((xmax_m)/40), 0, xmax_m ),
                        4000 : ( int((xmax_m)/40), 0, xmax_m ),
                       }

    signal_binning_m_width2 = {
                         200 : ( (xmax_m)/4 , 0, xmax_m ),
                         250 : ( (xmax_m)/4 , 0, xmax_m ),
                         300 : ( (xmax_m)/4 , 0, xmax_m ),
                         350 : ( (xmax_m)/5 , 0, xmax_m ),
                         400 : ( (xmax_m)/5 , 0, xmax_m ),
                         450 : ( (xmax_m)/8 , 0, xmax_m ),
                         500 : ( (xmax_m)/8 , 0, xmax_m ),
                         600 : ( (xmax_m)/8 , 0, xmax_m ),
                         700 : ( (xmax_m)/10, 0, xmax_m ),
                         800 : ( (xmax_m)/10, 0, xmax_m ),
                         900 : ( int((xmax_m)/15), 0, xmax_m ),
                        1000 : ( int((xmax_m)/15), 0, xmax_m ),
                        1200 : ( (xmax_m)/20, 0, xmax_m ),
                        1400 : ( (xmax_m)/25, 0, xmax_m ),
                        1600 : ( (xmax_m)/25, 0, xmax_m ),
                        1800 : ( int((xmax_m)/30), 0, xmax_m ),
                        2000 : ( int((xmax_m)/30), 0, xmax_m ),
                        2200 : ( int((xmax_m)/30), 0, xmax_m ),
                        2400 : ( int((xmax_m)/30), 0, xmax_m ),
                        2600 : ( int((xmax_m)/35), 0, xmax_m ),
                        2800 : ( int((xmax_m)/35), 0, xmax_m ),
                        3000 : ( int((xmax_m)/35), 0, xmax_m ),
                        3500 : ( int((xmax_m)/40), 0, xmax_m ),
                        4000 : ( int((xmax_m)/40), 0, xmax_m ),
                       }

    signal_binning_m = [ signal_binning_m_width1, signal_binning_m_width2 ]

    signal_binning_pt = {}
    for mass, binning in signal_binning_m_width1.iteritems() :
        pt_min = binning[1]/2.
        if pt_min < 50 :
            pt_min = 50
        signal_binning_pt[mass] = ( binning[0]/2., pt_min, binning[2]/2. )



    kine_vars = { #'mt_incl_lepph_z' : { 'var' : 'mt_lep_met_ph'   , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'m_incl_lepph_z'  : { 'var' : 'm_lep_met_ph'    , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  ##'mt_rotated'      : { 'var' : 'mt_rotated'      , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  'mt_fulltrans'    : { 'var' : 'mt_res'          , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'mt_constrwmass'  : { 'var' : 'recoM_lep_nu_ph' , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'ph_pt'           : { 'var' : 'ph_pt[0]'        , 'xvar' : xvar_pt , 'binning' : binning_pt, 'signal_binning' : signal_binning_pt },
                }

    selections = { 'base'    : { 
                                 'mu' : {'selection' : sel_base_mu }, 
                                 'el' : { 'selection' : sel_base_el }, 
                               },
                   #'jetVeto' : { 'mu' : {'selection' : sel_jetveto_mu }, 
                   #              'el' : { 'selection' : sel_jetveto_el } ,
                   #            },
                 }

    lepg_samps = { 'mu' : sampManMuG, 'el' : sampManElG }
    #lepg_samps = {'mu' : sampManMuG }

    for seltag, chdic in selections.iteritems() :

        print "seltag: ",seltag ,"chdic: ", chdic
        for ch, seldic in chdic.iteritems() :

            print "ch:", ch,"seldic",seldic
            for name, vardata in kine_vars.iteritems() :
                print "name",name,"vardata", vardata#['signal_binning']

                make_signal_fits( lepg_samps[ch], seldic['selection'], eta_cuts, vardata['var'], vardata['xvar'], vardata['signal_binning'], workspaces_to_save, suffix='%s_%s_%s'%(ch,name,seltag ), plots_dir = options.outputDir + "/plots")

    if options.outputDir is not None :

        for fileid, ws in workspaces_to_save.iteritems() :
            #for idx, ws in enumerate(ws_list) :
                #if idx == 0 :
                #    recreate = True
                #else  :
                #    recreate = False

            ws.writeToFile( '%s/%s.root' %( options.outputDir, fileid ) )

    #for key, result in sampManMuG.fitresults.iteritems():
    #    print "sample: %50s result %d chi2 %.2f"%(key, result.status(), sampManMuG.chi2[key])
    #    result.Print()

    #for key, result in sampManElG.fitresults.iteritems():
    #    print "sample: %50s result %d chi2 %.2f"%(key, result.status(), sampManElG.chi2[key])
    #    result.Print()


def make_signal_fits( sampMan, sel_base, eta_cuts, plot_var, xvar, binning, workspaces_to_save,  suffix, plots_dir = 'plots') : 

    sampMan.clear_hists()

    if not os.path.isdir( plots_dir ) :
       os.makedirs( plots_dir )

    for samp in sampMan.get_samples(isSignal=True ) :

        print 'Sample = ', samp.name


        res = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_.*', samp.name )
        if res is None :
            print 'Could not interpret path ', samp.name
        else :

            mass = float(res.group(2))
            iwidth = 0
            if samp.name.count( 'width0p01' ) :
                width = 0.0001
                wid = "0p01"
            else :
                res2 = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_width(\d)', samp.name )
                width = float(res2.group(3))/100.
                wid = res2.group(3)
                iwidth = 1

        if samp.name.count( 'MadGraph' ) == 0:
           continue
        if mass > 2000 or mass < 300:
           continue
        if iwidth >=len(binning):
           print "exclude", iwidth, binning
           continue
        if mass not in binning[iwidth]:
           print "exclude mass", mass, binning[iwidth]
           continue

        #ph_selection_sr = '%s==1' %defs.get_phid_selection('all')
        #ph_idx_sr =  defs.get_phid_idx( 'all' )
        #print binning[iwidth][mass]
        #addtl_cuts_sr = 'ph_pt[%s] > 50  && %s > %f && %s < %f ' %(ph_idx_sr, plot_var, binning[iwidth][mass][1], plot_var, binning[iwidth][mass][2] )

        #xvar.setBins(10000,'cache')
        #xvar.setMin('cache',-100)
        #xvar.setMax('cache',1500)

        weight_str = defs.get_weight_str()
        sel_base_mu = defs.get_base_selection( 'mu' )
        sel_base_el = defs.get_base_selection( 'el' )

        el_ip_str = '( fabs( el_d0[0] ) < 0.05 && fabs( el_dz[0] ) < 0.10 && fabs( el_sc_eta[0] )<= 1.479 ) || ( fabs( el_d0[0] ) < 0.10 && fabs( el_dz[0] ) < 0.20 && fabs( el_sc_eta[0] )> 1.479 )'

        el_tight = ' el_passVIDTight[0] == 1'
        el_eta   = ' fabs( el_eta[0] ) < 2.1 '

        ph_str = 'ph_n==1 && ph_IsEB[0] && ph_pt[0] > 50 && !ph_hasPixSeed[0]'
        ph_tightpt_str = 'ph_n==1 && ph_IsEB[0] && ph_pt[0] > 80 && !ph_hasPixSeed[0]'

        met_str = 'met_pt > 25'

        Zveto_str = 'fabs(m_lep_ph-91)>15.0'

        sel_mu_nominal      = '%s * ( %s && %s && %s )'            %(  weight_str,  sel_base_mu, ph_str, met_str)
        sel_el_nominal      = '%s * ( %s && %s && %s && %s && %s && %s && ( %s ))'     %(  weight_str, sel_base_el, el_tight, el_eta, ph_str, met_str, Zveto_str, el_ip_str )

        sel_mu_phpt_nominal      = '%s * ( %s && %s && %s && ADDITION)'            %(  weight_str,  sel_base_mu, ph_tightpt_str, met_str)
        sel_el_phpt_nominal      = '%s * ( %s && %s && %s && %s && %s && %s && ( %s ) && ADDITION)'     %(  weight_str, sel_base_el, el_tight, el_eta, ph_tightpt_str, met_str, Zveto_str, el_ip_str )

        sel_base_mu = sel_mu_phpt_nominal
        sel_base_el = sel_el_phpt_nominal

        for ieta in eta_cuts :

            #full_suffix = '%s_%s_%s' %(samp.name, suffix, ieta)
            name = "_".join(['MadGraphResonance', 'Mass', "%d"%mass, 'Width', wid])

            full_suffix = '%s_%s_%s' %(name, suffix, ieta)

            #eta_str_sr = 'ph_Is%s[%s]' %( ieta, ph_idx_sr )

            if 'mu' in suffix:
               sel_base = sel_base_mu
               extra_label = "Muon channel"
            else:
               sel_base = sel_base_el
               extra_label = "Electron channel"

            #full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr, eta_str_sr, addtl_cuts_sr] )
            full_sel_sr = sel_base.replace("ADDITION", " (%s > %d && %s < %d )"%(plot_var, binning[iwidth][mass][1], plot_var ,binning[iwidth][mass][2]))
            print full_sel_sr

            #hist_sr    = clone_sample_and_draw( sampMan, sampname, plot_var, full_sel_sr, binning )
            sampMan.create_hist( samp, plot_var, full_sel_sr, binning[iwidth][mass] ) 

            hist_sr = samp.hist

            integral = hist_sr.Integral()

            #hist_sr.Scale( 1.0/integral )

            #datahist = ROOT.RooDataHist( 'srhist_%s' %full_suffix, 'srhist', ROOT.RooArgList(xvar), hist_sr)

            #histpdf = ROOT.RooHistPdf( 'srhistpdf_%s' %(full_suffix), 'srhistpdf' , ROOT.RooArgSet( xvar), datahist, 3 )

            assert "mu" in suffix or "el" in suffix, "suffix %s must contain the mu or el channel."%suffix

            if 'mu' in suffix:
               workspace  = ROOT.RooWorkspace( 'workspace_signal_Mass_%d_Width_%s_mu'%(mass, wid) )
            else:
               workspace  = ROOT.RooWorkspace( 'workspace_signal_Mass_%d_Width_%s_el'%(mass, wid) )

            fit_max = mass * 1.20
            fit_min = max ( mass * 0.50,  200.0 )

            ## set the fit range
            xvar.setMin( fit_min )
            xvar.setMax( fit_max )

            #fitManager = FitManager( 'bwxcb', 0, samp.name, hist_sr, plot_var, ieta, xvar, full_suffix, True, 
                                    #sample_params={'mass' : mass, 'width' : width}, )
            fitManager = FitManager( 'dscb',  hist=hist_sr,  xvardata = xvar, label = full_suffix,
                                    sample_params={'mass' : mass, 'width' : width}, )

            #fitManager.make_func_pdf()
            fitManager.setup_fit()
            #fitManager.fit_histogram(workspace )
            fitManager.run_fit_minuit( fitrange = (fit_min, fit_max) )
            fitManager.get_results( workspace )
            #fitManager.save_fit( sampMan, workspace, stats_pos='left' , extra_label = extra_label , plotParam =True)
            canv = fitManager.draw( subplot = "pull", paramlayout = (0.15,0.5,0.82), useOldsetup = True)

            canv.Print("%s/%s.pdf"%(plots_dir, full_suffix) )
            canv.Print("%s/%s.C"%(plots_dir, full_suffix) )
            print "************"
            print " RooFitResult Status: %d"%fitManager.roofitresult.status()
            print "************"

        workspaces_to_save.update( { workspace.GetName() : workspace} )


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

    




    
    




