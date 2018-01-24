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

parser.add_argument('--baseDirMuGNoId',      default=None,           dest='baseDirMuGNoId',         required=False, help='Path to muon base directory')
parser.add_argument('--baseDirElGNoId',      default=None,           dest='baseDirElGNoId',         required=False, help='Path to electron base directory')
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


def get_cut_defaults( shape_var, ieta ) :

    cut_defaults = {'sigmaIEIE' : { 'EB' : ( 0.012, 0.02 ), 'EE' : ( 0.0, 0.0 ) },
                    'chIso'     : { 'EB' : ( 4, 10 ),       'EE' : (4, 10) },
                   }

    return cut_defaults[shape_var][ieta]


ROOT.gROOT.SetBatch(False)
if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

def main() :

    sampManMuGNoId = SampleManager( options.baseDirMuGNoId, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElGNoId = SampleManager( options.baseDirElGNoId, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    sampManMuGNoId.ReadSamples( _SAMPCONF )
    sampManElGNoId.ReadSamples( _SAMPCONF )
    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

    sampManMuGNoId.outputs = {}
    sampManElGNoId.outputs = {}
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

    signal_binning_m = { 200 : ( (xmax_m)/5 , 0, xmax_m ),
                         250 : ( (xmax_m)/5 , 0, xmax_m ),
                         300 : ( (xmax_m)/5 , 0, xmax_m ),
                         350 : ( (xmax_m)/5 , 0, xmax_m ),
                         400 : ( (xmax_m)/5 , 0, xmax_m ),
                         450 : ( (xmax_m)/5 , 0, xmax_m ),
                         500 : ( (xmax_m)/10 , 0, xmax_m ),
                         600 : ( (xmax_m)/10, 0, xmax_m ),
                         700 : ( (xmax_m)/10, 0, xmax_m ),
                         800 : ( (xmax_m)/10, 0, xmax_m ),
                         900 : ( (xmax_m)/10, 0, xmax_m ),
                        1000 : ( (xmax_m)/10, 0, xmax_m ),
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

    workspace_signal   = ROOT.RooWorkspace( 'workspace_signal' )
    workspace_wgamma   = ROOT.RooWorkspace( 'workspace_wgamma' )
    workspace_wgammalo = ROOT.RooWorkspace( 'workspace_wgammalo' )
    workspace_top    = ROOT.RooWorkspace( 'workspace_top' )
    workspace_zgamma = ROOT.RooWorkspace( 'workspace_zgamma' )
    wjets            = ROOT.RooWorkspace( 'workspace_wjets' )
    elefake          = ROOT.RooWorkspace( 'elefake' )

    lepg_samps = { 'mu' : sampManMuG, 'el' : sampManElG }

    for seltag, chdic in selections.iteritems() : 

        for ch, seldic in chdic.iteritems() : 
                                    
            if options.doSignal : 

                for name, vardata in kine_vars.iteritems() :

                    make_signal_fits( lepg_samps[ch], seldic['selection'], eta_cuts, vardata['var'], vardata['xvar'], vardata['signal_binning'], workspace_signal, suffix='%s_%s_%s'%(ch,name,seltag ) )
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

            if options.doWJets :

                    make_wjets_fit( sampManMuGNoId, 'Data', seldic['selection'], 'EB', vardata['var'], 'chIso', 'sigmaIEIE', vardata['binning'], vardata['xvar'], suffix='wjets_%s_EB_%s' %(ch,seltag), closure=False, workspace=wjets)

            if options.doEleFake : 

                if ch == 'el' :
                    elefake_res = make_elefake_fit( sampManElGNoId, 'EleFakeBackground', seldic['selection'], 'EB', 'mt_lep_met_ph',  (100, 0, 1000), xvar_m, workspace=elefake )

            if options.doClosure :

                closure_res_mu = make_wjets_fit( sampManMuGNoId, 'Wjets', seldic['selection'], 'EB', 'mt_lep_met_ph', 'chIso', 'sigmaIEIE', binning_m, xvar_m, suffix='closure_%s_EB_%s' %( ch, seltag ), closure=True )

    if options.outputDir is not None :

        if options.doSignal : 
            workspace_signal.writeToFile( '%s/%s.root' %( options.outputDir,workspace_signal.GetName() ) )
        if options.doTop : 
            workspace_top.writeToFile( '%s/%s.root' %( options.outputDir,workspace_top.GetName() ) )
        if options.doWGamma :
            workspace_wgamma.writeToFile( '%s/%s.root' %( options.outputDir,workspace_wgamma.GetName() ) )
            workspace_wgammalo.writeToFile( '%s/%s.root' %( options.outputDir,workspace_wgammalo.GetName() ) )
        if options.doZGamma: 
            workspace_zgamma.writeToFile( '%s/%s.root' %( options.outputDir,workspace_zgamma.GetName() ) )
        if options.doWJets :
            wjets.writeToFile( '%s/%s.root' %( options.outputDir,wjets.GetName() ) )
        if options.doEleFake : 
            elefake.writeToFile( '%s/%s.root' %( options.outputDir,elefake.GetName() ) )


        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        for key, can in sampManMuGNoId.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        for key, can in sampManElGNoId.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        for key, can in sampManMuG.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        for key, can in sampManElG.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )

#def make_toy_data( out_workspace, in_workspace, in_pdf, suffix='' ) :
#
#    in_workspace.Print()
#
#    pdf = in_workspace.pdf( in_pdf )
#
#    nevents = in_workspace.var( 'norm_%s' %in_pdf )
#
#    #dataset = pdf.generate( in_workspace.var('xvar'), Name='toydata%s' %suffix  )
#    dataset = pdf.generate( ROOT.RooArgSet(in_workspace.var('x')), nevents )
#    dataset.SetName( 'toydata%s' %suffix )
#    print dataset
#
#    getattr( out_workspace, 'import' )( dataset )



def make_signal_fits( sampMan, sel_base, eta_cuts, plot_var, xvar, binning, workspace, suffix ) : 

    sampMan.clear_hists()

    for samp in sampMan.get_samples(isSignal=True ) :

        print 'Sample = ', samp.name

        res = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_width(\d|0p01)', samp.name )
        if res is None :
            print 'Could not interpret path ', samp.name
        else :
            mass = float(res.group(2))
            width = res.group(3)
            if width == '0p01' :
                width = 0.0001
            else :
                width = float( width )

        if mass != 450 : 
            continue

        ph_selection_sr = '%s==1' %defs.get_phid_selection('all')
        ph_idx_sr =  defs.get_phid_idx( 'all' )
        print binning[mass]
        addtl_cuts_sr = 'ph_pt[%s] > 50  && %s > %f && %s < %f ' %(ph_idx_sr, plot_var, binning[mass][1], plot_var, binning[mass][2] )

        xvar.setBins(10000,'cache')
        xvar.setMin('cache',-100)
        xvar.setMax('cache',1500)

        for ieta in eta_cuts :

            full_suffix = '%s_%s_%s' %(samp.name, suffix, ieta)

            eta_str_sr = 'ph_Is%s[%s]' %( ieta, ph_idx_sr )

            full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr, eta_str_sr, addtl_cuts_sr] )

            #hist_sr    = clone_sample_and_draw( sampMan, sampname, plot_var, full_sel_sr, binning )
            sampMan.create_hist( samp, plot_var, full_sel_sr, binning[mass] ) 

            hist_sr = samp.hist

            integral = hist_sr.Integral()

            #hist_sr.Scale( 1.0/integral )

            datahist = ROOT.RooDataHist( 'srhist_%s' %full_suffix, 'srhist', ROOT.RooArgList(xvar), hist_sr)

            #histpdf = ROOT.RooHistPdf( 'srhistpdf_%s' %(full_suffix), 'srhistpdf' , ROOT.RooArgSet( xvar), datahist, 3 )

            fit_min = 0
            fit_max = mass*1.1
            fit_min = mass/2.
            if mass >= 1000 :
                fit_max = mass*1.05
                fit_min = mass*0.7

            ##------------------------------
            ## Breit-Wigner, has two parameters, the resonance mass and the width
            #------------------------------
            bw_width = mass*width
            #if bw_width < 0.05 : 
            bw_width = 0.05
            bw_m = ROOT.RooRealVar('bw_mass' , 'Resonance  Mass', mass, fit_min, fit_max, 'GeV')
            bw_w = ROOT.RooRealVar('bw_width', 'Breit-Wigner width',bw_width, 0, 200,'GeV')
            bw_m.setConstant()
            bw_w.setConstant()
            bw = ROOT.RooBreitWigner('bw' ,'A Breit-Wigner Distribution', xvar, bw_m,bw_w)

            ##------------------------------
            ## Gaussian, has two parameters, the resonance mass and the width
            ##------------------------------
            #gaus_width_val = mass*width
            #if gaus_width_val < 2. :
            #    gaus_width_val = 2.0
            #gaus_m = ROOT.RooRealVar('gaus_mass' , 'Resonance  Mass', mass, fit_min, fit_max,'GeV')
            #gaus_w = ROOT.RooRealVar('gaus_width', 'Breit-Wigner width',gaus_width_val , -100, 100,'GeV')
            #gaus_m.setConstant()
            ##gaus_w.setConstant()
            #gaus = ROOT.RooGaussian('gaus%s' %suffix,'A Gaussian Distribution', xvar, gaus_m,gaus_w)


            #------------------------------
            # crystal ball, has four parameters
            #------------------------------
            cb_cut   = ROOT.RooRealVar('cb_cut'   , 'Cut'  , 0.5, 0.38, 0.60 , '')
            cb_sigma = ROOT.RooRealVar('cb_sigma' , 'Width', 28.49, 5  , 100, 'GeV')
            cb_power = ROOT.RooRealVar('cb_power' , 'Power', 30.,   0.    , 130., '')
            cb_m0    = ROOT.RooRealVar('cb_mass'  , 'mass' , -18.84, -100.  , 0.,'GeV')

            #cb_cut = ROOT.RooRealVar('cb_cut'      , 'Cut'  , 0.3851, 0.22, 0.52 , '')
            #cb_cut = ROOT.RooRealVar('cb_cut'      , 'Cut'  , 0.438, 0.38, 0.50 , '')
            cb_cut = ROOT.RooRealVar('cb_cut'      , 'Cut'  , 0.5, 0.38, 0.60 , '')
            #cb_sigma = ROOT.RooRealVar('cb_sigma' , 'Width', 28.49, 20  , 40, 'GeV')
            cb_sigma = ROOT.RooRealVar('cb_sigma' , 'Width', 26.5, 24.  , 30., 'GeV')
            #cb_power = ROOT.RooRealVar('cb_power'      , 'Power', 30., 0.    , 130., '')
            cb_power = ROOT.RooRealVar('cb_power'      , 'Power', 2.415, 2.2    , 2.6, '')
            #cb_m0 = ROOT.RooRealVar('cb_mass' , 'mass' , -18.84, -20. , -15.,'GeV')
            cb_m0 = ROOT.RooRealVar('cb_mass' , 'mass' , -17.451, -19. , -15.,'GeV')
            cb_cut.setConstant()

            cb_cut.setError( 0.05 )
            cb_sigma.setError( 0.5 )
            cb_power.setError( 1. )
            cb_m0.setError( 1. )

            cb = ROOT.RooCBShape('cb', 'A  Crystal Ball Lineshape', xvar, cb_m0, cb_sigma,cb_cut,cb_power)

            model = ROOT.RooFFTConvPdf('sig_model','Convolution', xvar, bw, cb)

            datahist = ROOT.RooDataHist( 'datahist', 'datahist', ROOT.RooArgList(xvar), hist_sr )

            #model.fitTo( datahist, ROOT.RooFit.Range( fit_min, fit_max) ,ROOT.RooFit.SumW2Error(True) , ROOT.RooCmdArg( 'Minimizer', 0,0,0,0,'GSLMultiMin' ))
            #model.fitTo( datahist, ROOT.RooFit.Range( fit_min, fit_max) ,ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Minos', 1 ) )
            #model.fitTo( datahist, ROOT.RooFit.Range( fit_min, fit_max) ,ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Minos', 0 ) )
            model.fitTo( datahist, ROOT.RooFit.Range( fit_min, fit_max) ,ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Strategy', 3 ) )

            cb_sigma.setVal( cb_sigma.getValV() )
            cb_sigma.setMin( cb_sigma.getValV() - cb_sigma.getErrorLo() )
            cb_sigma.setMin( cb_sigma.getValV() + cb_sigma.getErrorHi() )
            model.fitTo( datahist, ROOT.RooFit.Range( fit_min, fit_max) ,ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Strategy', 3 ) )

            ## Construct unbinned likelihood of model w.r.t. data
            #nll = model.createNLL(datahist) ;
            #raw_input('cont1')
            ##// I n t e r a c t i v e   m i n i m i z a t i o n ,   e r r o r   a n a l y s i s
            ##// -------------------------------------------------------------------------------
            ##// Create MINUIT interface object
            #m = ROOT.RooMinimizer(nll) 
            #raw_input('cont2')
            ##// Activate verbose logging of MINUIT parameter space stepping
            #m.setVerbose(ROOT.kTRUE) 
            #raw_input('cont3')
            ##// Call MIGRAD to minimize the likelihood
            #m.migrad() 
            #raw_input('cont4')
            ##// Print values of all parameters, that reflect values (and error estimates)
            ##// that are back propagated from MINUIT
            #model.getParameters(ROOT.RooArgSet(xvar)).Print("s") 
            #raw_input('cont5')
            ##// Disable verbose logging
            #m.setVerbose(ROOT.kFALSE) 
            #raw_input('cont6')
            ##// Run HESSE to calculate errors from d2L/dp2
            #m.hesse() 
            #raw_input('cont7')
            ##// Print value (and error) of sigma_g2 parameter, that reflects
            ##// value and error back propagated from MINUIT
            #cb.Print() 
            #raw_input('cont8')
            #bw.Print() 
            #raw_input('cont9')
            #cb_cut.Print()
            #raw_input('cont10')
            #cb_sigma.Print()
            #raw_input('cont11')
            #cb_power.Print()
            #raw_input('cont12')
            #cb_m0.Print()
            #raw_input('cont13')
            ##// Run MINOS on sigma_g2 parameter only
            #m.minos(ROOT.RooArgSet(cb_power)) 
            #raw_input('cont14')
            #cb_power.Print()
            #raw_input('cont15')
            ##// Print value (and error) of sigma_g2 parameter, that reflects
            ##// value and error back propagated from MINUIT
            #sigma_g2.Print() ;


            can = ROOT.TCanvas( 'signal_can_%s' %( full_suffix ), '' )
            frame = xvar.frame(fit_min, fit_max) 
            datahist.plotOn(frame)
            model.plotOn( frame )
            model.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.1,0.5,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(3)));
            frame.Draw()

            #frame = xvar.frame()

            #datahist.plotOn( frame )
            #histpdf.plotOn( frame )

            #frame.Draw()
            sampMan.outputs[can.GetName()] = can

            norm_var = ROOT.RooRealVar( 'srhist_%s_norm' %( full_suffix ), 'signal normalization', integral )

            xs_var = ROOT.RooRealVar( 'cross_section_%s' %full_suffix, 'Cross section', samp.cross_section )
            tot_evt = ROOT.RooRealVar( 'total_events_%s' %full_suffix, 'Total Events', samp.total_events)
            scale = ROOT.RooRealVar( 'scale_%s' %full_suffix, 'Scale', samp.scale)

            getattr(workspace, 'import' )(model)
            getattr(workspace, 'import' )(datahist)
            getattr(workspace, 'import' )(norm_var)
            getattr(workspace, 'import' )(xs_var)
            getattr(workspace, 'import' )(tot_evt)
            getattr(workspace, 'import' )(scale)


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

        results[ieta] = fit_distribution( fitManager, sampMan, workspace )

    return results

