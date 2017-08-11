import os
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('--version', dest='version', required=True, help='Name of version directory (Resonances_v10)' )
parser.add_argument('--outputDir', dest='outputDir', required=True, help='output path' )
parser.add_argument('--fileKey', dest='fileKey', default=None, help='key to match files' )
parser.add_argument('--treeName', dest='treeName', default='tupel/EventTree', help='tree name' )

options = parser.parse_args()

_NTUPLE_DIR = '/store/user/jkunkle'

def main() :

    data_samples = ['SingleElectron', 'SingleMuon', 'SinglePhoton', 'DoubleMuon', 'DoubleElectron']

    mc_samples = []

    for samp in os.listdir( _NTUPLE_DIR ) :

        if samp in data_samples :
            continue

        if os.path.isfile( '%s/%s/hist.root' %( options.outputDir, samp ) ) :
            continue

        if os.path.isdir( '%s/%s/%s' %( _NTUPLE_DIR, samp, options.version ) ) :
            mc_samples.append( samp )

    for samp in mc_samples :

        samp_files = []

        for top, dirs, files in os.walk( _NTUPLE_DIR + '/' + samp + '/' + options.version ) :
            for f in files :
                if options.fileKey is None or f.count( options.fileKey ) > 0 :
                    samp_files.append('%s/%s' %(top, f ) ) 

        samp_dir = '%s/%s' %( options.outputDir, samp )

        if not os.path.isdir(samp_dir ) :
            os.makedirs( samp_dir )

        outfile = ROOT.TFile.Open( '%s/hist.root' %samp_dir , 'RECREATE' )

        print 'Make histogram for %s' %samp

        get_histograms( samp_files, outfile )

        outfile.Close()


def get_histograms(files, outfile) :

    branch_name = 'EvtPuCntTruth'

    chain = ROOT.TChain( options.treeName )

    for f in files :
        chain.AddFile( f )

    chain.SetBranchStatus('*', 0)
    chain.SetBranchStatus(branch_name, 1)
    chain.SetBranchStatus('EvtWeights', 1)

    outfile.cd()

    chain.Draw( '%s >> pileup_true(100,0,100)' %branch_name, '1 * ( EvtWeights[0] > 0 ) - 1* ( EvtWeights[0] < 0 ) ' )

    hist = outfile.Get('pileup_true')

    hist.Write()






main()

