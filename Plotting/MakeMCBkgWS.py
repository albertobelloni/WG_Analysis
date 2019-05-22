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
parser.add_argument('--outputDir',       default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')
parser.add_argument('--useRooFit',       default=False,     action='store_true',      dest='useRooFit',    required=False, help='Make fits using roostats' )
parser.add_argument('--doSignal',        default=False,     action='store_true',      dest='doSignal',     required=False, help='make signal fits' )
parser.add_argument('--doWGamma',        default=False,     action='store_true',      dest='doWGamma',     required=False, help='make wgamma fits' )
parser.add_argument('--doTop',           default=False,     action='store_true',      dest='doTop',        required=False, help='make top fits' )
parser.add_argument('--doTopGamma',      default=False,     action='store_true',      dest='doTopGamma',   required=False, help='make topgamma fits' )
parser.add_argument('--doZGamma',        default=False,     action='store_true',      dest='doZGamma',     required=False, help='make ZGamma fits' )
parser.add_argument('--doWJets',         default=False,     action='store_true',      dest='doWJets',      required=False, help='make w+jets fits' )
parser.add_argument('--doGammaGamma',    default=False,     action='store_true',      dest='doGammaGamma', required=False, help='make GammaGamma fits')
parser.add_argument('--doEleFake',       default=False,     action='store_true',      dest='doEleFake',    required=False, help='make electron fake fits' )
parser.add_argument('--doClosure',       default=False,     action='store_true',      dest='doClosure',    required=False, help='make closure tests' )
parser.add_argument('--doAll',           default=False,     action='store_true',      dest='doAll',        required=False, help='make all backgrounds fits' )

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

    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    #sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME)

    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

    sampManMuG.outputs = OrderedDict()
    sampManElG.outputs = {}
    sampManMuG.fitresults = OrderedDict()
    sampManMuG.chi2= OrderedDict()
    sampManMuG.chi2prob = OrderedDict()
    sampManElG.fitresults = OrderedDict()
    sampManElG.chi2= OrderedDict()
    sampManElG.chi2prob = OrderedDict()

    #sel_base_mu = 'mu_pt30_n==1 && mu_n==1'
    #sel_base_el = 'el_pt30_n==1 && el_n==1'
    weight_str = defs.get_weight_str()
    sel_base_mu = defs.get_base_selection( 'mu' )
    sel_base_el = defs.get_base_selection( 'el' )

    el_ip_str = '( fabs( el_d0[0] ) < 0.05 && fabs( el_dz[0] ) < 0.10 && fabs( el_sc_eta[0] )<= 1.479 ) || ( fabs( el_d0[0] ) < 0.10 && fabs( el_dz[0] ) < 0.20 && fabs( el_sc_eta[0] )> 1.479 )'

    el_tight = ' el_passVIDTight[0] == 1'
    el_eta   = ' fabs( el_eta[0] ) < 2.1 '

    ph_str = 'ph_n==1 && ph_IsEB[0] && ph_pt[0] > 50 && !ph_hasPixSeed[0]'
    ph_tightpt_str = 'ph_n==1 && ph_IsEB[0] && ph_pt[0] > 50 && !ph_hasPixSeed[0]'

    met_str = 'met_pt > 25'

    Zveto_str = 'fabs(m_lep_ph-91)>15.0'

    sel_mu_nominal      = '%s * ( %s && %s && %s )'            %(  weight_str,  sel_base_mu, ph_str, met_str)
    sel_el_nominal      = '%s * ( %s && %s && %s && %s && %s && %s && ( %s ))'     %(  weight_str, sel_base_el, el_tight, el_eta, ph_str, met_str, Zveto_str, el_ip_str )

    sel_mu_phpt_nominal      = '%s * ( %s && %s && %s && ADDITION)'            %(  weight_str,  sel_base_mu, ph_tightpt_str, met_str)
    sel_el_phpt_nominal      = '%s * ( %s && %s && %s && %s && %s && %s && ( %s ) && ADDITION)'     %(  weight_str, sel_base_el, el_tight, el_eta, ph_tightpt_str, met_str, Zveto_str, el_ip_str )

    sel_base_mu = sel_mu_phpt_nominal
    sel_base_el = sel_el_phpt_nominal

    sel_jetveto_mu = sel_base_mu + ' && jet_n == 0 '
    sel_jetveto_el = sel_base_el + ' && jet_n == 0 '

    #eta_cuts = ['EB', 'EE']
    eta_cuts = ['EB']

    workspaces_to_save = {}

    #xmin_m = 60
    xmin_m = 200
    xmax_m = 2000
    bin_width_m = 10

    xmin_pt = xmin_m/2
    if xmin_pt < 50 :
        xmin_pt = 50
    xmax_pt = xmax_m/2
    bin_width_pt = bin_width_m/2.

    binning_m = ((xmax_m-xmin_m)/bin_width_m, xmin_m, xmax_m)

    binning_pt = ( (xmax_pt - xmin_pt )/bin_width_pt, xmin_pt, xmax_pt )

    xvar_m = ROOT.RooRealVar( 'x_m', 'x_m',xmin_m , xmax_m)

    xvar_pt = ROOT.RooRealVar( 'x_pt', 'x_pt', xmin_pt, xmax_pt )

    signal_binning_m = { 200 : ( (xmax_m)/3 , 0, xmax_m ),
                         250 : ( (xmax_m)/3 , 0, xmax_m ),
                         300 : ( (xmax_m)/5 , 0, xmax_m ),
                         350 : ( (xmax_m)/5 , 0, xmax_m ),
                         400 : ( (xmax_m)/5 , 0, xmax_m ),
                         450 : ( (xmax_m)/5 , 0, xmax_m ),
                         500 : ( (xmax_m)/10 , 0, xmax_m ),
                         600 : ( (xmax_m)/10, 0, xmax_m ),
                         700 : ( (xmax_m)/10, 0, xmax_m ),
                         800 : ( (xmax_m)/15, 0, xmax_m ),
                         900 : ( (xmax_m)/15, 0, xmax_m ),
                        1000 : ( (xmax_m)/15, 0, xmax_m ),
                        1200 : ( (xmax_m)/20, 0, xmax_m ),
                        1400 : ( (xmax_m)/20, 0, xmax_m ),
                        1600 : ( (xmax_m)/20, 0, xmax_m ),
                        1800 : ( (xmax_m)/20, 0, xmax_m ),
                        2000 : ( (xmax_m)/20, 0, xmax_m ),
                       }

    signal_binning_pt = {}
    for mass, binning in signal_binning_m.iteritems() :
        pt_min = binning[1]/2.
        if pt_min < 50 :
            pt_min = 50
        signal_binning_pt[mass] = ( binning[0]/2., pt_min, binning[2]/2. )



    kine_vars = { #'mt_incl_lepph_z' : { 'var' : 'mt_lep_met_ph'   , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'m_incl_lepph_z'  : { 'var' : 'm_lep_met_ph'    , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  ##'mt_rotated'      : { 'var' : 'mt_rotated'      , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  'mt_fulltrans'    : { 'var' : 'mt_res'          , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'mt_constrwmass'  : { 'var' : 'recoM_lep_nu_ph' , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'ph_pt'           : { 'var' : 'ph_pt[0]'         , 'xvar' : xvar_pt , 'binning' : binning_pt, 'signal_binning' : signal_binning_pt },
                }

    selections = { 'base'    : { 
                                'mu' : { 'selection' : sel_base_mu }, 
                                'el' : { 'selection' : sel_base_el }, 
                               },
                   #'jetVeto' : { 'mu' : {'selection' : sel_jetveto_mu }, 
                   #              'el' : { 'selection' : sel_jetveto_el } ,
                   #            },
                 }

    workspace_wgamma            = ROOT.RooWorkspace( 'workspace_wgamma'   )
    workspace_wgammalo          = ROOT.RooWorkspace( 'workspace_wgammalo' )
    workspace_ttbar             = ROOT.RooWorkspace( 'workspace_ttbar'    )
    workspace_ttg               = ROOT.RooWorkspace( 'workspace_ttg'      )
    workspace_zgamma            = ROOT.RooWorkspace( 'workspace_zgamma'   )
    workspace_wjets             = ROOT.RooWorkspace( 'workspace_wjets'    )
    workspace_backgrounds       = ROOT.RooWorkspace( 'workspace_backgrounds' )
    workspace_gammagamma        = ROOT.RooWorkspace( 'workspace_gammagamma'  )

    lepg_samps = { 'mu' : sampManMuG, 'el' : sampManElG }
    #lepg_samps = { 'mu' : sampManMuG}

    for seltag, chdic in selections.iteritems() : 

        for ch, seldic in chdic.iteritems() : 

            if ch == 'mu':
               extra_label = "Muon Channel"
            else:
               extra_label = "Electron Channel"
                                    
            if options.doWGamma :

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'WGamma', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wgamma, extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )

            if options.doTopGamma : 

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'TTG',    seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_ttg,     extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots")

            if options.doTop :

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'TTbar',    seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_ttbar,     extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )

            if options.doZGamma: 


                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'Zgamma', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_zgamma,  extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots")

            if options.doWJets:
 
                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'Wjets', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wjets,  extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )

            if options.doGammaGamma:

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'GammaGamma', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_gammagamma,  extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )

            if options.doAll:
               
                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch],  [ 'WGamma', 'TTG', 'TTbar', 'Zgamma', 'Wjets', 'GammaGamma' ], seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_backgrounds,  extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )


    if options.outputDir is not None :

        if options.doTop : 
            workspace_ttbar.writeToFile( '%s/%s.root' %( options.outputDir,workspace_ttbar.GetName() ) )
        if options.doTopGamma:
            workspace_ttg.writeToFile( '%s/%s.root' %( options.outputDir,workspace_ttg.GetName() ) )
        if options.doWGamma :
            workspace_wgamma.writeToFile( '%s/%s.root' %( options.outputDir,workspace_wgamma.GetName() ) )
            workspace_wgammalo.writeToFile( '%s/%s.root' %( options.outputDir,workspace_wgammalo.GetName() ) )
        if options.doZGamma: 
            workspace_zgamma.writeToFile( '%s/%s.root' %( options.outputDir,workspace_zgamma.GetName() ) )
        if options.doWJets:
            workspace_wjets.writeToFile( '%s/%s.root' %( options.outputDir, workspace_wjets.GetName() ) )
        if options.doGammaGamma:
            workspace_gammagamma.writeToFile( '%s/%s.root' %( options.outputDir, workspace_gammagamma.GetName() ) )
        if options.doAll:
            workspace_backgrounds.writeToFile( '%s/%s.root' %( options.outputDir, workspace_backgrounds.GetName() ) )

        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        #for key, can in sampManMuG.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        #for key, can in sampManElG.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )

        #for key, result in sampManMuG.fitresults.iteritems():
        #    print "sample: %50s result %d chi2 %.2f"%(key, result.status(), sampManMuG.chi2[key])
        #    result.Print()


