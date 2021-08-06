import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import os
from SampleManager import SampleManager
from SampleManager import Sample

from argparse import ArgumentParser

p = ArgumentParser()

p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',  required=False,       help='Input directory base')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',  required=True,       help='Output directory')

options = p.parse_args()

_TREENAME = 'tupel/EventTree'
_FILENAME = 'tree.root'

if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )


def main() :



    baseDirMu   = '/data/users/jkunkle/Resonances/MuonEff_2016_01_30/'
    baseDirEl   = '/data/users/jkunkle/Resonances/ElectronEff_2016_01_30/'
    baseDirPhMu = '/data/users/jkunkle/Resonances/PhotonEffMuCh_2016_01_30/'
    baseDirPhEl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaMediumPhIDWithOlapPassPixSeed_2015_10_01'

    sampleConf = 'Modules/ResEff.py'

    makeMuPlots( baseDirMu, sampleConf, options.outputDir )
    makeMuPlots( baseDirMu, sampleConf, options.outputDir, trig=True )
    makeElPlots( baseDirEl, sampleConf, options.outputDir )
    makeElPlots( baseDirEl, sampleConf, options.outputDir, trig=True )
    makePhPlots( baseDirPhMu, sampleConf, options.outputDir, elevetoid=None, trig=True )
    makePhPlots( baseDirPhMu, sampleConf, options.outputDir, elevetoid=None )
    makePhPlots( baseDirPhMu, sampleConf, options.outputDir, elevetoid='Medium' )

    makeMetPlots( baseDirMu, sampleConf, options.outputDir )

def makeMetPlots( baseDir, sampleConf, outputDir=None ) :

    sampMan = SampleManager( baseDir, _TREENAME, filename=_FILENAME )
    sampMan.ReadSamples( sampleConf )

    samp_name = 'Comb'

    samp = sampMan.get_samples( name=samp_name )

    if not samp :
        print 'Could not find sample!'
        return

    binning_x = range( 0, 50, 5) + range( 50, 300, 10 ) + range( 300, 600, 20) + range( 600, 2000, 100 ) + [ 2000, 3000]
    binning_y = range( -1000, 1000, 10 )

    var = 'truemet_pt-recomet_pt:truemet_pt'

    sampMan.create_hist( samp[0], var, '', (binning_x, binning_y) )

    thishist = samp[0].hist.Clone('met')

    thishist_px = thishist.ProfileX( 'met_px' )

    can = ROOT.TCanvas( 'metRes', 'metRes' )

    thishist_px.Draw()
    can.SetLogx()
    if outputDir :
        can.SaveAs( '%s/MetResolution.pdf' %( outputDir ) )
    else :
        raw_input('cont')



def makePhPlots(baseDir, sampleConf, outputDir=None, elevetoid=None, trig=False) :

    sampMan = SampleManager( baseDir, _TREENAME, filename=_FILENAME )
    sampMan.ReadSamples( sampleConf )

    samp_name = 'Comb'

    samp = sampMan.get_samples( name=samp_name )

    if not samp :
        print 'Could not find sample!'
        return

    #binning = range( 0, 50, 5) + range( 50, 500, 10 ) + range( 500, 2000, 100 )
    binning = range( 0, 50, 5) + range( 50, 300, 10 ) + range( 300, 600, 20) + range( 600, 2000, 100 ) + [ 2000, 3000]

    var = 'truephot_pt'

    name = 'PhotonEff'

    if trig :
        labels = ['Mu17_Photon30']
        colors = [ROOT.kBlack]
        selections = ['', 'passTrig_Mu17_Photon30_CaloIdL_L1ISO']
        name += 'Trig'
    elif elevetoid is None :
        labels = ['Container Photons', 'Loose Photons', 'Medium Photons', 'Tight Photons']
        colors = [ROOT.kBlack, ROOT.kRed,ROOT.kGreen, ROOT.kBlue]
        selections = ['', 'hasTruthMatch', 'hasTruthMatch && phprobe_passLoose ', 'hasTruthMatch && phprobe_passMedium ', 'hasTruthMatch && phprobe_passTight ' ]
        name += 'EleVeto%s' %elevetoid
    else :
        labels = ['%s Photons' %elevetoid, '%s Photons + CSEV' %elevetoid, '%s Photons + PSV' %elevetoid]
        colors = [ROOT.kBlack, ROOT.kRed,ROOT.kGreen]
        selections = ['', 'hasTruthMatch', 'hasTruthMatch && phprobe_pass%s && phprobe_eleVeto '%elevetoid, 'hasTruthMatch && phprobe_pass%s && !phprobe_hasPixSeed '%elevetoid ]

    hists = []
    for idx, selection in enumerate(selections) :
        sampMan.create_hist( samp[0], var, selection, binning )

        thissamp = sampMan.get_samples( name=samp_name )

        hists.append( thissamp[0].hist.Clone( 'hist_%d' %idx ) )

    canvas = ROOT.TCanvas( name, name )

    DrawHists( canvas, hists, colors, labels, outputDir ) 

