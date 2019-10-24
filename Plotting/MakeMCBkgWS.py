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
from IPython.core.debugger import Tracer
#ROOT.TVirtualFitter.SetMaxIterations( 100000 )
ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)
import sys
print sys.version

from SampleManager import SampleManager
from argparse import ArgumentParser
parser = ArgumentParser()

tColor_Off="\033[0m"       # Text Reset
tPurple="\033[0;35m%s"+tColor_Off       # Purple

parser.add_argument('--baseDirMuG',      default=None,           dest='baseDirMuG',         required=False, help='Path to signal samples in muon channel')
parser.add_argument('--baseDirElG',      default=None,           dest='baseDirElG',         required=False, help='Path to signal samples in muon channel')
parser.add_argument('--outputDir',       default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')
parser.add_argument('--batch',           default=False,     action='store_true',          dest='batch',              required=False, help='Supress X11 output')
parser.add_argument('--weightHistName',     default="weighthist",  type=str ,        dest='weightHistName',         help='name of weight histogram')
parser.add_argument('--useRooFit',       default=False,     action='store_true',      dest='useRooFit',    required=False, help='Make fits using roostats' )
parser.add_argument('--doSignal',        default=False,     action='store_true',      dest='doSignal',     required=False, help='make signal fits' )
parser.add_argument('--doWGamma',        default=False,     action='store_true',      dest='doWGamma',     required=False, help='make wgamma fits' )
parser.add_argument('--doTop',           default=False,     action='store_true',      dest='doTop',        required=False, help='make top fits' )
parser.add_argument('--doTopW',          default=False,     action='store_true',      dest='doTopW',        required=False, help='make topW fits' )
parser.add_argument('--doAllTop',        default=False,     action='store_true',      dest='doAllTop',        required=False, help='make all top fits' )
parser.add_argument('--doTopGamma',      default=False,     action='store_true',      dest='doTopGamma',   required=False, help='make topgamma fits' )
parser.add_argument('--doZGamma',        default=False,     action='store_true',      dest='doZGamma',     required=False, help='make ZGamma fits' )
parser.add_argument('--doWJets',         default=False,     action='store_true',      dest='doWJets',      required=False, help='make w+jets fits' )
parser.add_argument('--doGammaGamma',    default=False,     action='store_true',      dest='doGammaGamma', required=False, help='make GammaGamma fits')
parser.add_argument('--doEleFake',       default=False,     action='store_true',      dest='doEleFake',    required=False, help='make electron fake fits' )
parser.add_argument('--doClosure',       default=False,     action='store_true',      dest='doClosure',    required=False, help='make closure tests' )
parser.add_argument('--doAll',           default=False,     action='store_true',      dest='doAll',        required=False, help='make all backgrounds fits' )
parser.add_argument('--doNonMajor',           default=False,     action='store_true',      dest='doNonMajor',        required=False, help='make all non-major backgrounds fits' )

options = parser.parse_args()


_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon16.py'
_LUMI     = 36000
_BASEPATH = '/home/jkunkle/usercode/Plotting/LimitSetting/'
_SAMPCONF = 'Modules/Resonance2016.py'


ROOT.gROOT.SetBatch(False)
if options.batch:
    ROOT.gROOT.SetBatch(True)
if options.outputDir is not None :
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )
if options.outputDir is None :
    options.outputDir = "Plots/" + __file__.rstrip(".py")

