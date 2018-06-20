#!/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/external/slc6_amd64_gcc530/bin/python

'''
Calculate the p.d.f. uncertainty for one specific model with options.mass and options.width,
generated with pythia 
'''
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import uuid
import time
import math
import os
from uncertainties import ufloat
import re
from collections import OrderedDict
import pickle

from SampleManager import SampleManager
from argparse import ArgumentParser
parser = ArgumentParser()

parser = ArgumentParser()
parser.add_argument('--baseDir',       default=None,           dest='baseDir',          required=False, help='Path to signal samples without any filter')
parser.add_argument('--outputFile',    default=None,           dest='outputFile',       required=False, help='Path to output file' )
parser.add_argument('--mass',          default=1000,           dest='mass',             required=False, help='signal model mass')
parser.add_argument('--width',         default=5,              dest='width',            required=False, help='signal model width')

options = parser.parse_args()

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


    for samp in sampManNoFilt.get_samples() :

        print 'Sample = ', samp.name

        #res = re.match( '(MadGraph|Pythia)ResonanceMass(\d+)_width(\d+)', samp.name )
        res = re.match( 'MadGraphResonanceMass(\d+)_width(\d+)', samp.name)

        if res is not None :

            width = int(res.group(2))
            mass  = int(res.group(1))

            # run on the signal with options.mass and options.width
            if mass!=int(options.mass):
               continue
            if width!=int(options.width):
               continue

            get_pdfuncertainties( sampManNoFilt, samp.name, cuts_nofilt)


def get_pdfuncertainties( sampManNoFilt, samp_name, cuts ):
    '''
    p.d.f set 263400, NNPDF30_lo_as_0130_nf_4
    in the ntuple, from 110 to 210
    '''

    ofile = ROOT.TFile.Open("%s_%s.root"%(options.outputFile, samp_name), "RECREATE")
    binning = ( 100, 0, 100 )

    # only look at two channels for the pdf uncertainty
    mode_accept_cuts = { 
                  'electron' : '( ( isWElDecay == 1 ) || ( isWTauDecay == 1 && isWTauElDecay == 1 ) )', 
                  'muon'     : '( ( isWMuDecay == 1 ) || ( isWTauDecay == 1 && isWTauMuDecay == 1 ) )',
                }

    for modename, modec in mode_accept_cuts.iteritems() :

        haccpt = ROOT.TH1F("hacceptance_%s"%modename, "hacceptance_%s"%modename, 800, 0.0, 0.8 )
        haccpt.Sumw2()

        cut_str = ''
        for cut_name, cut in cuts[modename].iteritems() :
            cut_str += ' && %s '%cut
        print cut_str

        sampManNoFilt.create_hist( samp_name, 'ph_n', Apply_MC_Reweight( modec ) , binning )
        ntotal = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

        sampManNoFilt.create_hist( samp_name, 'ph_n', Apply_MC_Reweight( modec + cut_str ), binning )
        npass = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

        accp = npass / ntotal

        print ntotal, npass, accp
        print "*******************************************"

        idx = 0 
        for idx in xrange(100):
            sampManNoFilt.create_hist( samp_name, 'ph_n', '(' + modec + ') * EventWeights[%d] * 1.0e5'%(idx + 110) , binning )
            ntotal = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

            sampManNoFilt.create_hist( samp_name, 'ph_n', '(' + modec + cut_str + ') * EventWeights[%d] * 1.e5'%(idx + 110), binning )
            npass = sampManNoFilt.get_samples( name=samp_name )[0].hist.Integral()

            accp = npass / ntotal

            print ntotal, npass, accp
            
            haccpt.Fill(accp)

        haccpt.Write() 

    ofile.Close()

def Apply_MC_Reweight( selection , ApplyReweight= True ):
    if ApplyReweight:
       return ' ( ' + selection + ' ) * ( NLOWeight * PUWeight + isData )'
    else:
       return selection
        

main()


