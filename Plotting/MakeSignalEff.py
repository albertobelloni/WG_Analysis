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
parser.add_argument('--baseDir',      default=None,           dest='baseDir',         required=False, help='Path to signal samples without any filter')
parser.add_argument('--outputFile',    default=None,           dest='outputFile',       required=False, help='Path to output file' )

options = parser.parse_args()

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000
_SAMPCONF = 'Modules/Resonance.py'

def main() :

    sampManNoFilt  = SampleManager( options.baseDir, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    #sampManNoFilt = SampleManager( options.baseDir, _TREENAME, filename=_FILENAME)
    sampManNoFilt.ReadSamples( _SAMPCONF )

    mode_cuts = { 'electron' : 'isWElDecay == 1', 'muon' : 'isWMuDecay == 1', 'tau' : 'isWTauDecay == 1' , 'tauel' : 'isWTauDecay == 1 && isWTauElDecay == 1'  , 'taumu' : 'isWTauDecay == 1 && isWTauMuDecay == 1' }
    cuts_nofilt = OrderedDict()

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

    cuts_nofilt['electron']['met'] = ' met_pt > 25 '
    cuts_nofilt['muon']    ['met'] = ' met_pt > 25 '

    cut_efficiencies = {}
    selected_samples = []

    for samp in sampManNoFilt.get_samples() :

        print 'Sample = ', samp.name

        #res = re.match( '(MadGraph|Pythia)ResonanceMass(\d+)_width(\d+)', samp.name )
        res = re.match( 'MadGraphResonanceMass(\d+)_width(\d+)', samp.name)

        if res is not None :

            width = int(res.group(2))
            mass  = int(res.group(1))
 
            #if mass!=1000:
            #   continue
            #if width!=5:
            #   continue

            cut_efficiencies.setdefault( width, {})
            cut_efficiencies[width].setdefault( mass, {} )
            selected_samples.append( samp.name )

            eff_ele = get_efficiencies( sampManNoFilt, samp.name, mode_cuts, cuts_nofilt['electron'] )
            eff_mu  = get_efficiencies( sampManNoFilt, samp.name, mode_cuts, cuts_nofilt['muon'] )

            cut_efficiencies[width][mass] = {'muon' : eff_mu, 'electron' : eff_ele}

    if options.outputFile is not None :

        dirpath = os.path.dirname( options.outputFile )

        if not os.path.isdir( dirpath ) :
            os.makedirs( dirpath )

        ofile = open( options.outputFile, 'wb' )

        pickle.dump( cut_efficiencies, ofile )

        ofile.close()


def get_efficiencies( sampManNoFilt, samp_name, mode_cuts, cuts ) :

    binning = ( 100, 0, 100 )
    cut_vals = {'counts' : {}, 'eff' : {}, 'ftau' : {}, 'effwithtau' : {}, 'effCorrftau' : {}}

    for modename, modec in mode_cuts.iteritems() :

        cut_vals['counts'].setdefault( modename, OrderedDict() )
        cut_vals['eff'].setdefault( modename, OrderedDict() )

        sampManNoFilt.create_hist( samp_name, 'ph_n', Apply_MC_Reweight( modec ), binning )
        ntotal = IntegralandError( sampManNoFilt.get_samples( name=samp_name )[0].hist )
        cut_vals['counts'][modename]['denominator'] = ntotal

        cut_str = ''
        for cut_name, cut in cuts.iteritems() :

            cut_str += ' && %s '%cut

            sampManNoFilt.create_hist( samp_name, 'ph_n',  Apply_MC_Reweight( modec + cut_str ), binning )
            npass = IntegralandError( sampManNoFilt.get_samples( name=samp_name )[0].hist )
            cut_vals['counts'][modename][cut_name] = npass

            nfail = UfloatMinus( ntotal, npass )

            # to get the correct binominal uncertainty
            cut_vals['eff'][modename][cut_name] = npass / ( npass + nfail )

    # now make the tau fraction
    for modename, mode_dic in cut_vals['counts'].iteritems() :

        if modename.count('tau') > 0 :
            continue

        cut_vals['effwithtau'].setdefault( modename, OrderedDict() )
        cut_vals['ftau'].setdefault( modename, OrderedDict() )
        cut_vals['effCorrftau'].setdefault( modename, OrderedDict() )

        if modename == 'muon' :
            taumode = 'taumu'
        if modename == 'electron' :
            taumode = 'tauel'

        tau_total = cut_vals['counts'][taumode]['denominator']
        lep_total = mode_dic['denominator']

        for cut_name, cut_res in mode_dic.iteritems() :
            if cut_name == 'denominator' :
                continue

            pass_tau = cut_vals['counts'][taumode][cut_name]
            pass_lep = cut_res

            fail_tau = UfloatMinus( tau_total, pass_tau )
            fail_lep = UfloatMinus( lep_total, pass_lep )

            effwithtau = ( pass_tau + pass_lep ) / ( pass_tau + pass_lep + fail_tau + fail_lep )
            ftau = ( pass_tau + fail_tau ) / (  pass_tau + pass_lep + fail_tau + fail_lep  )

            effCorrftau = effwithtau / ( 1 - ftau )

            cut_vals['ftau'][modename][cut_name] = ftau
            # I think in our analysis effwithtau is 'the' acceptance
            cut_vals['effwithtau'][modename][cut_name] = effwithtau
            cut_vals['effCorrftau'][modename][cut_name] = effCorrftau


    # now make the totals
    ## comment out the total section, does not make sense to me.
    '''
    cut_vals['counts']['total'] = {}
    cut_vals['eff']['total'] = {}

    cut_vals['counts']['total'].setdefault('denominator', 0 )

    for modename in mode_cuts.keys() :

        cut_vals['counts']['total']['denominator'] = cut_vals['counts']['total']['denominator'] + cut_vals['counts'][modename]['denominator']
        print modename,
        print cut_vals['counts'][modename]['denominator'],
        print cut_vals['counts']['total']['denominator']

        for cutname in cuts.keys() :

            cut_vals['counts']['total'].setdefault( cutname, 0 )
            cut_vals['counts']['total'][cutname] = cut_vals['counts']['total'][cutname] + cut_vals['counts'][modename][cutname]


    #now calculate efficiencies

    total = cut_vals['counts']['total']['denominator']

    for cutname, cutv in cut_vals['counts']['total'].iteritems() :
        npass_v = cutv
        nfail_v = total - npass_v

        npass = ufloat( npass_v, math.sqrt( npass_v ) )
        nfail = ufloat( nfail_v, math.sqrt( nfail_v ) )

        cut_vals['eff']['total'][cutname] = npass / ( npass + nfail )
    '''

    # print out
    '''
    for modename, vals in cut_vals['eff'].iteritems():
        print "*********************************************"
        print modename
        for cuts, val in vals.iteritems():
            print cuts,
            print val
        print "*********************************************"
    '''

    return cut_vals


def Apply_MC_Reweight( selection , ApplyReweight= True ):
    if ApplyReweight:
       return ' ( ' + selection + ' ) * ( NLOWeight * PUWeight + isData )'
    else:
       return selection

def IntegralandError( hist, IncludeOverUnderflow = False):
    ## return the result and error when integrating one histogram
    ## assume no correlation between bins
    total = 0.0
    err2 = 0.0

    firstbin = 1
    lastbin = hist.GetNbinsX()

    if IncludeOverUnderflow:
       firstin -= 1
       lastbin += 1

    for ibin in xrange( firstbin, lastbin+1):
        total += hist.GetBinContent( ibin )
        err2  += math.pow( hist.GetBinError( ibin ) , 2.0 )

    result = ufloat( total, math.sqrt( err2 ) )

    return result

def UfloatMinus(minuend, subtrahend):
    ## input two ufloat values, output the difference, but the uncertainty is minus instead of plus
    ## this is for binomal uncertainties calculations
    return ufloat( minuend.n - subtrahend.n, math.sqrt( minuend.s*minuend.s - subtrahend.s*subtrahend.s))


main()