def main() :

    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI , weightHistName=options.weightHistName )
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI , weightHistName=options.weightHistName )
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

    weight_str_mu = weight_str #+ '*(mu_trigSF*mu_idSF*mu_isoSF*mu_rcSF*ph_idSF*ph_psvSF*ph_csevSF)' ## FIXME
    weight_str_el = weight_str #+ '*(el_trigSF*el_idSF*el_recoSF*ph_idSF*ph_psvSF*ph_csevSF)'

    el_ip_str = '( fabs( el_d0[0] ) < 0.05 && fabs( el_dz[0] ) < 0.10 && fabs( el_sc_eta[0] )<= 1.479 ) || ( fabs( el_d0[0] ) < 0.10 && fabs( el_dz[0] ) < 0.20 && fabs( el_sc_eta[0] )> 1.479 )'

    el_tight = ' el_passVIDTight[0] == 1'
    el_eta   = ' fabs( el_eta[0] ) < 2.1 '

    ph_str         = 'ph_n==1 && ph_IsEB[0] && ph_pt[0] > 80 && ph_passMedium[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0]'
    ph_tightpt_str = 'ph_n==1 && ph_IsEB[0] && ph_pt[0] > 80 && ph_passMedium[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0]'

    met_str = 'met_pt > 25'

    Zveto_str = 'fabs(m_lep_ph-91)>15.0'

    sel_mu_nominal      = '%s * ( %s && %s && %s )'            %(  weight_str_mu,  sel_base_mu, ph_str, met_str)
    sel_el_nominal      = '%s * ( %s && %s && %s && %s && %s && %s && ( %s ))'     %(  weight_str_el, sel_base_el, el_tight, el_eta, ph_str, met_str, Zveto_str, el_ip_str )

    sel_mu_phpt_nominal      = '%s * ( %s && %s && %s && ADDITION)'            %(  weight_str_mu,  sel_base_mu, ph_tightpt_str, met_str)
    sel_el_phpt_nominal      = '%s * ( %s && %s && %s && %s && %s && %s && ( %s ) && ADDITION)'     %(  weight_str_el, sel_base_el, el_tight, el_eta, ph_tightpt_str, met_str, Zveto_str, el_ip_str )

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
    workspace_tw                = ROOT.RooWorkspace( 'workspace_tw'      )
    workspace_zgamma            = ROOT.RooWorkspace( 'workspace_zgamma'   )
    workspace_wjets             = ROOT.RooWorkspace( 'workspace_wjets'    )
    workspace_backgrounds       = ROOT.RooWorkspace( 'workspace_backgrounds' )
    workspace_nonmajor          = ROOT.RooWorkspace( 'workspace_nonmajor' )
    workspace_gammagamma        = ROOT.RooWorkspace( 'workspace_gammagamma'  )
    workspace_elefake           = ROOT.RooWorkspace( 'workspace_elefake' )

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

            if options.doTopW : 

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'TopW',    seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_tw,     extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots")

            if options.doAllTop :

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'AllTop',    seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_ttbar,     extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )

            if options.doTop :

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'AllTop',    seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_ttbar,     extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )

            if options.doZGamma:

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'Zgamma', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_zgamma,  extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots")

            if options.doWJets:
 
                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'Wjets', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wjets,  extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )


            if options.doEleFake:

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'Z+jets', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_elefake,  extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )

            if options.doGammaGamma:

                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'GammaGamma', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_gammagamma,  extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )

            if options.doAll:
                listall = ["WGamma", "AllTop", "Zgamma","Wjets","GammaGamma", "TopW"]
                #[ 'WGamma', 'TTG', 'TTbar', 'Zgamma', 'Wjets', 'GammaGamma']
                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], listall  , seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_backgrounds,  extra_label = extra_label, suffix='%s_%s_%s' %(ch,name,seltag ), plots_dir = options.outputDir + "/plots" )



    if options.outputDir is not None :

        if options.doTop : 
            workspace_ttbar.writeToFile( '%s/%s.root' %( options.outputDir,workspace_ttbar.GetName() ) )
        if options.doTopW:
            workspace_tw.writeToFile( '%s/%s.root' %( options.outputDir,workspace_tw.GetName() ) )
        if options.doTopGamma:
            workspace_ttg.writeToFile( '%s/%s.root' %( options.outputDir,workspace_ttg.GetName() ) )
        if options.doWGamma :
            workspace_wgamma.writeToFile( '%s/%s.root' %( options.outputDir,workspace_wgamma.GetName() ) )
            workspace_wgammalo.writeToFile( '%s/%s.root' %( options.outputDir,workspace_wgammalo.GetName() ) )
        if options.doZGamma: 
            workspace_zgamma.writeToFile( '%s/%s.root' %( options.outputDir,workspace_zgamma.GetName() ) )
        if options.doWJets:
            workspace_wjets.writeToFile( '%s/%s.root' %( options.outputDir, workspace_wjets.GetName() ) )
        if options.doWJets:
            workspace_elefake.writeToFile( '%s/%s.root' %( options.outputDir, workspace_elefake.GetName() ) )
        if options.doGammaGamma:
            workspace_gammagamma.writeToFile( '%s/%s.root' %( options.outputDir, workspace_gammagamma.GetName() ) )
        if options.doAll:
            workspace_backgrounds.writeToFile( '%s/%s.root' %( options.outputDir, workspace_backgrounds.GetName() ) )
        if options.doNonMajor:
            workspace_nonmajor.writeToFile( '%s/%s.root' %( options.outputDir, workspace_nonmajor.GetName() ) )

        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        for key, can in sampManMuG.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
            can.SaveAs('%s/%s.png' %( options.outputDir, key ) )
            can.SaveAs('%s/%s.C' %( options.outputDir, key ) )
        for key, can in sampManElG.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
            can.SaveAs('%s/%s.png' %( options.outputDir, key ) )
            can.SaveAs('%s/%s.C' %( options.outputDir, key ) )

        #for key, result in sampManMuG.fitresults.iteritems():
        #    print "sample: %50s result %d chi2 %.2f"%(key, result.status(), sampManMuG.chi2[key])
        #    result.Print()


