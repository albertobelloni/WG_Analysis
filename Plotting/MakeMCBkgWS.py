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

    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

    sampManMuG.outputs = {}
    sampManElG.outputs = {}

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
                  #'ph_pt'           : { 'var' : 'ph_pt[0]'        , 'xvar' : xvar_pt , 'binning' : binning_pt, 'signal_binning' : signal_binning_pt },
                }

    selections = { 'base'    : { 
                                'mu' : {'selection' : sel_base_mu }, 
                                 #'el' : { 'selection' : sel_base_el }, 
                               },
                   #'jetVeto' : { 'mu' : {'selection' : sel_jetveto_mu }, 
                   #              'el' : { 'selection' : sel_jetveto_el } ,
                   #            },
                 }

    workspace_wgamma   = ROOT.RooWorkspace( 'workspace_wgamma' )
    workspace_wgammalo = ROOT.RooWorkspace( 'workspace_wgammalo' )
    workspace_top    = ROOT.RooWorkspace( 'workspace_top' )
    workspace_zgamma = ROOT.RooWorkspace( 'workspace_zgamma' )

    lepg_samps = { 'mu' : sampManMuG, 'el' : sampManElG }

    for seltag, chdic in selections.iteritems() : 

        for ch, seldic in chdic.iteritems() : 
                                    
            if options.doWGamma :


                for name, vardata in kine_vars.iteritems() :

                    #get_mc_fit( lepg_samps[ch], 'WGToLNuG-madgraphMLM', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wgamma, suffix='%s_%s_%s' %(ch,name,seltag ) )
                    #get_mc_fit( lepg_samps[ch], 'WGToLNuG_PtG-130-madgraphMLM', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wgamma, suffix='%s_%s_%s' %(ch,name,seltag ) )
                    #get_mc_fit( lepg_samps[ch], 'WGToLNuG_PtG-500-madgraphMLM', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wgamma, suffix='%s_%s_%s' %(ch,name,seltag ) )

                    #get_mc_fit( lepg_samps[ch], 'WGToLNuG_PtG-500-amcatnloFXFX', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wgamma, suffix='%s_%s_%s' %(ch,name,seltag ) )
                    #get_mc_fit( lepg_samps[ch], 'WGToLNuG_PtG-130-amcatnloFXFX', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wgamma, suffix='%s_%s_%s' %(ch,name,seltag ) )
                    #get_mc_fit( lepg_samps[ch], 'WGToLNuG-amcatnloFXFX', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wgamma, suffix='%s_%s_%s' %(ch,name,seltag ) )
                    get_mc_fit( lepg_samps[ch], 'WgammaLO', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wgammalo, suffix='%s_%s_%s' %(ch,name,seltag ) )
                    get_mc_fit( lepg_samps[ch], 'Wgamma', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_wgamma, suffix='%s_%s_%s' %(ch,name,seltag ) )
            if options.doTop : 


                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'TTG', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_top, suffix='%s_%s_%s' %(ch,name,seltag ) )

            if options.doZGamma: 


                for name, vardata in kine_vars.iteritems() :

                    get_mc_fit( lepg_samps[ch], 'Zgamma', seldic['selection'], eta_cuts, vardata['xvar'], vardata['var'], vardata['binning'], workspace_top, suffix='%s_%s_%s' %(ch,name,seltag ) )

    if options.outputDir is not None :

        if options.doTop : 
            workspace_top.writeToFile( '%s/%s.root' %( options.outputDir,workspace_top.GetName() ) )
        if options.doWGamma :
            workspace_wgamma.writeToFile( '%s/%s.root' %( options.outputDir,workspace_wgamma.GetName() ) )
            workspace_wgammalo.writeToFile( '%s/%s.root' %( options.outputDir,workspace_wgammalo.GetName() ) )
        if options.doZGamma: 
            workspace_zgamma.writeToFile( '%s/%s.root' %( options.outputDir,workspace_zgamma.GetName() ) )

        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        for key, can in sampManMuG.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        for key, can in sampManElG.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )


