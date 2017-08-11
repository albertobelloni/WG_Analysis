import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import os
import uuid
import time
import math
import re
import pickle
import subprocess

from SampleManager import SampleManager
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--baseDirMu',      default=None,           dest='baseDirMu',         required=True, help='Path to muon base directory')
parser.add_argument('--baseDirEl',      default=None,           dest='baseDirEl',         required=True, help='Path to electron base directory')
parser.add_argument('--baseDirMuComp',      default=None,           dest='baseDirMuComp',         required=False, help='Path to muon base directory for comparisons')
parser.add_argument('--baseDirElComp',      default=None,           dest='baseDirElComp',         required=False, help='Path to electron base directory for comparisons')
parser.add_argument('--samplesConf',  default=None,           dest='samplesConf',     required=True, help='Sample configuration' )
parser.add_argument('--outputDir',  default=None,           dest='outputDir',     help='Path to output directory' )
parser.add_argument('--batch',  default=False,        dest='batch', action='store_true',    help='Submit limit setting jobs to the batch' )
parser.add_argument('--varComp',  default=False,        dest='varComp', action='store_true',    help='Do fit variable comparison' )
parser.add_argument('--jetComp',  default=False,        dest='jetComp', action='store_true',    help='Do jet cut comparison' )
parser.add_argument('--phIdComp',  default=False,        dest='phIdComp', action='store_true',    help='Do photon ID comparison' )
parser.add_argument('--evetoComp',  default=False,        dest='evetoComp', action='store_true',    help='Do photon electron veto ID comparison' )
parser.add_argument('--lepvetoComp',  default=False,        dest='lepvetoComp', action='store_true',    help='Do second lepton veto comparison' )
parser.add_argument('--phiCutComp',  default=False,        dest='phiCutComp', action='store_true',    help='Do phi cut comparison' )

options = parser.parse_args()



_TREENAME = 'tupel/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000
_BASEPATH = '/home/jkunkle/usercode/Plotting/LimitSetting/'
_BKGSAMP  = 'MCBackground'

rand = ROOT.TRandom3()
rand.SetSeed( int( time.time() ) )

ROOT.gROOT.SetBatch(False)

if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )


def main() :


    if options.varComp :
        doVarComparision( )

    if options.jetComp :
        doJetComparision( )

    if options.phIdComp :
        doPhIdComparision( )

    if options.evetoComp :
        doEvetoComparision( )

    if options.lepvetoComp :
        doSecLepVetoComparison( )

    if options.phiCutComp :
        doPhiCutComparison( )