def get_mc_fit( sampMan, sampnames, sel_base, eta_cuts, xvar, plot_var, binning, workspace, extra_label = "Muon Channel", suffix='' , plots_dir = "plots") :

    if not os.path.isdir( plots_dir ) :
       os.makedirs( plots_dir )

    print "\n *****************\n calling get_mc_fit for, ", sampnames, "\n *********************\n"

    xmin = xvar.getMin()
    xmax = xvar.getMax()

    results = {}
 
    full_sel_sr = sel_base.replace("ADDITION", " (%s > %d && %s < %d )"%(plot_var, xmin, plot_var , xmax))
    print full_sel_sr

    outname = "Backgrounds"

    if isinstance(sampnames, str):
       outname = sampnames
       sampnames = [ sampnames ]
       #hist_sr    = clone_sample_and_draw( sampMan, sampname, plot_var, full_sel_sr   , binning )

    print sampnames

    # list of samples
    hist_sr = clone_sample_and_draw( sampMan, sampnames[0], plot_var, full_sel_sr   , binning )
    for isamp in sampnames[1:]:
        hist_sr.Add( clone_sample_and_draw( sampMan, isamp, plot_var, full_sel_sr   , binning ) )

    print " **** sampname %s number of total events %f **********"%(outname, hist_sr.Integral(0, 100000))
    print " **** sampname %s number of events %f **********"%(outname, hist_sr.Integral())

    ieta = "EB"

    label = '%s_%s_%s'%(outname, suffix, ieta)
       

    #fitManager = FitManager( 'dijet', 3, sampnames, hist_sr, plot_var, ieta, xvar, label, False)
    fitManager = FitManager( 'dijet', hist = hist_sr, xvardata = xvar, label = label, norders = 2 )
    #fitManager = FitManager( 'power', 2, sampnames, hist_sr, plot_var, ieta, xvar, label, options.useRooFit)

    #fitManager.setup_fit()
    fitManager.run_rootfit( (xmin, xmax) )

    #fit_distribution( fitManager, sampMan, workspace, logy=True )
    #fitManager.make_func_pdf()
    #fitManager.fit_histogram( workspace )
    """ cast it from TF1 to RooGenericPdf """
    fitManager.calculate_func_pdf()
    fitManager.get_results( workspace )
    #results[ieta] = save_distribution( fitManager, sampMan, workspace, logy=True )
    #fitManager.save_fit( sampMan, workspace, logy = True, stats_pos='right', extra_label = extra_label)
    canv = fitManager.draw( subplot = "pull" )
    canv.Print("%s/%s.pdf"%(plots_dir, label) )

    return results

def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

main()

