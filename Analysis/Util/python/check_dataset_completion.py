
from argparse import ArgumentParser

import os
import sys
import eos_utilities as eosutil


import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
# disable file recovery
ROOT.gEnv.SetValue('TFile.Recover', 'OFF' )
#ROOT.gEnv.SaveLevel( ROOT.kEnvGlobal )

def main() :

    parser = ArgumentParser()
    
    parser.add_argument('--originalDS', dest='originalDS', default=None, required=True,help='Path to original dataset')
    parser.add_argument('--filteredDS', dest='filteredDS', default=None, required=True,help='Path to filtered dataset')
    parser.add_argument('--treeNameOrig',   dest='treeNameOrig',   default=None, required=False, help='Name of tree in original sample.  Use --treeNameOrig to read events from the tree or --histNameOrig to read from the histogram')
    parser.add_argument('--treeNameFilt',   dest='treeNameFilt',   default=None, required=False, help='Name of tree in filtered sample.  Use --treeNameFilt to read events from the tree or --histNameFilt to read from the histogram')
    parser.add_argument('--histNameOrig',   dest='histNameOrig',   default=None, required=False, help='Name of hist in original sample.  Use --treeNameOrig to read events from the tree or --histNameOrig to read from the histogram')
    parser.add_argument('--histNameFilt',   dest='histNameFilt',   default=None, required=False, help='Name of hist in filtered sample.  Use --treeNameFilt to read events from the tree or --histNameFilt to read from the histogram')
    parser.add_argument('--fileKeyOrig', dest='fileKeyOrig', default=None, help='key to match orginal files' )
    parser.add_argument('--fileKeyFilt', dest='fileKeyFilt', default=None, help='key to match filtered files' )
    
    options = parser.parse_args()

    orig_nevt_tree, orig_nevt_hist, filt_nevt_tree, filt_nevt_hist = check_dataset_completion( options.originalDS, options.filteredDS, options.treeNameOrig, options.treeNameFilt, options.histNameOrig, options.histNameFilt, options.fileKeyOrig, options.fileKeyFilt )

    orig_nevt = orig_nevt_tree
    if not orig_nevt :
        orig_nevt = orig_nevt_hist

    filt_nevt = filt_nevt_tree
    if not filt_nevt :
        filt_nevt = filt_nevt_hist


    print '%s : Orignal = %d events, filtered = %d events.  \033[1mDifference = %d\033[0m' %( options.filteredDS.split('/')[-1], orig_nevt, filt_nevt, orig_nevt-filt_nevt)

def check_dataset_completion( originalDS, filteredDS, treeNameOrig=None, treeNameFilt=None, histNameOrig=None, histNameFilt=None, fileKeyOrig=None, fileKeyFilt=None, quiet=False ) :


    assert treeNameOrig is not None or histNameOrig is not None, 'Must provide a histogram or tree name for original samples'
    assert treeNameFilt is not None or histNameFilt is not None, 'Must provide a histogram or tree name for filtered samples'

    #assert not (treeNameOrig is not None and histNameOrig is not None), 'Must provide a histogram or tree name for original samples, not both'
    #assert not (treeNameFilt is not None and histNameFilt is not None), 'Must provide a histogram or tree name for filtered samples, not both'

    filt_nevt_tree = 0 
    filt_nevt_hist = 0

    orig_nevt_tree, orig_nevt_hist  = get_dataset_counts( originalDS, fileKeyOrig, treeNameOrig, histNameOrig )


    if not orig_nevt_tree and not orig_nevt_hist  :
        if not quiet :
            print 'Did not get any original events.  Check the path'
        return orig_nevt_tree, orig_nevt_hist, filt_nevt_tree, filt_nevt_hist
        
    filt_nevt_tree, filt_nevt_hist  = get_dataset_counts( filteredDS, fileKeyFilt, treeNameFilt, histNameFilt )


    return orig_nevt_tree, orig_nevt_hist, filt_nevt_tree, filt_nevt_hist


def get_dataset_counts( dataset, fileKey, treeName=None, histName=None, vetoes=[] ) :

    if not isinstance( vetoes, list ) :
        vetoes = [vetoes]

    nevt_tree = 0
    nevt_hist = 0
    if dataset.count( '/eos/' ) :
        for top, dirs, files, sizes in eosutil.walk_eos( dataset ) :

            for file in files :

                filepath = top + '/' + file
                if vetoes :
                    match_veto = False
                    for v in vetoes :
                        if filepath.count(v) :
                            match_veto = True
                            break

                    if match_veto :
                        continue

                if fileKey is not None and not file.count(fileKey) : continue

                ofile = ROOT.TFile.Open( 'root://eoscms/' + filepath )
                if ofile == None :
                    continue
                if  ofile.IsZombie() :
                    continue
                if ofile.TestBit(ROOT.TFile.kRecovered) :
                    print 'File was recovered, and data is probably not available'
                    continue
                if treeName is not None :
                    try :
                        otree = ofile.Get(treeName)
                        nevt_tree += otree.GetEntries()
                    except ReferenceError :
                        print 'Could not access file'

                if histName is not None :
                    try :
                        ohist = ofile.Get(histName)
                    except ReferenceError :
                        print 'Could not access file'
                        continue

                    try  :
                        nevt_hist += ohist.GetBinContent(1)
                    except AttributeError :
                        print 'Could not access hist'
                        continue
                ofile.Close()


    else :
        for top, dirs, files in os.walk( dataset ) :
            for file in files :

                filepath = top + '/' + file
                if vetoes :
                    match_veto = False
                    for v in vetoes :
                        if filepath.count(v) :
                            match_veto = True
                            break

                    if match_veto :
                        continue

                if fileKey is not None and not file.count(fileKey) : continue

                ofile = ROOT.TFile.Open( filepath  )
                if ofile == None :
                    continue
                if ofile.IsZombie() :
                    continue
                if ofile.TestBit(ROOT.TFile.kRecovered) :
                    print 'File was recovered, and data is probably not available'
                    continue
                if treeName is not None :
                    try :
                        otree = ofile.Get(treeName)
                        otree.GetName()
                        nevt_tree += otree.GetEntries()
                    except ReferenceError :
                        print 'Could not access file with treename ', treeName

                if histName is not None :
                    try :
                        ohist = ofile.Get(histName)
                    except ReferenceError :
                        print 'Could not access file'
                    try :
                        nevt_hist += ohist.GetBinContent(1)
                    except AttributeError :
                        print 'Could not get hist from file %s' %(filepath)
                ofile.Close()


    return (nevt_tree, nevt_hist )

if __name__ == '__main__' :
    main()

