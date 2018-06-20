import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import uuid
import time
import math
import os, sys
from uncertainties import ufloat
import re
from collections import OrderedDict
import pickle
sys.path.append('/data/users/fengyb/CMSPLOTS')
from Plotter.myFunction import DrawGraphs

from SampleManager import SampleManager
from argparse import ArgumentParser
parser = ArgumentParser()

parser = ArgumentParser()
parser.add_argument('--baseDir',       default=None,           dest='baseDir',          required=False, help='Path to signal samples without any filter')
parser.add_argument('--outputFile',    default=None,           dest='outputFile',       required=False, help='Path to output file' )
parser.add_argument('--mass',          default=1000,           dest='mass',             required=False, help='signal model mass')
parser.add_argument('--width',         default=5,              dest='width',            required=False, help='signal model width')

options = parser.parse_args()

ROOT.gROOT.SetBatch(True)

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = '/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/cross_sections/photon15.py'
_LUMI     = 36000
_SAMPCONF = '/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/Modules/Resonance.py'


def main() :
    sampManNoFilt = SampleManager( options.baseDir, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI, quiet = True)
    #sampManNoFilt = SampleManager( options.baseDir, _TREENAME, filename=_FILENAME, quiet=True)
    sampManNoFilt.ReadSamples( _SAMPCONF )

    cuts_nofilt = OrderedDict()

    # list of selections

    cuts_nofilt = { 'electron' : OrderedDict(), 'muon' : OrderedDict() }

    cuts_nofilt['electron']['pass trigger'] = 'HLT_Ele27_eta2p1_WPTight_Gsf'
    cuts_nofilt['muon']    ['pass trigger'] = '(HLT_IsoMu24 || HLT_IsoTkMu24)'

    cuts_nofilt['electron']['One tight electron with pt $>$ 30']  = 'Sum$( el_pt > 30 ) == 1'
    cuts_nofilt['muon']    ['One tight muon with pt $>$ 30']      = 'Sum$( mu_pt > 30 ) == 1'

    cuts_nofilt['electron']['Electron trigger match'] = ' Sum$( el_hasTrigMatch ) > 0 '
    cuts_nofilt['muon']    ['Muon trigger match']      = ' Sum$( mu_hasTrigMatch ) > 0 '

    cuts_nofilt['electron']['Second Lepton Veto'] = 'Sum$( mu_pt > 10 ) == 0'
    cuts_nofilt['muon']    ['Second Lepton Veto'] = 'Sum$( el_pt > 10 ) == 0'

    cuts_nofilt['electron']['At least one Medium Photon'] = 'Sum$( ph_passMedium ) > 0'
    cuts_nofilt['muon']    ['At least one Medium Photon'] = 'Sum$( ph_passMedium ) > 0'

    cuts_nofilt['electron']['one Photon with pt $>$ 50 in the barrel'] = 'Sum$( ph_pt > 50 ) == 1 && ph_IsEB[0] '
    cuts_nofilt['muon']    ['one Photon with pt $>$ 50 in the barrel'] = 'Sum$( ph_pt > 50 ) == 1 && ph_IsEB[0] '

    GColor = {}
    GColor["0p01"]  = 2
    GColor["5"]     = 3

    GMStyle = {}
    GMStyle["0p01"] = 21
    GMStyle["5"]    = 22

    gerr = {}
    for ichan in ["muon", "electron"]:
        gerr[ichan] = {}
        for iwidth in ["5", "0p01"]:
            gerr[ichan][iwidth] = ROOT.TGraphErrors( 40 )
            gerr[ichan][iwidth].SetName( "pu_uncertainty_%s_width%s"%(ichan, iwidth))
            gerr[ichan][iwidth].SetTitle( "pu_uncertainty_%s_width%s"%(ichan, iwidth))
            gerr[ichan][iwidth].SetLineColor(int(GColor[iwidth]))
            gerr[ichan][iwidth].SetMarkerColor(int(GColor[iwidth]))
            gerr[ichan][iwidth].SetMarkerStyle(int(GMStyle[iwidth]))
            gerr[ichan][iwidth].SetMarkerSize(1)
            print gerr[ichan][iwidth].GetName()

    ipoint = 0

    for samp in sampManNoFilt.get_samples() :

        print 'Sample = ', samp.name

        #res = re.match( '(MadGraph|Pythia)ResonanceMass(\d+)_width(\d+)', samp.name )
        res = re.match( 'MadGraphResonanceMass(\d+)_width(\d+)', samp.name)

        if res is not None :

            if samp.name.count( 'width0p01' ):
               width = "0p01"
            else:
               width  = "5"

            mass  = int(res.group(1))

            puunc = get_puuncertainties( sampManNoFilt, samp.name, cuts_nofilt)
            
            gerr['electron'][width].SetPoint( ipoint, mass, puunc['electron'] )
            gerr['muon'    ][width].SetPoint( ipoint, mass, puunc['muon']     )

            ipoint += 1


    ## write to output
    ofile = ROOT.TFile.Open( "Acceptance/puuncertainty.root", 'RECREATE')
    for ichan in ["muon", "electron"]:
        for iwidth in ["5", "0p01"]:
            gerr[ichan][iwidth].Write()

    DrawGraphs([gerr["muon"]["0p01"], gerr["muon"]["5"]], ["muon width0p01", "muon width5"], 100, 4500, "gen_mass", 0, 0.02, "PU reweighting uncertainty", "pu_uncertainty_pythia_muon", dology = False)
    DrawGraphs([gerr["electron"]["0p01"], gerr["electron"]["5"]], ["electron width0p01", "electron width5"], 100, 4500, "gen_mass", 0, 0.02, "PU reweighting uncertainty", "pu_uncertainty_pythia_electron", dology = False)