def makeElPlots(baseDir, sampleConf, outputDir=None, trig=False) :

    sampMan = SampleManager( baseDir, _TREENAME, filename=_FILENAME )
    sampMan.ReadSamples( sampleConf )

    samp_name = 'Comb'

    samp = sampMan.get_samples( name=samp_name )

    if not samp :
        print 'Could not find sample!'
        return

    #binning = range( 0, 50, 5) + range( 50, 500, 10 ) + range( 500, 2000, 100 )
    binning = range( 0, 50, 5) + range( 50, 300, 10 ) + range( 300, 600, 20) + range( 600, 2000, 100 ) + [ 2000, 3000]

    var = 'trueel_pt'

    name = 'ElectronEff'

    if trig : 
        labels = ['Ele24_eta2p1_WPTight_Gsf']
        colors = [ROOT.kBlack]
        selections = ['', 'passTrig_Ele27_eta2p1_WPTight_Gsf' ]
        name += 'Trig'
    else :
        labels = ['Container Electrons', 'Loose Electrons', 'Medium Electrons', 'Tight Electrons']
        colors = [ROOT.kBlack, ROOT.kRed,ROOT.kGreen, ROOT.kBlue]
        selections = ['', 'hasTruthMatch', 'hasTruthMatch && elprobe_passLoose ', 'hasTruthMatch && elprobe_passMedium ', 'hasTruthMatch && elprobe_passTight ' ]

    hists = []
    for idx, selection in enumerate(selections) :
        sampMan.create_hist( samp[0], var, selection, binning )

        thissamp = sampMan.get_samples( name=samp_name )

        hists.append( thissamp[0].hist.Clone( 'hist_%d' %idx ) )

    canvas = ROOT.TCanvas( name, name )

    DrawHists( canvas, hists, colors, labels, outputDir ) 

def makeMuPlots(baseDirMu, sampleConf, outputDir=None, trig=False) :

    sampMan = SampleManager( baseDirMu, _TREENAME, filename=_FILENAME )
    sampMan.ReadSamples( sampleConf )

    samp_name = 'Comb'

    samp = sampMan.get_samples( name=samp_name )

    if not samp :
        print 'Could not find sample!'
        return

    #binning = range( 0, 50, 5) + range( 50, 500, 10 ) + range( 500, 2000, 100 )
    binning = range( 0, 50, 5) + range( 50, 300, 10 ) + range( 300, 600, 20) + range( 600, 2000, 100 ) + [ 2000, 3000]

    var = 'truemu_pt'

    name = 'MuonEff'

    if trig :
        labels = ['IsoMu24', 'IsoTkMu24', 'IsoTkMu24 || IsoMu24', 'Mu17_Photon30']
        colors = [ROOT.kBlack, ROOT.kRed, ROOT.kGreen, ROOT.kBlue]
        selections = ['', 'passTrig_IsoMu24', 'passTrig_IsoTkMu24', 'passTrig_IsoMu24 || passTrig_IsoTkMu24 ', 'passTrig_Mu17_Photon30_CaloIdL_L1ISO' ]
        name += 'Trig'

    else :
        #labels = ['Container Muons', 'Triggered Muons', 'Tight Muons', 'Triggered Tight Muons']
        labels = ['Container Muons', 'Tight Muons']
        colors = [ROOT.kBlack, ROOT.kRed]
        selections = ['', 'hasTruthMatch' , 'hasTruthMatch && muprobe_passTight ']

    hists = []
    for idx, selection in enumerate(selections) :
        sampMan.create_hist( samp[0], var, selection, binning )

        thissamp = sampMan.get_samples( name=samp_name )

        hists.append( thissamp[0].hist.Clone( 'hist_%d' %idx ) )

    print hists

    canvas = ROOT.TCanvas( name, name )


    DrawHists( canvas, hists, colors, labels, outputDir ) 

def DrawHists( canvas, hists, colors, labels, outputDir=None ) :

    for idx in range( 1, len(hists)  ) :
        print idx
        hists[idx].Divide(hists[0])
        hists[idx].SetLineColor( colors[idx-1] )
        hists[idx].SetLineWidth( 2 )
        hists[idx].SetStats( 0 )

        if idx == 1 :
            hists[idx].Draw()
        else :
            hists[idx].Draw('same')

    legend = ROOT.TLegend( 0.6, 0.2, 0.9, 0.5 )

    legend.SetFillColor(ROOT.kWhite)
    legend.SetBorderSize( 0 )

    for idx in range( 1, len(hists)  ) :

        legend.AddEntry( hists[idx], labels[idx-1], 'L' )

    legend.Draw()

    canvas.SetLogx()

    if outputDir :
        canvas.SaveAs( '%s/%s.pdf' %( outputDir, canvas.GetName() ) )
    else :
        raw_input("cont")














main()
