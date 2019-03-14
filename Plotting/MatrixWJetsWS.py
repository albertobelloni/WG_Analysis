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

    #sel_base_mu = 'mu_pt30_n==2 && mu_n==2 && m_ll < 96.2 && m_ll > 86.2 && mu_hasTrigMatch[0] && mu_passTight[0] && mu_hasTrigMatch[1] && mu_passTight[1]'
    sel_base_mu = 'mu_pt30_n==2 && mu_n==2 && m_ll < 110. && m_ll > 70. && (m_llph + m_ll < 180) && mu_hasTrigMatch[0] && mu_passTight[0] && mu_hasTrigMatch[1] && mu_passTight[1]'

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
                make_wjets_matrix( sampManMuMu, 'Zgamma', seldic['selection'], et, False, suffix='mc_%s' %( et ) )
                make_wjets_matrix( sampManMuMu, 'Z+jets', seldic['selection'], et, False, suffix='mc_%s' %( et ) )
                
                print 'WJets fit for data'
                make_wjets_matrix( sampManMuMu, 'Data', seldic['selection'], et, True, suffix='data_%s' %(et), workspace=wjets)


    if options.outputDir is not None :

        wjets.writeToFile( '%s/%s.root' %( options.outputDir,wjets.GetName() ) )

        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        outputFile = ROOT.TFile('%s/outfile_matrix_Pt15To25_%s.root' %( options.outputDir, wjets.GetName() ),'recreate') #set pt cut here
        for key, can in sampManMuMu.outputs.iteritems() :
            can.Write( '%s' %(key) )
        for can in sampManElEl.outputs.iteritems() :
            can.Write( '%s' %(key) )

        #for key, can in sampManMuMu.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        #for key, can in sampManElEl.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )




def make_wjets_matrix( sampMan, sample, sel_base, eta_cut, isdata=False, suffix='', workspace=None) :

    #---------------------------------------
    # Get the base selection for each region
    #---------------------------------------
    ph_sel_basic  = 'ph_n==1 && ph_Is%s[0]' %( eta_cut )
    ph_pt_15To25 = 'ph_pt[0] > 15.'# && ph_pt[0] < 25.'
    ph_pt_25To40 = 'ph_pt[0] > 25. && ph_pt[0] < 40.'
    ph_pt_40To70 = 'ph_pt[0] > 40. && ph_pt[0] < 70.'
    ph_pt_70Up = 'ph_pt[0] > 70.'
    ph_sel_preid = 'ph_passHOverEMedium[0]'# && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]'
    ph_sel_chiso_incl = 'ph_passSIEIEMedium[0]'
    ph_sel_sieie_incl = 'ph_passChIsoCorrMedium[0]'

    deltaR_real_sel         = 'min(dr_lep_ph, dr_lep2_ph) > 0.1 && min(dr_lep_ph, dr_lep2_ph) < 0.8'
    deltaR_fake_sel         = 'min(dr_lep_ph, dr_lep2_ph) > 1.'

    #---------------------------------------
    # put the cuts together
    #---------------------------------------

    myweight = ''
    if isdata :
        myweight = '(isData)'
    else :
        myweight = '(NLOWeight*PUWeight*mu_trigSF*mu_idSF*mu_isoSF)'


    real_sel_sieie_incl = ' && '.join( [sel_base, ph_sel_basic, ph_pt_15To25, ph_sel_preid, ph_sel_sieie_incl, deltaR_real_sel] ) #set pt cut here
    real_sel_sieie_incl = '(' + real_sel_sieie_incl + ')*' + myweight

    real_sel_chiso_incl = ' && '.join( [sel_base, ph_sel_basic, ph_pt_15To25, ph_sel_preid, ph_sel_chiso_incl, deltaR_real_sel] ) #set pt cut here
    real_sel_chiso_incl = '(' + real_sel_chiso_incl + ')*' + myweight

    fake_sel_sieie_incl = ' && '.join( [sel_base, ph_sel_basic, ph_pt_15To25, ph_sel_preid, ph_sel_sieie_incl, deltaR_fake_sel] ) #set pt cut here
    fake_sel_sieie_incl = '(' + fake_sel_sieie_incl + ')*' + myweight

    fake_sel_chiso_incl = ' && '.join( [sel_base, ph_sel_basic, ph_pt_15To25, ph_sel_preid, ph_sel_chiso_incl, deltaR_fake_sel] ) #set pt cut here
    fake_sel_chiso_incl = '(' + fake_sel_chiso_incl + ')*' + myweight


    predR_sel = ' && '.join( [sel_base, ph_sel_basic, ph_pt_15To25, ph_sel_preid] ) #set pt cut here
    predR_sel = '(' + predR_sel + ')*' + myweight

    zpeak_sel = sel_base
    zpeak_sel =  '(' + zpeak_sel + ')*' + myweight


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
    binning_sigIEIE_FR = [0.,0.01022,0.1]
    binning_chIso_FR = [0.,0.441,5.]
    binning_mll = (16, 70., 110.)
    binning_dr = (40, 0., 4.)

    chIso_var = 'ph_chIsoCorr[0]'
    sigIEIE_var = 'ph_sigmaIEIEFull5x5[0]'
    mll_var = 'm_ll'
    dr_var = 'min(dr_lep_ph,dr_lep2_ph)'

    hist_real_sigmaIEIE = clone_sample_and_draw( sampMan, sample, sigIEIE_var, real_sel_sieie_incl, binning_sigIEIE )
    hist_real_chIso = clone_sample_and_draw( sampMan, sample, chIso_var, real_sel_chiso_incl, binning_chIso )

    hist_real_sigmaIEIE_FR = clone_sample_and_draw( sampMan, sample, sigIEIE_var, real_sel_sieie_incl, binning_sigIEIE_FR )
    hist_real_chIso_FR = clone_sample_and_draw( sampMan, sample, chIso_var, real_sel_chiso_incl, binning_chIso_FR )

    hist_fake_sigmaIEIE = clone_sample_and_draw( sampMan, sample, sigIEIE_var, fake_sel_sieie_incl, binning_sigIEIE )
    hist_fake_chIso = clone_sample_and_draw( sampMan, sample, chIso_var, fake_sel_chiso_incl, binning_chIso )

    hist_fake_sigmaIEIE_FR = clone_sample_and_draw( sampMan, sample, sigIEIE_var, fake_sel_sieie_incl, binning_sigIEIE_FR )
    hist_fake_chIso_FR = clone_sample_and_draw( sampMan, sample, chIso_var, fake_sel_chiso_incl, binning_chIso_FR )

    hist_mll = clone_sample_and_draw( sampMan, sample, mll_var, zpeak_sel, binning_mll )
    hist_dr = clone_sample_and_draw( sampMan, sample, dr_var, predR_sel, binning_dr )
    
    sampMan.outputs['%s_sigmaIEIE_real_%s' %(sample,suffix)] = hist_real_sigmaIEIE
    sampMan.outputs['%s_chIso_real_%s' %(sample,suffix)] = hist_real_chIso
    sampMan.outputs['%s_sigmaIEIE_real_FR_%s' %(sample,suffix)] = hist_real_sigmaIEIE_FR
    sampMan.outputs['%s_chIso_real_FR_%s' %(sample,suffix)] = hist_real_chIso_FR

    sampMan.outputs['%s_sigmaIEIE_fake_%s' %(sample,suffix)] = hist_fake_sigmaIEIE
    sampMan.outputs['%s_chIso_fake_%s' %(sample,suffix)] = hist_fake_chIso
    sampMan.outputs['%s_sigmaIEIE_fake_FR_%s' %(sample,suffix)] = hist_fake_sigmaIEIE_FR
    sampMan.outputs['%s_chIso_fake_FR_%s' %(sample,suffix)] = hist_fake_chIso_FR

    sampMan.outputs['%s_mll_%s' %(sample,suffix)] = hist_mll
    sampMan.outputs['%s_dr_%s' %(sample,suffix)] = hist_dr

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

    




    
    