def get_puuncertainties( sampManNoFilt, samp_name, cuts ):

    binning = ( 100, 0, 100 )

    # only look at two channels for the pu uncertainty
    mode_accept_cuts = { 
                  'electron' : '( ( isWElDecay == 1 ) || ( isWTauDecay == 1 && isWTauElDecay == 1 ) )', 
                  'muon'     : '( ( isWMuDecay == 1 ) || ( isWTauDecay == 1 && isWTauMuDecay == 1 ) )',
                }

    puunc = OrderedDict()

    for modename, modec in mode_accept_cuts.iteritems() :

        cut_str = ''
        for cut_name, cut in cuts[modename].iteritems() :
            cut_str += ' && %s '%cut
        print cut_str

        sampManNoFilt.create_hist( samp_name, 'ph_n', Apply_MC_Reweight( modec ) , binning )
        ntotal = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

        sampManNoFilt.create_hist( samp_name, 'ph_n', Apply_MC_Reweight( modec + cut_str ), binning )
        npass = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

        accp = npass / ntotal

        ## shift PU up by 10%
        sampManNoFilt.create_hist( samp_name, 'ph_n', Apply_MC_Reweight( modec, tag = 'UP10') , binning )
        ntotalup = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

        sampManNoFilt.create_hist( samp_name, 'ph_n', Apply_MC_Reweight( modec + cut_str , tag = 'UP10'), binning )
        npassup = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

        accpup = npassup / ntotalup

        ## shift PU down by 10%
        sampManNoFilt.create_hist( samp_name, 'ph_n', Apply_MC_Reweight( modec, tag = 'DN10') , binning )
        ntotaldn = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

        sampManNoFilt.create_hist( samp_name, 'ph_n', Apply_MC_Reweight( modec + cut_str , tag = 'DN10'), binning )
        npassdn = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

        accpdn = npassdn / ntotaldn

        print "*******************************************"
        print ntotal,   npass,    accp
        print ntotalup, npassup,  accpup
        print ntotaldn, npassdn,  accpdn
        print " PU reweighting uncertainty %.2f"%(max(abs(accpdn - accp), abs(accpup - accp))/accp)
        print "*******************************************"

        puunc[modename] =  max(abs(accpdn - accp), abs(accpup - accp))/accp

    return puunc


def Apply_MC_Reweight( selection , ApplyReweight= True , tag = ''):
    if ApplyReweight:
       return ' ( ' + selection + ' ) * ( NLOWeight * PUWeight'+ tag + ' + isData )'
    else:
       return selection
        

main()


