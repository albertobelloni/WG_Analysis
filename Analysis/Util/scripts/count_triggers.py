import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os

from argparse import ArgumentParser

parser = ArgumentParser()

#parser.add_argument( '--file', dest='file', required=False, help='Comma separated ' )
parser.add_argument( '--path', dest='path', required=True, help='Path containing ntuples' )
parser.add_argument( '--fileKey', dest='fileKey', default=None, help='Select files containing this key' )
parser.add_argument( '--treeName', dest='treeName', required=True, help='Tree name within ntuples' )

options = parser.parse_args()

def main() :

    chain = ROOT.TChain( options.treeName ) 

    for top, dirs, files in os.walk( options.path ) :

        for fname in files :

            if options.fileKey is not None :
                if fname.count( options.fileKey ) :
                    chain.AddFile( top + '/' + fname )
            else :
                chain.AddFile( top + '/' + fname )

    trigger_branches = {}
    evt_count = 0

    for br in chain.GetListOfBranches() :

        brname = br.GetName()

        if brname.count('passTrig' ) :
            trigger_branches[ brname ] = 0


    print 'All trigger branches : '
    print trigger_branches.keys()


    for event in chain :
        evt_count+=1

        if evt_count%10000 == 0 :
            print 'Processed %d events' %evt_count

        for brname in trigger_branches :
            trigger_branches[brname] = trigger_branches[brname] + getattr( chain, brname )


    sorted_branches = trigger_branches.keys()
    sorted_branches.sort()

    for brname in sorted_branches :
        totals = trigger_branches[brname]

        print 'Trigger : %s, npass = %d, nfail = %d' %( brname, totals, evt_count-totals )











main()

