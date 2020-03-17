"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('--baseDir',      default=None,           dest='baseDir',         help='Path to base directory containing all ntuples')
p.add_argument('--baseDirModel',      default=None,           dest='baseDirModel', help='Path to base directory containing all ntuples for the model')
p.add_argument('--fileName',     default='tree.root',  dest='fileName',        help='( Default ntuple.root ) Name of files')
p.add_argument('--treeName',     default='UMDNTuple/EventTree'     ,  dest='treeName',        help='( Default events ) Name tree in root file')
p.add_argument('--treeNameModel',     default='photons'     ,  dest='treeNameModel',help='( Default photons ) Name tree in root file')
p.add_argument('--samplesConf',  default='Modules/Resonance2016.py',           dest='samplesConf',     help=('Use alternate sample configuration. '
                                                                                       'Must be a python file that implements the configuration '
                                                                                       'in the same manner as in the main() of this script.  If only '
                                                                                       'the file name is given it is assumed to be in the same directory '
                                                                                       'as this script, if a path is given, use that path' ) )

p.add_argument('--xsFile',     default='cross_sections/photon16.py',  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
p.add_argument('--lumi',     default=36000,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--weightHistName',     default="weighthist",  type=str ,        dest='weightHistName',         help='name of weight histogram')
p.add_argument('--mcweight',     default=None,  type=float ,        dest='mcweight',         help='Weight to apply to MC samples')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--readHists',     default=False,action='store_true',   dest='readHists',         help='read histograms from root files instead of trees')

p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')
p.add_argument('--jupyt',     default=False,action='store_true',   dest='jupyt',         help='use setting for jupyter notebook')
p.add_argument('--nodataFrame', default=True,action='store_false',   dest='dataFrame',   help='backwards compatibility for pre-2019 releases of ROOT')
p.add_argument('--batch',     default=False,action='store_true',   dest='batch',         help='use batch mode')
p.add_argument('--reload',     default=False,action='store_true',   dest='reload',         help='reload sample manager')
p.add_argument('--combine',     default=False,action='store_true',   dest='combine',         help='Combine years')

options = p.parse_args()

import sys
import os
import re
import math
import uuid
import copy
import imp
import ROOT
from ROOT import RooFit
from array import array
import numpy as np
if options.reload:
        import SampleManager;reload(SampleManager)
from SampleManager import SampleManager
if options.jupyt:
    try:
        from IPython.display import display, Math, Latex
        import rootnotes
    except ImportError: print "Fail to import jupyt modules"
elif options.batch:
    ROOT.gROOT.SetBatch(True)
else: ROOT.gROOT.SetBatch(False)

_LUMI  =  { 16: 35900,
            17: 41500,
            18: 59700,
          }

samples = None

def main() :

    global samples

    if not options.baseDir.count('/eos/') and not os.path.isdir( options.baseDir ) and not options.combine:
        print 'baseDir not found!'
        return


    if options.combine:

        samplelist = {}
        for year in [16,17,18]:
            print options.baseDir %year
            lumi = options.lumi if options.lumi>0 else _LUMI[year]
            samplelist[year] = SampleManager(options.baseDir %year, options.treeName, mcweight=options.mcweight,
                        treeNameModel=options.treeNameModel, filename=options.fileName, base_path_model=options.baseDirModel,
                        xsFile=options.xsFile %year , lumi=lumi, readHists=options.readHists,
                        quiet=options.quiet, weightHistName=options.weightHistName, dataFrame = options.dataFrame)
            samplelist[year].ReadSamples( options.samplesConf %year )

            if samples == None:  samples = samplelist[year]
            else:                samples.Merge(samplelist[year],"%d" %year)

    else:
        samples = SampleManager(options.baseDir, options.treeName, mcweight=options.mcweight, treeNameModel=options.treeNameModel,
                                filename=options.fileName, base_path_model=options.baseDirModel, xsFile=options.xsFile,
                                lumi=options.lumi, readHists=options.readHists, quiet=options.quiet, 
                                weightHistName=options.weightHistName, dataFrame = options.dataFrame)


        if options.samplesConf is not None :

           samples.ReadSamples( options.samplesConf )

       # print 'Samples ready.\n'

       # print 'The draw syntax follows that of TTree.Draw.  Examples : '
       #
       # print 'samples.Draw(\'met_et\', \'EventWeight && passcut_ee==1\', \'(300, 0, 300)\'\n'

       # print 'The first argument is a branch in the tree to draw'
       # print 'The second argument is a set of cuts and/or weights to apply'
       # print 'The third argument are the bin limits to use \n'

       # print 'To see all available branches do ListBranches()'


#---------------------------------------
# User functions
#---------------------------------------

#---------------------------------------
def DrawFormatted(varexp, selection, histpars=None ) :
    """ Example wrapper function.   Make a stack and then add some extra goodies """

    global samples

    print 'DrawFormatted histpars ', histpars
    samples.MakeStack(varexp, selection, histpars)

    statuslabel = ROOT.TLatex(0.4, 0.8, 'Atlas Internal')
    statuslabel.SetNDC()
    luminosity = ROOT.TLatex(0.4, 0.7, ' 10.0 fb^{-1}')
    luminosity.SetNDC()
    samples.add_decoration(statuslabel)
    samples.add_decoration(luminosity)

    samples.DrawCanvas()

    statuslabel.Draw()
    luminosity.Draw()

#---------------------------------------
def WriteCurrentHists( filename='hist.root') :
    """ write all histograms in samples to a root file """

    file = ROOT.TFile.Open( filename, 'RECREATE')

    for hist, samp in samples.samples.iteritems() :
        newhist = samp.hist.Clone(hist)
        file.cd()
        newhist.Write()

    file.Close()

#---------------------------------------
def SaveStack( name, can=None ) :
    if options.outputDir is None :
        print 'No outputDir given!'
        return

    samples.SaveStack( name, outputDir=options.outputDir, canname=can )



#---------------------------------------


#graveyard.py
#def MakeTAndPHists( outputfile, tagprobe_min=0, tagprobe_max=1e9, normalize=1 ) :
#def MakeTAndPPlots( ) :
#def MakeTAndPCompPlots( ) :
#def MakeTAndPCompPlotsFull( ) :
#def FitTAndPComp( ) :

#
# The following is to get the history 
#
import atexit
historyPath = os.path.expanduser("~/.pyhistory")
try:
    import readline
except ImportError:
    print "Module readline not available."
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")
    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)


# -----------------------------------------------------------------
def save_history(historyPath=historyPath):
    try:
        import readline
    except ImportError:
        print "Module readline not available."
    else:
        readline.write_history_file(historyPath)

atexit.register(save_history)

main()