def make_elefake_fit( sampMan, sample, sel_base, eta_cut, plot_var, binning, xvar, suffix='', closure=False, workspace=None) :

    ph_selection = 'ph_n==1 && ph_eleVeto[0] == 0 && ph_pt[0] > 50 ' 

    eta_selection = 'ph_Is%s[0]' %eta_cut

    weight_str = defs.get_weight_str()

    full_selection = ' %s * ( %s ) ' %( weight_str, ' && '.join( [sel_base, ph_selection, eta_selection] ) )

    hist_mc = clone_sample_and_draw( sampMan, sample, plot_var, full_selection, binning )
    result = fit_distribution( 'dijet', 2, hist_mc, xvar, 'EleFake', sampMan, workspace  )

    sampMan.outputs['EleFake'].Draw()


def make_wjets_fit( sampMan, sample, sel_base, eta_cut, plot_var, shape_var, num_var, binning, xvar, suffix='', closure=False, workspace=None) :

    ph_selection_sr = '%s==1' %defs.get_phid_selection('medium')
    ph_selection_den = '%s==1'%defs.get_phid_selection( num_var, shape_var )

    ph_selection_num = '%s==1' %defs.get_phid_selection( num_var )
    ph_selection_shape = '%s==1' %defs.get_phid_selection( shape_var )

    ph_idx_sr =  defs.get_phid_idx( 'medium' )
    ph_idx_den = defs.get_phid_idx( num_var, shape_var )
    ph_idx_num = defs.get_phid_idx( num_var )
    ph_idx_shape = defs.get_phid_idx( shape_var )

    xmin = xvar.getMin()
    xmax = xvar.getMax()

    addtl_cuts_sr = 'ph_pt[%s] > 50 && %s > %d && %s < %d '     %( ph_idx_sr, plot_var, xmin, plot_var, xmax )
    addtl_cuts_den = 'ph_pt[%s] > 50 && %s > %d && %s < %d  '   %( ph_idx_den, plot_var, xmin, plot_var, xmax )
    addtl_cuts_num = 'ph_pt[%s] > 50 && %s > %d && %s < %d  '   %( ph_idx_num, plot_var, xmin, plot_var, xmax )
    addtl_cuts_shape = 'ph_pt[%s] > 50 && %s > %d && %s < %d  ' %( ph_idx_shape, plot_var, xmin, plot_var, xmax )

    cut_var_shape = defs.get_phid_cut_var( shape_var )
    cut_var_num = defs.get_phid_cut_var( num_var )

    eta_str_shape = 'ph_Is%s[%s]' %( eta_cut, ph_idx_shape )
    eta_str_den = 'ph_Is%s[%s]' %( eta_cut, ph_idx_den)
    eta_str_num = 'ph_Is%s[%s]' %( eta_cut, ph_idx_num )
    eta_str_sr = 'ph_Is%s[%s]' %( eta_cut, ph_idx_sr )

    cut_vals_shape = get_cut_defaults( shape_var, eta_cut )
    cut_vals_num = get_cut_defaults( num_var, eta_cut )

    cut_str_base = ' {var}[{idx}] > {val_low} && {var}[{idx}] < {val_high}'

    cut_str_shape = cut_str_base.format(var=cut_var_shape, idx=ph_idx_shape, val_low=cut_vals_shape[0], val_high=cut_vals_shape[1] )
    cut_str_num = cut_str_base.format(var=cut_var_num, idx=ph_idx_num, val_low=cut_vals_num[0], val_high=cut_vals_num[1] )

    cut_str_den_1 = cut_str_base.format(var=cut_var_shape, idx=ph_idx_den, val_low=cut_vals_shape[0], val_high=cut_vals_shape[1] )
    cut_str_den_2 = cut_str_base.format(var=cut_var_num, idx=ph_idx_den, val_low=cut_vals_num[0], val_high=cut_vals_num[1] )

    cut_str_den = cut_str_den_1 + ' && ' + cut_str_den_2

    full_sel_shape = ' && '.join( [sel_base, ph_selection_shape, eta_str_shape, addtl_cuts_shape, cut_str_shape ] )
    full_sel_num   = ' && '.join( [sel_base, ph_selection_num, eta_str_num, addtl_cuts_num, cut_str_num] )
    full_sel_den   = ' && '.join( [sel_base, ph_selection_den, eta_str_den, addtl_cuts_den, cut_str_den] )
    full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr, eta_str_sr, addtl_cuts_sr] )

    label_shape = 'shape_%s' %suffix
    label_num   = 'num_%s' %suffix
    label_den   = 'den_%s' %suffix
    label_sr    = 'sr_%s' %suffix

    if workspace is None :
        ws = ROOT.RooWorkspace( 'ws') 
    else :
        ws = workspace

    hist_shape = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_shape, binning )
    result_shape= fit_distribution( 'dijet', 2, hist_shape, xvar, label_shape  , sampMan, ws  )
    hist_num   = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_num  , binning )
    result_num = fit_distribution(  'dijet', 2, hist_num, xvar, label_num , sampMan, ws )
    hist_den   = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_den  , binning )
    result_den = fit_distribution( 'dijet', 2,  hist_den, xvar, label_den , sampMan, ws )

    _integral_num =  ws.pdf( 'dijet_%s' %label_num ).getNormIntegral(ROOT.RooArgSet( xvar ) )
    func_integral_num  = _integral_num.getValV()
    _integral_den =  ws.pdf( 'dijet_%s' %label_den).getNormIntegral(ROOT.RooArgSet( xvar ) )
    func_integral_den  = _integral_den.getValV()
    _integral_shape =  ws.pdf( 'dijet_%s' %label_shape).getNormIntegral(ROOT.RooArgSet( xvar ) )
    func_integral_shape  = _integral_shape.getValV()

    hist_integral_num = result_num['integral'].n
    hist_integral_den = result_den['integral'].n
    hist_integral_shape = result_shape['integral'].n

    norm_num = hist_integral_num / func_integral_num
    norm_den = hist_integral_den / func_integral_den
    norm_shape = hist_integral_shape / func_integral_shape

    print 'func integral Num = ', func_integral_num
    print 'hist integral Num = ', hist_integral_num
    print 'normalization Num = ', norm_num

    print 'func integral Den = ', func_integral_den
    print 'hist integral Den = ', hist_integral_den
    print 'normalization Den = ', norm_den

    print 'func integral Shape = ', func_integral_shape
    print 'hist integral Shape = ', hist_integral_shape
    print 'normalization Shape = ', norm_shape

    power_pred_name    = 'power_pred_%s' %suffix
    logcoef_pred_name  = 'logcoef_pred_%s' %suffix
    #power_ratio_name   = 'power_ratio_%s' %suffix
    #logcoef_ratio_name = 'logcoef_ratio_%s' %suffix


    val_power_num   = ws.var( 'power_dijet_%s' %label_num   )
    val_power_den   = ws.var( 'power_dijet_%s' %label_den   )
    val_power_shape = ws.var( 'power_dijet_%s' %label_shape )

    val_logcoef_num   = ws.var( 'logcoef_dijet_%s' %label_num   )
    val_logcoef_den   = ws.var( 'logcoef_dijet_%s' %label_den   )
    val_logcoef_shape = ws.var( 'logcoef_dijet_%s' %label_shape )

    power_pred    = ROOT.RooRealVar( power_pred_name   , 'power'  , (val_power_num.getValV() + val_power_shape.getValV() - val_power_den.getValV()) , -100, 100)
    logcoef_pred  = ROOT.RooRealVar( logcoef_pred_name , 'logcoef', (val_logcoef_num.getValV() + val_logcoef_shape.getValV() - val_logcoef_den.getValV()), -10, 10 )
    #power_ratio   = ROOT.RooRealVar( power_ratio_name  , 'power'  , val_power_num - val_power_den , -100, 100)
    #logcoef_ratio = ROOT.RooRealVar( logcoef_ratio_name, 'logcoef', val_logcoef_num - val_logcoef_den, -10, 10 )

    can_ratio = ROOT.TCanvas( str(uuid.uuid4()), '' )

    func = 'TMath::Power(@0/13000, @1+@2*TMath::Log10(@0/13000))'  
    prediction = ROOT.RooGenericPdf('dijet_prediction_%s' %suffix , 'prediction', func, ROOT.RooArgList(xvar,power_pred, logcoef_pred))
    norm_pred = ROOT.RooRealVar( 'dijet_prediction_%s_norm' %(suffix), 'prediction normalization', (hist_integral_shape * hist_integral_num) / hist_integral_den )
    getattr( ws , 'import' ) ( norm_pred )
    getattr( ws , 'import' ) ( prediction )

    ratio_func = ROOT.TF1( 'ratio_func', '( [2]*TMath::Power(x/13000, [0] + [1]*TMath::Log10(x/13000) ) ) ', xmin, xmax )

    ratio_func.SetParameter(0, result_num['power'].n - result_den['power'].n)
    ratio_func.SetParameter(1, result_num['logcoef'].n  - result_den['logcoef'].n )
    ratio_func.SetParameter(2, norm_num / norm_den )

    ratiohist = hist_num.Clone( 'closure_ratio_%s' %(suffix) )
    ratiohist.Divide( hist_den )
    ratiohist.SetMarkerStyle(20)
    ratiohist.SetMarkerSize(1)
    ratiohist.GetXaxis().SetTitle( 'Transverse Mass [GeV]' )
    ratiohist.GetYaxis().SetTitle( 'ratio of passing to failing %s' %shape_var )
    ratiohist.Draw()
    ratiohist.SetStats(0)

    ratio_func.Draw('same')

    ratio_power_v = val_power_num.getValV() - val_power_den.getValV()
    ratio_power_e = math.sqrt(val_power_num.getErrorHi()*val_power_num.getErrorHi() + val_power_den.getErrorHi()*val_power_den.getErrorHi() )
    ratio_logcoef_v = val_logcoef_num.getValV() - val_logcoef_den.getValV()
    ratio_logcoef_e = math.sqrt(val_logcoef_num.getErrorHi()*val_logcoef_num.getErrorHi() + val_logcoef_den.getErrorHi()*val_logcoef_den.getErrorHi() )

    power_tex   = ROOT.TLatex(0, 0, 'power = %.01f #pm %.02f' %( ratio_power_v,  ratio_power_e ))
    logcoef_tex = ROOT.TLatex(0, 0, 'logcoef = %.01f #pm %.02f' %( ratio_logcoef_v,  ratio_logcoef_e ))

    power_tex.SetNDC()
    logcoef_tex.SetNDC()

    power_tex  .SetX( 0.6 )
    power_tex  .SetY( 0.84 )
    logcoef_tex.SetX( 0.6 )
    logcoef_tex.SetY( 0.78 )

    power_tex.Draw()
    logcoef_tex.Draw()

    if closure :
        sampMan.outputs['wjetsclosure_ratio_%s' %suffix] = can_ratio 
    else :
        sampMan.outputs['wjets_ratio_%s' %suffix] = can_ratio 
    
    if closure :

        hist_sr    = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_sr   , binning )
        result_sr  = fit_distribution( 'dijet', 2, hist_sr, xvar, label_sr, sampMan, ws )

        can_sr = ROOT.TCanvas( str(uuid.uuid4()), '' )

        pred_val = (hist_integral_shape * hist_integral_num) / hist_integral_den 

        tot_sr = hist_sr.Integral( hist_sr.FindBin( xmin ), hist_sr.FindBin( xmax ) )
        print 'SR integral = ', tot_sr
        sr_func = ROOT.TF1( 'sr_func', '( [2]*TMath::Power(x/13000, [0] + [1]*TMath::Log10(x/13000) ) ) ', xmin, xmax )
        sr_func.SetParameter(0, result_num['power'].n + result_shape['power'].n - result_den['power'].n )
        sr_func.SetParameter(1, result_num['logcoef'].n + result_shape['logcoef'].n - result_den['logcoef'].n )
        sr_func.SetParameter(2, 1 )
        sr_int = sr_func.Integral( xmin, xmax )
        print 'Normalization = ',(norm_shape*norm_num) / norm_den
        print 'func Integral SR Before = ', sr_func.Integral( xmin, xmax )
        sr_func.SetParameter(2, pred_val/sr_int )

        hist_sr.Draw()
        sr_func.Draw('same')

        sampMan.outputs['wjetsclosure_pred_%s' %suffix] = can_sr


        tot_ratio = result_num['integral']/result_den['integral']



def fit_pol1( hist, xmin, xmax ) :

    lin_func = ROOT.TF1( 'lin_func', '[0] + [1]*x', xmin, xmax )

    lin_func.SetParameter( 0, 0.5 )
    lin_func.SetParameter( 1, 0 )

    hist.Fit( lin_func, 'R' )

    hist.Draw()
    lin_func.Draw('same')

def fit_distribution( fitManager, sampMan=None, workspace=None ) :

    fitManager.fit_histogram()
    fitManager.calculate_func_pdf()

    if sampMan is not None :

        can = ROOT.TCanvas( str(uuid.uuid4()), '' )
        frame = fitManager.xvar.frame() 
        fitManager.datahist.plotOn(frame)
        fitManager.func_pdf.plotOn( frame )
        fitManager.func_pdf.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        ymax = frame.GetMaximum()
        frame.SetMinimum( 0.001 )
        frame.SetMaximum( ymax*10 )
        can.SetLogy()
        can.SetLogx()

        raw_input('cont')

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

    




    
    