def get_mc_fit( sampMan, sampname, sel_base, eta_cuts, xvar, plot_var, binning, workspace, suffix='' ) :

    ph_selection_sr = 'ph_n == 1'
    xmin = xvar.getMin()
    xmax = xvar.getMax()
    addtl_cuts_sr = 'ph_pt[0] > 50 && %s > %d && %s < %d  ' %(plot_var, xmin, plot_var , xmax )

    results = {}

    for ieta in eta_cuts :

        eta_str_sr = 'ph_Is%s[0]' %( ieta )

        full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr, eta_str_sr, addtl_cuts_sr] )

        hist_sr    = clone_sample_and_draw( sampMan, sampname, plot_var, full_sel_sr   , binning )
        
        label = '%s_%s_%s'%(sampname, suffix, ieta)

        fitManager = FitManager( 'dijet', 2, sampname, hist_sr, plot_var, ieta, xvar, label, options.useRooFit)

        fit_distribution( fitManager, sampMan, workspace, logy=True )
        results[ieta] = save_distribution( fitManager, sampMan, workspace, logy=True )

    return results

def fit_pol1( hist, xmin, xmax ) :

    lin_func = ROOT.TF1( 'lin_func', '[0] + [1]*x', xmin, xmax )

    lin_func.SetParameter( 0, 0.5 )
    lin_func.SetParameter( 1, 0 )

    hist.Fit( lin_func, 'R' )

    hist.Draw()
    lin_func.Draw('same')

def fit_distribution( fitManager ) :

    fitManager.fit_histogram()
    fitManager.calculate_func_pdf()

def save_fit( fitManager, sampMan=None, workspace=None, logy=False, stats_pos='right' ) :

    if sampMan is not None :

        can = ROOT.TCanvas( str(uuid.uuid4()), '' )
        frame = fitManager.xvar.frame() 
        fitManager.datahist.plotOn(frame)
        fitManager.func_pdf.plotOn( frame )
        if stats_pos == 'left' : 
            fitManager.func_pdf.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.1,0.5,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(3)));
        if stats_pos == 'right' :
            fitManager.func_pdf.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        if logy :
            ymax = frame.GetMaximum()
            frame.SetMinimum( 0.001 )
            frame.SetMaximum( ymax*10 )
            can.SetLogy()
            can.SetLogx()

        sampMan.outputs[fitManager.label] = can

    integral = fitManager.Integral( )

    #power_res = ufloat( power.getValV(), power.getErrorHi() )
    #log_res   = ufloat( logcoef.getValV(), logcoef.getErrorHi())
    #int_res   = ufloat( integral, math.sqrt( integral ) )

    power_res = ufloat( 0, 0 )
    log_res   = ufloat( 0,0)
    int_res   = ufloat( 0, 0)

    integral_var = ROOT.RooRealVar('dijet_%s_norm' %( fitManager.label ), 'normalization', integral )

    #power.SetName( power_name )
    #logcoef.SetName( logcoef_name )

    if workspace is not None :
        getattr( workspace , 'import' ) ( fitManager.datahist )
        getattr( workspace , 'import' ) ( fitManager.func_pdf )
        getattr( workspace , 'import' ) ( integral_var )


    return {'power' : power_res, 'logcoef' : log_res, 'integral' : int_res, 'function_str' : fitManager.get_fit_function(), 'object' : fitManager.func_pdf }


def fit_dijet_3( hist, xvar, label='', sampMan=None, workspace=None ) :

    xmin = xvar.getMin()
    xmax = xvar.getMax()

    power_name = 'power_dijet3_%s'  %label
    logsqcoef_name = 'logcoef_dijet3_%s' %label
    logcoef_name = 'logcoef_dijet3_%s' %label

    power = ROOT.RooRealVar( 'power', 'power', -9.9, -100, 100)
    logsqcoef = ROOT.RooRealVar( 'logsqcoef', 'logsqcoef', -0.85, -10, 10 )
    logcoef = ROOT.RooRealVar( 'logcoef', 'logcoef', -0.85, -10, 10 )

    func = 'TMath::Power(@0/13000, @1+@2*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) + @3*TMath::Log10(@0/13000))'  
    dijet = ROOT.RooGenericPdf('dijet3_%s' %label, 'dijet3', func, ROOT.RooArgList(xvar,power, logsqcoef, logcoef))

    #datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )
    datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )

    dijet.fitTo( datahist, ROOT.RooFit.Range( xmin, xmax),ROOT.RooFit.SumW2Error(True)  )

    integral =  dijet.getNormIntegral(ROOT.RooArgSet( xvar ) )

    #power.setConstant()
    #logcoef.setConstant()

    if sampMan is not None :
        can = ROOT.TCanvas( str(uuid.uuid4()), '' )
        frame = xvar.frame() 
        datahist.plotOn(frame)
        dijet.plotOn( frame )
        dijet.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        ymax = frame.GetMaximum()
        frame.SetMinimum( 0.001 )
        frame.SetMaximum( ymax*10 )
        can.SetLogy()

        sampMan.outputs[label] = can

    integral = hist.Integral( hist.FindBin( xmin), hist.FindBin( xmax ) )

    power_res = ufloat( power.getValV(), power.getErrorHi() )
    log_res   = ufloat( logcoef.getValV(), logcoef.getErrorHi())
    int_res   = ufloat( integral, math.sqrt( integral ) )

    integral_var = ROOT.RooRealVar('dijet3_%s_norm' %( label ), 'normalization', integral )

    power.SetName( power_name )
    logcoef.SetName( logcoef_name )

    if workspace is not None :
        getattr( workspace , 'import' ) ( datahist )
        getattr( workspace , 'import' ) ( dijet )
        getattr( workspace , 'import' ) ( integral_var )


    return {'power' : power_res, 'logcoef' : log_res, 'integral' : int_res, 'function_str' : func, 'object' : dijet }

