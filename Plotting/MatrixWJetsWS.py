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
parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')

options = parser.parse_args()

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon16.py'
_LUMI     = 36000
#_BASEPATH = '/afs/cern.ch/work/f/friccita/WG_Analysis/Plotting/LimitSetting/'
_BASEPATH = '/home/friccita/WGamma/WG_Analysis/Plotting/LimitSetting/'
_SAMPCONF = 'Modules/Resonance2016.py'


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

    sampManMuMu = SampleManager( options.baseDirMuMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI, weightHistName = "weighthist" )

    sampManMuMu.ReadSamples( _SAMPCONF )

    sampManMuMu.outputs = {}

    sel_base_mu = 'mu_n==2 && m_ll < 130. && m_ll > 50. && mu_pt_rc[0] > 52. && mu_pt_rc[1] > 30. && mu_hasTrigMatch[0] && mu_passTight[0] && mu_hasTrigMatch[1] && mu_passTight[1]'

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
                make_wjets_matrix( sampManMuMu, 'ZJets', seldic['selection'], et, False, suffix='mc_%s' %( et ) )
                #make_wjets_matrix( sampManMuMu, 'WWG', seldic['selection'], et, False, suffix='mc_%s' %( et ) )
                #make_wjets_matrix( sampManMuMu, 'AllTop', seldic['selection'], et, False, suffix='mc_%s' %( et ) )
                
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

        outputFile = ROOT.TFile('%s/outfile_matrix_LepLep_2016_%s.root' %( options.outputDir, wjets.GetName() ),'recreate') #set pt cut here
        for key, can in sampManMuMu.outputs.iteritems() :
            can.Write( '%s' %(key) )

        #for key, can in sampManMuMu.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )




def make_wjets_matrix( sampMan, sample, sel_base, eta_cut, isdata=False, suffix='', workspace=None) :

    #---------------------------------------
    # Get the base selection for each region
    #---------------------------------------
    #ph_sel_basic  = 'ph_n==1 && ph_Is%s[0] && (m_llph + m_ll < 180)' %( eta_cut )
    ph_sel_basic  = 'ph_n==1 && ph_Is%s[0] && (ph_pt[0] > 40.*m_llph/150.)' %( eta_cut )
    ph_pt_15To25 = 'ph_pt[0] > 15.'# && ph_pt[0] < 25.'
    ph_pt_25To40 = 'ph_pt[0] > 25. && ph_pt[0] < 40.'
    ph_pt_40To70 = 'ph_pt[0] > 40. && ph_pt[0] < 70.'
    ph_pt_70Up = 'ph_pt[0] > 70.'
    ph_pt_40Up = 'ph_pt[0] > 40.'
    ph_sel_preid = ' ph_passEleVeto[0] && ph_passHOverETight[0] && ph_passNeuIsoCorrTight[0] && ph_passPhoIsoCorrTight[0]'
    ph_sel_chiso_incl = 'ph_passSIEIETight[0]'
    ph_sel_sieie_incl = 'ph_passChIsoCorrTight[0]'
    chiso_fail_sel = 'ph_chIsoCorr[0] > 4 && ph_chIsoCorr[0] < 10'

    #deltaR_real_sel         = 'min(dr_lep_ph, dr_lep2_ph) > 0.1 && min(dr_lep_ph, dr_lep2_ph) < 0.8'
    deltaR_real_sel         = 'min(dr_lep_ph, dr_lep2_ph) > 0.4'
    deltaR_fake_sel         = 'min(dr_lep_ph, dr_lep2_ph) > 1.'


    #---------------------------------------
    # put the cuts together
    #---------------------------------------

    myweight = ''
    if isdata :
        myweight = '(isData)'
    else :
        #myweight = '(NLOWeight*PUWeight)'
        myweight = '(NLOWeight*PUWeight*mu_trigSF*mu_idSF*mu_isoSF*ph_idSF*ph_csevSF)'


    real_sel_sieie_incl = ' && '.join( [sel_base, ph_sel_basic, ph_pt_40Up, ph_sel_preid, ph_sel_sieie_incl] ) #set pt cut here
    real_sel_sieie_incl = '(' + real_sel_sieie_incl + ')*' + myweight

    real_sel_chiso_incl = ' && '.join( [sel_base, ph_sel_basic, ph_pt_40Up, ph_sel_preid, ph_sel_chiso_incl] ) #set pt cut here
    real_sel_chiso_incl = '(' + real_sel_chiso_incl + ')*' + myweight

    fake_sel_sieie_incl = ' && '.join( [sel_base, ph_sel_basic, ph_pt_40Up, ph_sel_preid, chiso_fail_sel] ) #set pt cut here
    fake_sel_sieie_incl = '(' + fake_sel_sieie_incl + ')*' + myweight

    fake_sel_chiso_incl = ' && '.join( [sel_base, ph_sel_basic, ph_pt_40Up, ph_sel_preid, chiso_fail_sel] ) #set pt cut here
    fake_sel_chiso_incl = '(' + fake_sel_chiso_incl + ')*' + myweight


    predR_sel = ' && '.join( [sel_base, ph_sel_basic, ph_pt_15To25, ph_sel_preid] ) #set pt cut here
    predR_sel = '(' + predR_sel + ')*' + myweight

    zpeak_sel = ' && '.join( [sel_base, ph_sel_basic, ph_pt_40Up, ph_sel_preid, ph_sel_sieie_incl, ph_sel_chiso_incl] ) 
    zpeak_sel =  '(' + zpeak_sel + ')*' + myweight

    sel_smp_zpeak = 'mu_n==2 && m_ll < 106.2 && m_ll > 76.2 && mu_pt_rc[0] > 25. && mu_pt_rc[1] > 25. && mu_hasTrigMatch[0] && mu_passTight[0] && mu_hasTrigMatch[1] && mu_passTight[1] && (mu_charge[0]*mu_charge[1] < 0) && ph_n == 0'

    if workspace is None :
        ws = ROOT.RooWorkspace( 'ws') 
    else :
        ws = workspace


    #---------------------------------------
    # plot sigmaIEIE in regions A and B(shape)
    # plot chIso in regions A and C(num)
    # and whatever else you want...
    #---------------------------------------

    binning_sigIEIE = (30,0.,0.03)
    binning_chIso = (100,0.,10.)
    binning_pt = (300,0.,750.)
    binning_sigIEIE_FR = [0.,0.00994,0.1]
    binning_chIso_FR = [0.,0.202,5.]
    binning_mll = (40, 50., 130.)
    binning_mt = (100,0.,1000.)
    binning_dr = (40, 0., 4.)
    binning_vtx = (40, 0., 40.)
    binning_njet = (10,-0.5, 9.5)

    chIso_var = 'ph_chIsoCorr[0]'
    sigIEIE_var = 'ph_sigmaIEIEFull5x5[0]'
    mll_var = 'm_ll'
    dr_var = 'min(dr_lep_ph,dr_lep2_ph)'
    jetn_var = 'jet_n'
    vtx_var = 'vtx_n'
    pu_var = 'pu_n'
    mt_var = 'mt_res'
    met_var = 'met_pt'
    mu_pt_var = 'mu_pt_rc[0]'

    hist_real_sigmaIEIE = clone_sample_and_draw( sampMan, sample, sigIEIE_var, real_sel_sieie_incl, binning_sigIEIE )
    hist_real_chIso = clone_sample_and_draw( sampMan, sample, chIso_var, real_sel_chiso_incl, binning_chIso )

    hist_real_sigmaIEIE_FR = clone_sample_and_draw( sampMan, sample, sigIEIE_var, real_sel_sieie_incl, binning_sigIEIE_FR )
    #hist_real_chIso_FR = clone_sample_and_draw( sampMan, sample, chIso_var, real_sel_chiso_incl, binning_chIso_FR )

    hist_fake_sigmaIEIE = clone_sample_and_draw( sampMan, sample, sigIEIE_var, fake_sel_sieie_incl, binning_sigIEIE )
    hist_fake_chIso = clone_sample_and_draw( sampMan, sample, chIso_var, fake_sel_chiso_incl, binning_chIso )

    hist_fake_sigmaIEIE_FR = clone_sample_and_draw( sampMan, sample, sigIEIE_var, fake_sel_sieie_incl, binning_sigIEIE_FR )
    #hist_fake_chIso_FR = clone_sample_and_draw( sampMan, sample, chIso_var, fake_sel_chiso_incl, binning_chIso_FR )

    hist_mll = clone_sample_and_draw( sampMan, sample, mll_var, zpeak_sel, binning_mll )
    #hist_mll_smp = clone_sample_and_draw( sampMan, sample, mll_var, sel_smp_zpeak, binning_mll )
    hist_dr_nosieie = clone_sample_and_draw( sampMan, sample, dr_var, real_sel_sieie_incl, binning_dr )
    hist_dr_nochiso = clone_sample_and_draw( sampMan, sample, dr_var, real_sel_chiso_incl, binning_dr )
    hist_jetn_nosieie = clone_sample_and_draw( sampMan, sample, jetn_var, real_sel_sieie_incl, binning_njet )
    hist_jetn_nochiso = clone_sample_and_draw( sampMan, sample, jetn_var, real_sel_chiso_incl, binning_njet )
    hist_nvtx = clone_sample_and_draw( sampMan, sample, vtx_var, zpeak_sel, binning_vtx )
    #hist_mt = clone_sample_and_draw( sampMan, sample, mt_var, zpeak_sel, binning_mt )
    #hist_met = clone_sample_and_draw( sampMan, sample, met_var, zpeak_sel, binning_mt )
    hist_npu = clone_sample_and_draw( sampMan, sample, pu_var, zpeak_sel, binning_vtx )
    
    sampMan.outputs['%s_sigmaIEIE_real_%s' %(sample,suffix)] = hist_real_sigmaIEIE
    sampMan.outputs['%s_chIso_real_%s' %(sample,suffix)] = hist_real_chIso
    sampMan.outputs['%s_sigmaIEIE_real_FR_%s' %(sample,suffix)] = hist_real_sigmaIEIE_FR
    #sampMan.outputs['%s_chIso_real_FR_%s' %(sample,suffix)] = hist_real_chIso_FR

    sampMan.outputs['%s_sigmaIEIE_fake_%s' %(sample,suffix)] = hist_fake_sigmaIEIE
    sampMan.outputs['%s_chIso_fake_%s' %(sample,suffix)] = hist_fake_chIso
    sampMan.outputs['%s_sigmaIEIE_fake_FR_%s' %(sample,suffix)] = hist_fake_sigmaIEIE_FR
    #sampMan.outputs['%s_chIso_fake_FR_%s' %(sample,suffix)] = hist_fake_chIso_FR

    sampMan.outputs['%s_mll_%s' %(sample,suffix)] = hist_mll
    #sampMan.outputs['%s_mllsmp_%s' %(sample,suffix)] = hist_mll_smp
    sampMan.outputs['%s_dr_nosieie_%s' %(sample,suffix)] = hist_dr_nosieie
    sampMan.outputs['%s_dr_nochiso_%s' %(sample,suffix)] = hist_dr_nochiso
    sampMan.outputs['%s_jetn_nosieie_%s' %(sample,suffix)] = hist_jetn_nosieie
    sampMan.outputs['%s_jetn_nochiso_%s' %(sample,suffix)] = hist_jetn_nochiso
    sampMan.outputs['%s_vtxn_%s' %(sample,suffix)] = hist_nvtx
    #sampMan.outputs['%s_mtres_%s' %(sample,suffix)] = hist_mt
    sampMan.outputs['%s_pun_%s' %(sample,suffix)] = hist_npu
    #sampMan.outputs['%s_met_%s' %(sample,suffix)] = hist_met




def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :
    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning, ismodel=False, overflow=True )
    return newSamp.hist

main()

    




    
    