def get_mc_fit( sampMan, sampnames, sel_base, eta_cuts, xvar, plot_var, binning, workspace, extra_label = "Muon Channel", suffix='' , plots_dir = "plots") :

    if not os.path.isdir( plots_dir ) :
       os.makedirs( plots_dir )

    print "\n *****************\n calling get_mc_fit for, ", tPurple %(sampnames), "\n *********************\n"

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

    fitfunc = "dijet"
    label = '%s_%s_%s_%s'%(outname, suffix, ieta, fitfunc)


    #fitManager = FitManager( 'dijet', 3, sampnames, hist_sr, plot_var, ieta, xvar, label, False)
    if fitfunc == "dijet": fitManager = FitManager( 'dijet', hist = hist_sr, xvardata = xvar, label = label, norders = 2 )
    #fitManager = FitManager( 'power', 2, sampnames, hist_sr, plot_var, ieta, xvar, label, options.useRooFit)
    if fitfunc == "power": fitManager = FitManager( 'power', hist_sr, xvar, label, norders =1)
    if fitfunc == "atlas": fitManager = FitManager( 'atlas', hist_sr, xvar, label, norders =1)
    #Tracer()()
    canv = fitManager.draw(  paramlayout = (0.7,0.5,0.82), useOldsetup = True, logy=1, yrange=(5e-3, 2e4) )

    #fitManager.setup_fit()
    fitManager.setup_rootfit( (xmin, xmax) )
    fitManager.func.Draw("same")
    canv.Print("%s/%sbefore.pdf"%(plots_dir, label) )
    canv.Print("%s/%sbefore.png"%(plots_dir, label) )
    canv.Print("%s/%sbefore.C"%(plots_dir, label) )
    fitManager.run_rootfit()

    #fit_distribution( fitManager, sampMan, workspace, logy=True )
    #fitManager.make_func_pdf()
    #fitManager.fit_histogram( workspace )
    """ cast it from TF1 to RooGenericPdf """
    #Tracer()()
    fitManager.calculate_func_pdf()
    fitManager.get_results( workspace )
    #results[ieta] = save_distribution( fitManager, sampMan, workspace, logy=True )
    #fitManager.save_fit( sampMan, workspace, logy = True, stats_pos='right', extra_label = extra_label)
    canv = fitManager.draw( subplot = "pull", paramlayout = (0.7,0.5,0.82), useOldsetup = True, logy=1, yrange=(5e-3, 2e4) )
    canv.Print("%s/%s.pdf"%(plots_dir, label) )
    canv.Print("%s/%s.png"%(plots_dir, label) )
    canv.Print("%s/%s.C"%(plots_dir, label) )

    return results

def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

main()