def fit_dijet_4( hist, xvar, label='', sampMan=None, workspace=None ) :

    xmin = xvar.getMin()
    xmax = xvar.getMax()

    power_name = 'power_dijet4_%s'  %label
    logcubcoef_name = 'logcubcoef_dijet4_%s' %label
    logsqcoef_name = 'logsqcoef_dijet4_%s' %label
    logcoef_name = 'logcoef_dijet4_%s' %label

    power = ROOT.RooRealVar( 'power', 'power', -9.9, -100, 100)
    logsqcoef = ROOT.RooRealVar( 'logsqcoef', 'logsqcoef', 0.0, -10, 10 )
    logcubcoef = ROOT.RooRealVar( 'logcubcoef', 'logcubcoef', 0.0, -10, 10 )
    #exp = ROOT.RooRealVar( 'exp', 'exp', -0.85, -10, 10 )
    logcoef = ROOT.RooRealVar( 'logcoef', 'logcoef', -0.85, -10, 10 )

    #func = 'TMath::Power(@0/13000, @1+@2*TMath::Log10(@0/13000))*TMath::Exp( @0*@3) '  
    func = 'TMath::Power(@0/13000, @1+@2*TMath::Log10(@0/13000)*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) +@3*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) + @4*TMath::Log10(@0/13000))'  
    dijet = ROOT.RooGenericPdf('dijet4_%s' %label, 'dijet4', func, ROOT.RooArgList(xvar,power, logcubcoef, logsqcoef, logcoef))

    #datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )
    datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )

    dijet.fitTo( datahist, ROOT.RooFit.Range( xmin, xmax),ROOT.RooFit.SumW2Error(True)  )

    integral =  dijet.getNormIntegral(ROOT.RooArgSet( xvar ) )

    #power.setConstant()
    #logcoef.setConstant()

    if sampMan is not None :
        can = ROOT.TCanvas( str(uuid.uuid4()), '' )
        frame = xvar.frame() 
        datahist.plotOn(frame)
        dijet.plotOn( frame )
        dijet.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        ymax = frame.GetMaximum()
        frame.SetMinimum( 0.001 )
        frame.SetMaximum( ymax*10 )
        can.SetLogy()

        sampMan.outputs[label] = can

    integral = hist.Integral( hist.FindBin( xmin), hist.FindBin( xmax ) )

    power_res = ufloat( power.getValV(), power.getErrorHi() )
    log_res   = ufloat( logcoef.getValV(), logcoef.getErrorHi())
    int_res   = ufloat( integral, math.sqrt( integral ) )

    integral_var = ROOT.RooRealVar('dijet3_%s_norm' %( label ), 'normalization', integral )

    power.SetName( power_name )
    logcoef.SetName( logcoef_name )

    if workspace is not None :
        getattr( workspace , 'import' ) ( datahist )
        getattr( workspace , 'import' ) ( dijet )
        getattr( workspace , 'import' ) ( integral_var )


    return {'power' : power_res, 'logcoef' : log_res, 'integral' : int_res, 'function_str' : func, 'object' : dijet }

