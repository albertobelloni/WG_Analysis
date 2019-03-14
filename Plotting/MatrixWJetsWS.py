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

parser.add_argument('--baseDirMuMu',      default=None,           dest='baseDirMuMu',         required=False, help='Path to muon base directory')
parser.add_argument('--baseDirElEl',      default=None,           dest='baseDirElEl',         required=False, help='Path to electron base directory')
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

    cut_defaults = {'sigmaIEIE' : { 'EB' : ( 0.012, 0.02 ), 'EE' : ( 0.04, 0.05 ) },
                    'chIso'     : { 'EB' : ( 4, 10 ),       'EE' : (4, 10) },
                   }

    return cut_defaults[shape_var][ieta]


ROOT.gROOT.SetBatch(False)
if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

def main() :

    sampManMuMu = SampleManager( options.baseDirMuMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElEl = SampleManager( options.baseDirElEl, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    sampManMuMu.ReadSamples( _SAMPCONF )
    sampManElEl.ReadSamples( _SAMPCONF )

    sampManMuMu.outputs = {}
    sampManElEl.outputs = {}

    sel_base_mu = 'mu_pt30_n==2 && mu_n==2 && m_ll < 110. && m_ll > 70. && mu_hasTrigMatch[0] && mu_passTight[0]'

    #eta_cuts = ['EB', 'EE']
    eta_cuts = ['EB']

    workspaces_to_save = {}

    selections = { 'base'    : { 
                                'mu' : {'selection' : sel_base_mu }, 
                               },
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
            for et in eta_cuts :
                print 'WJets fit for MC'
                make_wjets_matrix( sampManMuMu, 'Zgamma', seldic['selection'], et, 'chIso', 'sigmaIEIE', suffix='mc_%s_%s_%s' %( ch,et,seltag ) )
                make_wjets_matrix( sampManMuMu, 'Z+jets', seldic['selection'], et, 'chIso', 'sigmaIEIE', suffix='mc_%s_%s_%s' %( ch,et,seltag ) )
                
                print 'WJets fit for data'
                make_wjets_matrix( sampManMuMu, 'Data', seldic['selection'], et, 'chIso', 'sigmaIEIE', suffix='data_%s_%s_%s' %(ch,et,seltag), workspace=wjets)


    if options.outputDir is not None :

        wjets.writeToFile( '%s/%s.root' %( options.outputDir,wjets.GetName() ) )

        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        outputFile = ROOT.TFile('%s/outfile_matrix_%s.root' %( options.outputDir, wjets.GetName() ),'recreate')
        for key, can in sampManMuMu.outputs.iteritems() :
            can.Write( '%s' %(key) )
        for can in sampManElEl.outputs.iteritems() :
            can.Write( '%s' %(key) )

        #for key, can in sampManMuMu.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        #for key, can in sampManElEl.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )




def make_wjets_matrix( sampMan, sample, sel_base, eta_cut, shape_var, num_var, suffix='', workspace=None) :

    #---------------------------------------
    # Get the base selection for each region
    #---------------------------------------
    ph_selection_loose    = '%s==1' %defs.get_phid_selection('loose')
    ph_selection_medium    = '%s==1' %defs.get_phid_selection('medium')
    ph_selection_num   = '%s==1' %defs.get_phid_selection( num_var )
    ph_selection_shape = '%s==1' %defs.get_phid_selection( shape_var )
    ph_selection_incl  = 'ph_n==1'

    deltaR_sel         = 'dr_lep_ph>1.'

    ph_idx_loose =  defs.get_phid_idx( 'loose' )
    ph_idx_medium =  defs.get_phid_idx( 'medium' )
    ph_idx_num = defs.get_phid_idx( num_var )
    ph_idx_shape = defs.get_phid_idx( shape_var )

    #---------------------------------------
    # Add eta cuts, (IsEB, IsEE)
    #---------------------------------------
    eta_str_loose = 'ph_Is%s[%s]' %( eta_cut, ph_idx_loose )
    eta_str_medium = 'ph_Is%s[%s]' %( eta_cut, ph_idx_medium )
    eta_str_shape = 'ph_Is%s[%s]' %( eta_cut, ph_idx_shape )
    eta_str_num = 'ph_Is%s[%s]' %( eta_cut, ph_idx_num )
    eta_str_incl = 'ph_Is%s[0]' %( eta_cut )

    #---------------------------------------
    # Add additional cuts, mainly restricting
    # the fitted variable to the plotting limits
    #---------------------------------------
    addtl_cuts_loose = 'ph_pt[%s] > 25'     %( ph_idx_loose )#50
    addtl_cuts_medium = 'ph_pt[%s] > 25'     %( ph_idx_medium )#50
    addtl_cuts_num = 'ph_pt[%s] > 25'   %( ph_idx_num )#50
    addtl_cuts_shape = 'ph_pt[%s] > 25' %( ph_idx_shape )#50
    addtl_cuts_incl = 'ph_pt[0] > 25'


    #---------------------------------------
    # Get the cuts that define the photon
    # sideband regions
    #---------------------------------------
    cut_str_base = ' {var}[{idx}] > {val_low} && {var}[{idx}] < {val_high}'
    cut_var_shape = defs.get_phid_cut_var( shape_var )
    cut_var_num = defs.get_phid_cut_var( num_var )

    cut_vals_shape = get_cut_defaults( shape_var, eta_cut )
    cut_vals_num = get_cut_defaults( num_var, eta_cut )

    cut_str_shape = cut_str_base.format(var=cut_var_shape, idx=ph_idx_shape, val_low=cut_vals_shape[0], val_high=cut_vals_shape[1] )
    cut_str_num = cut_str_base.format(var=cut_var_num, idx=ph_idx_num, val_low=cut_vals_num[0], val_high=cut_vals_num[1] )

    #---------------------------------------
    # put the cuts together
    #---------------------------------------
    full_sel_loose    = ' && '.join( [sel_base, ph_selection_loose, eta_str_loose, addtl_cuts_loose, deltaR_sel] )
    full_sel_loose = '(' + full_sel_loose + ')*(NLOWeight*PUWeight + isData)'

    full_sel_medium    = ' && '.join( [sel_base, ph_selection_medium, eta_str_medium, addtl_cuts_medium, deltaR_sel] )
    full_sel_medium = '(' + full_sel_medium + ')*(NLOWeight*PUWeight + isData)'

    full_sel_shape = ' && '.join( [sel_base, ph_selection_shape, eta_str_shape, addtl_cuts_shape, cut_str_shape, deltaR_sel] )
    full_sel_shape = '(' + full_sel_shape + ')*(NLOWeight*PUWeight + isData)'

    full_sel_num   = ' && '.join( [sel_base, ph_selection_num, eta_str_num, addtl_cuts_num, cut_str_num, deltaR_sel] )
    full_sel_num = '(' + full_sel_num + ')*(NLOWeight*PUWeight + isData)'

    incl_sel    = ' && '.join( [sel_base, ph_selection_incl, eta_str_incl, addtl_cuts_incl, deltaR_sel] )
    incl_sel = '(' + incl_sel + ')*(NLOWeight*PUWeight + isData)'

    if workspace is None :
        ws = ROOT.RooWorkspace( 'ws') 
    else :
        ws = workspace


    #---------------------------------------
    # plot sigmaIEIE in regions A and B(shape)
    # plot chIso in regions A and C(num)
    #---------------------------------------

    binning_sigIEIE = (50,0.,0.05)
    binning_chIso = (90,0.,45.)
    binning_pt = (300,0.,750.)

    chIso_B_var = 'ph_chIsoCorr[ptSorted_ph_mediumNoChIso_idx[0]]'
    sigIEIE_B_var = 'ph_sigmaIEIEFull5x5[ptSorted_ph_mediumNoChIso_idx[0]]'
    chIso_C_var = 'ph_chIsoCorr[ptSorted_ph_mediumNoSIEIE_idx[0]]'
    sigIEIE_C_var = 'ph_sigmaIEIEFull5x5[ptSorted_ph_mediumNoSIEIE_idx[0]]'
    
    chIso_Am_var = 'ph_chIsoCorr[ptSorted_ph_medium_idx[0]]'
    sigIEIE_Am_var = 'ph_sigmaIEIEFull5x5[ptSorted_ph_medium_idx[0]]'
    chIso_Al_var = 'ph_chIsoCorr[ptSorted_ph_loose_idx[0]]'
    sigIEIE_Al_var = 'ph_sigmaIEIEFull5x5[ptSorted_ph_loose_idx[0]]'

    chIso_incl_var = 'ph_chIsoCorr[0]'
    sigIEIE_incl_var = 'ph_sigmaIEIEFull5x5[0]'

    pt_Al_var = 'ph_pt[ptSorted_ph_loose_idx[0]]'
    pt_Am_var = 'ph_pt[ptSorted_ph_medium_idx[0]]'
    pt_B_var = 'ph_pt[ptSorted_ph_mediumNoChIso_idx[0]]'
    pt_C_var = 'ph_pt[ptSorted_ph_mediumNoSIEIE_idx[0]]'
    pt_incl_var = 'ph_pt[0]'


    hist_sigmaIEIE_B = clone_sample_and_draw( sampMan, sample, sigIEIE_B_var, full_sel_shape, binning_sigIEIE )
    hist_chIso_B = clone_sample_and_draw( sampMan, sample, chIso_B_var, full_sel_shape, binning_chIso )
    #hist_phpt_B = clone_sample_and_draw( sampMan, sample, pt_B_var, full_sel_shape, binning_pt )

    hist_sigmaIEIE_C = clone_sample_and_draw( sampMan, sample, sigIEIE_C_var, full_sel_num, binning_sigIEIE )
    hist_chIso_C = clone_sample_and_draw( sampMan, sample, chIso_C_var, full_sel_num, binning_chIso )
    #hist_phpt_C = clone_sample_and_draw( sampMan, sample, pt_C_var, full_sel_num, binning_pt )

    hist_sigmaIEIE_Al = clone_sample_and_draw( sampMan, sample, sigIEIE_Al_var, full_sel_loose, binning_sigIEIE )
    hist_chIso_Al = clone_sample_and_draw( sampMan, sample, chIso_Al_var, full_sel_loose, binning_chIso )
    #hist_phpt_Al = clone_sample_and_draw( sampMan, sample, pt_Al_var, full_sel_loose, binning_pt )

    hist_sigmaIEIE_Am = clone_sample_and_draw( sampMan, sample, sigIEIE_Am_var, full_sel_medium, binning_sigIEIE )
    hist_chIso_Am = clone_sample_and_draw( sampMan, sample, chIso_Am_var, full_sel_medium, binning_chIso )
    #hist_phpt_Am = clone_sample_and_draw( sampMan, sample, pt_Am_var, full_sel_medium, binning_pt )

    hist_sigmaIEIE_incl = clone_sample_and_draw( sampMan, sample, sigIEIE_incl_var, incl_sel, binning_sigIEIE )
    hist_chIso_incl = clone_sample_and_draw( sampMan, sample, chIso_incl_var, incl_sel, binning_chIso )
    #hist_phpt_incl = clone_sample_and_draw( sampMan, sample, pt_incl_var, incl_sel, binning_pt )
    
    sampMan.outputs['%s_sigmaIEIE_Al_%s' %(sample,suffix)] = hist_sigmaIEIE_Al
    sampMan.outputs['%s_sigmaIEIE_Am_%s' %(sample,suffix)] = hist_sigmaIEIE_Am
    sampMan.outputs['%s_sigmaIEIE_B_%s' %(sample,suffix)] = hist_sigmaIEIE_B
    sampMan.outputs['%s_sigmaIEIE_C_%s' %(sample,suffix)] = hist_sigmaIEIE_C
    sampMan.outputs['%s_sigmaIEIE_incl_%s' %(sample,suffix)] = hist_sigmaIEIE_incl
    sampMan.outputs['%s_chIso_Al_%s' %(sample,suffix)] = hist_chIso_Al
    sampMan.outputs['%s_chIso_Am_%s' %(sample,suffix)] = hist_chIso_Am
    sampMan.outputs['%s_chIso_B_%s' %(sample,suffix)] = hist_chIso_B
    sampMan.outputs['%s_chIso_C_%s' %(sample,suffix)] = hist_chIso_C
    sampMan.outputs['%s_chIso_incl_%s' %(sample,suffix)] = hist_chIso_incl

    #sampMan.outputs['%s_phpt_Al_%s' %(sample,suffix)] = hist_phpt_Al
    #sampMan.outputs['%s_phpt_Am_%s' %(sample,suffix)] = hist_phpt_Am
    #sampMan.outputs['%s_phpt_B_%s' %(sample,suffix)] = hist_phpt_B
    #sampMan.outputs['%s_phpt_C_%s' %(sample,suffix)] = hist_phpt_C
    #sampMan.outputs['%s_phpt_incl_%s' %(sample,suffix)] = hist_phpt_incl



def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :
    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

main()

    




    
    




