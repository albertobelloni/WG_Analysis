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

parser.add_argument('--baseDirMu',      default=None,           dest='baseDirMu',         required=False, help='Path to muon base directory')
parser.add_argument('--baseDirEl',      default=None,           dest='baseDirEl',         required=False, help='Path to electron base directory')
parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')
parser.add_argument('--nodataFrame', default=False,action='store_false',   dest='dataFrame',   help='backwards compatibility for pre-2019 releases of ROOT')

options = parser.parse_args()

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon18.py'
_LUMI     = 36000
#_BASEPATH = '/afs/cern.ch/work/f/friccita/WG_Analysis/Plotting/LimitSetting/'
_BASEPATH = '/home/friccita/WGamma/WG_Analysis/Plotting/LimitSetting/'
_SAMPCONF = 'Modules/Resonance2018.py'


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
    print('DEBUG:',options.dataFrame)
    sampManMu = SampleManager( options.baseDirMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI, weightHistName = "weighthist", dataFrame = options.dataFrame )
    sampManEl = SampleManager( options.baseDirEl, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI, weightHistName = "weighthist", dataFrame = options.dataFrame )

    sampManMu.ReadSamples( _SAMPCONF )
    sampManEl.ReadSamples( _SAMPCONF )

    sampManMu.outputs = {}
    sampManEl.outputs = {}

    #Analysis signal region
    #val_sel_mu = 'mu_pt30_n==1 && mu_n==1 && el_n==0  && ph_n==1 && ph_IsEB[0] && ph_pt[0] > 80 && ph_passHOverEMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0] && met_pt > 25 &&  (mt_res > 200 && mt_res < 2000 )'
    #val_sel_el = 'el_pt35_n==1 && el_n==1 && mu_n==0  && ph_n==1 && ph_IsEB[0] && ph_pt[0] > 80 && ph_passHOverEMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0] && met_pt > 25 &&  (mt_res > 200 && mt_res < 2000 )'

    #Wgamma enriched
    val_sel_mu = 'mu_pt30_n==1 && mu_n==1 && el_n==0 && ph_n==1 && ph_IsEB[0] && ph_pt[0] > 80 && ph_passHOverETight[0] && ph_passNeuIsoCorrTight[0] && ph_passPhoIsoCorrTight[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0] && met_pt > 40 && (m_lep_ph < 75 || m_lep_ph > 105)'
    val_sel_el = 'el_pt35_n==1 && el_n==1 && mu_n==0 && ph_n==1 && ph_IsEB[0] && ph_pt[0] > 80 && ph_passHOverETight[0] && ph_passNeuIsoCorrTight[0] && ph_passPhoIsoCorrTight[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0] && met_pt > 40 && (m_lep_ph < 75 || m_lep_ph > 105)'

    #Zgamma enriched
    #val_sel_mu = 'mu_n==2 && m_ll < 130. && m_ll > 50. && mu_pt_rc[0] > 52. && mu_pt_rc[1] > 30. && mu_hasTrigMatch[0] && mu_passTight[0] && mu_hasTrigMatch[1] && mu_passTight[1] && ph_n==1 && ph_IsEB[0] && ph_pt[0] > 40 && ph_passHOverETight[0] && ph_passNeuIsoCorrTight[0] && ph_passPhoIsoCorrTight[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0] && (ph_pt[0] > 40.*m_llph/150.)'
    #val_sel_el = ''

    #W+Jets enriched
    #val_sel_mu = 'mu_pt30_n==1 && mu_n==1 && mu_eta[0] > -2.4 && mu_eta[0] < 2.4 && mu_hasTrigMatch[0] && mu_passTight[0] && mt_lep_met > 50. && leadjet_pt > 30. && jet_n >= 1 && jet_eta[0] > -2.4 && jet_eta[0] < 2.4 && jet_CSVMedium_n == 0 && ph_n == 0'
    #val_sel_mu = 'mu_pt30_n==1 && mu_n==1 && el_n==0 && mu_eta[0] < 2.4 && mu_passTight[0] && mt_lep_met > 50. && ph_n==1 && ph_IsEB[0] && ph_pt[0] > 25 && ph_passHOverEMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0]'
    #val_sel_el = ''

    #eta_cuts = ['EB', 'EE']
    eta_cuts = ['EB']

    workspaces_to_save = {}

    selections = { 'base'    : { 
                                'mu' : {'selection' : val_sel_mu }, 
                                'el' : {'selection' : val_sel_el }, 
                               },
                 }

    #workspace_signal   = ROOT.RooWorkspace( 'workspace_signal' )
    #workspace_wgamma   = ROOT.RooWorkspace( 'workspace_wgamma' )
    #workspace_wgammalo = ROOT.RooWorkspace( 'workspace_wgammalo' )
    #workspace_top      = ROOT.RooWorkspace( 'workspace_top' )
    #workspace_zgamma   = ROOT.RooWorkspace( 'workspace_zgamma' )
    wjets              = ROOT.RooWorkspace( 'workspace_wjets' )
    #elefake            = ROOT.RooWorkspace( 'elefake' )

    for seltag, chdic in selections.items() : 
        
        for ch, seldic in chdic.items() : 
            for et in eta_cuts :
                if ch == 'mu':
                    print('Jet fake rate: MC - %s' %(ch))
                    make_wjets_matrix( sampManMu, 'WJets', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManMu, 'WGamma', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManMu, 'TTbar_DiLep', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManMu, 'TTbar_SingleLep', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManMu, 'Zgamma', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManMu, 'ZJets', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManMu, 'GJets', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManMu, 'TTGJets', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManMu, 'GammaGamma', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                
                    print('Jet fake rate: data - %s' %(ch))
                    #make_wjets_matrix( sampManMu, 'Data', seldic['selection'], et, True, suffix='data_%s_%s' %(et,ch))
                if ch == 'el':
                    print('Jet fake rate: MC - %s' %(ch))
                    make_wjets_matrix( sampManEl, 'WJets', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManEl, 'WGamma', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManEl, 'TTbar_DiLep', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManEl, 'TTbar_SingleLep', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManEl, 'Zgamma', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManEl, 'ZJets', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManEl, 'GJets', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManEl, 'TTGJets', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                    make_wjets_matrix( sampManEl, 'GammaGamma', seldic['selection'], et, False, suffix='mc_%s_%s' %( et,ch ) )
                
                    print('Jet fake rate: data - %s' %(ch))
                    #make_wjets_matrix( sampManEl, 'Data', seldic['selection'], et, True, suffix='data_%s_%s' %(et,ch))

    if options.outputDir is not None :

        wjets.writeToFile( '%s/%s.root' %( options.outputDir,wjets.GetName() ) )

        #for fileid, ws_list in workspaces_to_save.iteritems() :
        #    for idx, ws in enumerate(ws_list) :
        #        if idx == 0 :
        #            recreate = True
        #        else  :
        #            recreate = False
        #        ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        outputFile = ROOT.TFile('%s/outfile_matrixFR_wgamma18_%s.root' %( options.outputDir, wjets.GetName() ),'recreate')
        for key, can in sampManMu.outputs.items() :
            can.Write( '%s' %(key) )
        for key, can in sampManEl.outputs.items() :
            can.Write( '%s' %(key) )
        #for key, can in sampManEl.outputs.iteritems() :
        #    can.Write( '%s' %(key) )





def make_wjets_matrix( sampMan, sample, sel_base, eta_cut, isdata=False, suffix='', workspace=None) :

    #---------------------------------------
    # Get the base selection for each region
    #---------------------------------------
    #ph_sel_basic  = 'ph_n==1 && ph_Is%s[0] && (m_llph + m_ll < 180)' %( eta_cut )

    #ph_sel_T = 'ph_passSIEIETight[0]'
    #ph_sel_L = '!ph_passSIEIETight[0]'
    ph_sel_T = 'ph_sigmaIEIEFull5x5[0] < 0.00994'
    ph_sel_L = 'ph_sigmaIEIEFull5x5[0] >= 0.00994'


    #chiso_fail_sel = 'ph_chIsoCorr[0] > 4 && ph_chIsoCorr[0] < 10'
    chiso_fail_sel = '!ph_passChIsoCorrTight[0]'
    chiso_pass_sel = 'ph_passChIsoCorrTight[0]'


    #---------------------------------------
    # put the cuts together
    #---------------------------------------

    myweight = ''
    if isdata:
        myweight = 'isData'
    else:
        #myweight = '(PUWeight * NLOWeight * el_trigSF * el_idSF * el_recoSF * ph_idSF * ph_psvSF * ph_csevSF * mu_trigSF * mu_isoSF * mu_trkSF * mu_idSF  * Alt$(prefweight,1))' #2016, 2017
        myweight = '(PUWeight * NLOWeight * el_trigSF * el_idSF * el_recoSF * ph_idSF * ph_psvSF * ph_csevSF * mu_trigSF * mu_isoSF * mu_trkSF * mu_idSF)' #2018
        #myweight = '(PUWeight * NLOWeight * Alt$(prefweight,1))' #2016, 2017 without SF
        #myweight = '(PUWeight * NLOWeight)' #2018, without SF


    full_sel_T = ' && '.join( [sel_base, ph_sel_T, chiso_pass_sel] )
    full_sel_T = '(' + full_sel_T + ')*' + myweight

    full_sel_L = ' && '.join( [sel_base, ph_sel_L, chiso_pass_sel] )
    full_sel_L = '(' + full_sel_L + ')*' + myweight

    if workspace is None :
        ws = ROOT.RooWorkspace( 'ws') 
    else :
        ws = workspace


    #---------------------------------------
    # plot sigmaIEIE for regions T and L
    # and whatever else you want...
    #---------------------------------------

    binning_sigIEIE = (30,0.,0.03)
    binning_chIso = (100,0.,10.)
    binning_mt = (100,0.,1000.)
    binning_dr = (35,0.,3.5)


    chIso_var = 'ph_chIsoCorr[0]'
    sigIEIE_var = 'ph_sigmaIEIEFull5x5[0]'
    mt_var = 'mt_res'

    hist_T_sigmaIEIE = clone_sample_and_draw( sampMan, sample, sigIEIE_var, full_sel_T, binning_sigIEIE )
    #hist_T_mt = clone_sample_and_draw( sampMan, sample, mt_var, full_sel_T, binning_mt )

    hist_L_sigmaIEIE = clone_sample_and_draw( sampMan, sample, sigIEIE_var, full_sel_L, binning_sigIEIE )
    #hist_L_mt = clone_sample_and_draw( sampMan, sample, mt_var, full_sel_L, binning_mt )

    sampMan.outputs['%s_sigmaIEIE_T_%s' %(sample,suffix)] = hist_T_sigmaIEIE
    sampMan.outputs['%s_sigmaIEIE_L_%s' %(sample,suffix)] = hist_L_sigmaIEIE

    #sampMan.outputs['%s_mt_T_%s' %(sample,suffix)] = hist_T_mt
    #sampMan.outputs['%s_mt_L_%s' %(sample,suffix)] = hist_L_mt



def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :
    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

main()

    




    
    