def ReadMuElSamples( baseDirMu=None, baseDirEl=None) :

    if baseDirMu is None :
        baseDirMu = options.baseDirMu
    if baseDirEl is None :
        baseDirEl = options.baseDirEl


    sampManMu = SampleManager( baseDirMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManEl = SampleManager( baseDirEl, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    if options.samplesConf is not None :

        sampManMu.ReadSamples( options.samplesConf )
        sampManEl.ReadSamples( options.samplesConf )
    else :
        print 'Must provide a sample configuration.  Exiting'
        return

    return sampManMu, sampManEl 

def doPhiCutComparison( ) :

    sampManMu, sampManEl = ReadMuElSamples( )

    name = 'limits_phicut_comp'

    signals = []

    for samp in sampManMu.get_samples() :
        if samp.name.count('width5') :
            continue
        if samp.name.count('ResonanceMass') > 0 :
            signals.append( samp.name ) 

    sig_masses = {}

    for sig in signals :
        res = re.match('ResonanceMass(\d+).*', sig )

        if res is not None :
            sig_masses[int( res.group(1))] = sig 

    selection_mu = 'mu_n == 1 && ph_n==1 '
    selection_el = 'el_n == 1 && ph_n==1 '


    binning_res = range( 100, 500, 25 ) + range( 500, 800, 50) + range( 800, 2600, 100 ) 
    var = 'mt_res'

    configs = [ 
        { 'name' : 'no_phi_cut' , 'label' : 'No Phi Cut'  , 'color' : ROOT.kBlack  , 'selection' : 'dphi_lep_ph > 0', 'binning' : binning_res },
        { 'name' : 'phi_cut_0.2', 'label' : 'DPhi > 0.2' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 0.2', 'binning' : binning_res },
        { 'name' : 'phi_cut_0.4', 'label' : 'DPhi > 0.4' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 0.4', 'binning' : binning_res },
        { 'name' : 'phi_cut_0.6', 'label' : 'DPhi > 0.6' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 0.6', 'binning' : binning_res },
        { 'name' : 'phi_cut_0.8', 'label' : 'DPhi > 0.8' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 0.8', 'binning' : binning_res },
        { 'name' : 'phi_cut_1.0', 'label' : 'DPhi > 1.0' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 1.0', 'binning' : binning_res },
        { 'name' : 'phi_cut_1.2', 'label' : 'DPhi > 1.2' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 1.2', 'binning' : binning_res },
        { 'name' : 'phi_cut_1.4', 'label' : 'DPhi > 1.4' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 1.4', 'binning' : binning_res },
        { 'name' : 'phi_cut_1.6', 'label' : 'DPhi > 1.6' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 1.6', 'binning' : binning_res },
        { 'name' : 'phi_cut_1.8', 'label' : 'DPhi > 1.8' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 1.8', 'binning' : binning_res },
        { 'name' : 'phi_cut_2.0', 'label' : 'DPhi > 2.0' , 'color' : ROOT.kRed    , 'selection' : 'dphi_lep_ph > 2.0', 'binning' : binning_res },
    ]

    cards_mu = {}
    cards_el = {}

    for config in configs :

        cards_mu[config['name']] = {}
        cards_el[config['name']] = {}

        sampManMu.create_hist( _BKGSAMP, var, 'NLOWeight * ( ' + selection_mu + ' && %s )' %( config['selection']), config['binning'] )
        sampManEl.create_hist( _BKGSAMP, var, 'NLOWeight * ( ' + selection_el + ' && %s )' %( config['selection']), config['binning'] )

        bkg_samp_mu = sampManMu.get_samples( name=_BKGSAMP )
        bkg_samp_el = sampManEl.get_samples( name=_BKGSAMP )

        bkg_hist_mu = bkg_samp_mu[0].hist
        bkg_hist_el = bkg_samp_el[0].hist

        for sigm, sig in sig_masses.iteritems() :

            sampManMu.create_hist(sig, var, 'NLOWeight * ( ' + selection_mu + ' && %s ) ' %( config['selection']) , config['binning'] )
            sampManEl.create_hist(sig, var, 'NLOWeight * ( ' + selection_el + ' && %s ) ' %( config['selection']) , config['binning'] )

            sig_samp_mu = sampManMu.get_samples( name=sig )
            sig_samp_el = sampManEl.get_samples( name=sig )


            sig_hist_mu = sig_samp_mu[0].hist
            sig_hist_el = sig_samp_el[0].hist


            card_path_mu = MakeCombineResults( sig_hist_mu, bkg_hist_mu, name = '%s_muon_%d' %(config['name'], sigm ) )
            card_path_el = MakeCombineResults( sig_hist_el, bkg_hist_el, name = '%s_electron_%d' %(config['name'], sigm ) )


    results = GetCombineLimits( {'mu' : cards_mu, 'el' : cards_el}, batch=options.batch )

    for conf, confdic in results.iteritems() :
        for ch, chdic in confdic.iteritems() :
            for mass, massdic in chdic.iteritems() : 
                scale = massdic['limit_scale']
                # get the cross section for this sample
                sig_samp = sig_masses[mass]
                xs = sampManMu.get_samples( name=sig_samp )[0].cross_section
                results[conf][ch][mass]['cross_section'] = xs
                if scale is None :
                    results[conf][ch][mass]['limit_cross_section'] = None
                else :
                    results[conf][ch][mass]['limit_cross_section'] = xs*scale

    MakeStandardOutput( configs, results, name )

def doSecLepVetoComparison( ) :

    name = 'limits_seclepveto_comp'

    sampManMu, sampManEl = ReadMuElSamples( )
    sampManMuComp, sampManElComp = ReadMuElSamples(options.baseDirMuComp, options.baseDirElComp )

    signals = []

    for samp in sampManMu.get_samples() :
        if samp.name.count('width5') :
            continue
        if samp.name.count('ResonanceMass') > 0 :
            signals.append( samp.name ) 

    sig_masses = {}

    for sig in signals :
        res = re.match('ResonanceMass(\d+).*', sig )

        if res is not None :
            sig_masses[int( res.group(1))] = sig 

    selection_mu = 'mu_n == 1 && ph_n==1 '
    selection_el = 'el_n == 1 && ph_n==1 '


    binning_res = range( 100, 500, 25 ) + range( 500, 800, 50) + range( 800, 2600, 100 ) 
    var = 'mt_res'

    configs = [ 
        { 'name' : 'no_lep_veto' , 'label' : 'No Second Lepton Veto'  , 'color' : ROOT.kBlack,  'sampManMu' : sampManMuComp, 'sampManEl' : sampManElComp, 'binning' : binning_res },
        { 'name' : 'with_lep_veto', 'label' : 'With Second Lepton Veto' , 'color' : ROOT.kRed,  'sampManMu' : sampManMu, 'sampManEl' : sampManEl,'binning' : binning_res },
    ]

    cards_mu = {}
    cards_el = {}

    for config in configs :

        cards_mu[config['name']] = {}
        cards_el[config['name']] = {}

        config['sampManMu'].create_hist( 'NLOWeight * ( ' + _BKGSAMP + ' ) ', var, selection_mu , config['binning'] )
        config['sampManEl'].create_hist( 'NLOWeight * ( ' + _BKGSAMP + ' ) ', var, selection_el , config['binning'] )

        bkg_samp_mu = config['sampManMu'].get_samples( name=_BKGSAMP )
        bkg_samp_el = config['sampManEl'].get_samples( name=_BKGSAMP )

        bkg_hist_mu = bkg_samp_mu[0].hist
        bkg_hist_el = bkg_samp_el[0].hist

        for sigm, sig in sig_masses.iteritems() :

            config['sampManMu'].create_hist(sig, var, 'NLOWeight * ( ' + selection_mu + ' ) '  , config['binning'] )
            config['sampManEl'].create_hist(sig, var, 'NLOWeight * ( ' + selection_el + ' ) '  , config['binning'] )

            sig_samp_mu = config['sampManMu'].get_samples( name=sig )
            sig_samp_el = config['sampManEl'].get_samples( name=sig )


            sig_hist_mu = sig_samp_mu[0].hist
            sig_hist_el = sig_samp_el[0].hist


            card_path_mu = MakeCombineResults( sig_hist_mu, bkg_hist_mu, name = '%s_muon_%d' %(config['name'], sigm ) )
            card_path_el = MakeCombineResults( sig_hist_el, bkg_hist_el, name = '%s_electron_%d' %(config['name'], sigm ) )

            cards_mu[config['name']][ sigm] =  card_path_mu
            cards_el[config['name']][ sigm] =  card_path_el

    results = GetCombineLimits( {'mu' : cards_mu, 'el' : cards_el}, batch=options.batch )

    for conf, confdic in results.iteritems() :
        for ch, chdic in confdic.iteritems() :
            for mass, massdic in chdic.iteritems() : 
                scale = massdic['limit_scale']

                # get the cross section for this sample
                sig_samp = sig_masses[mass]
                xs = sampManMu.get_samples( name=sig_samp )[0].cross_section
                results[conf][ch][mass]['cross_section'] = xs
                if scale is None :
                    results[conf][ch][mass]['limit_cross_section'] = None
                else :
                    results[conf][ch][mass]['limit_cross_section'] = xs*scale

    MakeStandardOutput( configs, results, name )



def doEvetoComparision( ) :

    sampManMu, sampManEl = ReadMuElSamples( )

    name = 'limits_eveto_comp'

    signals = []

    for samp in sampManMu.get_samples() :
        if samp.name.count('width5') :
            continue
        if samp.name.count('ResonanceMass') > 0 :
            signals.append( samp.name ) 

    sig_masses = {}

    for sig in signals :
        res = re.match('ResonanceMass(\d+).*', sig )

        if res is not None :
            sig_masses[int( res.group(1))] = sig 

    selection_mu = 'mu_n == 1 && ph_n==1 '
    selection_el = 'el_n == 1 && ph_n==1 '


    binning_res = range( 100, 500, 25 ) + range( 500, 800, 50) + range( 800, 2600, 100 ) 
    var = 'mt_res'

    configs = [ 
        { 'name' : 'no_eveto' , 'label' : 'NoVeto'  , 'color' : ROOT.kBlack  , 'selection' : 'ph_passMedium[0]==1', 'binning' : binning_res },
        { 'name' : 'csev', 'label' : 'Pass CSEV' , 'color' : ROOT.kRed    , 'selection' : 'ph_passMedium[0]==1 && ph_eleVeto[0] == 1', 'binning' : binning_res },
        { 'name' : 'psv' , 'label' : 'Pass PSV'  , 'color' : ROOT.kBlue    , 'selection' : 'ph_passMedium[0]==1 && ph_hasPixSeed[0] == 0', 'binning' : binning_res },
    ]

    cards_mu = {}
    cards_el = {}

    for config in configs :

        cards_mu[config['name']] = {}
        cards_el[config['name']] = {}

        sampManMu.create_hist( _BKGSAMP, var, 'NLOWeight * ( ' + selection_mu + ' && %s ) ' %( config['selection']), config['binning'] )
        sampManEl.create_hist( _BKGSAMP, var, 'NLOWeight * ( ' + selection_el + ' && %s ) ' %( config['selection']), config['binning'] )

        bkg_samp_mu = sampManMu.get_samples( name=_BKGSAMP )
        bkg_samp_el = sampManEl.get_samples( name=_BKGSAMP )

        bkg_hist_mu = bkg_samp_mu[0].hist
        bkg_hist_el = bkg_samp_el[0].hist

        for sigm, sig in sig_masses.iteritems() :

            sampManMu.create_hist(sig, var, 'NLOWeight * ( ' + selection_mu + ' && %s ) ' %( config['selection']) , config['binning'] )
            sampManEl.create_hist(sig, var, 'NLOWeight * ( ' + selection_el + ' && %s ) ' %( config['selection']) , config['binning'] )

            sig_samp_mu = sampManMu.get_samples( name=sig )
            sig_samp_el = sampManEl.get_samples( name=sig )


            sig_hist_mu = sig_samp_mu[0].hist
            sig_hist_el = sig_samp_el[0].hist


            card_path_mu = MakeCombineResults( sig_hist_mu, bkg_hist_mu, name = '%s_muon_%d' %(config['name'], sigm ) )
            card_path_el = MakeCombineResults( sig_hist_el, bkg_hist_el, name = '%s_electron_%d' %(config['name'], sigm ) )

            cards_mu[config['name']][ sigm] =  card_path_mu
            cards_el[config['name']][ sigm] =  card_path_el

    results = GetCombineLimits( {'mu' : cards_mu, 'el' : cards_el}, batch=options.batch )

    for conf, confdic in results.iteritems() :
        for ch, chdic in confdic.iteritems() :
            for mass, massdic in chdic.iteritems() : 
                scale = massdic['limit_scale']

                # get the cross section for this sample
                sig_samp = sig_masses[mass]
                xs = sampManMu.get_samples( name=sig_samp )[0].cross_section
                results[conf][ch][mass]['cross_section'] = xs
                if scale is None :
                    results[conf][ch][mass]['limit_cross_section'] = None
                else :
                    results[conf][ch][mass]['limit_cross_section'] = xs*scale

    MakeStandardOutput( configs, results, name )

def doPhIdComparision( ) :

    sampManMu, sampManEl = ReadMuElSamples( )

    name = 'limits_phid_comp'

    signals = []

    for samp in sampManMu.get_samples() :
        if samp.name.count('width5') :
            continue
        if samp.name.count('ResonanceMass') > 0 :
            signals.append( samp.name ) 

    sig_masses = {}

    for sig in signals :
        res = re.match('ResonanceMass(\d+).*', sig )

        if res is not None :
            sig_masses[int( res.group(1))] = sig 

    selection_mu = 'mu_n == 1 '
    selection_el = 'el_n == 1 '


    binning_res = range( 100, 500, 25 ) + range( 500, 800, 50) + range( 800, 2600, 100 ) 
    var = 'mt_res'

    configs = [ 
        { 'name' : 'phid_loose' , 'label' : 'Loose'  , 'color' : ROOT.kBlack  , 'selection' : 'Sum$(ph_passLoose) == 1', 'binning' : binning_res },
        { 'name' : 'phid_medium', 'label' : 'Medium' , 'color' : ROOT.kRed    , 'selection' : 'Sum$(ph_passMedium)  == 1', 'binning' : binning_res },
        { 'name' : 'phid_tight' , 'label' : 'Tight'  , 'color' : ROOT.kRed    , 'selection' : 'Sum$(ph_passTight)  == 1', 'binning' : binning_res },
    ]

    cards_mu = {}
    cards_el = {}

    for config in configs :

        cards_mu[config['name']] = {}
        cards_el[config['name']] = {}

        sampManMu.create_hist( _BKGSAMP, var, 'NLOWeight * ( ' + selection_mu + ' && %s ) ' %( config['selection']), config['binning'] )
        sampManEl.create_hist( _BKGSAMP, var, 'NLOWeight * ( ' + selection_el + ' && %s ) ' %( config['selection']), config['binning'] )

        bkg_samp_mu = sampManMu.get_samples( name=_BKGSAMP )
        bkg_samp_el = sampManEl.get_samples( name=_BKGSAMP )

        bkg_hist_mu = bkg_samp_mu[0].hist
        bkg_hist_el = bkg_samp_el[0].hist

        for sigm, sig in sig_masses.iteritems() :

            sampManMu.create_hist(sig, var, 'NLOWeight * ( ' + selection_mu + ' && %s ) ' %( config['selection']) , config['binning'] )
            sampManEl.create_hist(sig, var, 'NLOWeight * ( ' + selection_el + ' && %s ) ' %( config['selection']) , config['binning'] )

            sig_samp_mu = sampManMu.get_samples( name=sig )
            sig_samp_el = sampManEl.get_samples( name=sig )


            sig_hist_mu = sig_samp_mu[0].hist
            sig_hist_el = sig_samp_el[0].hist


            card_path_mu = MakeCombineResults( sig_hist_mu, bkg_hist_mu, name = '%s_muon_%d' %(config['name'], sigm ) )
            card_path_el = MakeCombineResults( sig_hist_el, bkg_hist_el, name = '%s_electron_%d' %(config['name'], sigm ) )


            cards_mu[config['name']][ sigm] =  card_path_mu
            cards_el[config['name']][ sigm] =  card_path_el

    results = GetCombineLimits( {'mu' : cards_mu, 'el' : cards_el}, batch=options.batch )

    for conf, confdic in results.iteritems() :
        for ch, chdic in confdic.iteritems() :
            for mass, massdic in chdic.iteritems() : 
                scale = massdic['limit_scale']

                # get the cross section for this sample
                sig_samp = sig_masses[mass]
                xs = sampManMu.get_samples( name=sig_samp )[0].cross_section
                results[conf][ch][mass]['cross_section'] = xs
                if scale is None :
                    results[conf][ch][mass]['limit_cross_section'] = None
                else :
                    results[conf][ch][mass]['limit_cross_section'] = xs*scale

    MakeStandardOutput( configs, results, name )

def doJetComparision() :

    sampManMu, sampManEl = ReadMuElSamples( )

    name = 'limits_jet_comp'

    signals = []

    for samp in sampManMu.get_samples() :
        if samp.name.count('width5') :
            continue
        if samp.name.count('ResonanceMass') > 0 :
            signals.append( samp.name ) 

    sig_masses = {}

    for sig in signals :
        res = re.match('ResonanceMass(\d+).*', sig )

        if res is not None :
            sig_masses[int( res.group(1))] = sig 

    selection_mu = 'mu_n == 1 && ph_n == 1 '
    selection_el = 'el_n == 1 && ph_n == 1 '


    binning_res = range( 100, 500, 25 ) + range( 500, 800, 50) + range( 800, 2600, 100 ) 
    binning_pt = range(20, 200, 20 ) + range( 200, 500, 50) + range(500, 1600, 100)
    var = 'mt_res'
    #var = 'ph_pt[0]'

    configs = [ 
        { 'name' : 'no_jet_veto'     , 'label' : 'No Jet Veto'      , 'color' : ROOT.kBlack  , 'selection' : 'jet_n >= 0', 'binning' : binning_res },
        { 'name' : 'jet_veto'        , 'label' : 'Jet Veto'         , 'color' : ROOT.kRed    , 'selection' : 'jet_n == 0', 'binning' : binning_res },
        { 'name' : 'bjet_veto_loose' , 'label' : 'Loose b-jet veto' , 'color' : ROOT.kBlue   , 'selection' : 'Sum$(jet_bTagCSVV2>0.5426)==0', 'binning' : binning_res },
        { 'name' : 'bjet_veto_medium', 'label' : 'Medium b-jet veto', 'color' : ROOT.kGreen  , 'selection' : 'Sum$(jet_bTagCSVV2>0.8484)==0', 'binning' : binning_res },
        { 'name' : 'bjet_veto_tight' , 'label' : 'Tight b-jet veto' , 'color' : ROOT.kMagenta, 'selection' : 'Sum$(jet_bTagCSVV2>0.9535)==0', 'binning' : binning_res },
        #{ 'name' : 'no_jet_veto'     , 'label' : 'No Jet Veto'      , 'color' : ROOT.kBlack  , 'selection' : 'jet_n >= 0', 'binning' : binning_pt },
        #{ 'name' : 'jet_veto'        , 'label' : 'Jet Veto'         , 'color' : ROOT.kRed    , 'selection' : 'jet_n == 0', 'binning' : binning_pt },
        #{ 'name' : 'bjet_veto_loose' , 'label' : 'Loose b-jet veto' , 'color' : ROOT.kBlue   , 'selection' : 'Sum$(jet_bTagCSVV2>0.5426)==0', 'binning' : binning_pt },
        #{ 'name' : 'bjet_veto_medium', 'label' : 'Medium b-jet veto', 'color' : ROOT.kGreen  , 'selection' : 'Sum$(jet_bTagCSVV2>0.8484)==0', 'binning' : binning_pt },
        #{ 'name' : 'bjet_veto_tight' , 'label' : 'Tight b-jet veto' , 'color' : ROOT.kMagenta, 'selection' : 'Sum$(jet_bTagCSVV2>0.9535)==0', 'binning' : binning_pt },
    ]

    cards_mu = {}
    cards_el = {}

    for config in configs :

        cards_mu[config['name']] = {}
        cards_el[config['name']] = {}

        sampManMu.create_hist( _BKGSAMP, var, 'NLOWeight * ( ' + selection_mu + ' && %s ) ' %( config['selection']), config['binning'] )
        sampManEl.create_hist( _BKGSAMP, var, 'NLOWeight * ( ' + selection_el + ' && %s ) ' %( config['selection']), config['binning'] )

        bkg_samp_mu = sampManMu.get_samples( name=_BKGSAMP )
        bkg_samp_el = sampManEl.get_samples( name=_BKGSAMP )

        bkg_hist_mu = bkg_samp_mu[0].hist
        bkg_hist_el = bkg_samp_el[0].hist

        for sigm, sig in sig_masses.iteritems() :

            sampManMu.create_hist(sig, var, 'NLOWeight * ( ' + selection_mu + ' && %s ) ' %( config['selection']) , config['binning'] )
            sampManEl.create_hist(sig, var, 'NLOWeight * ( ' + selection_el + ' && %s ) ' %( config['selection']) , config['binning'] )

            sig_samp_mu = sampManMu.get_samples( name=sig )
            sig_samp_el = sampManEl.get_samples( name=sig )


            sig_hist_mu = sig_samp_mu[0].hist
            sig_hist_el = sig_samp_el[0].hist


            card_path_mu = MakeCombineResults( sig_hist_mu, bkg_hist_mu, name = '%s_muon_%d' %(config['name'], sigm ) )
            card_path_el = MakeCombineResults( sig_hist_el, bkg_hist_el, name = '%s_electron_%d' %(config['name'], sigm ) )

            cards_mu[config['name']][ sigm] =  card_path_mu
            cards_el[config['name']][ sigm] =  card_path_el

    results = GetCombineLimits( {'mu' : cards_mu, 'el' : cards_el}, batch=options.batch )

    for conf, confdic in results.iteritems() :
        for ch, chdic in confdic.iteritems() :
            for mass, massdic in chdic.iteritems() : 
                scale = massdic['limit_scale']

                # get the cross section for this sample
                sig_samp = sig_masses[mass]
                xs = sampManMu.get_samples( name=sig_samp )[0].cross_section
                results[conf][ch][mass]['cross_section'] = xs
                if scale is None :
                    results[conf][ch][mass]['limit_cross_section'] = None
                else :
                    results[conf][ch][mass]['limit_cross_section'] = xs*scale

    MakeStandardOutput( configs, results, name )

def doVarComparision( ) :

    sampManMu, sampManEl = ReadMuElSamples( )

    name = 'limits_var_comp'

    signals = []

    for samp in sampManMu.get_samples() :
        if samp.name.count('width5') :
            continue
        if samp.name.count('ResonanceMass') > 0 :
            signals.append( samp.name ) 

    sig_masses = {}

    for sig in signals :
        res = re.match('ResonanceMass(\d+).*', sig )

        if res is not None :
            sig_masses[int( res.group(1))] = sig 

    selection_mu = 'mu_n == 1 && ph_n == 1 '
    selection_el = 'el_n == 1 && ph_n == 1 '

    theta = math.atan(1./2.0)

    binning_res = range( 100, 500, 25 ) + range( 500, 800, 50) + range( 800, 2600, 100 ) 
    binning_pt = range(20, 200, 20 ) + range( 200, 500, 50) + range(500, 1600, 100)

    configs = [ 
        { 'name' : 'mt_res'         , 'label' : 'Transverse Mass'   , 'color' : ROOT.kBlack, 'var' : 'mt_res', 'binning' : binning_res },
        { 'name' : 'ph_pt'          , 'label' : 'Photon pT'         , 'color' : ROOT.kRed  , 'var' : 'ph_pt', 'binning' : binning_pt },
        { 'name' : 'recoM_lep_nu_ph', 'label' : 'Neutrino Reco mass', 'color' : ROOT.kBlue , 'var' : 'recoM_lep_nu_ph', 'binning' : binning_res },
        { 'name' : 'rotated'        , 'label' : 'Combined mT and pT', 'color' : ROOT.kGreen, 'var' : 'ph_pt[0] *sin( %f ) + mt_res*cos(%f)' %(theta,theta), 'binning' : binning_res },
    ]

    cards_mu = {}
    cards_el = {}
    for config in configs :

        cards_mu[config['name']] = {}
        cards_el[config['name']] = {}

        sampManMu.create_hist( _BKGSAMP, config['var'], 'NLOWeight * ( ' + selection_mu + ' && %s > %d ) ' %( config['var'], config['binning'][0]), config['binning'] )
        sampManEl.create_hist( _BKGSAMP, config['var'], 'NLOWeight * ( ' + selection_el + ' && %s > %d ) ' %( config['var'], config['binning'][0]), config['binning'] )

        bkg_samp_mu = sampManMu.get_samples( name=_BKGSAMP )
        bkg_samp_el = sampManEl.get_samples( name=_BKGSAMP )

        bkg_hist_mu = bkg_samp_mu[0].hist
        bkg_hist_el = bkg_samp_el[0].hist

        for sigm, sig in sig_masses.iteritems() :

            sampManMu.create_hist(sig, config['var'], 'NLOWeight * ( ' + selection_mu + ' && %s > %d ) ' %( config['var'], config['binning'][0] ) , config['binning'] )
            sampManEl.create_hist(sig, config['var'], 'NLOWeight * ( ' + selection_el + ' && %s > %d ) ' %( config['var'], config['binning'][0] ) , config['binning'] )

            sig_samp_mu = sampManMu.get_samples( name=sig )
            sig_samp_el = sampManEl.get_samples( name=sig )


            sig_hist_mu = sig_samp_mu[0].hist
            sig_hist_el = sig_samp_el[0].hist


            card_path_mu = MakeCombineResults( sig_hist_mu, bkg_hist_mu, name = '%s_muon_%d' %(config['name'], sigm ) )
            card_path_el = MakeCombineResults( sig_hist_el, bkg_hist_el, name = '%s_electron_%d' %(config['name'], sigm ) )

            cards_mu[config['name']][ sigm] =  card_path_mu
            cards_el[config['name']][ sigm] =  card_path_el

    results = GetCombineLimits( {'mu' : cards_mu, 'el' : cards_el}, batch=options.batch )
    for conf, confdic in results.iteritems() :
        for ch, chdic in confdic.iteritems() :
            for mass, massdic in chdic.iteritems() : 
                scale = massdic['limit_scale']

                # get the cross section for this sample
                sig_samp = sig_masses[mass]
                xs = sampManMu.get_samples( name=sig_samp )[0].cross_section
                results[conf][ch][mass]['cross_section'] = xs
                if scale is None :
                    results[conf][ch][mass]['limit_cross_section'] = None
                else :
                    results[conf][ch][mass]['limit_cross_section'] = xs*scale

    MakeStandardOutput( configs, results, name )

def MakeStandardOutput( configs, limit_results, name ) :

    graphs_el   = {}
    graphs_mu   = {}
    graphs_comb = {}
    leg_mu   = ROOT.TLegend( 0.5, 0.5, 0.9 ,0.9 )
    leg_el   = ROOT.TLegend( 0.5, 0.5, 0.9 ,0.9 )
    leg_comb = ROOT.TLegend( 0.5, 0.5, 0.9 ,0.9 )

    for config in configs :

        conf_name = config['name']
        conf_color = config['color']
        conf_results = limit_results[conf_name]

        mass_order = conf_results['mu'].keys()
        mass_order.sort()

        graphs_mu  [conf_name] = ROOT.TGraph( len(conf_results['mu']) )
        graphs_el  [conf_name] = ROOT.TGraph( len(conf_results['el']) )
        graphs_comb[conf_name] = ROOT.TGraph( len(conf_results['chcomb']) )

        graphs_mu  [conf_name].SetName( config['name']+'_mu' )
        graphs_el  [conf_name].SetName( config['name']+'_el' )
        graphs_comb[conf_name].SetName( config['name']+'_comb' )

        graphs_mu  [conf_name].SetMarkerStyle(20)
        graphs_el  [conf_name].SetMarkerStyle(20)
        graphs_comb[conf_name].SetMarkerStyle(20)

        graphs_mu  [conf_name].SetMarkerSize(1.2)
        graphs_el  [conf_name].SetMarkerSize(1.2)
        graphs_comb[conf_name].SetMarkerSize(1.2)

        graphs_mu  [conf_name].SetLineWidth(2)
        graphs_el  [conf_name].SetLineWidth(2)
        graphs_comb[conf_name].SetLineWidth(2)

        graphs_mu  [conf_name].SetLineColor(conf_color)
        graphs_el  [conf_name].SetLineColor(conf_color)
        graphs_comb[conf_name].SetLineColor(conf_color)

        graphs_mu  [conf_name].SetMarkerColor(conf_color)
        graphs_el  [conf_name].SetMarkerColor(conf_color)
        graphs_comb[conf_name].SetMarkerColor(conf_color)


        for idx, mass in enumerate(mass_order) :

            val_mu   = conf_results['mu'][mass]['limit_cross_section']
            val_el   = conf_results['el'][mass]['limit_cross_section']
            val_comb = conf_results['chcomb'][mass]['limit_cross_section']

            if val_mu is not None :
                graphs_mu[conf_name].SetPoint( idx, mass, val_mu )
            if val_el is not None :
                graphs_el[conf_name].SetPoint( idx, mass, val_el )
            if val_comb is not None :
                graphs_comb[conf_name].SetPoint( idx, mass, val_comb )


        leg_mu  .AddEntry( graphs_mu[conf_name],   config['label'], 'P' )
        leg_el  .AddEntry( graphs_el[conf_name],   config['label'], 'P' )
        leg_comb.AddEntry( graphs_comb[conf_name], config['label'], 'P' )


    can_mu = ROOT.TCanvas( 'can_mu', 'can_mu' )

    first = True
    for gr in graphs_mu.values() :
        if first :
            gr.Draw('ALP' )
            first = False
        else :
            gr.Draw('LPsame')

    leg_mu.Draw()

    if options.outputDir is None :
        raw_input('cont')
    else :
        can_mu.SaveAs( '%s/%s_mu.pdf' %( options.outputDir, name ) )

    can_el = ROOT.TCanvas( 'can_el', 'can_el' )
    first = True
    for gr in graphs_el.values() :
        if first :
            gr.Draw('ALP' )
            first = False
        else :
            gr.Draw('LPsame')

    leg_el.Draw()
    if options.outputDir is None :
        raw_input('cont')
    else :
        can_el.SaveAs( '%s/%s_el.pdf' %( options.outputDir, name ) )

    can_comb = ROOT.TCanvas( 'can_comb', 'can_comb' )
    first = True
    for gr in graphs_comb.values() :
        if first :
            gr.Draw('ALP' )
            first = False
        else :
            gr.Draw('LPsame')

    leg_comb.Draw()
    if options.outputDir is None :
        raw_input('cont')
    else :
        can_comb.SaveAs( '%s/%s_comb.pdf' %( options.outputDir, name ) )

    if options.outputDir is not None :
        fname = '%s/results_%s.pickle' %( options.outputDir, name )
        print 'write %s' %fname
        ofile = open( fname, 'w' )
        pickle.dump( limit_results, ofile )
        ofile.close()
    

def GetCombineLimits( cards, batch=False ) :

    results = {}

    commands = []

    for ch, chcards in cards.iteritems() :
        for conf, confdic in chcards.iteritems() :

            results.setdefault( conf, {} )
            results[conf].setdefault( ch, {} )

            for mass, card in confdic.iteritems() :

                this_command = []

                results[conf][ch][mass] = {}

                cardname = os.path.basename( card )

                outname = 'results_%s' %cardname

                outpath = '%s/outputs/%s' %( _BASEPATH, outname )

                this_command.append( 'cd %s/CMSSW_7_4_7' %_BASEPATH )
                this_command.append( 'scramv1 runtime -csh' )
                this_command.append( 'combine -M Asymptotic %s >> %s ' %( card, outpath ) )

                commands.append( {'command' : this_command, 'outpath' : outpath, 'channel' : ch, 'mass' : mass, 'config' : conf })

                #os.system( 'cd %s/CMSSW_7_4_7 ; scramv1 runtime -csh ; combine -M Asymptotic %s >> %s ' %( _BASEPATH, card, outpath ) )
                # read the result file

                #results[ch][mass]['limit_scale'] = readResults( outpath )

    # add the combined e/mu cards
    if len( cards ) > 1  :

        for conf, confdic in cards.values()[0].iteritems() :
            results.setdefault(conf, {} )
            results[conf]['chcomb'] = {}
            for mass, card in confdic.iteritems() :

                this_command = []
                results[conf]['chcomb'][mass] = {}

                cardname = os.path.basename( card )
                cardpath = os.path.dirname( card )

                outname = 'results_chcomb_%s' %cardname

                outpath = '%s/outputs/%s' %( _BASEPATH, outname )

                comb_cards_cmd = 'combineCards.py ' 
                for idx, ch in enumerate(cards.keys()) :
                    comb_cards_cmd += 'Name%d=%s ' %( idx+1, cards[ch][conf][mass] )

                comb_cards_cmd += '  >  %s/chcomb_%s' %( cardpath, cardname )

                this_command.append( 'cd %s/CMSSW_7_4_7' %_BASEPATH )
                this_command.append( 'scramv1 runtime -csh' )
                this_command.append( comb_cards_cmd )
                this_command.append( 'combine -M Asymptotic %s >> %s ' %( card, outpath ) )

                commands.append( {'command' : this_command, 'outpath' : outpath, 'channel' : 'chcomb', 'mass' : mass, 'config' : conf })

    if batch :

        jde_file = '%s/ExeFiles/job_desc.txt' %(_BASEPATH)
        submit_command = 'condor_submit %s' %jde_file

        desc_entries = [
                        '#Use only the vanilla universe',
                        'universe = vanilla',
                        '# This is the executable to run.  If a script,',
                        '#   be sure to mark it "#!<path to interp>" on the first line.',
                        '# Filename for stdout, otherwise it is lost',
                        '# Copy the submittor environment variables.  Usually required.',
                        'getenv = True',
                        '# Copy output files when done.  REQUIRED to run in a protected directory',
                        'when_to_transfer_output = ON_EXIT_OR_EVICT',
                        'priority=0',
                        ]

        for idx, command_dic in enumerate(commands) :

            exe_file = '%s/ExeFiles/setLimit_%d.sh' %(_BASEPATH, idx)

            desc_entries += [
                             'Executable = %s' %exe_file,
                             'Initialdir = %s' %_BASEPATH,
                             '# Queue job',
                             'queue'
                            ]


            ofile = open( exe_file, 'w' )
            ofile.write( '#!/bin/bash\n' )
            for cmd in command_dic['command'] :
                ofile.write( cmd + '\n' )
            ofile.close()

            os.system( 'chmod 777 %s' %( exe_file ) )

        ofile = open( jde_file, 'w' )
        for line in desc_entries:
            ofile.write( line + '\n' )
        ofile.close()

        os.system( submit_command )

        wait_for_jobs()

        for command_dic in commands  :
            conf = command_dic['config']
            ch = command_dic['channel']
            mass = command_dic['mass']
            outpath = command_dic['outpath']

            results[conf][ch][mass]['limit_scale'] = readResults( outpath )
    else :

        for command_dic in commands :
            conf = command_dic['config']
            ch = command_dic['channel']
            mass = command_dic['mass']
            outpath = command_dic['outpath']

            cmd = ' ; '.join( command_dic['command'] )

            os.system( cmd )

            # read the result file
            results[conf][ch][mass]['limit_scale'] = readResults( outpath )

    return results

def wait_for_jobs( ) :

    while 1 :
        time.sleep(20)
        status = subprocess.Popen( ['condor_q'], stdout=subprocess.PIPE).communicate()[0]

        n_limits = 0

        for line in status.split('\n') :
            if line.count('setLimit' ) :
                n_limits += 1

        if n_limits == 0 :
            return
        else : 
            print '%d Jobs still running' %n_limits

def readResults( filepath ) :

    ofile = open( filepath, 'r' )

    result = None

    for line in ofile :

        if line.count( 'Expected' ) : 
            res = re.match( 'Expected 50.0%: r < (.*)', line.rstrip('\n') )

            if res is not None :

                result = float( res.group(1) )

    ofile.close()

    return result



def MakeCombineResults( sig_hist, bkg_hist, name ) :

    nbins = sig_hist.GetNbinsX()
    base_path = '%s/cards' %(_BASEPATH)

    bkg_bins = []
    sig_bins = []
    obs_bins = []
    
    for i in xrange( 0, nbins ) :
        bkg_val = bkg_hist.GetBinContent( i+1 )
        sig_val = sig_hist.GetBinContent( i+1 )

        obs = rand.Poisson( bkg_val )

        bkg_bins.append( bkg_val )
        sig_bins.append( sig_val )
        obs_bins.append( obs     )

    file_entries = []

    file_entries.append( r'# ' + name )
    file_entries.append( 'imax %d' %nbins )
    file_entries.append( 'jmax 1'  )
    file_entries.append( 'kmax %d' %(1+nbins) )

    file_entries.append( '------------'  )
    file_entries.append( r'#now list the bins and observations'  )

    bin_text = 'bin         '
    obs_text = 'observation '

    for idx, obs in enumerate(obs_bins ) :

        bin_text += '  %d  ' %idx
        obs_text += '  %d  ' %obs

    file_entries.append( bin_text )
    file_entries.append( obs_text )

    file_entries.append( '------------'  )
    file_entries.append( r'#now list the background and signal expectations'  )

    bin_text      = 'bin      '
    proc_text_str = 'process  '
    proc_text_id  = 'process  '
    rate_text     = 'rate     '

    for idx, bkg in enumerate(bkg_bins ) :

        bin_text      += '   %d   %d  ' %( idx, idx )
        proc_text_str += '   sig   bkg'
        proc_text_id  += '   0     1  '
        rate_text     += '   %f    %f ' %( sig_bins[idx], bkg )

    file_entries.append( bin_text )
    file_entries.append( proc_text_str )
    file_entries.append( proc_text_id )
    file_entries.append( rate_text )

    file_entries.append( '------------'  )
    file_entries.append( r'#now list the uncertainties'  )

    
    lumi_text = 'lumi       lnN   '
    for idx, bkg in enumerate( bkg_bins ) :
        lumi_text += '   1.1    1.1'

    file_entries.append( lumi_text )

    for idx, bkg in enumerate( bkg_bins ) :
        bkg_text  = 'bkg_norm_bin%d   lnN   '%idx
        for sidx in xrange( 0, len(bkg_bins) ) :
            if sidx == idx :
                bkg_text  += ' -   1.1 '
            else :
                bkg_text  += ' -  -  '

        file_entries.append( bkg_text  )

    file_name = base_path + '/' + name + '.txt'

    print 'Write File ', file_name

    ofile = open( file_name , 'w' )

    for line in file_entries :

        ofile.write( line + '\n' )
    
    ofile.close()

    return file_name


main()


