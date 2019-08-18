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

parser.add_argument('--baseDirMuNoG',      default=None,           dest='baseDirMuNoG',         required=False, help='Path to muon base directory')
parser.add_argument('--baseDirElNoG',      default=None,           dest='baseDirElNoG',         required=False, help='Path to electron base directory')
parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')

options = parser.parse_args()

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000
_BASEPATH = '/afs/cern.ch/work/f/friccita/WG_Analysis/Plotting/LimitSetting/'
#_BASEPATH = '/home/friccita/WGamma/WG_Analysis/Plotting/LimitSetting/'
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

    sampManMuNoG = SampleManager( options.baseDirMuNoG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElNoG = SampleManager( options.baseDirElNoG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    sampManMuNoG.ReadSamples( _SAMPCONF )
    sampManElNoG.ReadSamples( _SAMPCONF )

    sampManMuNoG.outputs = {}
    sampManElNoG.outputs = {}

    sel_base_mu = 'mu_pt30_n==1 && mu_n==1'
    sel_base_el = 'el_pt30_n==1 && el_n==1'

    #eta_cuts = ['EB', 'EE']
    eta_cuts = ['EB']

    workspaces_to_save = {}

    xmin_m = 160
    xmax_m = 2000
    bin_width_m = 20

    xmin_pt = xmin_m/2
    if xmin_pt < 50 :
        xmin_pt = 50
    xmax_pt = xmax_m/2
    bin_width_pt = bin_width_m/2.

    binning_m = ((xmax_m-xmin_m)/bin_width_m, xmin_m, xmax_m)

    binning_pt = ( (xmax_pt - xmin_pt )/bin_width_pt, xmin_pt, xmax_pt )

    #binning_leadjet_pt = (128, 0., 640.)
    xvar_m = ROOT.RooRealVar( 'x_m', 'x_m',xmin_m , xmax_m)

    xvar_pt = ROOT.RooRealVar( 'x_pt', 'x_pt', xmin_pt, xmax_pt )

    kine_vars = { #'mt_incl_lepph_z' : { 'var' : 'mt_lep_met_ph'   , 'xvar' : xvar_m  , 'binning' : binning_m},
                  #'m_incl_lepph_z'  : { 'var' : 'm_lep_met_ph'    , 'xvar' : xvar_m  , 'binning' : binning_m},
                  'mt_fulltrans'    : { 'var' : 'mt_res'          , 'xvar' : xvar_m  , 'binning' : binning_m},
                  #'mt_constrwmass'  : { 'var' : 'recoM_lep_nu_ph' , 'xvar' : xvar_m  , 'binning' : binning_m},
                  #'ph_pt'           : { 'var' : 'ph_pt[0]'        , 'xvar' : xvar_pt , 'binning' : binning_pt},
                }

    selections = { 'base'    : { 
                                'mu' : {'selection' : sel_base_mu }, 
                   #             'el' : { 'selection' : sel_base_el }, 
                               },
                   #'jetVeto' : { 'mu' : {'selection' : sel_jetveto_mu }, 
                   #              'el' : { 'selection' : sel_jetveto_el } ,
                   #            },
                 }

    workspace_signal   = ROOT.RooWorkspace( 'workspace_signal' )
    workspace_wgamma   = ROOT.RooWorkspace( 'workspace_wgamma' )
    workspace_wgammalo = ROOT.RooWorkspace( 'workspace_wgammalo' )
    workspace_top      = ROOT.RooWorkspace( 'workspace_top' )
    workspace_zgamma   = ROOT.RooWorkspace( 'workspace_zgamma' )
    wjets              = ROOT.RooWorkspace( 'workspace_wjets' )
    elefake            = ROOT.RooWorkspace( 'elefake' )

    for seltag, chdic in selections.iteritems() : 

        for ch, seldic in chdic.iteritems() : 

            for name, vardata in kine_vars.iteritems() :
                                    
                print 'MC background k-factor calculation'
                make_kfactor_calc( sampManMuNoG, 'Wjets', seldic['selection'], False, suffix='wjets_%s' %(ch), workspace=wjets)
                make_kfactor_calc( sampManMuNoG, 'Wgamma', seldic['selection'], False, suffix='wjets_%s' %(ch), workspace=wjets)
                make_kfactor_calc( sampManMuNoG, 'Zgamma', seldic['selection'], False, suffix='wjets_%s' %(ch), workspace=wjets)
                make_kfactor_calc( sampManMuNoG, 'AllTop', seldic['selection'], False, suffix='wjets_%s' %(ch), workspace=wjets)
                make_kfactor_calc( sampManMuNoG, 'Z+jets', seldic['selection'], False, suffix='wjets_%s' %(ch), workspace=wjets)
                make_kfactor_calc( sampManMuNoG, 'Data', seldic['selection'], True, suffix='wjets_%s' %(ch), workspace=wjets)


    if options.outputDir is not None :

        wjets.writeToFile( '%s/outfile_kfactor.root' %( options.outputDir ) )

        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        outputFile = ROOT.TFile('%s/outfile_kfactor.root' %( options.outputDir ),'recreate')
        for key, can in sampManMuNoG.outputs.iteritems() :
            can.Write( '%s' %(key) )
        for key, can in sampManElNoG.outputs.iteritems() :
            can.Write( '%s' %(key) )

        #for key, can in sampManMuNoG.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        #for key, can in sampManElNoG.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )




#def make_kfactor_calc( sampMan, sample, sel_base, plot_var, binning, suffix='', workspace=None) :
def make_kfactor_calc( sampMan, sample, sel_base, isdata=False, suffix='', workspace=None) :

    #---------------------------------------
    # W selection for lepton
    #---------------------------------------
    
    #w_selection = 'mt_lep_met > 50. && mt_lep_met < 100. && mu_pt[0] > 50.'
    w_selection = 'mt_lep_met > 50. && mu_pt[0] > 50. && mu_hasTrigMatch[0] && mu_eta[0] < 2.4 && mu_eta[0] > -2.4 && mu_passTight[0]'
    smpvj_selection = 'mu_pt30_n==1 && mu_n==1 && mu_eta[0] > -2.4 && mu_eta[0] < 2.4 && mu_hasTrigMatch[0] && mu_passTight[0] && mt_lep_met > 50. && leadjet_pt > 30. && jet_n >= 1 && jet_eta[0] > -2.4 && jet_eta[0] < 2.4 && ph_n == 0'
    #---------------------------------------
    # Add eta cuts, (IsEB, IsEE)
    #---------------------------------------
    #eta_str_base = 'ph_Is%s[%s]' %( eta_cut, ph_idx_shape )

    #---------------------------------------
    # Add additional cuts, mainly restricting
    # the fitted variable to the plotting limits
    #---------------------------------------
    jet_selection = 'leadjet_pt > 30. && jet_n >= 1 && jet_CSVMedium_n == 0'
    jet_non_selection = 'leadjet_pt > 30.'


    #---------------------------------------
    # put the cuts together
    #---------------------------------------

    myweight = ''

    if isdata :
        myweight = '(isData)'
    else:
        myweight = '(NLOWeight*PUWeight*mu_trigSF*mu_idSF*mu_isoSF)'

    full_sel = ' && '.join( [sel_base, w_selection, jet_selection ] )
    full_sel = '(' + full_sel + ')*' + myweight
    
    almostfull_sel = ' && '.join( [sel_base, w_selection, jet_non_selection ] )
    almostfull_sel = '(' + almostfull_sel + ')*' + myweight

    smp_sel = '(' + smpvj_selection + ')*' + myweight

    if workspace is None :
        ws = ROOT.RooWorkspace( 'ws') 
    else :
        ws = workspace

    
    #---------------------------------------
    # draw the histograms
    #---------------------------------------
    binning_leadjet_pt = (128, 0., 640.)
    jet_var = 'leadjet_pt'
    hist_leadjetpt = clone_sample_and_draw( sampMan, sample, jet_var, smp_sel, binning_leadjet_pt )
    sampMan.outputs['%s_leadjetpt_%s' %(sample,suffix)] = hist_leadjetpt

    binning_mt = (100,0.,800.)
    mt_var = 'mt_lep_met'
    hist_mtW = clone_sample_and_draw( sampMan, sample, mt_var, smp_sel, binning_mt )
    sampMan.outputs['%s_mtmumet_%s' %(sample,suffix)] = hist_mtW

    binning_met = (100,0.,1000.)
    met_var = 'met_pt'
    hist_met = clone_sample_and_draw( sampMan, sample, met_var, smp_sel, binning_met )
    sampMan.outputs['%s_met_%s' %(sample,suffix)] = hist_met

    binning_jetn = (10,0.,10.)
    jetn_var = 'jet_n'
    hist_jetn = clone_sample_and_draw( sampMan, sample, jetn_var, smp_sel, binning_jetn )
    sampMan.outputs['%s_jetn_%s' %(sample,suffix)] = hist_jetn

    binning_wpt = (100,0.,500.)
    wpt_var = 'recoW_pt'
    hist_wpt = clone_sample_and_draw( sampMan, sample, wpt_var, smp_sel, binning_wpt )
    sampMan.outputs['%s_wpt_%s' %(sample,suffix)] = hist_wpt

    binning_wmass = (100,0.,500.)
    wmass_var = 'RecoWMass'
    hist_wmass = clone_sample_and_draw( sampMan, sample, wmass_var, smp_sel, binning_wmass )
    sampMan.outputs['%s_wmass_%s' %(sample,suffix)] = hist_wmass


def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist



main()

    




    
    