def fit_dijet_mod( hist, xvar, label='', sampMan=None, workspace=None ) :

    xmin = xvar.getMin()
    xmax = xvar.getMax()

    power_name = 'power_dijetmod_%s'  %label
    logsqcoef_name = 'logcoef_dijetmod_%s' %label
    logcoef_name = 'logcoef_dijetmod_%s' %label

    numpower = ROOT.RooRealVar( 'numpower', 'numpower', -9.9, -100, 100)
    power = ROOT.RooRealVar( 'power', 'power', -9.9, -100, 100)
    logcoef = ROOT.RooRealVar( 'logcoef', 'logcoef', -0.85, -10, 10 )

    func = 'TMath::Power(@0/13000, @3)/(TMath::Power(@0/13000, @1+@2*TMath::Log10(@0/13000)))'  
    dijet = ROOT.RooGenericPdf('dijetmod_%s' %label, 'dijetmod', func, ROOT.RooArgList(xvar,power, logcoef, numpower))

    #datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )
    datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )

    dijet.fitTo( datahist, ROOT.RooFit.Range( xmin, xmax),ROOT.RooFit.SumW2Error(True)  )

    integral =  dijet.getNormIntegral(ROOT.RooArgSet( xvar ) )

    #power.setConstant()
    #logcoef.setConstant()

    if sampMan is not None :
        can = ROOT.TCanvas( str(uuid.uuid4()), '' )
        frame = xvar.frame() 
        datahist.plotOn(frame)
        dijet.plotOn( frame )
        dijet.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        ymax = frame.GetMaximum()
        frame.SetMinimum( 0.1 )
        frame.SetMaximum( ymax*5 )
        can.SetLogy()

        sampMan.outputs[label] = can

    integral = hist.Integral( hist.FindBin( xmin), hist.FindBin( xmax ) )

    power_res = ufloat( power.getValV(), power.getErrorHi() )
    log_res   = ufloat( logcoef.getValV(), logcoef.getErrorHi())
    int_res   = ufloat( integral, math.sqrt( integral ) )

    integral_var = ROOT.RooRealVar('dijetmod_%s_norm' %( label ), 'normalization', integral )

    power.SetName( power_name )
    logcoef.SetName( logcoef_name )

    if workspace is not None :
        getattr( workspace , 'import' ) ( datahist )
        getattr( workspace , 'import' ) ( dijet )
        getattr( workspace , 'import' ) ( integral_var )


    return {'power' : power_res, 'logcoef' : log_res, 'integral' : int_res, 'function_str' : func, 'object' : dijet }


def fit_exppow( hist, xvar, label='', sampMan=None, workspace=None ) :

    xmin = xvar.getMin()
    xmax = xvar.getMax()

    power_name = 'power_exppow_%s'  %label
    exp_name = 'exp_exppow_%s' %label

    power1 = ROOT.RooRealVar( 'power1', 'power1', -9.9, -100, 100)
    power2 = ROOT.RooRealVar( 'power2', 'power2', -9.9, -100, 100)
    #frac = ROOT.RooRealVar( 'frac', 'frac', 1, -100, 100 )

    #func = 'TMath::Power(@0/13000, @1)*TMath::Exp((@0/13000)*@1) + @2*TMath::Power(@0/13000, @3)*TMath::Exp((@0/13000)*@3)'  
    func = 'TMath::Power(@0/13000, @1)*TMath::Exp((@0/13000)*@2)'  
    dijet = ROOT.RooGenericPdf('exppow%s' %label, 'exppow', func, ROOT.RooArgList(xvar, power1, power2))

    #datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )
    datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )

    dijet.fitTo( datahist, ROOT.RooFit.Range( xmin, xmax),ROOT.RooFit.SumW2Error(True)  )

    integral =  dijet.getNormIntegral(ROOT.RooArgSet( xvar ) )

    #power.setConstant()
    #logcoef.setConstant()

    if sampMan is not None :
        can = ROOT.TCanvas( str(uuid.uuid4()), '' )
        frame = xvar.frame() 
        datahist.plotOn(frame)
        dijet.plotOn( frame )
        dijet.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        ymax = frame.GetMaximum()
        frame.SetMinimum( 0.1 )
        frame.SetMaximum( ymax*5 )
        can.SetLogy()

        sampMan.outputs[label] = can

    integral = hist.Integral( hist.FindBin( xmin), hist.FindBin( xmax ) )

    #power_res = ufloat( power.getValV(), power.getErrorHi() )
    #log_res   = ufloat( logcoef.getValV(), logcoef.getErrorHi())
    #int_res   = ufloat( integral, math.sqrt( integral ) )

    integral_var = ROOT.RooRealVar('exppow_%s_norm' %( label ), 'normalization', integral )

    #power.SetName( power_name )
    #logcoef.SetName( logcoef_name )

    if workspace is not None :
        getattr( workspace , 'import' ) ( datahist )
        getattr( workspace , 'import' ) ( dijet )
        getattr( workspace , 'import' ) ( integral_var )


    #return {'power' : power_res, 'logcoef' : log_res, 'integral' : int_res, 'function_str' : func, 'object' : dijet }
    return {}



def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

main()

    




    
    




